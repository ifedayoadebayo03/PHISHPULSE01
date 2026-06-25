import { motion } from 'framer-motion';

export default function RiskGauge({ score, size = 200 }) {
  const radius = (size - 12) / 2;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (score / 100) * circumference;
  
  const getColor = (s) => {
    if (s <= 30) return '#00ff88';
    if (s <= 60) return '#ffb800';
    return '#ff2a2a';
  };
  
  const strokeColor = getColor(score);
  const fontSize = size > 100 ? 'text-4xl' : size > 60 ? 'text-lg' : 'text-xs';

  return (
    <div className="relative flex items-center justify-center" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="transform -rotate-90 absolute">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="rgba(255,255,255,0.05)"
          strokeWidth={size > 100 ? 8 : 4}
        />
        <motion.circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={strokeColor}
          strokeWidth={size > 100 ? 8 : 4}
          strokeLinecap="round"
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset }}
          transition={{ duration: 1.5, ease: "easeOut" }}
          style={{ filter: size > 100 ? `drop-shadow(0 0 10px ${strokeColor}40)` : 'none' }}
        />
      </svg>
      
      <div className="relative z-10 flex flex-col items-center justify-center">
        <motion.span
          initial={{ opacity: 0, scale: 0.5 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.5 }}
          className={`font-bold ${fontSize}`}
          style={{ color: strokeColor, fontFamily: 'Space Grotesk, sans-serif', lineHeight: 1 }}
        >
          {score}
        </motion.span>
        {size > 100 && (
          <span className="text-[10px] font-mono uppercase tracking-wider" style={{ color: '#8b8b9a' }}>
            {score <= 30 ? 'Clean' : score <= 60 ? 'Suspicious' : score <= 85 ? 'Malicious' : 'Critical'}
          </span>
        )}
      </div>

      {score > 60 && size > 100 && (
        <motion.div
          animate={{ scale: [1, 1.2, 1], opacity: [0.3, 0, 0.3] }}
          transition={{ duration: 2, repeat: Infinity }}
          className="absolute inset-0 rounded-full"
          style={{ border: `2px solid ${strokeColor}`, filter: 'blur(4px)' }}
        />
      )}
    </div>
  );
}
