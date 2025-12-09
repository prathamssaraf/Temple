import React from 'react';

export function ProfileView() {
    return (
        <div className="view-section px-4 md:px-8 py-6 relative z-10 animate-slide-up">
            {/* Header / Hero */}
            <header className="mb-12 flex flex-col md:flex-row items-center gap-8">
                <div className="relative group">
                    <div className="w-24 h-24 md:w-32 md:h-32 rounded-full bg-gradient-to-br from-gray-700 to-black border-2 border-accent/30 shadow-[0_0_30px_-10px_rgba(16,185,129,0.3)] flex items-center justify-center text-4xl font-bold text-gray-500 group-hover:text-white transition-colors">
                        TT
                    </div>
                    <div className="absolute bottom-0 right-0 w-8 h-8 rounded-full bg-surface border border-border flex items-center justify-center text-accent shadow-lg cursor-pointer hover:bg-accent hover:text-black transition-colors">
                        <svg width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 20h9M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z" /></svg>
                    </div>
                </div>

                <div className="text-center md:text-left">
                    <h2 className="font-header text-3xl md:text-4xl font-semibold text-white mb-2">Top Trader</h2>
                    <div className="flex flex-wrap justify-center md:justify-start gap-3 text-sm">
                        <span className="text-gray-400">trader@temple.io</span>
                        <span className="text-gray-600">•</span>
                        <span className="text-accent font-mono">PRO PLAN</span>
                        <span className="text-gray-600">•</span>
                        <span className="text-gray-400">Member since 2024</span>
                    </div>
                </div>
            </header>

            {/* Content Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

                {/* 1. Account Details */}
                <section className="bg-surface/50 border border-border rounded-xl p-6 backdrop-blur-sm">
                    <h3 className="font-header text-lg font-semibold text-white mb-6 flex items-center gap-2">
                        <svg className="text-gray-400" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" /><circle cx="12" cy="7" r="4" /></svg>
                        Account Information
                    </h3>
                    <div className="space-y-4">
                        <div>
                            <label className="block text-[10px] uppercase tracking-wider text-gray-500 font-semibold mb-1">Display Name</label>
                            <input type="text" value="Top Trader" className="w-full bg-bg border border-border rounded-lg px-3 py-2 text-sm text-white focus:border-accent focus:outline-none transition-colors" />
                        </div>
                        <div>
                            <label className="block text-[10px] uppercase tracking-wider text-gray-500 font-semibold mb-1">Email Address</label>
                            <input type="email" value="trader@temple.io" className="w-full bg-bg border border-border rounded-lg px-3 py-2 text-sm text-white focus:border-accent focus:outline-none transition-colors" />
                        </div>
                        <div>
                            <label className="block text-[10px] uppercase tracking-wider text-gray-500 font-semibold mb-1">API Key</label>
                            <div className="flex gap-2">
                                <input type="password" value="sk_live_..." className="flex-1 bg-bg border border-border rounded-lg px-3 py-2 text-sm text-gray-400 font-mono focus:border-accent focus:outline-none transition-colors" readOnly />
                                <button className="px-3 py-2 bg-white/5 hover:bg-white/10 rounded-lg text-gray-300 transition-colors">Copy</button>
                            </div>
                        </div>
                    </div>
                </section>

                {/* 2. Subscription */}
                <section className="bg-surface/50 border border-border rounded-xl p-6 backdrop-blur-sm relative overflow-hidden group">
                    <div className="absolute top-0 right-0 p-4 opacity-50 group-hover:opacity-100 transition-opacity">
                        <div className="text-[10px] font-mono text-accent border border-accent/30 bg-accent/5 px-2 py-0.5 rounded">ACTIVE</div>
                    </div>

                    <h3 className="font-header text-lg font-semibold text-white mb-6 flex items-center gap-2">
                        <svg className="text-gray-400" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2"><rect x="1" y="4" width="22" height="16" rx="2" ry="2" /><line x1="1" y1="10" x2="23" y2="10" /></svg>
                        Subscription
                    </h3>

                    <div className="flex flex-col gap-4">
                        <div className="p-4 rounded-lg bg-gradient-to-br from-gray-800/50 to-black border border-border group-hover:border-accent/30 transition-colors">
                            <span className="text-xs text-gray-400 block mb-1">Current Plan</span>
                            <div className="flex items-baseline gap-1">
                                <span className="text-2xl font-header font-bold text-white">Pro</span>
                                <span className="text-sm text-gray-500">/ month</span>
                            </div>
                        </div>

                        <div className="space-y-2">
                            <div className="flex justify-between text-sm">
                                <span className="text-gray-400">Pattern Limit</span>
                                <span className="text-white">Unlimited</span>
                            </div>
                            <div className="flex justify-between text-sm">
                                <span className="text-gray-400">Updates</span>
                                <span className="text-white">Real-time</span>
                            </div>
                            <div className="flex justify-between text-sm">
                                <span className="text-gray-400">Support</span>
                                <span className="text-white">Priority</span>
                            </div>
                        </div>

                        <button className="mt-2 w-full py-2 rounded-lg bg-white/5 hover:bg-white/10 border border-white/5 hover:border-white/20 text-sm text-white transition-all">
                            Manage Subscription
                        </button>
                    </div>
                </section>

                {/* 3. Preferences */}
                <section className="bg-surface/50 border border-border rounded-xl p-6 backdrop-blur-sm">
                    <h3 className="font-header text-lg font-semibold text-white mb-6 flex items-center gap-2">
                        <svg className="text-gray-400" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="3" /><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z" /></svg>
                        Preferences
                    </h3>
                    <div className="space-y-6">

                        <div className="flex items-center justify-between">
                            <div>
                                <span className="text-sm text-white block">Email Notifications</span>
                                <span className="text-xs text-gray-500">Weekly digests & alerts</span>
                            </div>
                            <div className="w-10 h-6 rounded-full bg-accent/20 border border-accent/50 p-1 cursor-pointer relative">
                                <div className="w-4 h-4 rounded-full bg-accent absolute right-1"></div>
                            </div>
                        </div>

                        <div className="flex items-center justify-between">
                            <div>
                                <span className="text-sm text-white block">Theme</span>
                                <span className="text-xs text-gray-500">Interface appearance</span>
                            </div>
                            <div className="flex gap-2">
                                <div className="w-6 h-6 rounded bg-gray-800 border-2 border-accent cursor-pointer"></div>
                                <div className="w-6 h-6 rounded bg-white border border-gray-600 cursor-pointer opacity-50 hover:opacity-100"></div>
                            </div>
                        </div>

                        <div className="flex items-center justify-between">
                            <div>
                                <span className="text-sm text-white block">Sound Effects</span>
                                <span className="text-xs text-gray-500">UI interactions and alerts</span>
                            </div>
                            <div className="w-10 h-6 rounded-full bg-gray-800 border border-gray-600 p-1 cursor-pointer relative">
                                <div className="w-4 h-4 rounded-full bg-gray-400 absolute left-1"></div>
                            </div>
                        </div>

                        <div className="pt-4 border-t border-border">
                            <button className="text-sm text-red-400 hover:text-red-300 transition-colors">Sign Out</button>
                        </div>
                    </div>
                </section>

            </div>
        </div>
    );
}
