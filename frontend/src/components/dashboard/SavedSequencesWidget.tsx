import React from 'react';

export function SavedSequencesWidget() {
    return (
        <div className="p-5 rounded-xl bg-surface border border-border shadow-sm">
            <div className="flex items-center justify-between mb-4">
                <h3 className="font-header font-semibold text-white text-sm">Saved Sequences</h3>
                <svg className="text-gray-500 hover:text-white cursor-pointer transition-colors" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M5 12h14M12 5v14" /></svg>
            </div>

            <div className="flex flex-col gap-2">
                {/* Item 1 */}
                <div className="group p-3 rounded-lg border border-border bg-bg/50 hover:border-accent/40 hover:bg-surface transition-all cursor-pointer">
                    <div className="flex items-center justify-between mb-2">
                        <span className="text-sm font-medium text-gray-200 group-hover:text-white">Morning Reversal</span>
                        <span className="w-2 h-2 rounded-full bg-accent/50 group-hover:bg-accent group-hover:shadow-[0_0_8px_#10b981] transition-all"></span>
                    </div>
                    <div className="flex gap-1">
                        <span className="px-1.5 py-0.5 rounded bg-white/5 text-[10px] text-gray-500">15m</span>
                        <span className="px-1.5 py-0.5 rounded bg-white/5 text-[10px] text-gray-500">RSI &lt; 30</span>
                    </div>
                </div>

                {/* Item 2 */}
                <div className="group p-3 rounded-lg border border-border bg-bg/50 hover:border-accent/40 hover:bg-surface transition-all cursor-pointer">
                    <div className="flex items-center justify-between mb-2">
                        <span className="text-sm font-medium text-gray-200 group-hover:text-white">Gap Fill Long</span>
                        <span className="w-2 h-2 rounded-full bg-blue-500/50 group-hover:bg-blue-500 transition-all"></span>
                    </div>
                    <div className="flex gap-1">
                        <span className="px-1.5 py-0.5 rounded bg-white/5 text-[10px] text-gray-500">1h</span>
                        <span className="px-1.5 py-0.5 rounded bg-white/5 text-[10px] text-gray-500">Gap &gt; 1%</span>
                    </div>
                </div>
            </div>

            <button className="w-full mt-4 py-2 rounded-lg border border-dashed border-gray-700 text-xs text-gray-500 hover:text-white hover:border-gray-500 transition-colors">
                View All Saved
            </button>
        </div>
    );
}
