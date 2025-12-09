import React from 'react';

interface ScannerTableProps {
    onRowClick: () => void;
}

export function ScannerTable({ onRowClick }: ScannerTableProps) {
    const handleMouseMove = (e: React.MouseEvent<HTMLTableRowElement>) => {
        const row = e.currentTarget;
        const rect = row.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        row.style.background = `radial-gradient(circle at ${x}px ${y}px, rgba(255,255,255,0.03) 0%, rgba(255,255,255,0) 300px)`;
    };

    const handleMouseLeave = (e: React.MouseEvent<HTMLTableRowElement>) => {
        e.currentTarget.style.background = 'transparent';
    };

    return (
        <div className="w-full overflow-hidden rounded-xl border border-border bg-surface/50 backdrop-blur-sm">
            <table className="w-full text-left border-collapse">
                <thead>
                    <tr className="border-b border-border/50 text-gray-400 text-xs uppercase font-medium tracking-wider">
                        <th className="p-3 md:p-4 font-normal">Ticker</th>
                        <th className="p-3 md:p-4 font-normal">Pattern</th>
                        <th className="p-3 md:p-4 font-normal hidden md:table-cell">Timeframe</th>
                        <th className="p-3 md:p-4 font-normal">Confidence</th>
                        <th className="p-3 md:p-4 font-normal text-right">Action</th>
                    </tr>
                </thead>
                <tbody>
                    {/* Row 1 */}
                    <tr
                        className="group flashlight-row border-b border-border/30 cursor-pointer relative transition-colors"
                        onMouseMove={handleMouseMove}
                        onMouseLeave={handleMouseLeave}
                        onClick={onRowClick}
                    >
                        <td className="p-3 md:p-4 font-header font-bold text-white relative z-10">NVDA</td>
                        <td className="p-3 md:p-4 relative z-10">
                            <span className="px-2 py-1 rounded-md bg-white/5 text-gray-200 text-xs border border-white/10">
                                Bullish Engulfing
                            </span>
                        </td>
                        <td className="p-3 md:p-4 text-gray-400 text-sm hidden md:table-cell relative z-10">15m</td>
                        <td className="p-3 md:p-4 relative z-10 w-32 md:w-48">
                            <div className="flex items-center gap-3">
                                <div className="flex-1 h-1.5 bg-gray-800 rounded-full overflow-hidden">
                                    <div className="h-full bg-accent w-[92%] rounded-full shadow-[0_0_10px_#10b981]"></div>
                                </div>
                                <span className="text-accent text-xs font-bold">92%</span>
                            </div>
                        </td>
                        <td className="p-3 md:p-4 text-right relative z-10">
                            <button className="text-gray-400 hover:text-white transition-colors">
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    width="16"
                                    height="16"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    strokeWidth="2"
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                >
                                    <circle cx="12" cy="12" r="1"></circle>
                                    <circle cx="19" cy="12" r="1"></circle>
                                    <circle cx="5" cy="12" r="1"></circle>
                                </svg>
                            </button>
                        </td>
                    </tr>
                    {/* Row 2 */}
                    <tr
                        className="group flashlight-row border-b border-border/30 cursor-pointer relative transition-colors"
                        onMouseMove={handleMouseMove}
                        onMouseLeave={handleMouseLeave}
                        onClick={onRowClick}
                    >
                        <td className="p-3 md:p-4 font-header font-bold text-white relative z-10">TSLA</td>
                        <td className="p-3 md:p-4 relative z-10">
                            <span className="px-2 py-1 rounded-md bg-white/5 text-gray-200 text-xs border border-white/10">
                                Double Bottom
                            </span>
                        </td>
                        <td className="p-3 md:p-4 text-gray-400 text-sm hidden md:table-cell relative z-10">1h</td>
                        <td className="p-3 md:p-4 relative z-10 w-32 md:w-48">
                            <div className="flex items-center gap-3">
                                <div className="flex-1 h-1.5 bg-gray-800 rounded-full overflow-hidden">
                                    <div className="h-full bg-accent w-[78%] rounded-full opacity-80"></div>
                                </div>
                                <span className="text-accent text-xs font-bold opacity-80">78%</span>
                            </div>
                        </td>
                        <td className="p-3 md:p-4 text-right relative z-10">
                            <button className="text-gray-400 hover:text-white transition-colors">
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    width="16"
                                    height="16"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    strokeWidth="2"
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                >
                                    <circle cx="12" cy="12" r="1"></circle>
                                    <circle cx="19" cy="12" r="1"></circle>
                                    <circle cx="5" cy="12" r="1"></circle>
                                </svg>
                            </button>
                        </td>
                    </tr>
                    {/* Row 3 */}
                    <tr
                        className="group flashlight-row border-b border-border/30 cursor-pointer relative transition-colors"
                        onMouseMove={handleMouseMove}
                        onMouseLeave={handleMouseLeave}
                        onClick={onRowClick}
                    >
                        <td className="p-3 md:p-4 font-header font-bold text-white relative z-10">AMD</td>
                        <td className="p-3 md:p-4 relative z-10">
                            <span className="px-2 py-1 rounded-md bg-white/5 text-gray-200 text-xs border border-white/10">
                                Flag (Continuation)
                            </span>
                        </td>
                        <td className="p-3 md:p-4 text-gray-400 text-sm hidden md:table-cell relative z-10">4h</td>
                        <td className="p-3 md:p-4 relative z-10 w-32 md:w-48">
                            <div className="flex items-center gap-3">
                                <div className="flex-1 h-1.5 bg-gray-800 rounded-full overflow-hidden">
                                    <div className="h-full bg-accent w-[65%] rounded-full opacity-60"></div>
                                </div>
                                <span className="text-accent text-xs font-bold opacity-60">65%</span>
                            </div>
                        </td>
                        <td className="p-3 md:p-4 text-right relative z-10">
                            <button className="text-gray-400 hover:text-white transition-colors">
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    width="16"
                                    height="16"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    strokeWidth="2"
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                >
                                    <circle cx="12" cy="12" r="1"></circle>
                                    <circle cx="19" cy="12" r="1"></circle>
                                    <circle cx="5" cy="12" r="1"></circle>
                                </svg>
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    );
}
