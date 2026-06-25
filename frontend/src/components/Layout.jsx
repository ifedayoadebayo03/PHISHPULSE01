import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Activity, Shield, FileText, Settings, Zap, Terminal, ChevronRight, Menu, X } from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';
import { cn } from '../lib/utils';

const navItems = [
  { path: '/', icon: Activity, label: 'Pulse', desc: 'Live threat monitor' },
  { path: '/scan', icon: Zap, label: 'Inject', desc: 'Run analysis' },
  { path: '/reports', icon: FileText, label: 'Dossiers', desc: 'Case files' },
  { path: '/settings', icon: Settings, label: 'Config', desc: 'System tuning' },
];

export default function Layout({ children }) {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [terminalOpen, setTerminalOpen] = useState(false);
  const location = useLocation();

  return (
    <div className="min-h-screen flex relative overflow-hidden" style={{ backgroundColor: '#0a0a0f' }}>
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-0 left-1/4 w-96 h-96 rounded-full blur-[128px]" style={{ backgroundColor: 'rgba(0, 240, 255, 0.05)' }} />
      </div>

      <aside className="relative z-20 flex flex-col border-r" style={{ width: sidebarOpen ? 260 : 72, backgroundColor: 'rgba(20, 20, 31, 0.9)', backdropFilter: 'blur(24px)', borderColor: 'rgba(30, 30, 46, 0.3)' }}>
        <div className="p-6 border-b" style={{ borderColor: 'rgba(30, 30, 46, 0.2)' }}>
          <div className="flex items-center gap-3">
            <Shield className="w-8 h-8" style={{ color: '#00f0ff' }} />
            {sidebarOpen && (
              <div>
                <h1 className="font-bold text-lg tracking-tight" style={{ color: '#e4e4f0', fontFamily: 'Space Grotesk, sans-serif' }}>PHISHPULSE</h1>
                <p className="text-[10px] uppercase tracking-[0.2em]" style={{ color: '#8b8b9a', fontFamily: 'monospace' }}>v2.0.0 · PhantomSecDy</p>
              </div>
            )}
          </div>
        </div>

        <nav className="flex-1 p-3 space-y-1">
          {navItems.map((item) => {
            const isActive = location.pathname === item.path;
            const Icon = item.icon;
            return (
              <Link key={item.path} to={item.path}>
                <div className={cn('flex items-center gap-3 px-3 py-3 rounded-lg transition-all duration-200 relative', isActive ? 'border' : 'border border-transparent hover:bg-white/5')} style={isActive ? { backgroundColor: 'rgba(0, 240, 255, 0.1)', borderColor: 'rgba(0, 240, 255, 0.2)' } : {}}>
                  <Icon className="w-5 h-5 shrink-0" style={{ color: isActive ? '#00f0ff' : '#8b8b9a' }} />
                  {sidebarOpen && (
                    <div>
                      <div className="font-medium text-sm" style={{ color: isActive ? '#00f0ff' : '#8b8b9a' }}>{item.label}</div>
                      <div className="text-[10px]" style={{ color: 'rgba(139, 139, 154, 0.6)' }}>{item.desc}</div>
                    </div>
                  )}
                  {isActive && <div className="absolute right-3 w-1 h-6 rounded-full" style={{ backgroundColor: '#00f0ff' }} />}
                </div>
              </Link>
            );
          })}
        </nav>

        <div className="p-3 space-y-1 border-t" style={{ borderColor: 'rgba(30, 30, 46, 0.2)' }}>
          <button onClick={() => setTerminalOpen(!terminalOpen)} className="w-full flex items-center gap-3 px-3 py-3 rounded-lg hover:bg-white/5">
            <Terminal className="w-5 h-5" style={{ color: '#8b8b9a' }} />
            {sidebarOpen && <span className="text-sm" style={{ color: '#8b8b9a' }}>Terminal</span>}
          </button>
          <button onClick={() => setSidebarOpen(!sidebarOpen)} className="w-full flex items-center gap-3 px-3 py-3 rounded-lg hover:bg-white/5">
            {sidebarOpen ? <ChevronRight className="w-5 h-5 rotate-180" style={{ color: '#8b8b9a' }} /> : <Menu className="w-5 h-5" style={{ color: '#8b8b9a' }} />}
          </button>
        </div>
      </aside>

      <main className="flex-1 relative z-10 overflow-auto">
        <div className="p-8 max-w-7xl mx-auto">
          <AnimatePresence mode="wait">
            <motion.div key={location.pathname} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }} transition={{ duration: 0.3 }}>
              {children}
            </motion.div>
          </AnimatePresence>
        </div>
      </main>

      <AnimatePresence>
        {terminalOpen && (
          <motion.div initial={{ opacity: 0, y: '100%' }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: '100%' }} className="fixed bottom-0 left-0 right-0 h-64 z-50 p-4 border-t" style={{ backgroundColor: 'rgba(10, 10, 15, 0.95)', backdropFilter: 'blur(24px)', borderColor: 'rgba(0, 240, 255, 0.2)', fontFamily: 'monospace' }}>
            <div className="flex items-center justify-between mb-2">
              <span style={{ color: '#00f0ff' }}>phishpulse@parrot:~$</span>
              <button onClick={() => setTerminalOpen(false)}><X className="w-4 h-4" style={{ color: '#8b8b9a' }} /></button>
            </div>
            <div style={{ color: '#8b8b9a' }}>
              <p>{`>`} System initialized. 4 models loaded.</p>
              <p>{`>`} Awaiting input...</p>
              <p className="animate-pulse" style={{ color: '#00f0ff' }}>_</p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
