/**
 * Stock Detail Modal - Shows detailed chart and pattern analysis for a stock.
 */

import { useState, useEffect } from 'react';
import { ComposedChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, ReferenceDot, Scatter } from 'recharts';
import { usePatternMatch } from '../../hooks/useTempleApi';
import type { PatternDefinition, PatternMatchResponse } from '../../types/api';

interface StockDetailModalProps {
  symbol: string;
  pattern: PatternDefinition;
  lookbackDays: number;
  onClose: () => void;
}

export default function StockDetailModal({ symbol, pattern, lookbackDays, onClose }: StockDetailModalProps) {
  const { data: matchData, loading, matchPattern } = usePatternMatch();

  useEffect(() => {
    matchPattern(symbol, pattern, lookbackDays);
  }, [symbol, pattern, lookbackDays, matchPattern]);

  if (loading) {
    return (
      <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50">
        <div className="bg-surface border border-border rounded-xl p-8 max-w-4xl w-full mx-4">
          <div className="flex items-center justify-center space-x-3">
            <div className="w-8 h-8 border-4 border-accent border-t-transparent rounded-full animate-spin"></div>
            <span className="text-white">Loading {symbol} data...</span>
          </div>
        </div>
      </div>
    );
  }

  if (!matchData) return null;

  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 overflow-y-auto">
      <div className="min-h-screen flex items-center justify-center p-4">
        <div className="bg-surface border border-border rounded-xl max-w-7xl w-full my-8 relative animate-slide-up">
        {/* Header */}
        <div className="relative p-[1px] rounded-t-xl bg-gradient-to-r from-accent via-accent to-accent">
          <div className="bg-surface rounded-t-xl px-6 py-4 flex items-center justify-between">
            <div>
              <h2 className="font-header text-2xl font-semibold text-white">{symbol}</h2>
              <p className="text-gray-400 text-sm">{pattern.name} Pattern Analysis</p>
            </div>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-white transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Stats Grid */}
          <div className="grid grid-cols-4 gap-4">
            <div className="bg-bg border border-border rounded-lg p-4">
              <div className="text-xs text-gray-400 mb-1">Match Status</div>
              <div className={`text-lg font-semibold ${matchData.matched ? 'text-accent' : 'text-red-400'}`}>
                {matchData.matched ? 'MATCHED ✓' : 'NO MATCH'}
              </div>
            </div>
            <div className="bg-bg border border-border rounded-lg p-4">
              <div className="text-xs text-gray-400 mb-1">Confidence</div>
              <div className="text-lg font-semibold text-white">
                {(matchData.confidence * 100).toFixed(1)}%
              </div>
            </div>
            <div className="bg-bg border border-border rounded-lg p-4">
              <div className="text-xs text-gray-400 mb-1">Occurrences</div>
              <div className="text-lg font-semibold text-accent">
                {matchData.occurrences}x
              </div>
            </div>
            <div className="bg-bg border border-border rounded-lg p-4">
              <div className="text-xs text-gray-400 mb-1">Timeframe</div>
              <div className="text-sm font-semibold text-white">
                {new Date(matchData.timeframe_start).toLocaleDateString()}
              </div>
            </div>
          </div>

          {/* Price Chart */}
          <div className="bg-bg border border-border rounded-lg p-6">
            <h3 className="font-header text-lg font-semibold text-white mb-4">
              Price Movement & Pattern Occurrences
            </h3>
            {matchData.price_data && matchData.price_data.length > 0 ? (
              <div className="h-96">
                <ResponsiveContainer width="100%" height="100%">
                  <ComposedChart
                    data={matchData.price_data.map((price) => {
                      // Find if this date is part of any pattern occurrence
                      const occurrence = matchData.occurrence_details.find(occ => {
                        const priceDate = new Date(price.date);
                        const startDate = new Date(occ.start_date);
                        const endDate = new Date(occ.end_date);
                        return priceDate >= startDate && priceDate <= endDate;
                      });

                      return {
                        date: new Date(price.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
                        fullDate: price.date,
                        close: price.close,
                        open: price.open,
                        high: price.high,
                        low: price.low,
                        volume: price.volume,
                        isPattern: occurrence ? price.close : null,
                        patternStart: occurrence && price.date === occurrence.start_date ? price.close : null,
                        patternEnd: occurrence && price.date === occurrence.end_date ? price.close : null,
                      };
                    })}
                    margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
                  >
                    <defs>
                      <linearGradient id="colorPrice" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.1}/>
                        <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                    <XAxis
                      dataKey="date"
                      stroke="#9ca3af"
                      tick={{ fill: '#9ca3af', fontSize: 11 }}
                      interval="preserveStartEnd"
                      minTickGap={50}
                    />
                    <YAxis
                      stroke="#9ca3af"
                      tick={{ fill: '#9ca3af', fontSize: 12 }}
                      label={{ value: 'Price ($)', angle: -90, position: 'insideLeft', fill: '#9ca3af' }}
                      domain={['auto', 'auto']}
                    />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: '#1f2937',
                        border: '1px solid #374151',
                        borderRadius: '8px',
                        color: '#fff'
                      }}
                      formatter={(value: any, name: string) => {
                        if (name === 'close') return [`$${Number(value).toFixed(2)}`, 'Close'];
                        if (name === 'isPattern') return [`$${Number(value).toFixed(2)}`, 'Pattern Active'];
                        return [value, name];
                      }}
                    />
                    {/* Background area for price */}
                    <Area
                      type="monotone"
                      dataKey="close"
                      stroke="none"
                      fillOpacity={1}
                      fill="url(#colorPrice)"
                    />
                    {/* Main price line */}
                    <Line
                      type="monotone"
                      dataKey="close"
                      stroke="#3b82f6"
                      strokeWidth={2}
                      dot={false}
                      activeDot={{ r: 4 }}
                    />
                    {/* Highlight pattern occurrences */}
                    <Line
                      type="monotone"
                      dataKey="isPattern"
                      stroke="#10b981"
                      strokeWidth={3}
                      dot={false}
                      connectNulls={false}
                    />
                    {/* Pattern start markers */}
                    <Scatter
                      dataKey="patternStart"
                      fill="#10b981"
                      shape="circle"
                      r={6}
                    />
                    {/* Pattern end markers */}
                    <Scatter
                      dataKey="patternEnd"
                      fill="#ef4444"
                      shape="circle"
                      r={6}
                    />
                  </ComposedChart>
                </ResponsiveContainer>
                <div className="flex items-center justify-center gap-6 mt-4 text-sm">
                  <div className="flex items-center gap-2">
                    <div className="w-4 h-0.5 bg-blue-500"></div>
                    <span className="text-gray-400">Stock Price</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-4 h-0.5 bg-accent"></div>
                    <span className="text-gray-400">Pattern Active</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-accent"></div>
                    <span className="text-gray-400">Pattern Start</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-red-500"></div>
                    <span className="text-gray-400">Pattern End</span>
                  </div>
                </div>
              </div>
            ) : (
              <div className="h-96 flex items-center justify-center text-gray-400">
                <p>Price data not available</p>
              </div>
            )}
          </div>


          {/* Pattern Details */}
          <div className="bg-bg border border-border rounded-lg p-6">
            <h3 className="font-header text-lg font-semibold text-white mb-4">
              Pattern Configuration
            </h3>
            <div className="space-y-3 text-sm">
              <div className="flex items-start gap-2">
                <span className="text-gray-400 min-w-[120px]">Pattern Name:</span>
                <span className="text-white font-medium">{pattern.name}</span>
              </div>
              <div className="flex items-start gap-2">
                <span className="text-gray-400 min-w-[120px]">Description:</span>
                <span className="text-white">{pattern.description}</span>
              </div>
              <div className="flex items-start gap-2">
                <span className="text-gray-400 min-w-[120px]">Min Occurrences:</span>
                <span className="text-white">{pattern.frequency.min_occurrences}</span>
              </div>
              <div className="flex items-start gap-2">
                <span className="text-gray-400 min-w-[120px]">Timeframe:</span>
                <span className="text-white">{pattern.frequency.timeframe_days} days</span>
              </div>
            </div>
          </div>

          {/* Close Button */}
          <div className="flex justify-end">
            <button
              onClick={onClose}
              className="px-6 py-2 bg-accent text-black rounded-lg font-semibold hover:bg-accent/90 transition shadow-glow"
            >
              Close
            </button>
          </div>
        </div>
        </div>
      </div>
    </div>
  );
}
