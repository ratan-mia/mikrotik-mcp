'use client';

import { useEffect, useState } from 'react';

export default function DebugAuth() {
    const [debug, setDebug] = useState<any>({});

    useEffect(() => {
        const token = localStorage.getItem('access_token');
        const refreshToken = localStorage.getItem('refresh_token');

        setDebug({
            hasToken: !!token,
            tokenLength: token?.length || 0,
            tokenPreview: token ? token.substring(0, 50) + '...' : 'No token',
            hasRefreshToken: !!refreshToken,
            localStorageKeys: Object.keys(localStorage),
        });

        // Test API call
        if (token) {
            fetch('/api/v1/auth/me', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
                .then(res => {
                    setDebug((prev: any) => ({
                        ...prev,
                        authMeStatus: res.status,
                        authMeOk: res.ok
                    }));
                    return res.json();
                })
                .then(data => {
                    setDebug((prev: any) => ({
                        ...prev,
                        authMeData: data
                    }));
                })
                .catch(err => {
                    setDebug((prev: any) => ({
                        ...prev,
                        authMeError: err.message
                    }));
                });
        }
    }, []);

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 p-8">
            <div className="max-w-4xl mx-auto">
                <h1 className="text-3xl font-bold text-white mb-6">🔍 Authentication Debug</h1>

                <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
                    <pre className="text-green-400 text-sm overflow-auto">
                        {JSON.stringify(debug, null, 2)}
                    </pre>
                </div>

                <div className="mt-6 space-y-3">
                    <button
                        onClick={() => {
                            localStorage.clear();
                            window.location.reload();
                        }}
                        className="bg-red-600 hover:bg-red-700 text-white font-semibold py-2 px-6 rounded-lg transition w-full"
                    >
                        Clear All Storage & Reload
                    </button>

                    <button
                        onClick={() => window.location.href = '/'}
                        className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-6 rounded-lg transition w-full"
                    >
                        Go to Home
                    </button>

                    <button
                        onClick={() => window.location.href = '/routers'}
                        className="bg-green-600 hover:bg-green-700 text-white font-semibold py-2 px-6 rounded-lg transition w-full"
                    >
                        Go to Routers
                    </button>
                </div>
            </div>
        </div>
    );
}
