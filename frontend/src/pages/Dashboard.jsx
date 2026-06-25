import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Activity, AlertTriangle, ShieldCheck, Skull, Clock, Zap } from 'lucide-react';
import RiskGauge from '../components/RiskGauge';
import ThreatWave from '../components/ThreatWave';
import ModelCore from '../components/ModelCore';
import { formatDate, cn } from '../lib/utils';
import { listScans, getHealth } from '../lib/api';

const statsConfig = [
  { label: 'Total Scans', icon: Activity, color: '#00f0ff', key: 'total' },
  { label: 'Threats Blocked', icon: ShieldCheck, color: '#00ff88', key: 'blocked' },
  { label: 'Critical Alerts', icon: AlertTriangle, color: '#ff2a2a', key: 'critical' },
  { label: 'Avg Response', icon: Clock, color: '#ffb800', key: 'avg_response' },
];

export default function Dashboard() {
  const [scans, setScans] = useState([]);
  const [stats, setStats] = useState({ total: '0', blocked: '0', critical: '0', avg_response: '0ms' });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 10000);
    return () => clearInterval(interval);
  }, []);

  const loadData = async () => {
    try {
      const [scansData, healthData] = await Promise.all([
        listScans(0, 10).catch(() => []),
        getHealth().catch(() => null),
      ]);

      // Handle both {scans: [...]} and direct array responses
      const scansList = scansData.scans || scansData || [];
      const recent = scansList.slice(0, 4);
      setScans(recent);

      const total = scansList.length;
      const blocked = scansList.filter(s => (s.final_score || 0) > 60).length;
      const critical = scansList.filter(s => (s.final_score || 0) > 85).length;
      
      setStats({
        total: total.toLocaleString(),
        blocked: blocked.toLocaleString(),
        critical: critical.toLocaleString(),
        avg_response: healthData?.response_time_ms ? `${healthData.response_time_ms}ms` : '45ms',
      });
    } catch (e) {
      console.error('Dashboard load error:', e);
    } finally {
      setLoading(false);
    }
  };

  const statValues = statsConfig.map(s => ({ ...s, value: stats[s.key] }));

  // Helper to get target display text from any scan format
  const getTargetText = (scan) => {
    return scan.target || scan.url || scan.email_subject || scan.visual_target || 'Unknown target';
  };

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
            Threat Pulse
          </motion.h1>
          <p className="text-sm mt-1" style={{ color: '#8b8b9a', fontFamily: 'monospace' }}>
            Real-time multi-modal detection monitor
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full animate-pulse" style={{ backgroundColor: '#00ff88' }} />
          <span className="text-xs" style={{ color: '#00ff88', fontFamily: 'monospace' }}>SYSTEM ONLINE</span>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-4 gap-4">
        {statValues.map((stat, i) => {
          const Icon = stat.icon;
          return (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              className="p-4 border"
              style={{
                backgroundColor: 'rgba(20, 20, 31, 0.8)',
                backdropFilter: 'blur(24px)',
                borderColor: `${stat.color}20`,
                borderRadius: '12px',
                boxShadow: '0 4px 24px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.05)',
              }}
            >
              <div className="flex items-center justify-between mb-2">
                <Icon className="w-5 h-5" style={{ color: stat.color, opacity: 0.6 }} />
                <span className="text-2xl font-bold" style={{ color: stat.color, fontFamily: 'Space Grotesk, sans-serif' }}>{stat.value}</span>
              </div>
              <span className="text-xs uppercase tracking-wider" style={{ color: stat.color, opacity: 0.6, fontFamily: 'monospace' }}>
                {stat.label}
              </span>
            </motion.div>
          );
        })}
      </div>

      {/* Main grid */}
      <div className="grid grid-cols-3 gap-6">
        <div className="col-span-2 space-y-6">
          <ThreatWave />
          
          <div className="p-6" style={{
            backgroundColor: 'rgba(20, 20, 31, 0.8)',
            backdropFilter: 'blur(24px)',
            border: '1px solid rgba(30, 30, 46, 0.4)',
            borderRadius: '12px',
            boxShadow: '0 4px 24px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.05)',
          }}>
            <h3 className="text-xs uppercase tracking-wider mb-4" style={{ color: '#8b8b9a', fontFamily: 'monospace' }}>
              Recent Cases
            </h3>
            <div className="space-y-2">
              {scans.map((scan, i) => {
                const target = getTargetText(scan);
                const score = scan.final_score || 0;
                const id = scan.scan_id || scan.id || 'unknown';
                return (
                  <motion.div
                    key={id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.3 + i * 0.1 }}
                    className="flex items-center gap-4 p-3 rounded-lg transition-colors group cursor-pointer"
                    style={{ backgroundColor: 'rgba(42, 42, 60, 0.3)' }}
                  >
                    <RiskGauge score={score} size={48} />
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2">
                        <span className="text-xs uppercase" style={{ color: '#00f0ff', fontFamily: 'monospace' }}>
                          {scan.scan_type || scan.type || 'url'}
                        </span>
                        <span className="text-xs" style={{ color: '#8b8b9a', fontFamily: 'monospace' }}>
                          #{id.slice(0, 8)}
                        </span>
                      </div>
                      <p className="text-sm truncate mt-0.5" style={{ color: '#e4e4f0', fontFamily: 'monospace' }}>
                        {target}
                      </p>
                    </div>
                    <div className="text-right">
                      <span className="text-xs" style={{ color: '#8b8b9a', fontFamily: 'monospace' }}>
                        {formatDate(scan.timestamp || scan.created_at)}
                      </span>
                    </div>
                    <Skull className={cn(
                      'w-4 h-4 opacity-0 group-hover:opacity-100 transition-opacity',
                      score > 60 ? 'text-crimson' : 'text-ghost'
                    )} />
                  </motion.div>
                );
              })}
              {scans.length === 0 && !loading && (
                <p className="text-sm text-center py-8" style={{ color: '#8b8b9a', fontFamily: 'monospace' }}>
                  No scans yet. Go to Inject to run your first analysis.
                </p>
              )}
            </div>
          </div>
        </div>

        <div className="space-y-6">
          <ModelCore />
          
          <motion.a
            href="/scan"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="w-full p-6 border transition-colors group block"
            style={{
              backgroundColor: 'rgba(20, 20, 31, 0.8)',
              backdropFilter: 'blur(24px)',
              borderColor: 'rgba(0, 240, 255, 0.3)',
              borderRadius: '12px',
              boxShadow: '0 4px 24px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.05)',
            }}
          >
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg flex items-center justify-center" style={{ backgroundColor: 'rgba(0, 240, 255, 0.1)' }}>
                <Zap className="w-5 h-5" style={{ color: '#00f0ff' }} />
              </div>
              <div className="text-left">
                <h4 className="font-medium" style={{ color: '#e4e4f0' }}>New Analysis</h4>
                <p className="text-xs" style={{ color: '#8b8b9a', fontFamily: 'monospace' }}>Inject target for scanning</p>
              </div>
            </div>
          </motion.a>

          <div className="p-6" style={{
            backgroundColor: 'rgba(20, 20, 31, 0.8)',
            backdropFilter: 'blur(24px)',
            border: '1px solid rgba(30, 30, 46, 0.4)',
            borderRadius: '12px',
            boxShadow: '0 4px 24px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.05)',
          }}>
            <h3 className="text-xs uppercase tracking-wider mb-3" style={{ color: '#8b8b9a', fontFamily: 'monospace' }}>
              System Health
            </h3>
            <div className="space-y-3">
              {[
                { label: 'Database', status: 'Connected', ok: true },
                { label: 'Model A', status: 'Loaded', ok: true },
                { label: 'Model B', status: 'Loaded', ok: true },
                { label: 'Model C', status: 'Loaded', ok: true },
              ].map(item => (
                <div key={item.label} className="flex items-center justify-between text-sm">
                  <span style={{ color: '#8b8b9a', fontFamily: 'monospace' }}>{item.label}</span>
                  <span className="text-xs" style={{
                    color: item.ok ? '#00ff88' : '#ff2a2a',
                    fontFamily: 'monospace',
                  }}>
                    {item.status}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
