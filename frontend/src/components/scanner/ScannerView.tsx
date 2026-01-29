/**
 * Scanner View - Main scanning interface with API integration.
 */

import { useState, useEffect } from 'react';
import { useScanStocks, useUniverses, useExamplePatterns } from '../../hooks/useTempleApi';
import type { PatternDefinition, ScanResultItem } from '../../types/api';
import StockDetailModal from './StockDetailModal';

export default function ScannerView() {
  const [selectedPattern, setSelectedPattern] = useState<PatternDefinition | null>(null);
  const [scanType, setScanType] = useState<'symbols' | 'universe'>('symbols');
  const [symbols, setSymbols] = useState('AAPL, MSFT, GOOGL, AMZN, NVDA');
  const [selectedUniverse, setSelectedUniverse] = useState('tech');
  const [minConfidence, setMinConfidence] = useState(0.7);
  const [parallel, setParallel] = useState(true);
  const [lookbackDays, setLookbackDays] = useState(365);
  const [showPatternInfo, setShowPatternInfo] = useState(false);

  // Pattern customization parameters
  const [smaPeriod, setSmaPeriod] = useState(20);
  const [tolerance, setTolerance] = useState(1.5);
  const [minOccurrences, setMinOccurrences] = useState(8);
  const [minIntervalDays, setMinIntervalDays] = useState(3);
  const [maxIntervalDays, setMaxIntervalDays] = useState(30);

  // Stock detail modal
  const [selectedStock, setSelectedStock] = useState<string | null>(null);

  const { data: scanData, loading: scanning, error: scanError, scanStocks } = useScanStocks();
  const { data: universesData, fetchUniverses } = useUniverses();
  const { data: examplesData, fetchExamples } = useExamplePatterns();

  useEffect(() => {
    fetchUniverses();
    fetchExamples();
  }, [fetchUniverses, fetchExamples]);

  useEffect(() => {
    if (examplesData && examplesData.length > 0 && !selectedPattern) {
      setSelectedPattern(examplesData[0]);
    }
  }, [examplesData, selectedPattern]);

  // Update default parameters when pattern changes
  useEffect(() => {
    if (selectedPattern) {
      switch (selectedPattern.name) {
        case 'Mean Reversion':
          setSmaPeriod(20);
          setMinIntervalDays(3);
          setMaxIntervalDays(30);
          setMinOccurrences(8);
          setTolerance(1.5);
          break;
        case 'Support Bounce':
          setTolerance(1.5);
          setMinOccurrences(5);
          break;
        case 'Volatility Cycle':
          setTolerance(8.0);
          setMinOccurrences(4);
          break;
      }
    }
  }, [selectedPattern?.name]);

  const handleScan = async () => {
    if (!selectedPattern) {
      alert('Please select a pattern');
      return;
    }

    try {
      // Apply custom parameters to the pattern
      const customizedPattern: PatternDefinition = { ...selectedPattern };

      // Apply Mean Reversion customizations
      if (selectedPattern.name === 'Mean Reversion') {
        customizedPattern.sequence = [
          {
            event: {
              event_type: 'PRICE_CROSSES_BELOW',
              parameters: {
                reference: `SMA${smaPeriod}`
              }
            }
          },
          {
            event: {
              event_type: 'PRICE_CROSSES_ABOVE',
              parameters: {
                reference: `SMA${smaPeriod}`
              }
            },
            min_interval_days: minIntervalDays,
            max_interval_days: maxIntervalDays
          }
        ];
        customizedPattern.frequency = {
          min_occurrences: minOccurrences,
          timeframe_days: lookbackDays
        };
      }

      // Apply Support Bounce customizations
      if (selectedPattern.name === 'Support Bounce') {
        customizedPattern.sequence[0].event.parameters.tolerance = tolerance;
        customizedPattern.frequency.min_occurrences = minOccurrences;
      }

      // Apply Volatility Cycle customizations
      if (selectedPattern.name === 'Volatility Cycle') {
        customizedPattern.sequence[0].event.parameters.min_change = tolerance;
        customizedPattern.sequence[1].event.parameters.min_change = tolerance;
        customizedPattern.frequency.min_occurrences = minOccurrences;
      }

      if (scanType === 'symbols') {
        const symbolList = symbols.split(',').map(s => s.trim()).filter(s => s);
        if (symbolList.length === 0) {
          alert('Please enter at least one symbol');
          return;
        }
        await scanStocks({ symbols: symbolList }, customizedPattern, minConfidence, parallel, lookbackDays);
      } else {
        await scanStocks({ universe: selectedUniverse }, customizedPattern, minConfidence, parallel, lookbackDays);
      }
    } catch (error) {
      console.error('Scan failed:', error);
    }
  };

  const matches = scanData?.results.filter(r => r.matched).sort((a, b) => b.confidence - a.confidence) || [];

  return (
    <div className="flex-1 p-8 overflow-y-auto animate-slide-up">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="font-header text-3xl font-semibold text-white mb-2">Stock Scanner</h1>
          <p className="text-gray-400">Scan multiple stocks for pattern matches</p>
        </div>

        {/* Two Column Layout */}
        <div className="grid grid-cols-2 gap-6 mb-6">
          {/* Left Column - Scan Configuration */}
          <div className="relative p-[1px] rounded-xl bg-gradient-to-r from-border via-border to-border group">
            <div className="absolute inset-0 bg-accent/5 blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            <div className="relative bg-surface rounded-xl p-6 shadow-glow">
              <h2 className="font-header text-xl font-semibold text-white mb-4">Scan Configuration</h2>

          {/* Pattern Selection */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Pattern
            </label>
            <select
              className="w-full bg-bg border border-border rounded-lg px-4 py-2 text-white focus:outline-none focus:border-accent transition-colors"
              value={selectedPattern?.name || ''}
              onChange={(e) => {
                const pattern = examplesData?.find(p => p.name === e.target.value);
                setSelectedPattern(pattern || null);
              }}
            >
              {examplesData?.map(pattern => (
                <option key={pattern.name} value={pattern.name}>
                  {pattern.name}
                </option>
              ))}
            </select>
            {selectedPattern && (
              <div className="flex items-start gap-2 mt-2">
                <p className="text-sm text-gray-400 flex-1">{selectedPattern.description}</p>
                <button
                  type="button"
                  onClick={() => setShowPatternInfo(true)}
                  className="flex-shrink-0 w-5 h-5 rounded-full border border-accent/50 text-accent text-xs flex items-center justify-center hover:bg-accent/10 transition-colors"
                  title="More information"
                >
                  i
                </button>
              </div>
            )}
          </div>

          {/* Scan Type */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Scan Type
            </label>
            <div className="flex gap-4">
              <button
                className={`px-4 py-2 rounded-lg font-medium transition ${
                  scanType === 'symbols'
                    ? 'bg-accent text-black shadow-glow'
                    : 'bg-surface border border-border text-gray-400 hover:text-white hover:border-accent/50'
                }`}
                onClick={() => setScanType('symbols')}
              >
                Custom Symbols
              </button>
              <button
                className={`px-4 py-2 rounded-lg font-medium transition ${
                  scanType === 'universe'
                    ? 'bg-accent text-black shadow-glow'
                    : 'bg-surface border border-border text-gray-400 hover:text-white hover:border-accent/50'
                }`}
                onClick={() => setScanType('universe')}
              >
                Universe
              </button>
            </div>
          </div>

          {/* Symbols or Universe Input */}
          {scanType === 'symbols' ? (
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Symbols (comma-separated)
              </label>
              <input
                type="text"
                className="w-full bg-bg border border-border rounded-lg px-4 py-2 text-white focus:outline-none focus:border-accent transition-colors"
                value={symbols}
                onChange={(e) => setSymbols(e.target.value)}
                placeholder="AAPL, MSFT, GOOGL"
              />
            </div>
          ) : (
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Universe
              </label>
              <select
                className="w-full bg-bg border border-border rounded-lg px-4 py-2 text-white focus:outline-none focus:border-accent transition-colors"
                value={selectedUniverse}
                onChange={(e) => setSelectedUniverse(e.target.value)}
              >
                {universesData?.universes.map(universe => (
                  <option key={universe.name} value={universe.name}>
                    {universe.description} ({universe.symbol_count} stocks)
                  </option>
                ))}
              </select>
            </div>
          )}

          {/* Advanced Options */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Time Range
            </label>
            <select
              className="w-full bg-bg border border-border rounded-lg px-4 py-2 text-white focus:outline-none focus:border-accent transition-colors"
              value={lookbackDays}
              onChange={(e) => setLookbackDays(parseInt(e.target.value))}
            >
              <option value={30}>1 Month (30 days)</option>
              <option value={90}>3 Months (90 days)</option>
              <option value={180}>6 Months (180 days)</option>
              <option value={365}>1 Year (365 days)</option>
              <option value={730}>2 Years (730 days)</option>
              <option value={1825}>5 Years (1825 days)</option>
            </select>
          </div>

          {/* Min Confidence */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Min Confidence: {(minConfidence * 100).toFixed(0)}%
            </label>
            <input
              type="range"
              min="0"
              max="100"
              value={minConfidence * 100}
              onChange={(e) => setMinConfidence(parseInt(e.target.value) / 100)}
              className="w-full"
            />
          </div>

          {/* Parallel Processing */}
          <div className="mb-4">
            <label className="flex items-center gap-2 text-gray-300">
              <input
                type="checkbox"
                checked={parallel}
                onChange={(e) => setParallel(e.target.checked)}
                className="w-4 h-4 rounded"
              />
              <span className="text-sm">Parallel Processing</span>
            </label>
          </div>

          {/* Scan Button */}
          <button
            onClick={handleScan}
            disabled={scanning || !selectedPattern}
            className="w-full bg-accent text-black py-3 rounded-lg font-semibold hover:bg-accent/90 transition shadow-glow disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {scanning ? 'Scanning...' : 'Start Scan'}
          </button>

          {scanError && (
            <div className="mt-4 p-3 bg-red-500/10 border border-red-500/50 rounded-lg text-red-400 text-sm">
              {scanError}
            </div>
          )}
            </div>
          </div>

          {/* Right Column - Pattern Modifier */}
          <div className="relative p-[1px] rounded-xl bg-gradient-to-r from-border via-border to-border group">
            <div className="absolute inset-0 bg-accent/5 blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            <div className="relative bg-surface rounded-xl p-6 shadow-glow">
              <h2 className="font-header text-xl font-semibold text-white mb-4">Pattern Modifier</h2>

              {selectedPattern ? (
                <div className="space-y-4">
                  {/* Tolerance */}
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      Tolerance: {tolerance}%
                    </label>
                    <input
                      type="range"
                      min="0.5"
                      max="20"
                      step="0.5"
                      value={tolerance}
                      onChange={(e) => setTolerance(parseFloat(e.target.value))}
                      className="w-full"
                    />
                    <div className="flex justify-between text-xs text-gray-500 mt-1">
                      <span>0.5%</span>
                      <span>20%</span>
                    </div>
                  </div>

                  {/* Minimum Occurrences */}
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      Minimum Occurrences: {minOccurrences}
                    </label>
                    <input
                      type="range"
                      min="1"
                      max="20"
                      value={minOccurrences}
                      onChange={(e) => setMinOccurrences(parseInt(e.target.value))}
                      className="w-full"
                    />
                    <div className="flex justify-between text-xs text-gray-500 mt-1">
                      <span>1</span>
                      <span>20</span>
                    </div>
                  </div>

                  {/* Pattern-specific parameters */}
                  {selectedPattern?.name === 'Mean Reversion' && (
                    <>
                      <div className="border-t border-border pt-4">
                        <h3 className="text-sm font-semibold text-white mb-3">Mean Reversion Settings</h3>

                        <div className="mb-4">
                          <label className="block text-sm font-medium text-gray-300 mb-2">
                            SMA Period: {smaPeriod} days
                          </label>
                          <input
                            type="range"
                            min="5"
                            max="200"
                            step="5"
                            value={smaPeriod}
                            onChange={(e) => setSmaPeriod(parseInt(e.target.value))}
                            className="w-full"
                          />
                          <div className="flex justify-between text-xs text-gray-500 mt-1">
                            <span>5</span>
                            <span>200</span>
                          </div>
                        </div>

                        <div className="grid grid-cols-2 gap-3">
                          <div>
                            <label className="block text-sm font-medium text-gray-300 mb-2">
                              Min Interval
                            </label>
                            <input
                              type="number"
                              min="1"
                              max="60"
                              value={minIntervalDays}
                              onChange={(e) => setMinIntervalDays(parseInt(e.target.value))}
                              className="w-full bg-bg border border-border rounded-lg px-3 py-2 text-white text-sm"
                            />
                          </div>
                          <div>
                            <label className="block text-sm font-medium text-gray-300 mb-2">
                              Max Interval
                            </label>
                            <input
                              type="number"
                              min="1"
                              max="90"
                              value={maxIntervalDays}
                              onChange={(e) => setMaxIntervalDays(parseInt(e.target.value))}
                              className="w-full bg-bg border border-border rounded-lg px-3 py-2 text-white text-sm"
                            />
                          </div>
                        </div>
                      </div>
                    </>
                  )}

                  {(selectedPattern?.name.includes('Pivot') ||
                    selectedPattern?.name === 'Support Bounce' ||
                    selectedPattern?.name === 'Volatility Cycle') && (
                    <div className="text-xs text-gray-400 bg-bg/50 border border-border rounded-lg p-3">
                      <p>Adjust tolerance and occurrences above to customize this pattern.</p>
                    </div>
                  )}

                  {/* Reset Button */}
                  <div className="pt-4 border-t border-border">
                    <button
                      type="button"
                      onClick={() => {
                        // Reset to defaults based on pattern
                        if (selectedPattern?.name === 'Mean Reversion') {
                          setSmaPeriod(20);
                          setMinIntervalDays(3);
                          setMaxIntervalDays(30);
                          setMinOccurrences(8);
                          setTolerance(1.5);
                        } else if (selectedPattern?.name === 'Support Bounce') {
                          setTolerance(1.5);
                          setMinOccurrences(5);
                        } else if (selectedPattern?.name === 'Volatility Cycle') {
                          setTolerance(8.0);
                          setMinOccurrences(4);
                        } else if (selectedPattern?.name.includes('Pivot')) {
                          setTolerance(5.0);
                          setMinOccurrences(8);
                        }
                      }}
                      className="w-full px-4 py-2 bg-bg border border-border rounded-lg text-accent hover:bg-accent/10 hover:border-accent/50 transition-colors text-sm font-medium"
                    >
                      Reset to Defaults
                    </button>
                  </div>
                </div>
              ) : (
                <div className="flex items-center justify-center h-64 text-gray-500">
                  Select a pattern to customize parameters
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Loading Animation */}
        {scanning && (
          <div className="relative p-[1px] rounded-xl bg-gradient-to-r from-accent via-accent to-accent mb-6 overflow-hidden">
            <div className="absolute inset-0 bg-accent/20 blur-xl animate-pulse"></div>
            <div className="relative bg-surface rounded-xl p-8 shadow-glow">
              <div className="flex flex-col items-center justify-center space-y-4">
                {/* Spinner */}
                <div className="relative w-16 h-16">
                  <div className="absolute inset-0 border-4 border-border rounded-full"></div>
                  <div className="absolute inset-0 border-4 border-accent border-t-transparent rounded-full animate-spin"></div>
                </div>

                {/* Status Text */}
                <div className="text-center">
                  <h3 className="font-header text-xl font-semibold text-white mb-2">Scanning Market</h3>
                  <p className="text-gray-400">
                    Analyzing patterns across {scanType === 'symbols' ? symbols.split(',').length : 'universe'} stocks...
                  </p>
                </div>

                {/* Progress Bar */}
                <div className="w-full max-w-md">
                  <div className="h-2 bg-border rounded-full overflow-hidden">
                    <div className="h-full bg-accent animate-pulse rounded-full" style={{ width: '100%' }}></div>
                  </div>
                </div>

                {/* Fun Loading Messages */}
                <p className="text-sm text-accent animate-pulse">
                  Fetching data from Yahoo Finance • Running pattern detection • Calculating confidence scores
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Results */}
        {scanData && !scanning && (
          <div className="space-y-6">
            {/* Summary */}
            <div className="relative p-[1px] rounded-xl bg-gradient-to-r from-border via-border to-border">
              <div className="bg-surface rounded-xl p-6 shadow-glow">
                <h2 className="font-header text-xl font-semibold text-white mb-4">Scan Results</h2>
              <div className="grid grid-cols-4 gap-4">
                <div>
                  <div className="text-sm text-gray-400">Total Scanned</div>
                  <div className="text-2xl font-bold text-white">{scanData.total_symbols}</div>
                </div>
                <div>
                  <div className="text-sm text-gray-400">Matches Found</div>
                  <div className="text-2xl font-bold text-accent">{scanData.matches_found}</div>
                </div>
                <div>
                  <div className="text-sm text-gray-400">Avg Confidence</div>
                  <div className="text-2xl font-bold text-accent">
                    {(scanData.average_confidence * 100).toFixed(1)}%
                  </div>
                </div>
                <div>
                  <div className="text-sm text-gray-400">Duration</div>
                  <div className="text-2xl font-bold text-white">{scanData.duration_seconds.toFixed(2)}s</div>
                </div>
              </div>
              </div>
            </div>

            {/* Matches Table */}
            {matches.length > 0 && (
              <div className="relative p-[1px] rounded-xl bg-gradient-to-r from-border via-border to-border overflow-hidden">
                <div className="bg-surface rounded-xl overflow-hidden shadow-glow">
                  <div className="p-6">
                    <h3 className="font-header text-lg font-semibold text-white mb-4">
                      Top Matches ({matches.length})
                    </h3>
                  </div>
                  <div className="overflow-x-auto">
                    <table className="w-full">
                      <thead className="bg-bg/50 border-b border-border">
                        <tr>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                            Symbol
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                            Confidence
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                            Occurrences
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                            Timeframe
                          </th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-border">
                      {matches.map((result) => (
                        <tr
                          key={result.symbol}
                          onClick={() => setSelectedStock(result.symbol)}
                          className="hover:bg-bg/30 transition cursor-pointer group"
                        >
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm font-medium text-white group-hover:text-accent transition">
                              {result.symbol}
                            </div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="flex items-center gap-2">
                              <div className="flex-1 bg-border rounded-full h-2 max-w-[100px]">
                                <div
                                  className="bg-accent h-2 rounded-full shadow-glow"
                                  style={{ width: `${result.confidence * 100}%` }}
                                />
                              </div>
                              <span className="text-sm text-white">{(result.confidence * 100).toFixed(1)}%</span>
                            </div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                            {result.occurrences}x
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-400">
                            {new Date(result.timeframe_start).toLocaleDateString()} - {new Date(result.timeframe_end).toLocaleDateString()}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
            )}

            {matches.length === 0 && (
              <div className="relative p-[1px] rounded-xl bg-gradient-to-r from-border via-border to-border">
                <div className="bg-surface rounded-xl p-12 text-center">
                  <p className="text-gray-400">No matches found. Try lowering the confidence threshold.</p>
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Stock Detail Modal */}
      {selectedStock && selectedPattern && (
        <StockDetailModal
          symbol={selectedStock}
          pattern={selectedPattern}
          lookbackDays={lookbackDays}
          onClose={() => setSelectedStock(null)}
        />
      )}

      {/* Pattern Info Modal */}
      {showPatternInfo && selectedPattern && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-surface border border-accent/50 rounded-xl max-w-2xl w-full animate-slide-up">
            {/* Header */}
            <div className="relative p-[1px] rounded-t-xl bg-gradient-to-r from-accent via-accent to-accent">
              <div className="bg-surface rounded-t-xl px-6 py-4 flex items-center justify-between">
                <h3 className="font-header text-xl font-semibold text-white">Pattern Information</h3>
                <button
                  onClick={() => setShowPatternInfo(false)}
                  className="text-gray-400 hover:text-white transition-colors"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>

            {/* Content */}
            <div className="p-6 space-y-4">
              <div>
                <h4 className="text-lg font-semibold text-accent mb-2">{selectedPattern.name}</h4>
                <p className="text-gray-300 text-sm leading-relaxed">{selectedPattern.description}</p>
              </div>

              <div className="border-t border-border pt-4">
                <h5 className="text-sm font-semibold text-white mb-3">Pattern Details</h5>

                {/* Sequence Steps */}
                <div className="space-y-3 mb-4">
                  <div className="text-xs text-gray-400 uppercase tracking-wide">Sequence</div>
                  {selectedPattern.sequence.map((step, index) => (
                    <div key={index} className="flex gap-3">
                      <div className="flex-shrink-0 w-6 h-6 rounded-full bg-accent/20 border border-accent/50 flex items-center justify-center text-accent text-xs font-semibold">
                        {index + 1}
                      </div>
                      <div className="flex-1">
                        <div className="text-sm text-white font-medium">
                          {step.event.event_type.replace(/_/g, ' ')}
                        </div>
                        {step.min_interval_days && (
                          <div className="text-xs text-gray-400 mt-1">
                            Min interval: {step.min_interval_days} days
                          </div>
                        )}
                        {step.max_interval_days && (
                          <div className="text-xs text-gray-400 mt-1">
                            Max interval: {step.max_interval_days} days
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>

                {/* Frequency Requirements */}
                <div className="bg-bg/50 border border-border rounded-lg p-4">
                  <div className="text-xs text-gray-400 uppercase tracking-wide mb-2">Frequency Requirements</div>
                  <div className="flex items-center gap-4">
                    <div>
                      <div className="text-sm text-gray-400">Min Occurrences</div>
                      <div className="text-lg font-semibold text-accent">{selectedPattern.frequency.min_occurrences}</div>
                    </div>
                    <div className="text-gray-600">in</div>
                    <div>
                      <div className="text-sm text-gray-400">Timeframe</div>
                      <div className="text-lg font-semibold text-white">{selectedPattern.frequency.timeframe_days} days</div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Close Button */}
              <div className="flex justify-end pt-2">
                <button
                  onClick={() => setShowPatternInfo(false)}
                  className="px-6 py-2 bg-accent text-black rounded-lg font-semibold hover:bg-accent/90 transition-colors shadow-glow"
                >
                  Got it
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
