import React, { useState } from 'react';
import { Navbar } from './components/layout/Navbar';
import { DashboardView } from './components/dashboard/DashboardView';
import { BuilderView } from './components/builder/BuilderView';
import { ProfileView } from './components/profile/ProfileView';
import { PatternDetailView } from './components/dashboard/PatternDetailView';
import ScannerView from './components/scanner/ScannerView';

type View = 'dashboard' | 'builder' | 'profile' | 'detail' | 'scanner';

function App() {
    const [activeView, setActiveView] = useState<View>('dashboard');

    return (
        <div className="flex min-h-screen antialiased selection:bg-accent selection:text-black bg-bg text-white overflow-hidden">

            {/* Background Decorations */}
            <div className="fixed top-20 right-20 w-96 h-96 bg-accent/5 rounded-full blur-[100px] pointer-events-none z-0"></div>
            <div className="fixed bottom-20 left-60 w-64 h-64 bg-purple-500/5 rounded-full blur-[80px] pointer-events-none z-0"></div>

            {/* Navigation (Apple-style Header) */}
            <Navbar activeView={activeView as any} onNavigate={setActiveView as any} />

            {/* Main Content Area */}
            <main className="flex-1 relative h-full overflow-y-auto overflow-x-hidden pt-20">
                <div className="w-full max-w-7xl mx-auto">
                    {activeView === 'dashboard' && (
                        <DashboardView
                            onNavigateBuilder={() => setActiveView('builder')}
                            onNavigateDetail={() => setActiveView('detail')}
                        />
                    )}
                    {activeView === 'builder' && (
                        <BuilderView />
                    )}
                    {activeView === 'scanner' && (
                        <ScannerView />
                    )}
                    {activeView === 'profile' && (
                        <ProfileView />
                    )}
                    {activeView === 'detail' && (
                        <PatternDetailView onBack={() => setActiveView('dashboard')} />
                    )}
                </div>
            </main>
        </div>
    );
}

export default App;
