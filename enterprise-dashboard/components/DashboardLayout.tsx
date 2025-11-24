'use client';

import { useAuthStore } from '@/lib/store';
import {
    Activity,
    Bell,
    LayoutDashboard,
    LogOut,
    Menu,
    Server,
    Settings,
    X
} from 'lucide-react';
import Link from 'next/link';
import { ReactNode, useState } from 'react';

interface DashboardLayoutProps {
    children: ReactNode;
}

export default function DashboardLayout({ children }: DashboardLayoutProps) {
    const { user, logout } = useAuthStore();
    const [sidebarOpen, setSidebarOpen] = useState(true);

    const navigation = [
        { name: 'Overview', href: '/', icon: LayoutDashboard },
        { name: 'Routers', href: '/routers', icon: Server },
        { name: 'Monitoring', href: '/monitoring', icon: Activity },
        { name: 'Alerts', href: '/alerts', icon: Bell },
        { name: 'Settings', href: '/settings', icon: Settings },
    ];

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
            {/* Sidebar */}
            <aside
                className={`fixed top-0 left-0 z-40 h-screen transition-transform ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'
                    } bg-slate-800/50 backdrop-blur-sm border-r border-slate-700 w-64`}
            >
                <div className="h-full px-3 py-4 overflow-y-auto">
                    <div className="flex items-center justify-between mb-6 px-3">
                        <div className="flex items-center space-x-3">
                            <Server className="h-8 w-8 text-blue-500" />
                            <span className="text-xl font-bold text-white">MikroTik</span>
                        </div>
                        <button
                            onClick={() => setSidebarOpen(false)}
                            className="lg:hidden text-slate-400 hover:text-white"
                        >
                            <X className="h-6 w-6" />
                        </button>
                    </div>

                    <ul className="space-y-2">
                        {navigation.map((item) => (
                            <li key={item.name}>
                                <Link
                                    href={item.href}
                                    className="flex items-center p-3 text-slate-300 rounded-lg hover:bg-slate-700/50 transition"
                                >
                                    <item.icon className="h-5 w-5 mr-3" />
                                    {item.name}
                                </Link>
                            </li>
                        ))}
                    </ul>

                    <div className="absolute bottom-4 left-0 right-0 px-6">
                        <div className="bg-slate-700/50 rounded-lg p-4 mb-3">
                            <p className="text-sm text-slate-400">Logged in as</p>
                            <p className="text-white font-medium">{user?.username}</p>
                            <p className="text-xs text-slate-500 capitalize">{user?.role}</p>
                        </div>
                        <button
                            onClick={logout}
                            className="flex items-center w-full p-3 text-red-400 hover:bg-red-500/10 rounded-lg transition"
                        >
                            <LogOut className="h-5 w-5 mr-3" />
                            Logout
                        </button>
                    </div>
                </div>
            </aside>

            {/* Main content */}
            <div className={`${sidebarOpen ? 'lg:ml-64' : ''} transition-all duration-300`}>
                {/* Top bar */}
                <header className="bg-slate-800/30 backdrop-blur-sm border-b border-slate-700 sticky top-0 z-30">
                    <div className="px-4 py-4 flex items-center justify-between">
                        <button
                            onClick={() => setSidebarOpen(!sidebarOpen)}
                            className="text-slate-400 hover:text-white"
                        >
                            <Menu className="h-6 w-6" />
                        </button>
                        <h1 className="text-xl font-semibold text-white">Enterprise Management</h1>
                        <div className="w-10"></div>
                    </div>
                </header>

                {/* Page content */}
                <main className="p-6">
                    {children}
                </main>
            </div>
        </div>
    );
}
