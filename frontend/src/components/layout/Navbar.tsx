import React from 'react';

interface NavbarProps {
    activeView: 'dashboard' | 'builder' | 'profile';
    onNavigate: (view: 'dashboard' | 'builder' | 'profile') => void;
}

export function Navbar({ activeView, onNavigate }: NavbarProps) {
    return (
        <nav className="fixed top-0 left-0 right-0 h-16 z-50 flex items-center justify-between px-6 md:px-12 bg-black/40 backdrop-blur-2xl border-b border-white/5 transition-all duration-300">

            {/* 1. Logo Section */}
            <div className="flex items-center gap-8 cursor-pointer" onClick={() => onNavigate('dashboard')}>
                <h1 className="font-header font-bold text-xl tracking-wide text-white flex items-center gap-2">
                    {/* Minimal Logo Icon */}
                    <div className="w-5 h-5 bg-accent rounded-full shadow-[0_0_15px_rgba(16,185,129,0.4)]"></div>
                    TEMPLE
                </h1>
            </div>

            {/* 2. Central Navigation (Pill Style) */}
            <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 hidden md:flex items-center p-1 rounded-full bg-white/5 border border-white/5 backdrop-blur-md">
                <button
                    onClick={() => onNavigate('dashboard')}
                    className={`px-6 py-1.5 rounded-full text-sm font-medium transition-all duration-300 ${activeView === 'dashboard'
                        ? 'bg-surface text-white shadow-lg shadow-black/20'
                        : 'text-gray-400 hover:text-white'
                        }`}
                >
                    Dashboard
                </button>
                <button
                    onClick={() => onNavigate('builder')}
                    className={`px-6 py-1.5 rounded-full text-sm font-medium transition-all duration-300 ${activeView === 'builder'
                        ? 'bg-surface text-white shadow-lg shadow-black/20'
                        : 'text-gray-400 hover:text-white'
                        }`}
                >
                    Builder
                </button>
            </div>

            {/* 3. Right Actions (Profile/Tools) */}
            <div className="flex items-center gap-6">
                {/* Indicators */}
                <div className="hidden md:flex items-center gap-4 text-xs font-mono text-gray-400">
                    <div className="flex items-center gap-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse"></span>
                        <span>SYSTEM ONLINE</span>
                    </div>
                </div>

                {/* Profile */}
                <div
                    className={`flex items-center gap-3 pl-6 border-l border-white/5 cursor-pointer group transition-opacity ${activeView === 'profile' ? 'opacity-100' : 'opacity-80 hover:opacity-100'}`}
                    onClick={() => onNavigate('profile')}
                >
                    <div className="flex flex-col items-end">
                        <span className={`text-sm font-semibold transition-colors ${activeView === 'profile' ? 'text-white' : 'text-gray-300 group-hover:text-white'}`}>Top Trader</span>
                        <span className="text-[10px] text-accent">PRO ACC</span>
                    </div>
                    <div className={`w-9 h-9 rounded-full bg-gradient-to-br from-gray-700 to-black border shadow-inner transition-colors ${activeView === 'profile' ? 'border-accent' : 'border-white/10 group-hover:border-white/30'}`}></div>
                </div>
            </div>
        </nav>
    );
}
