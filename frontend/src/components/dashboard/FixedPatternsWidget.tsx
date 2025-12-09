import React from 'react';

export function FixedPatternsWidget() {
    return (
        <div className="p-5 rounded-xl bg-surface border border-border shadow-sm">
            <div className="flex items-center justify-between mb-4">
                <h3 className="font-header font-semibold text-white text-sm">Fixed Patterns</h3>
            </div>

            <div className="grid grid-cols-2 gap-2">
                {[
                    'Double Bottom', 'Head & Shoulders', 'Cup & Handle', 'Bull Flag', 'Ascending Triangle', 'Falling Wedge'
                ].map((pattern) => (
                    <div key={pattern} className="px-3 py-2 rounded-lg bg-white/5 border border-transparent hover:border-white/10 hover:bg-white/10 cursor-pointer transition-colors text-center">
                        <span className="text-xs font-medium text-gray-400 hover:text-white">{pattern}</span>
                    </div>
                ))}
            </div>
        </div>
    );
}
