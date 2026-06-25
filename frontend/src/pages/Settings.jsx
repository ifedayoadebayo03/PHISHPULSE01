import { useState } from 'react';
import { motion } from 'framer-motion';
import { Settings, Sliders, Database, Bell, Shield, Save, RotateCcw } from 'lucide-react';

const SECTIONS = [
  {
    id: 'thresholds',
    label: 'Risk Thresholds',
    icon: Sliders,
    description: 'Adjust classification boundaries',
    settings: [
      { label: 'Clean → Suspicious', value: 30, color: '#00ff88', max: 100 },
      { label: 'Suspicious → Malicious', value: 60, color: '#ffb800', max: 100 },
      { label: 'Malicious → Critical', value: 85, color: '#ff2a2a', max: 100 },
    ],
  },
  {
    id: 'weights',
    label: 'Model Weights',
    icon: Shield,
    description: 'Tune AI engine consensus',
    settings: [
      { label: 'URL Lexical (A)', value: 30, color: '#00f0ff', max: 100 },
      { label: 'Email Forensic (B)', value: 35, color: '#00f0ff', max: 100 },
      { label: 'Visual Detector (C)', value: 35, color: '#00f0ff', max: 100 },
    ],
  },
  {
    id: 'system',
    label: 'System',
    icon: Database,
    description: 'Backend and database config',
    settings: [
      { label: 'API Endpoint', value: 'http://localhost:8000', type: 'text' },
      { label: 'Request Timeout (ms)', value: 5000, color: '#8b8b9a', max: 30000 },
      { label: 'Auto-save Reports', value: 1, type: 'toggle' },
    ],
  },
];

function SliderSetting({ label, value, color, max, onChange }) {
  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <span className="text-sm" style={{ color: '#e4e4f0' }}>{label}</span>
        <span className="text-xs font-bold" style={{ color, fontFamily: 'monospace' }}>{value}</span>
      </div>
      <input
        type="range"
        min={0}
        max={max}
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        className="w-full h-1.5 rounded-full appearance-none cursor-pointer"
        style={{
          background: `linear-gradient(to right, ${color} 0%, ${color} ${(value / max) * 100}%, rgba(30, 30, 46, 0.6) ${(value / max) * 100}%, rgba(30, 30, 46, 0.6) 100%)`,
          accentColor: color,
        }}
      />
    </div>
  );
}

