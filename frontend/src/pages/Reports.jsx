import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FileText, Download, Search, Calendar, ShieldCheck, AlertTriangle, Skull, Loader2 } from 'lucide-react';
import RiskGauge from '../components/RiskGauge';
import { formatDate } from '../lib/utils';
import { listScans, downloadReport } from '../lib/api';

const TYPE_ICONS = {
  url: ShieldCheck,
  email: FileText,
  visual: AlertTriangle,
};

const getScoreColor = (score) => {
  if (score <= 30) return '#00ff88';
  if (score <= 60) return '#ffb800';
  return '#ff2a2a';
};

export default function Reports() {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [search, setSearch] = useState('');
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    loadReports();
  }, []);

  const loadReports = async () => {
    try {
      setLoading(true);
      const data = await listScans(0, 100);
      const scansList = data.scans || data || [];
      setReports(scansList);
      setError(null);
    } catch (e) {
      setError(e.message);
      setReports([]);
    } finally {
      setLoading(false);
    }
  };

  const getTargetText = (scan) => {
    return scan.target || scan.url || scan.email_subject || scan.visual_target || 'Unknown target';
  };

  const filtered = reports.filter(r => {
    const target = getTargetText(r);
    const matchesSearch = target.toLowerCase().includes(search.toLowerCase()) || (r.scan_id || r.id || '').includes(search);
    const classification = (r.classification || 'clean').toLowerCase();
    const matchesFilter = filter === 'all' || classification === filter;
    return matchesSearch && matchesFilter;
  });

  return (
    <div className="space-y-6">
      <div className="flex items-end justify-between">
        <div>
          <motion.h1 
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-3xl font-bold"
            style={{ color: '#e4e4f0', fontFamily: 'Space Grotesk, sans-serif' }}
          >
            Case Dossiers
          </motion.h1>
          <p className="text-sm mt-1" style={{ color: '#8b8b9a', fontFamily: 'monospace' }}>
            {loading ? 'Loading...' : `${filtered.length} reports · ${reports.filter(r => (r.final_score || 0) > 60).length} threats detected`}
          </p>
        </div>
        <button 
          onClick={loadReports}
          className="flex items-center gap-2 px-3 py-2 rounded-lg text-xs border transition-colors hover:bg-white/5"
          style={{ color: '#8b8b9a', borderColor: 'rgba(30, 30, 46, 0.6)', fontFamily: 'monospace' }}
        >
          <Loader2 className={`w-3 h-3 ${loading ? 'animate-spin' : ''}`} /> Refresh
        </button>
      </div>

      {/* Search & filter */}
      <div className="flex items-center gap-3">
        <div className="flex-1 flex items-center gap-2 px-4 py-2.5 rounded-lg border" style={{ backgroundColor: 'rgba(20, 20, 31, 0.8)', borderColor: 'rgba(30, 30, 46, 0.4)' }}>
          <Search className="w-4 h-4" style={{ color: '#8b8b9a' }} />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search by target or ID..."
            className="flex-1 bg-transparent outline-none text-sm"
            style={{ color: '#e4e4f0', fontFamily: 'monospace' }}
          />
        </div>
        {['all', 'clean', 'suspicious', 'malicious'].map(f => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className="px-3 py-2 rounded-lg text-xs uppercase border transition-colors"
            style={{
              backgroundColor: filter === f ? 'rgba(0, 240, 255, 0.1)' : 'rgba(20, 20, 31, 0.8)',
              borderColor: filter === f ? 'rgba(0, 240, 255, 0.3)' : 'rgba(30, 30, 46, 0.4)',
              color: filter === f ? '#00f0ff' : '#8b8b9a',
              fontFamily: 'monospace',
            }}
          >
            {f}
          </button>
        ))}
      </div>

      {/* Error */}
      {error && (
        <div className="p-4 border rounded-lg" style={{ backgroundColor: 'rgba(255, 42, 42, 0.1)', borderColor: 'rgba(255, 42, 42, 0.3)' }}>
          <p className="text-sm flex items-center gap-2" style={{ color: '#ff2a2a', fontFamily: 'monospace' }}>
            <AlertTriangle className="w-4 h-4" /> {error}
          </p>
        </div>
      )}

      {/* Grid */}
      {loading ? (
        <div className="flex items-center justify-center py-20">
          <Loader2 className="w-8 h-8 animate-spin" style={{ color: '#00f0ff' }} />
        </div>
      ) : (
        <div className="grid grid-cols-2 gap-4">
          {filtered.map((report, i) => {
            const type = report.scan_type || report.type || 'url';
            const TypeIcon = TYPE_ICONS[type] || ShieldCheck;
            const score = report.final_score || 0;
            const scoreColor = getScoreColor(score);
            const classification = report.classification || (score > 60 ? 'Malicious' : score > 30 ? 'Suspicious' : 'Clean');
            const target = getTargetText(report);
            const id = report.scan_id || report.id || 'unknown';
            
            return (
              <motion.div
                key={id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.05 }}
                className="p-5 border rounded-xl group cursor-pointer transition-all hover:border-cyan/20"
                style={{
                  backgroundColor: 'rgba(20, 20, 31, 0.8)',
                  borderColor: 'rgba(30, 30, 46, 0.4)',
                  boxShadow: '0 4px 24px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.05)',
                }}
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-lg flex items-center justify-center" style={{ backgroundColor: `${scoreColor}15` }}>
                      <TypeIcon className="w-5 h-5" style={{ color: scoreColor }} />
                    </div>
                    <div className="min-w-0 flex-1">
                      <p className="text-sm font-medium truncate" style={{ color: '#e4e4f0', fontFamily: 'monospace' }}>{target}</p>
                      <p className="text-xs" style={{ color: '#8b8b9a', fontFamily: 'monospace' }}>#{id.slice(0, 8)}</p>
                    </div>
                  </div>
                  <RiskGauge score={score} size={48} />
                </div>

                <div className="flex items-center justify-between pt-3 border-t" style={{ borderColor: 'rgba(30, 30, 46, 0.3)' }}>
                  <div className="flex items-center gap-3">
                    <span className="flex items-center gap-1 text-xs" style={{ color: '#8b8b9a', fontFamily: 'monospace' }}>
                      <Calendar className="w-3 h-3" /> {formatDate(report.timestamp || report.created_at)}
                    </span>
                    <span
                      className="px-2 py-0.5 rounded text-[10px] uppercase border"
                      style={{
                        color: scoreColor,
                        borderColor: `${scoreColor}30`,
                        backgroundColor: `${scoreColor}10`,
                        fontFamily: 'monospace',
                      }}
                    >
                      {classification}
                    </span>
                  </div>
                  <a 
                    href={downloadReport(id)}
                    className="opacity-0 group-hover:opacity-100 transition-opacity flex items-center gap-1 text-xs"
                    style={{ color: '#00f0ff', fontFamily: 'monospace' }}
                  >
                    <Download className="w-3 h-3" /> PDF
                  </a>
                </div>
              </motion.div>
            );
          })}
        </div>
      )}

      {!loading && filtered.length === 0 && (
        <div className="text-center py-16">
          <FileText className="w-16 h-16 mx-auto mb-4" style={{ color: 'rgba(0, 240, 255, 0.1)' }} />
          <p style={{ color: '#8b8b9a', fontFamily: 'monospace' }}>No reports found.</p>
        </div>
      )}
    </div>
  );
}
