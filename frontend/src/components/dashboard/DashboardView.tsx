import React from 'react';
import { ScannerTable } from './ScannerTable';
import { SavedSequencesWidget } from './SavedSequencesWidget';
import { WatchlistWidget } from './WatchlistWidget';
import { FixedPatternsWidget } from './FixedPatternsWidget';
import { BackgroundSequencesWidget } from './BackgroundSequencesWidget';

interface DashboardViewProps {
    onNavigateBuilder: () => void;
    onNavigateDetail: () => void;
}

export function DashboardView({ onNavigateBuilder, onNavigateDetail }: DashboardViewProps) {
    return (
        <div className="view-section px-4 md:px-8 py-6 relative z-10 animate-slide-up">
            {/* Header / Hero */}
            <header className="mb-8">
                <h2 className="font-header text-2xl md:text-3xl font-semibold mb-1 text-white">Welcome back, Trader.</h2>
                <p className="text-gray-400 text-sm">
                    Markets are volatile today. The "Morning Star" pattern is trending in Tech.
                </p>
            </header>

            {/* Main Grid Layout */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">

                {/* Left Column (Main Content) - Spans 8 cols */}
                <div className="lg:col-span-8 flex flex-col gap-6">

                    {/* Top Row: Active Sequence + Background Scans */}
                    <div className="flex flex-col xl:flex-row gap-6">
                        {/* 1. Pattern Builder Card (Compacted) */}
                        <section className="flex-none">
                            <div className="relative w-fit p-[1px] rounded-xl bg-gradient-to-r from-border via-border to-border hover:via-accent/30 transition-all duration-500 group">
                                <div className="absolute inset-0 bg-accent/5 blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>

                                <div className="relative bg-surface rounded-xl p-5 overflow-hidden shadow-glow hover:shadow-[0_0_60px_-15px_rgba(16,185,129,0.15)] transition-shadow duration-300">
                                    <div className="flex justify-between items-center mb-4">
                                        <div>
                                            <h3 className="font-header text-base font-semibold text-white flex items-center gap-2">
                                                <span className="w-2 h-2 rounded-full bg-accent animate-pulse"></span>
                                                Active Sequence
                                            </h3>
                                        </div>
                                        <button
                                            onClick={onNavigateBuilder}
                                            className="relative inline-flex h-8 overflow-hidden rounded-lg p-[1px] focus:outline-none focus:ring-2 focus:ring-accent focus:ring-offset-2 focus:ring-offset-gray-900 group/btn"
                                        >
                                            <span className="absolute inset-[-1000%] animate-spin-slow bg-[conic-gradient(from_90deg_at_50%_50%,#09090b_0%,#10b981_50%,#09090b_100%)]"></span>
                                            <span className="inline-flex h-full w-full cursor-pointer items-center justify-center rounded-lg bg-surface px-4 py-1 text-xs font-medium text-white backdrop-blur-3xl transition-colors hover:bg-surface/80">
                                                Open Builder
                                            </span>
                                        </button>
                                    </div>

                                    {/* Compact Visualization */}
                                    <div className="relative h-48 bg-bg/50 rounded-lg border border-border/50 flex items-center justify-center p-4">
                                        {/* Grid Lines */}
                                        <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:24px_24px]"></div>

                                        {/* Steps */}
                                        <div className="flex items-center gap-12 md:gap-20 z-10 relative">
                                            {/* Step 1 */}
                                            <div className="flex flex-col items-center gap-3">
                                                <div className="w-16 h-16 rounded-2xl bg-surface border border-border flex items-center justify-center text-gray-400 shadow-lg">
                                                    <svg width="28" height="28" fill="none" className="opacity-80">
                                                        <rect width="28" height="28" rx="6" fill="currentColor" />
                                                    </svg>
                                                </div>
                                                <span className="text-xs font-mono text-gray-500 font-medium tracking-wide">ENTRY</span>
                                            </div>

                                            {/* Compact Beam - Legacy Exact Match */}
                                            <div className="relative w-32 h-[2px] bg-border overflow-visible">
                                                {/* Static Track */}
                                                <div className="absolute top-1/2 left-0 -translate-y-1/2 w-full h-[1px] bg-accent/20"></div>
                                                {/* Moving Beam */}
                                                <div className="absolute top-1/2 left-0 -translate-y-1/2 h-[3px] w-8 bg-accent blur-[2px] animate-beam-flow"></div>
                                            </div>

                                            {/* Step 2 */}
                                            <div className="flex flex-col items-center gap-3">
                                                <div className="w-16 h-16 rounded-2xl bg-surface border border-accent/20 shadow-[0_0_20px_-5px_#10b981] flex items-center justify-center text-white">
                                                    <svg
                                                        width="28"
                                                        height="28"
                                                        viewBox="0 0 24 24"
                                                        fill="none"
                                                        stroke="currentColor"
                                                        strokeWidth="2"
                                                    >
                                                        <polyline points="22 7 13.5 15.5 8.5 10.5 2 17"></polyline>
                                                        <polyline points="16 7 22 7 22 13"></polyline>
                                                    </svg>
                                                </div>
                                                <span className="text-xs font-mono text-accent font-medium tracking-wide">TRIGGER</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </section>

                        {/* 2. Background Sequences Widget */}
                        <BackgroundSequencesWidget />
                    </div>

                    {/* 3. Scanner Table (Compacted) */}
                    <section>
                        <div className="flex items-center justify-between mb-4">
                            <h3 className="font-header text-lg font-semibold">Live Signals</h3>
                            <div className="flex gap-2">
                                <span className="px-2 py-0.5 rounded bg-accent/10 text-accent text-[10px] font-mono">LIVE</span>
                            </div>
                        </div>
                        <ScannerTable onRowClick={onNavigateDetail} />
                    </section>
                </div>

                {/* Right Column (Widgets) - Spans 4 cols */}
                <div className="lg:col-span-4 flex flex-col gap-6">
                    <SavedSequencesWidget />
                    <WatchlistWidget />
                    <FixedPatternsWidget />
                </div>

            </div>
        </div>
    );
}