export default function SettingsPage() {
  const [settings, setSettings] = useState(() => {
    const s = {};
    SECTIONS.forEach(sec => {
      s[sec.id] = {};
      sec.settings.forEach((set, i) => {
        s[sec.id][i] = set.value;
      });
    });
    return s;
  });

  const updateSetting = (sectionIdx, settingIdx, value) => {
    setSettings(prev => ({
      ...prev,
      [SECTIONS[sectionIdx].id]: {
        ...prev[SECTIONS[sectionIdx].id],
        [settingIdx]: value,
      },
    }));
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
            System Config
          </motion.h1>
          <p className="text-sm mt-1" style={{ color: '#8b8b9a', fontFamily: 'monospace' }}>
            Tune detection engine parameters
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            className="flex items-center gap-2 px-4 py-2 rounded-lg text-xs border transition-colors hover:bg-white/5"
            style={{ color: '#8b8b9a', borderColor: 'rgba(30, 30, 46, 0.6)', fontFamily: 'monospace' }}
          >
            <RotateCcw className="w-3 h-3" /> Reset Defaults
          </button>
          <button
            className="flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-medium transition-colors"
            style={{ backgroundColor: 'rgba(0, 240, 255, 0.15)', color: '#00f0ff', border: '1px solid rgba(0, 240, 255, 0.3)', fontFamily: 'monospace' }}
          >
            <Save className="w-3 h-3" /> Save Config
          </button>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-6">
        {SECTIONS.map((section, secIdx) => {
          const SectionIcon = section.icon;
          return (
            <motion.div
              key={section.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: secIdx * 0.1 }}
              className="p-6 border rounded-xl"
              style={{
                backgroundColor: 'rgba(20, 20, 31, 0.8)',
                borderColor: 'rgba(30, 30, 46, 0.4)',
                boxShadow: '0 4px 24px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.05)',
              }}
            >
              <div className="flex items-center gap-3 mb-1">
                <SectionIcon className="w-5 h-5" style={{ color: '#00f0ff' }} />
                <h3 className="font-medium" style={{ color: '#e4e4f0' }}>{section.label}</h3>
              </div>
              <p className="text-xs mb-5" style={{ color: '#8b8b9a', fontFamily: 'monospace' }}>{section.description}</p>

              <div className="space-y-5">
                {section.settings.map((setting, setIdx) => {
                  if (setting.type === 'text') {
                    return (
                      <div key={setIdx} className="space-y-2">
                        <span className="text-sm" style={{ color: '#e4e4f0' }}>{setting.label}</span>
                        <input
                          type="text"
                          value={settings[section.id][setIdx]}
                          onChange={(e) => updateSetting(secIdx, setIdx, e.target.value)}
                          className="w-full px-3 py-2 rounded-lg border text-sm outline-none"
                          style={{
                            backgroundColor: 'rgba(10, 10, 15, 0.8)',
                            borderColor: 'rgba(30, 30, 46, 0.6)',
                            color: '#e4e4f0',
                            fontFamily: 'monospace',
                          }}
                        />
                      </div>
                    );
                  }
                  if (setting.type === 'toggle') {
                    return (
                      <div key={setIdx} className="flex items-center justify-between">
                        <span className="text-sm" style={{ color: '#e4e4f0' }}>{setting.label}</span>
                        <button
                          onClick={() => updateSetting(secIdx, setIdx, settings[section.id][setIdx] ? 0 : 1)}
                          className="w-10 h-5 rounded-full transition-colors relative"
                          style={{ backgroundColor: settings[section.id][setIdx] ? 'rgba(0, 240, 255, 0.3)' : 'rgba(30, 30, 46, 0.6)' }}
                        >
                          <motion.div
                            animate={{ x: settings[section.id][setIdx] ? 20 : 2 }}
                            className="w-3.5 h-3.5 rounded-full absolute top-0.5"
                            style={{ backgroundColor: settings[section.id][setIdx] ? '#00f0ff' : '#8b8b9a' }}
                          />
                        </button>
                      </div>
                    );
                  }
                  return (
                    <SliderSetting
                      key={setIdx}
                      label={setting.label}
                      value={settings[section.id][setIdx]}
                      color={setting.color}
                      max={setting.max}
                      onChange={(v) => updateSetting(secIdx, setIdx, v)}
                    />
                  );
                })}
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Danger zone */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
        className="p-6 border rounded-xl"
        style={{
          backgroundColor: 'rgba(255, 42, 42, 0.05)',
          borderColor: 'rgba(255, 42, 42, 0.2)',
        }}
      >
        <h3 className="text-sm font-medium mb-2 flex items-center gap-2" style={{ color: '#ff2a2a' }}>
          <Shield className="w-4 h-4" /> Danger Zone
        </h3>
        <p className="text-xs mb-4" style={{ color: '#8b8b9a', fontFamily: 'monospace' }}>
          These actions are irreversible. Proceed with caution.
        </p>
        <div className="flex gap-3">
          <button className="px-4 py-2 rounded-lg text-xs border transition-colors hover:bg-red-500/10" style={{ color: '#ff2a2a', borderColor: 'rgba(255, 42, 42, 0.3)', fontFamily: 'monospace' }}>
            Clear All Reports
          </button>
          <button className="px-4 py-2 rounded-lg text-xs border transition-colors hover:bg-red-500/10" style={{ color: '#ff2a2a', borderColor: 'rgba(255, 42, 42, 0.3)', fontFamily: 'monospace' }}>
            Retrain All Models
          </button>
        </div>
      </motion.div>
    </div>
  );
}
