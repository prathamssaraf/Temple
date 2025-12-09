import React from 'react';

export function BackgroundSequencesWidget() {
    return (
        <section className="flex-1 min-w-[300px]">
            <div className="relative h-full p-[1px] rounded-xl bg-gradient-to-r from-border via-border to-border hover:via-accent/30 transition-all duration-500 group">
                <div className="absolute inset-0 bg-accent/5 blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>

                <div className="relative h-full bg-surface rounded-xl p-5 overflow-hidden shadow-glow hover:shadow-[0_0_60px_-15px_rgba(16,185,129,0.15)] transition-shadow duration-300 flex flex-col">
                    <div className="flex justify-between items-center mb-4">
                        <h3 className="font-header text-base font-semibold text-white flex items-center gap-2">
                            <span className="w-1.5 h-1.5 rounded-full bg-gray-500"></span>
                            Background Scans
                        </h3>
                        <span className="text-[10px] bg-border/50 text-gray-400 px-2 py-0.5 rounded font-mono">3 RUNNING</span>
                    </div>

                    <div className="flex-1 flex flex-col gap-3">
                        {/* Item 1 */}
                        <div className="flex items-center gap-3 p-2 rounded-lg hover:bg-white/5 transition-colors cursor-pointer group/item">
                            <div className="w-8 h-8 rounded bg-bg border border-border flex items-center justify-center text-gray-400 group-hover/item:text-accent group-hover/item:border-accent/50 transition-colors">
                                <svg width="14" height="14" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 2v20M2 17h20M2 12h20M2 7h20" /></svg>
                            </div>
                            <div className="flex-1 min-w-0">
                                <div className="flex justify-between">
                                    <span className="text-xs font-semibold text-gray-200">Bull Flag</span>
                                    <span className="text-[10px] text-gray-500">15m</span>
                                </div>
                                <div className="text-[10px] text-gray-500 truncate">Tech Sector • High Volatility</div>
                            </div>
                            <div className="w-1.5 h-1.5 rounded-full bg-accent animate-pulse"></div>
                        </div>

                        {/* Item 2 */}
                        <div className="flex items-center gap-3 p-2 rounded-lg hover:bg-white/5 transition-colors cursor-pointer group/item">
                            <div className="w-8 h-8 rounded bg-bg border border-border flex items-center justify-center text-gray-400 group-hover/item:text-accent group-hover/item:border-accent/50 transition-colors">
                                <svg width="14" height="14" fill="none" stroke="currentColor" strokeWidth="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2" /></svg>
                            </div>
                            <div className="flex-1 min-w-0">
                                <div className="flex justify-between">
                                    <span className="text-xs font-semibold text-gray-200">RSI Divergence</span>
                                    <span className="text-[10px] text-gray-500">1h</span>
                                </div>
                                <div className="text-[10px] text-gray-500 truncate">Crypto • Top 10</div>
                            </div>
                            <div className="w-1.5 h-1.5 rounded-full bg-accent animate-pulse" style={{ animationDelay: '0.5s' }}></div>
                        </div>

                        {/* Item 3 */}
                        <div className="flex items-center gap-3 p-2 rounded-lg hover:bg-white/5 transition-colors cursor-pointer group/item">
                            <div className="w-8 h-8 rounded bg-bg border border-border flex items-center justify-center text-gray-400 group-hover/item:text-accent group-hover/item:border-accent/50 transition-colors">
                                <svg width="14" height="14" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10" /><path d="M16 12l-4-4-4 4M12 16V9" /></svg>
                            </div>
                            <div className="flex-1 min-w-0">
                                <div className="flex justify-between">
                                    <span className="text-xs font-semibold text-gray-200">Morning Star</span>
                                    <span className="text-[10px] text-gray-500">4h</span>
                                </div>
                                <div className="text-[10px] text-gray-500 truncate">Energy • Breakout</div>
                            </div>
                            <div className="w-1.5 h-1.5 rounded-full bg-accent animate-pulse" style={{ animationDelay: '1s' }}></div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
}
