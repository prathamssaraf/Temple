/**
 * Scanner View - Main scanning interface with API integration.
 */

import { useState, useEffect } from 'react';
import { useScanStocks, useUniverses, useExamplePatterns } from '../../hooks/useTempleApi';
import type { PatternDefinition, ScanResultItem } from '../../types/api';

export default function ScannerView() {
  const [selectedPattern, setSelectedPattern] = useState<PatternDefinition | null>(null);
  const [scanType, setScanType] = useState<'symbols' | 'universe'>('symbols');
  const [symbols, setSymbols] = useState('AAPL, MSFT, GOOGL, AMZN, NVDA');
  const [selectedUniverse, setSelectedUniverse] = useState('tech');
  const [minConfidence, setMinConfidence] = useState(0.7);
  const [parallel, setParallel] = useState(true);

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

  const handleScan = async () => {
    if (!selectedPattern) {
      alert('Please select a pattern');
      return;
    }

    try {
      if (scanType === 'symbols') {
        const symbolList = symbols.split(',').map(s => s.trim()).filter(s => s);
        if (symbolList.length === 0) {
          alert('Please enter at least one symbol');
          return;
        }
        await scanStocks({ symbols: symbolList }, selectedPattern, minConfidence, parallel);
      } else {
        await scanStocks({ universe: selectedUniverse }, selectedPattern, minConfidence, parallel);
      }
    } catch (error) {
      console.error('Scan failed:', error);
    }
  };

  const matches = scanData?.results.filter(r => r.matched).sort((a, b) => b.confidence - a.confidence) || [];

  return (
    <div className="flex-1 p-8 overflow-y-auto">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">Stock Scanner</h1>
          <p className="text-gray-400">Scan multiple stocks for pattern matches</p>
        </div>

        {/* Configuration Panel */}
        <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl border border-gray-700/50 p-6 mb-6">
          <h2 className="text-xl font-semibold text-white mb-4">Scan Configuration</h2>

          {/* Pattern Selection */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Pattern
            </label>
            <select
              className="w-full bg-gray-900/50 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-purple-500"
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
              <p className="text-sm text-gray-400 mt-2">{selectedPattern.description}</p>
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
                    ? 'bg-purple-600 text-white'
                    : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                }`}
                onClick={() => setScanType('symbols')}
              >
                Custom Symbols
              </button>
              <button
                className={`px-4 py-2 rounded-lg font-medium transition ${
                  scanType === 'universe'
                    ? 'bg-purple-600 text-white'
                    : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
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
                className="w-full bg-gray-900/50 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-purple-500"
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
                className="w-full bg-gray-900/50 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-purple-500"
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
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
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
            <div className="flex items-end">
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
          </div>

          {/* Scan Button */}
          <button
            onClick={handleScan}
            disabled={scanning || !selectedPattern}
            className="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-3 rounded-lg font-semibold hover:from-purple-700 hover:to-pink-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {scanning ? 'Scanning...' : 'Start Scan'}
          </button>

          {scanError && (
            <div className="mt-4 p-3 bg-red-500/10 border border-red-500/50 rounded-lg text-red-400 text-sm">
              {scanError}
            </div>
          )}
        </div>

        {/* Results */}
        {scanData && (
          <div className="space-y-6">
            {/* Summary */}
            <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl border border-gray-700/50 p-6">
              <h2 className="text-xl font-semibold text-white mb-4">Scan Results</h2>
              <div className="grid grid-cols-4 gap-4">
                <div>
                  <div className="text-sm text-gray-400">Total Scanned</div>
                  <div className="text-2xl font-bold text-white">{scanData.total_symbols}</div>
                </div>
                <div>
                  <div className="text-sm text-gray-400">Matches Found</div>
                  <div className="text-2xl font-bold text-green-400">{scanData.matches_found}</div>
                </div>
                <div>
                  <div className="text-sm text-gray-400">Avg Confidence</div>
                  <div className="text-2xl font-bold text-purple-400">
                    {(scanData.average_confidence * 100).toFixed(1)}%
                  </div>
                </div>
                <div>
                  <div className="text-sm text-gray-400">Duration</div>
                  <div className="text-2xl font-bold text-blue-400">{scanData.duration_seconds.toFixed(2)}s</div>
                </div>
              </div>
            </div>

            {/* Matches Table */}
            {matches.length > 0 && (
              <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl border border-gray-700/50 overflow-hidden">
                <div className="p-6">
                  <h3 className="text-lg font-semibold text-white mb-4">
                    Top Matches ({matches.length})
                  </h3>
                </div>
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead className="bg-gray-900/50">
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
                    <tbody className="divide-y divide-gray-700">
                      {matches.map((result) => (
                        <tr key={result.symbol} className="hover:bg-gray-700/30 transition">
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm font-medium text-white">{result.symbol}</div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="flex items-center gap-2">
                              <div className="flex-1 bg-gray-700 rounded-full h-2 max-w-[100px]">
                                <div
                                  className="bg-gradient-to-r from-purple-600 to-pink-600 h-2 rounded-full"
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
            )}

            {matches.length === 0 && (
              <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl border border-gray-700/50 p-12 text-center">
                <p className="text-gray-400">No matches found. Try lowering the confidence threshold.</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
