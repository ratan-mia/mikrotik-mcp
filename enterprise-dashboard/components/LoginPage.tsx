'use client';

import { useAuthStore } from '@/lib/store';
import { Lock, Mail, Server } from 'lucide-react';
import { useState } from 'react';

export default function LoginPage() {
    const [email, setEmail] = useState('admin@mikrotik.local');
    const [password, setPassword] = useState('Admin123!');
    const { login, error, isLoading } = useAuthStore();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await login(email, password);
        } catch (error) {
            // Error is handled by store
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center p-4">
            <div className="max-w-md w-full">
                <div className="bg-slate-800/50 backdrop-blur-sm rounded-2xl shadow-2xl p-8 border border-slate-700">
                    <div className="flex flex-col items-center mb-8">
                        <div className="bg-blue-600 p-4 rounded-full mb-4">
                            <Server className="h-12 w-12 text-white" />
                        </div>
                        <h1 className="text-3xl font-bold text-white mb-2">MikroTik Enterprise</h1>
                        <p className="text-slate-400">Management System</p>
                    </div>

                    <form onSubmit={handleSubmit} className="space-y-6">
                        <div>
                            <label className="block text-sm font-medium text-slate-300 mb-2">
                                <Mail className="inline h-4 w-4 mr-2" />
                                Email
                            </label>
                            <input
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                className="w-full px-4 py-3 bg-slate-700/50 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                                placeholder="admin@mikrotik.local"
                                required
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-slate-300 mb-2">
                                <Lock className="inline h-4 w-4 mr-2" />
                                Password
                            </label>
                            <input
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className="w-full px-4 py-3 bg-slate-700/50 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                                placeholder="Enter your password"
                                required
                            />
                        </div>

                        {error && (
                            <div className="bg-red-500/10 border border-red-500 text-red-500 px-4 py-3 rounded-lg">
                                {error}
                            </div>
                        )}

                        <button
                            type="submit"
                            disabled={isLoading}
                            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            {isLoading ? 'Signing in...' : 'Sign In'}
                        </button>
                    </form>

                    <div className="mt-6 text-center text-sm text-slate-400">
                        <p>Default credentials:</p>
                        <p className="text-slate-500">admin@mikrotik.local / Admin123!</p>
                    </div>
                </div>
            </div>
        </div>
    );
}
