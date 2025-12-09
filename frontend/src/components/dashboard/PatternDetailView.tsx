import React from 'react';

interface PatternDetailViewProps {
    onBack: () => void;
}

export function PatternDetailView({ onBack }: PatternDetailViewProps) {
    return (
        <div className="view-section px-4 md:px-8 py-6 relative z-10 animate-slide-up">

            {/* Header Navigation */}
            <div className="mb-6">
                <button
                    onClick={onBack}
                    className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors group"
                >
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="group-hover:-translate-x-1 transition-transform">
                        <path d="M19 12H5M12 19l-7-7 7-7" />
                    </svg>
                    <span className="text-sm font-medium">Back to Dashboard</span>
                </button>
            </div>

            {/* Main Header */}
            <header className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-8 border-b border-border/50 pb-8">
                <div>
                    <div className="flex items-center gap-4 mb-2">
                        <h1 className="font-header text-5xl font-bold text-white tracking-tight">NVDA</h1>
                        <span className="px-3 py-1 rounded-md bg-accent/10 text-accent text-sm font-mono border border-accent/20">
                            BULLISH ENGULFING
                        </span>
                        <span className="px-2 py-1 rounded bg-gray-800 text-gray-400 text-xs font-mono">15m</span>
                    </div>
                    <p className="text-gray-400 text-sm max-w-xl">
                        Strong reversal signal detected at key support level. Volume confirmation indicates high probability of trend reversal.
                    </p>
                </div>

                <div className="flex items-center gap-4">
                    <div className="text-right mr-4">
                        <div className="text-xs text-gray-500 uppercase tracking-wide mb-1">Confidence</div>
                        <div className="text-3xl font-bold text-accent">92%</div>
                    </div>
                    <button className="h-12 px-6 rounded-lg bg-accent text-black font-semibold hover:bg-accent/90 transition-colors shadow-[0_0_20px_rgba(16,185,129,0.2)]">
                        Execute Trade
                    </button>
                    <button className="h-12 w-12 rounded-lg border border-border bg-surface hover:bg-white/5 flex items-center justify-center text-gray-400 hover:text-white transition-colors">
                        <svg width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2"><path d="M5 12h14M12 5l7 7-7 7" /></svg>
                    </button>
                </div>
            </header>

            {/* Grid Layout */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

                {/* Left Column - Chart (Spans 2) */}
                <div className="lg:col-span-2 space-y-6">
                    {/* Chart Placeholder */}
                    <div className="w-full h-[500px] bg-surface/50 border border-border rounded-xl p-4 relative overflow-hidden group">
                        <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.03)_1px,transparent_1px)] bg-[size:40px_40px]"></div>

                        {/* Mock Candle Representation */}
                        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                            <span className="text-gray-600 font-mono text-sm">[ Interactive Chart Placeholder ]</span>
                        </div>

                        {/* Overlay Controls */}
                        <div className="absolute top-4 right-4 flex gap-2">
                            <button className="px-3 py-1.5 rounded bg-black/40 border border-white/10 text-xs text-gray-300 hover:text-white">1H</button>
                            <button className="px-3 py-1.5 rounded bg-black/40 border border-white/10 text-xs text-gray-300 hover:text-white">4H</button>
                            <button className="px-3 py-1.5 rounded bg-accent/20 border border-accent/40 text-xs text-accent">1D</button>
                        </div>
                    </div>

                    {/* Stats Grid */}
                    <div className="grid grid-cols-4 gap-4">
                        <div className="p-4 rounded-lg bg-surface border border-border">
                            <span className="text-xs text-gray-500 block mb-1">Entry Price</span>
                            <span className="text-lg font-mono text-white">$452.30</span>
                        </div>
                        <div className="p-4 rounded-lg bg-surface border border-border">
                            <span className="text-xs text-gray-500 block mb-1">Stop Loss</span>
                            <span className="text-lg font-mono text-red-400">$448.50</span>
                        </div>
                        <div className="p-4 rounded-lg bg-surface border border-border">
                            <span className="text-xs text-gray-500 block mb-1">Target 1</span>
                            <span className="text-lg font-mono text-green-400">$460.00</span>
                        </div>
                        <div className="p-4 rounded-lg bg-surface border border-border">
                            <span className="text-xs text-gray-500 block mb-1">Target 2</span>
                            <span className="text-lg font-mono text-green-400">$475.00</span>
                        </div>
                    </div>
                </div>

                {/* Right Column - Analysis */}
                <div className="space-y-6">

                    {/* Signal Analysis */}
                    <section className="p-6 rounded-xl bg-surface/30 border border-border">
                        <h3 className="font-header text-lg font-semibold text-white mb-4">Signal Analysis</h3>
                        <div className="space-y-4">
                            <div className="flex gap-4 items-start">
                                <div className="mt-1 w-2 h-2 rounded-full bg-accent shadow-[0_0_10px_#10b981]"></div>
                                <div>
                                    <h4 className="text-sm font-medium text-white">Trend Alignment</h4>
                                    <p className="text-xs text-gray-400 mt-1">Pattern formed in direction of major 4H trend.</p>
                                </div>
                            </div>
                            <div className="flex gap-4 items-start">
                                <div className="mt-1 w-2 h-2 rounded-full bg-accent shadow-[0_0_10px_#10b981]"></div>
                                <div>
                                    <h4 className="text-sm font-medium text-white">Volume Spike</h4>
                                    <p className="text-xs text-gray-400 mt-1">2.5x relative volume on the engulfing candle.</p>
                                </div>
                            </div>
                            <div className="flex gap-4 items-start">
                                <div className="mt-1 w-2 h-2 rounded-full bg-yellow-500"></div>
                                <div>
                                    <h4 className="text-sm font-medium text-white">RSI Divergence</h4>
                                    <p className="text-xs text-gray-400 mt-1">Mild bullish divergence on 15m timeframe.</p>
                                </div>
                            </div>
                        </div>
                    </section>

                    {/* Market Context */}
                    <section className="p-6 rounded-xl bg-surface/30 border border-border">
                        <h3 className="font-header text-lg font-semibold text-white mb-4">Market Context</h3>
                        <div className="space-y-3">
                            <div className="flex justify-between items-center text-sm">
                                <span className="text-gray-400">Sector (Tech)</span>
                                <span className="text-green-400 font-mono">+1.2%</span>
                            </div>
                            <div className="flex justify-between items-center text-sm">
                                <span className="text-gray-400">SPY Correlation</span>
                                <span className="text-white font-mono">0.85</span>
                            </div>
                            <div className="flex justify-between items-center text-sm">
                                <span className="text-gray-400">VIX</span>
                                <span className="text-red-400 font-mono">-2.4%</span>
                            </div>
                        </div>
                    </section>

                    <button className="w-full py-3 rounded-lg border border-border hover:bg-white/5 text-sm text-gray-300 transition-colors">
                        Add to Watchlist
                    </button>

                </div>

            </div>
        </div>
    );
}
