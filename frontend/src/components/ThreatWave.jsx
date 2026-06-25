import { motion } from 'framer-motion';
import { useMemo } from 'react';

export default function ThreatWave({ data = [] }) {
  const bars = useMemo(() => {
    return Array.from({ length: 40 }, (_, i) => ({
      id: i,
      height: Math.random() * 60 + 20,
      delay: i * 0.05,
    }));
  }, []);

  return (
    <div className="glass-panel p-6 h-48 flex items-end justify-between gap-1 overflow-hidden relative">
      <div className="absolute top-4 left-4 font-mono text-xs text-ghost uppercase tracking-wider">
        Live Threat Signal
      </div>
      {bars.map((bar) => (
        <motion.div
          key={bar.id}
          className="flex-1 bg-cyan/30 rounded-t-sm"
          initial={{ height: '10%' }}
          animate={{
            height: [`${bar.height}%`, `${bar.height * 0.5}%`, `${bar.height * 1.2}%`],
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            repeatType: 'reverse',
            delay: bar.delay,
            ease: 'easeInOut',
          }}
        />
      ))}
      <div className="absolute inset-0 bg-gradient-to-t from-obsidian via-transparent to-transparent pointer-events-none" />
    </div>
  );
}
