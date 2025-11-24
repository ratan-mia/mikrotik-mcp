'use client';

import { useEffect, useState } from 'react';

export default function TestAuthPage() {
    const [results, setResults] = useState<any>({});
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        testAuth();
    }, []);

    const testAuth = async () => {
        const result: any = {
            timestamp: new Date().toISOString(),
            localStorage: {},
            apiTests: {}
        };

        // Check localStorage
        if (typeof window !== 'undefined') {
            result.localStorage.token = localStorage.getItem('access_token');
            result.localStorage.tokenLength = result.localStorage.token?.length || 0;
            result.localStorage.tokenPrefix = result.localStorage.token?.substring(0, 50);
        }

        // Test /auth/me endpoint
        try {
            const token = localStorage.getItem('access_token');
            const response = await fetch('/api/v1/auth/me', {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });
            result.apiTests.authMe = {
                status: response.status,
                statusText: response.statusText,
                ok: response.ok
            };
            if (response.ok) {
                result.apiTests.authMeData = await response.json();
            }
        } catch (error: any) {
            result.apiTests.authMe = { error: error.message };
        }

        // Test /routers/ endpoint
        try {
            const token = localStorage.getItem('access_token');
            const response = await fetch('/api/v1/routers/', {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });
            result.apiTests.routers = {
                status: response.status,
                statusText: response.statusText,
                ok: response.ok
            };
            if (response.ok) {
                result.apiTests.routersData = await response.json();
            }
        } catch (error: any) {
            result.apiTests.routers = { error: error.message };
        }

        setResults(result);
        setLoading(false);
    };

    const clearAndReload = () => {
        localStorage.clear();
        window.location.href = '/';
    };

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-gray-900">
                <div className="text-white">Testing authentication...</div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-900 p-8">
            <div className="max-w-4xl mx-auto">
                <h1 className="text-3xl font-bold text-white mb-6">🔍 Authentication Test</h1>

                <div className="bg-gray-800 rounded-lg p-6 mb-4">
                    <h2 className="text-xl font-semibold text-white mb-4">Test Results</h2>
                    <pre className="bg-gray-900 text-green-400 p-4 rounded overflow-auto text-sm">
                        {JSON.stringify(results, null, 2)}
                    </pre>
                </div>

                <div className="bg-gray-800 rounded-lg p-6 mb-4">
                    <h2 className="text-xl font-semibold text-white mb-4">Quick Diagnosis</h2>
                    <div className="space-y-2 text-white">
                        {results.localStorage?.token ? (
                            <div className="flex items-center text-green-400">
                                <span className="mr-2">✓</span>
                                <span>Token exists in localStorage</span>
                            </div>
                        ) : (
                            <div className="flex items-center text-red-400">
                                <span className="mr-2">✗</span>
                                <span>No token found - Need to log in</span>
                            </div>
                        )}

                        {results.apiTests?.authMe?.ok ? (
                            <div className="flex items-center text-green-400">
                                <span className="mr-2">✓</span>
                                <span>/auth/me works - Token is valid</span>
                            </div>
                        ) : (
                            <div className="flex items-center text-red-400">
                                <span className="mr-2">✗</span>
                                <span>/auth/me failed - Status: {results.apiTests?.authMe?.status}</span>
                            </div>
                        )}

                        {results.apiTests?.routers?.ok ? (
                            <div className="flex items-center text-green-400">
                                <span className="mr-2">✓</span>
                                <span>/routers/ works - Found {results.apiTests?.routersData?.length || 0} router(s)</span>
                            </div>
                        ) : (
                            <div className="flex items-center text-red-400">
                                <span className="mr-2">✗</span>
                                <span>/routers/ failed - Status: {results.apiTests?.routers?.status}</span>
                            </div>
                        )}
                    </div>
                </div>

                <div className="flex gap-4">
                    <button
                        onClick={clearAndReload}
                        className="px-6 py-3 bg-red-600 hover:bg-red-700 text-white rounded-lg font-semibold"
                    >
                        Clear Storage & Go to Login
                    </button>
                    <button
                        onClick={testAuth}
                        className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold"
                    >
                        Re-test
                    </button>
                    <a
                        href="/routers"
                        className="px-6 py-3 bg-green-600 hover:bg-green-700 text-white rounded-lg font-semibold inline-block text-center"
                    >
                        Go to Routers
                    </a>
                </div>

                <div className="mt-8 bg-yellow-900/30 border border-yellow-600 rounded-lg p-6">
                    <h3 className="text-yellow-400 font-semibold mb-3">💡 Browser Cache Issue?</h3>
                    <p className="text-yellow-200 mb-3">
                        If you're seeing 401 errors but the backend works (confirmed via PowerShell),
                        your browser is serving old cached JavaScript.
                    </p>
                    <div className="text-yellow-100 space-y-2">
                        <p><strong>Solution 1:</strong> Press <code className="bg-gray-800 px-2 py-1 rounded">Ctrl+Shift+R</code> (hard refresh)</p>
                        <p><strong>Solution 2:</strong> Press <code className="bg-gray-800 px-2 py-1 rounded">Ctrl+Shift+Delete</code> and clear cache</p>
                        <p><strong>Solution 3:</strong> Use Incognito mode (<code className="bg-gray-800 px-2 py-1 rounded">Ctrl+Shift+N</code>)</p>
                        <p><strong>Solution 4:</strong> Open DevTools (F12) → Network tab → Disable cache checkbox</p>
                    </div>
                </div>
            </div>
        </div>
    );
}
