import React, { useState, useEffect, useRef } from 'react';
import { Search, FileText, Info, Loader2, Database, Upload, X, CheckCircle, AlertCircle, Plus } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

function App() {
    const API_BASE = import.meta.env.VITE_API_URL || '';
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);
    const [stats, setStats] = useState(null);
    const [isUploading, setIsUploading] = useState(false);
    const [dragActive, setDragActive] = useState(false);
    const fileInputRef = useRef(null);

    useEffect(() => {
        console.log('App initialized. Connecting to API at:', API_BASE || '(relative path)');
        fetchStats();
    }, []);

    const fetchStats = async () => {
        try {
            const res = await fetch(`${API_BASE}/api/info`);
            const data = await res.json();
            setStats(data);
        } catch (e) {
            console.error('Failed to fetch stats', e);
        }
    };

    const onDrag = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    };

    const onDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFiles(e.dataTransfer.files);
        }
    };

    const handleFiles = async (files) => {
        setIsUploading(true);
        const formData = new FormData();
        for (let i = 0; i < files.length; i++) {
            formData.append('files', files[i]);
        }

        try {
            const res = await fetch(`${API_BASE}/api/upload`, {
                method: 'POST',
                body: formData,
            });
            const data = await res.json();
            if (data.status === 'success') {
                fetchStats();
                alert(`Successfully ingested ${files.length} documents!`);
            } else {
                alert("Processing Error: " + data.message);
            }
        } catch (e) {
            console.error('Upload failed', e);
            alert("Network Error: Could not connect to the indexing server.");
        } finally {
            setIsUploading(false);
        }
    };

    const handleSearch = async (e) => {
        e.preventDefault();
        if (!query.trim()) return;

        setLoading(true);
        try {
            const res = await fetch(`${API_BASE}/api/search`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query, top_k: 5 }),
            });
            const data = await res.json();
            setResults(data);
        } catch (e) {
            console.error('Search failed', e);
        } finally {
            setLoading(false);
        }
    };

    // Debounced search could be added here for even better UX

    return (
        <div className="container">
            <header>
                <motion.div
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5 }}
                >
                    <div className="title-gradient">EndeeSem</div>
                    <p style={{ color: 'var(--text-muted)' }}>Semantic PDF Search Engine</p>
                </motion.div>
            </header>

            <main className="main-content">
                <div className="search-section">
                    <section className="search-container">
                        <form onSubmit={handleSearch} className="glass-panel">
                            <div className="search-input-wrapper">
                                <Search size={20} color="var(--accent-primary)" />
                                <input
                                    type="text"
                                    placeholder="Search across your documents..."
                                    value={query}
                                    onChange={(e) => setQuery(e.target.value)}
                                />
                                {loading ? (
                                    <Loader2 className="animate-spin" size={20} color="var(--accent-primary)" />
                                ) : (
                                    <button type="submit" style={{ display: 'none' }} />
                                )}
                            </div>
                        </form>
                    </section>

                    <div className="results-grid">
                        <AnimatePresence mode="popLayout">
                            {results.length > 0 ? (
                                results.map((result, idx) => (
                                    <motion.div
                                        key={result.id + idx}
                                        initial={{ opacity: 0, x: -20 }}
                                        animate={{ opacity: 1, x: 0 }}
                                        exit={{ opacity: 0, scale: 0.95 }}
                                        transition={{ duration: 0.3, delay: idx * 0.05 }}
                                        className="result-card glass-panel"
                                    >
                                        <div className="result-header">
                                            <div className="file-name">
                                                <FileText size={18} />
                                                {result.metadata.file_name || 'Document'}
                                            </div>
                                            <div className="score-badge">
                                                {(result.score * 100).toFixed(1)}% match
                                            </div>
                                        </div>
                                        <p className="result-text">{result.metadata.text}</p>
                                        <div className="page-indicator">
                                            <Database size={14} />
                                            Page {result.metadata.page || 1} • ID: {result.id}
                                        </div>
                                    </motion.div>
                                ))
                            ) : query && !loading ? (
                                <motion.div
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    className="empty-state"
                                >
                                    No matching passages found. Try a different query.
                                </motion.div>
                            ) : !query && (
                                <motion.div
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    className="welcome-text"
                                    style={{ textAlign: 'center', padding: '4rem 0', opacity: 0.5 }}
                                >
                                    <Search size={48} color="var(--accent-primary)" style={{ marginBottom: '1rem' }} />
                                    <h2>Start Querying Your Documents</h2>
                                    <p>Type a question or phrase above to search semantically across your uploaded PDFs.</p>
                                </motion.div>
                            )}
                        </AnimatePresence>
                    </div>
                </div>

                <aside className="sidebar">
                    <div className="glass-panel management-panel" style={{ padding: '1.5rem' }}>
                        <h3 style={{ marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                            <Upload size={20} color="var(--accent-secondary)" />
                            Manage Library
                        </h3>

                        <div
                            className={`upload-zone ${dragActive ? 'active' : ''} ${isUploading ? 'loading' : ''}`}
                            onDragEnter={onDrag}
                            onDragLeave={onDrag}
                            onDragOver={onDrag}
                            onDrop={onDrop}
                            onClick={() => fileInputRef.current.click()}
                            style={{
                                border: '2px dashed var(--glass-border)',
                                borderRadius: '12px',
                                padding: '2rem',
                                textAlign: 'center',
                                cursor: 'pointer',
                                transition: 'all 0.2s',
                                background: dragActive ? 'rgba(139, 92, 246, 0.05)' : 'transparent',
                                borderColor: dragActive ? 'var(--accent-secondary)' : 'var(--glass-border)'
                            }}
                        >
                            <input
                                ref={fileInputRef}
                                type="file"
                                multiple
                                accept=".pdf"
                                onChange={(e) => handleFiles(e.target.files)}
                                style={{ display: 'none' }}
                            />

                            {isUploading ? (
                                <div className="upload-content">
                                    <Loader2 className="animate-spin" size={32} color="var(--accent-secondary)" style={{ margin: '0 auto 1rem' }} />
                                    <p>Processing Library...</p>
                                </div>
                            ) : (
                                <div className="upload-content">
                                    <Plus size={32} color="var(--accent-secondary)" style={{ margin: '0 auto 1rem' }} />
                                    <p>Drop PDFs here or <span style={{ color: 'var(--accent-secondary)', fontWeight: 600 }}>Browse</span></p>
                                </div>
                            )}
                        </div>

                        {stats && (
                            <div className="stats-mini" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginTop: '1.5rem' }}>
                                <div className="stat-item" style={{ textAlign: 'center' }}>
                                    <div style={{ fontSize: '1.25rem', fontWeight: 'bold' }}>{stats.total_chunks || 0}</div>
                                    <div style={{ color: 'var(--text-muted)', fontSize: '0.75rem' }}>Passages</div>
                                </div>
                                <div className="stat-item" style={{ textAlign: 'center' }}>
                                    <div style={{ fontSize: '1.25rem', fontWeight: 'bold' }}>{Object.keys(stats.files || {}).length}</div>
                                    <div style={{ color: 'var(--text-muted)', fontSize: '0.75rem' }}>Documents</div>
                                </div>
                            </div>
                        )}

                        <button
                            className="btn btn-outline"
                            onClick={async () => {
                                if (confirm("Are you sure? This will delete all indexed data.")) {
                                    await fetch(`${API_BASE}/api/reset`, { method: 'POST' });
                                    fetchStats();
                                    setResults([]);
                                }
                            }}
                            style={{
                                width: '100%',
                                marginTop: '1.5rem',
                                background: 'rgba(239, 68, 68, 0.1)',
                                color: '#ef4444',
                                border: '1px solid rgba(239, 68, 68, 0.2)',
                                padding: '0.75rem',
                                borderRadius: '8px',
                                fontWeight: 600,
                                cursor: 'pointer'
                            }}
                        >
                            Reset Index
                        </button>
                    </div>
                </aside>
            </main>

            <footer style={{ marginTop: '4rem', textAlign: 'center', color: 'var(--text-muted)', fontSize: '0.875rem' }}>
                Powered by Endee Vector DB & Sentence Transformers
            </footer>
        </div>
    );
}

export default App;
