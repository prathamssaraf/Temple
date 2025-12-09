import React from 'react';

interface SidebarProps {
    activeView: 'dashboard' | 'builder';
    onNavigate: (view: 'dashboard' | 'builder') => void;
}

export function Sidebar({ activeView, onNavigate }: SidebarProps) {
    return (
        <>
            {/* Mobile Nav Toggle (Hidden on Desktop) - Placeholder for now */}
            <div className="md:hidden fixed bottom-0 left-0 right-0 z-50 bg-surface border-t border-border p-4 flex justify-between items-center glass-sidebar">
                {/* Simplified mobile nav for initial port */}
                <span className="text-xs text-gray-500">Mobile Nav Pending</span>
            </div>

            {/* Sidebar (Desktop) */}
            <aside className="hidden md:flex w-[240px] flex-col glass-sidebar fixed h-full z-40">
                {/* Logo */}
                <div className="h-20 flex items-center px-8 border-b border-border/50">
                    <h1 className="font-header font-bold text-xl tracking-ultra-wide text-white">TEMPLE</h1>
                </div>

                {/* Navigation */}
                <nav className="flex-1 py-8 flex flex-col gap-2 px-0">
                    {/* Active Item (Dashboard) */}
                    <button
                        onClick={() => onNavigate('dashboard')}
                        className={`group relative flex items-center gap-4 px-8 py-3 text-sm font-medium transition-colors border-l-2 border-r-2 border-transparent w-full text-left ${activeView === 'dashboard'
                                ? 'text-white bg-surface/50 border-r-transparent'
                                : 'text-gray-400 hover:text-white'
                            }`}
                    >
                        {activeView === 'dashboard' && (
                            <div className="absolute left-0 top-0 bottom-0 w-[2px] bg-accent shadow-[0_0_10px_rgba(16,185,129,0.5)]"></div>
                        )}

                        <svg
                            className={activeView === 'dashboard' ? 'text-accent' : 'group-hover:text-white transition-colors'}
                            width="24"
                            height="24"
                            viewBox="0 0 24 24"
                            fill="none"
                            xmlns="http://www.w3.org/2000/svg"
                        >
                            <path d="M14 14H19" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
                            <path d="M14 10H19" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
                            <path
                                opacity="0.5"
                                d="M10 19C10 20.6569 13.3579 22 17.5 22C21.6421 22 25 20.6569 25 19V5C25 3.34315 21.6421 2 17.5 2C13.3579 2 10 3.34315 10 5V19Z"
                                stroke="currentColor"
                                strokeWidth="1.5"
                            />
                            <path
                                d="M10 5C10 6.65685 6.64214 8 2.5 8C3.88071 8 0.5 6.65685 0.5 5C0.5 3.34315 3.88071 2 8 2"
                                stroke="currentColor"
                                strokeWidth="1.5"
                            />
                            <rect x="2" y="2" width="9" height="9" rx="2" stroke="currentColor" strokeWidth="1.5" />
                            <rect x="13" y="13" width="9" height="9" rx="2" stroke="currentColor" strokeWidth="1.5" />
                            <rect x="13" y="2" width="9" height="9" rx="2" stroke="currentColor" strokeWidth="1.5" opacity="0.5" />
                            <rect x="2" y="13" width="9" height="9" rx="2" stroke="currentColor" strokeWidth="1.5" opacity="0.5" />
                        </svg>
                        Dashboard
                    </button>

                    {/* Inactive Item (Builder) */}
                    <button
                        onClick={() => onNavigate('builder')}
                        className={`group relative flex items-center gap-4 px-8 py-3 text-sm font-medium transition-colors border-l-2 border-r-2 border-transparent w-full text-left ${activeView === 'builder'
                                ? 'text-white bg-surface/50 border-r-transparent'
                                : 'text-gray-400 hover:text-white'
                            }`}
                    >
                        {activeView === 'builder' && (
                            <div className="absolute left-0 top-0 bottom-0 w-[2px] bg-accent shadow-[0_0_10px_rgba(16,185,129,0.5)]"></div>
                        )}
                        <svg
                            className={activeView === 'builder' ? 'text-accent' : 'group-hover:text-white transition-colors'}
                            width="24"
                            height="24"
                            viewBox="0 0 24 24"
                            fill="none"
                            xmlns="http://www.w3.org/2000/svg"
                        >
                            <path
                                d="M21 16V8C21 6.89543 20.1046 6 19 6H5C3.89543 6 3 6.89543 3 8V16C3 17.1046 3.89543 18 5 18H19C20.1046 18 21 17.1046 21 16Z"
                                stroke="currentColor"
                                strokeWidth="1.5"
                                opacity="0.5"
                            />
                            <path d="M12 18V6" stroke="currentColor" strokeWidth="1.5" />
                            <path d="M16 18V12" stroke="currentColor" strokeWidth="1.5" />
                            <path d="M8 18V14" stroke="currentColor" strokeWidth="1.5" />
                        </svg>
                        Builder
                    </button>

                    <button className="group relative flex items-center gap-4 px-8 py-3 text-sm font-medium text-gray-400 hover:text-white transition-colors border-l-2 border-transparent w-full text-left">
                        <svg
                            className="group-hover:text-white transition-colors"
                            width="24"
                            height="24"
                            viewBox="0 0 24 24"
                            fill="none"
                            xmlns="http://www.w3.org/2000/svg"
                        >
                            <circle cx="11" cy="11" r="7" stroke="currentColor" strokeWidth="1.5" opacity="0.5" />
                            <path d="M20 20L17 17" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
                        </svg>
                        Scanner
                    </button>

                    <button className="group relative flex items-center gap-4 px-8 py-3 text-sm font-medium text-gray-400 hover:text-white transition-colors border-l-2 border-transparent w-full text-left">
                        <svg
                            className="group-hover:text-white transition-colors"
                            width="24"
                            height="24"
                            viewBox="0 0 24 24"
                            fill="none"
                            xmlns="http://www.w3.org/2000/svg"
                        >
                            <path
                                d="M20 18H4C2.89543 18 2 17.1046 2 16V6C2 4.89543 2.89543 4 4 4H20C21.1046 4 22 4.89543 22 6V16C22 17.1046 21.1046 18 20 18Z"
                                stroke="currentColor"
                                strokeWidth="1.5"
                                opacity="0.5"
                            />
                            <path d="M9 12H15" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
                        </svg>
                        Library
                    </button>
                </nav>

                {/* User Profile (Bottom) */}
                <div className="h-20 border-t border-border/50 flex items-center px-8 gap-3">
                    <div className="w-8 h-8 rounded-full bg-gradient-to-br from-gray-700 to-black border border-gray-600"></div>
                    <div className="flex flex-col">
                        <span className="text-xs font-semibold text-white">Top Trader</span>
                        <span className="text-[10px] text-gray-400">Pro Plan</span>
                    </div>
                </div>
            </aside>
        </>
    );
}
