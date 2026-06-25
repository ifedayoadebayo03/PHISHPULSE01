import { motion } from 'framer-motion';
import { Cpu, Eye, Mail, Link2 } from 'lucide-react';
import { cn } from '../lib/utils';

const models = [
  { id: 'A', name: 'URL Lexical', icon: Link2, status: 'active', load: 87 },
  { id: 'B', name: 'Email Forensic', icon: Mail, status: 'active', load: 64 },
  { id: 'C', name: 'Visual Detector', icon: Eye, status: 'active', load: 92 },
  { id: 'D', name: 'Risk Fusion', icon: Cpu, status: 'standby', load: 45 },
];

export default function ModelCore() {
  return (
    <div className="glass-panel p-6">
      <h3 className="font-mono text-xs text-ghost uppercase tracking-wider mb-4">
        AI Core Status
      </h3>
      <div className="grid grid-cols-2 gap-4">
        {models.map((model, i) => {
          const Icon = model.icon;
          const isActive = model.status === 'active';
          return (
            <motion.div
              key={model.id}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: i * 0.1 }}
              className={cn(
                'relative p-4 rounded-lg border transition-all duration-300',
                isActive 
                  ? 'bg-cyan/5 border-cyan/20' 
                  : 'bg-surface/50 border-slate/20'
              )}
            >
              <div className="absolute -top-2 -right-2 w-6 h-6 bg-obsidian border border-cyan/30 rounded flex items-center justify-center">
                <span className="text-[10px] font-mono text-cyan font-bold">
                  {model.id}
                </span>
              </div>
              
              <div className="flex items-center gap-3 mb-3">
                <Icon className={cn(
                  'w-4 h-4',
                  isActive ? 'text-cyan' : 'text-ghost'
                )} />
                <span className="text-sm font-medium text-frost">
                  {model.name}
                </span>
              </div>
              
              <div className="h-1 bg-slate/30 rounded-full overflow-hidden">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${model.load}%` }}
                  transition={{ duration: 1, delay: 0.5 }}
                  className={cn(
                    'h-full rounded-full',
                    model.load > 80 ? 'bg-crimson' : model.load > 50 ? 'bg-amber' : 'bg-emerald'
                  )}
                />
              </div>
              <span className="text-[10px] font-mono text-ghost mt-1 block">
                Load: {model.load}%
              </span>

              {isActive && (
                <motion.div
                  animate={{ opacity: [0, 0.5, 0] }}
                  transition={{ duration: 2, repeat: Infinity }}
                  className="absolute inset-0 rounded-lg"
                  style={{
                    background: 'linear-gradient(90deg, transparent, rgba(0,240,255,0.05), transparent)',
                  }}
                />
              )}
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
