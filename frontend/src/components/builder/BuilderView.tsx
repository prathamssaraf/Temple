import React, { useState } from 'react';

// Types for Builder Nodes
interface BuilderNode {
    id: string;
    type: string;
    label: string;
}

export function BuilderView() {
    const [nodes, setNodes] = useState<BuilderNode[]>([
        { id: '1', type: 'condition', label: 'Condition 1' },
    ]);
    const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);

    const addNode = (label: string, type: string) => {
        const newNode: BuilderNode = {
            id: Date.now().toString(),
            label,
            type,
        };
        // Insert before the last item if we were strictly following the "Add Step" placeholder logic,
        // but simplified here: append to list
        setNodes([...nodes, newNode]);
    };

    return (
        <div className="h-full flex flex-col relative z-10 animate-slide-up">
            {/* Builder Header */}
            <header className="h-16 border-b border-border flex items-center justify-between px-6 bg-surface/50 backdrop-blur-md sticky top-0 z-30">
                <div className="flex items-center gap-4">
                    <h2 className="font-header text-lg font-semibold text-white">New Pattern Sequence</h2>
                    <span className="px-2 py-0.5 rounded text-[10px] bg-border text-gray-400 font-mono">DRAFT</span>
                </div>
                <div className="flex gap-3">
                    <button className="px-4 py-1.5 text-sm text-gray-400 hover:text-white transition-colors">Discard</button>
                    <button className="px-4 py-1.5 rounded-lg bg-accent text-black text-sm font-semibold hover:bg-accent/90 transition-colors shadow-glow">
                        Save Pattern
                    </button>
                </div>
            </header>

            {/* Builder Layout: 3 Columns */}
            <div className="flex-1 flex overflow-hidden">
                {/* 1. Toolbox (Left) */}
                <div className="w-64 border-r border-border bg-bg/50 flex flex-col">
                    <div className="p-4 border-b border-border/50">
                        <span className="text-xs uppercase tracking-wider text-gray-500 font-semibold">Nodes</span>
                    </div>
                    <div className="p-4 flex flex-col gap-3 overflow-y-auto">
                        {/* Tool Items */}
                        {[
                            { label: 'One Candle', iconPath: 'M8 2v20M5 6h6v12H5z', type: 'candle' },
                            { label: 'Pattern Group', iconPath: 'M3 8h4v8H3zM9 4h4v12H9zM15 10h4v6h-4z', type: 'group' },
                            { label: 'Indicator (RSI)', iconPath: 'M22 12h-4l-3 9L9 3l-3 9H2', type: 'indicator' },
                            { label: 'Condition (If/Else)', iconPath: 'M6 9l6 6 6-6', type: 'logic' }
                        ].map((tool) => (
                            <div
                                key={tool.label}
                                onClick={() => addNode(tool.label, tool.type)}
                                className="group p-3 rounded-lg border border-border bg-surface hover:border-accent/50 cursor-move transition-all flex items-center gap-3"
                            >
                                <div className="w-8 h-8 rounded bg-white/5 flex items-center justify-center text-gray-400">
                                    <svg width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2">
                                        <path d={tool.iconPath} />
                                    </svg>
                                </div>
                                <span className="text-sm font-medium text-gray-300 group-hover:text-white">{tool.label}</span>
                            </div>
                        ))}
                    </div>
                </div>

                {/* 2. Canvas (Center) */}
                <div className="flex-1 bg-[linear-gradient(#27272a_1px,transparent_1px),linear-gradient(90deg,#27272a_1px,transparent_1px)] bg-[size:40px_40px] bg-[position:center] relative overflow-hidden flex items-center justify-center">
                    <div className="absolute inset-0 bg-bg/80"></div> {/* Dim grid */}

                    {/* Canvas Content acts as a sequence */}
                    <div className="relative z-10 flex items-center gap-0 overflow-x-auto p-8 max-w-full">

                        {/* Start Node */}
                        <div className="flex items-center flex-shrink-0">
                            <div className="w-32 h-16 rounded-full border border-dashed border-gray-600 bg-surface/50 flex items-center justify-center text-xs text-gray-500 font-mono">
                                START
                            </div>
                            <div className="w-16 h-[2px] bg-gray-700"></div>
                        </div>

                        {/* Dynamic Nodes */}
                        {nodes.map((node) => (
                            <React.Fragment key={node.id}>
                                <div
                                    className="relative group cursor-pointer animate-slide-up flex-shrink-0"
                                    onClick={(e) => {
                                        e.stopPropagation();
                                        setSelectedNodeId(node.id);
                                    }}
                                >
                                    <div
                                        className={`w-48 p-4 rounded-xl bg-surface border shadow-lg flex flex-col gap-2 relative z-10 transition-colors ${selectedNodeId === node.id
                                            ? 'border-accent shadow-[0_0_20px_-5px_rgba(16,185,129,0.2)]'
                                            : 'border-border hover:border-accent/50'
                                            }`}
                                    >
                                        <div className="flex items-center justify-between">
                                            <span className="text-xs font-bold text-gray-300 uppercase tracking-wider">{node.label}</span>
                                            <svg className="text-gray-500" width="14" height="14" fill="none" stroke="currentColor">
                                                <circle cx="7" cy="7" r="6" />
                                            </svg>
                                        </div>
                                        <div className="text-sm text-gray-500">Not Configured</div>
                                    </div>
                                </div>

                                {/* Connection Line (Always present after node for simplicity in this prototype) */}
                                <div className="w-16 h-[2px] bg-gray-700 relative flex-shrink-0">
                                    <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-4 h-4 rounded-full bg-bg border border-gray-600 flex items-center justify-center text-[8px] text-gray-400 text-center leading-none">
                                        +
                                    </div>
                                </div>
                            </React.Fragment>
                        ))}

                        {/* Placeholder */}
                        <div className="w-48 h-24 rounded-xl border-2 border-dashed border-gray-700 bg-surface/20 flex flex-col items-center justify-center gap-2 hover:border-gray-500 hover:bg-surface/40 transition-all cursor-pointer flex-shrink-0">
                            <span className="text-2xl text-gray-600 font-light">+</span>
                            <span className="text-xs text-gray-500">Add Step</span>
                        </div>
                    </div>
                </div>

                {/* 3. Properties (Right) */}
                <div className="w-72 border-l border-border bg-bg/90 backdrop-blur flex flex-col">
                    <div className="p-4 border-b border-border/50">
                        <span className="text-xs uppercase tracking-wider text-gray-500 font-semibold">Properties</span>
                    </div>
                    <div className="p-6 flex flex-col gap-6">
                        {selectedNodeId ? (
                            <>
                                <div>
                                    <label className="block text-[10px] text-gray-500 uppercase tracking-wider font-semibold mb-2">
                                        Block Type
                                    </label>
                                    <input
                                        type="text"
                                        value={nodes.find(n => n.id === selectedNodeId)?.label || ''}
                                        className="w-full bg-surface border border-border rounded p-2 text-sm text-white focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent"
                                        disabled
                                    />
                                </div>

                                <div>
                                    <label className="block text-[10px] text-gray-500 uppercase tracking-wider font-semibold mb-2">
                                        Configuration
                                    </label>
                                    <p className="text-xs text-gray-400">Settings for this node would appear here.</p>
                                </div>

                                <div className="pt-4 border-t border-border/50">
                                    <button
                                        onClick={() => {
                                            setNodes(nodes.filter(n => n.id !== selectedNodeId));
                                            setSelectedNodeId(null);
                                        }}
                                        className="w-full py-2 rounded border border-red-500/30 text-red-400 text-xs hover:bg-red-500/10 transition-colors"
                                    >
                                        Remove Node
                                    </button>
                                </div>
                            </>
                        ) : (
                            <div className="text-sm text-gray-500 italic">Select a node on the canvas to configure properties.</div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
