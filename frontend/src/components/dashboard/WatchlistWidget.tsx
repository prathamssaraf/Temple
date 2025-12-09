import React from 'react';

export function WatchlistWidget() {
    return (
        <div className="p-5 rounded-xl bg-surface border border-border shadow-sm">
            <div className="flex items-center justify-between mb-4">
                <h3 className="font-header font-semibold text-white text-sm">Watchlist</h3>
                <button className="text-xs text-accent hover:text-white transition-colors">+ Add</button>
            </div>

            <div className="flex flex-col gap-1">
                {[
                    { ticker: 'NVDA', price: '892.40', change: '+2.4%', up: true },
                    { ticker: 'TSLA', price: '178.20', change: '-1.2%', up: false },
                    { ticker: 'AMD', price: '164.55', change: '+0.8%', up: true },
                    { ticker: 'SPY', price: '512.30', change: '+0.4%', up: true },
                ].map((item) => (
                    <div key={item.ticker} className="flex items-center justify-between p-2 hover:bg-white/5 rounded-lg transition-colors cursor-pointer group">
                        <div className="flex items-center gap-3">
                            <div className={`w-1 h-8 rounded-full ${item.up ? 'bg-accent' : 'bg-red-500/80'}`}></div>
                            <div>
                                <div className="font-bold text-sm text-white group-hover:text-accent transition-colors">{item.ticker}</div>
                                <div className="text-[10px] text-gray-500">Vol: 24M</div>
                            </div>
                        </div>
                        <div className="text-right">
                            <div className="text-sm font-medium text-gray-200">{item.price}</div>
                            <div className={`text-xs ${item.up ? 'text-accent' : 'text-red-400'}`}>{item.change}</div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
