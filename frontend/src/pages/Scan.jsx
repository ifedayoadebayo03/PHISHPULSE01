import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Zap, Link2, Mail, Eye, Upload, Copy, Download, AlertTriangle, ShieldCheck, Skull, Activity, Loader2, Image } from 'lucide-react';
import RiskGauge from '../components/RiskGauge';
import { cn } from '../lib/utils';
import { scanURL, scanEmail, scanVisual } from '../lib/api';

const TABS = [
  { id: 'url', label: 'URL', icon: Link2, placeholder: 'https://suspicious-site.com/login' },
  { id: 'email', label: 'Email', icon: Mail, placeholder: 'Paste raw email headers + body...' },
  { id: 'visual', label: 'Visual', icon: Eye, placeholder: 'Drop image or paste base64 data' },
];

export default function Scan() {
  const [activeTab, setActiveTab] = useState('url');
  const [input, setInput] = useState('');
  const [scanning, setScanning] = useState(false);
  const [result, setResult] = useState(null);
  const [glitching, setGlitching] = useState(false);
  const [terminalLines, setTerminalLines] = useState([]);
  const [error, setError] = useState(null);
  const [droppedImage, setDroppedImage] = useState(null);
  const terminalRef = useRef(null);

  const addTerminalLine = (line) => {
    setTerminalLines(prev => [...prev.slice(-25), `[${new Date().toLocaleTimeString('en-GB', { hour12: false })}] ${line}`]);
  };

  const fileToBase64 = (file) => new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result.split(',')[1]);
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });

  const handleScan = async () => {
    if (!input.trim() && activeTab !== 'visual') return;
    setScanning(true);
    setResult(null);
    setError(null);
    setGlitching(true);
    setTerminalLines([]);
    
    addTerminalLine(`Initializing scan sequence...`);
    addTerminalLine(`Mode: ${activeTab.toUpperCase()}`);

    try {
      let data;
      const startTime = performance.now();

      if (activeTab === 'url') {
        addTerminalLine(`Target: ${input.slice(0, 60)}${input.length > 60 ? '...' : ''}`);
        addTerminalLine('Model A: URL Lexical Analyzer → ACTIVE');
        data = await scanURL(input);
      } else if (activeTab === 'email') {
        addTerminalLine(`Analyzing email headers...`);
        addTerminalLine('Model B: Email Forensic Analyzer → ACTIVE');
        data = await scanEmail(input);
      } else {
        // Visual — send base64 if we have a file, otherwise send the input as-is
        let visualTarget = input;
        if (droppedImage) {
          addTerminalLine(`Encoding image: ${droppedImage.name}...`);
          visualTarget = await fileToBase64(droppedImage);
        }
        addTerminalLine('Model C: Visual Detector → ACTIVE');
        data = await scanVisual(visualTarget);
      }

      const elapsed = Math.round(performance.now() - startTime);
      addTerminalLine(`Model D: Risk Fusion Engine → AGGREGATING`);
      addTerminalLine(`Scan complete in ${elapsed}ms`);
      addTerminalLine(`Classification: ${(data.classification || 'UNKNOWN').toUpperCase()}`);

      setGlitching(false);
      setScanning(false);
      setResult(data);
    } catch (e) {
      setGlitching(false);
      setScanning(false);
      setError(e.message);
      addTerminalLine(`ERROR: ${e.message}`);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      setDroppedImage(file);
      setInput(file.name);
      addTerminalLine(`Visual target loaded: ${file.name} (${(file.size / 1024).toFixed(1)}KB)`);
    } else {
      addTerminalLine(`ERROR: Only image files supported`);
    }
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file && file.type.startsWith('image/')) {
      setDroppedImage(file);
      setInput(file.name);
      addTerminalLine(`Visual target loaded: ${file.name} (${(file.size / 1024).toFixed(1)}KB)`);
    }
  };

  const currentTab = TABS.find(t => t.id === activeTab);
  const Icon = currentTab.icon;

  useEffect(() => {
    if (terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
    }
  }, [terminalLines]);

  const getScore = () => result?.final_score || 0;
  const getClassification = () => result?.classification || 'Unknown';
  const getIndicators = () => result?.indicators || [];
  const getMitigation = () => result?.mitigation_steps || [];
  const getModelBreakdown = () => result?.model_breakdown || {};
  const getScanId = () => result?.scan_id || result?.id || 'N/A';

  const getScoreColor = (score) => {
    if (score <= 30) return '#00ff88';
    if (score <= 60) return '#ffb800';
    return '#ff2a2a';
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-end justify-between">
        <div>
          <motion.h1 
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-3xl font-bold"
            style={{ color: '#e4e4f0', fontFamily: 'Space Grotesk, sans-serif' }}
          >
            Inject Target
          </motion.h1>
          <p className="text-sm mt-1" style={{ color: '#8b8b9a', fontFamily: 'monospace' }}>
            Multi-modal threat analysis engine
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full animate-pulse" style={{ backgroundColor: '#00f0ff' }} />
          <span className="text-xs" style={{ color: '#00f0ff', fontFamily: 'monospace' }}>READY</span>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-2">
        {TABS.map(tab => {
          const TabIcon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => { 
                setActiveTab(tab.id); 
                setInput(''); 
                setResult(null); 
                setError(null); 
                setTerminalLines([]); 
                setDroppedImage(null);
              }}
              className="flex items-center gap-2 px-4 py-2.5 rounded-lg border transition-all duration-200"
              style={{
                backgroundColor: activeTab === tab.id ? 'rgba(0, 240, 255, 0.1)' : 'rgba(20, 20, 31, 0.8)',
                borderColor: activeTab === tab.id ? 'rgba(0, 240, 255, 0.3)' : 'rgba(30, 30, 46, 0.4)',
                color: activeTab === tab.id ? '#00f0ff' : '#8b8b9a',
                fontFamily: 'monospace',
                fontSize: '13px',
              }}
            >
              <TabIcon className="w-4 h-4" />
              {tab.label}
            </button>
          );
        })}
      </div>

      {/* Input */}
      <motion.div
        animate={glitching ? { x: [0, -3, 3, -2, 2, 0], opacity: [1, 0.8, 1, 0.9, 1] } : {}}
        transition={{ duration: 0.3 }}
      >
        <div
          className="border rounded-xl overflow-hidden"
          style={{
            backgroundColor: 'rgba(20, 20, 31, 0.8)',
            borderColor: error ? 'rgba(255, 42, 42, 0.4)' : 'rgba(30, 30, 46, 0.4)',
            boxShadow: error ? '0 0 20px rgba(255, 42, 42, 0.1)' : '0 4px 24px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.05)',
          }}
          onDragOver={(e) => e.preventDefault()}
          onDrop={activeTab === 'visual' ? handleDrop : undefined}
        >
          <div className="flex items-center gap-2 px-4 py-2 border-b" style={{ borderColor: 'rgba(30, 30, 46, 0.4)', backgroundColor: 'rgba(10, 10, 15, 0.5)' }}>
            <div className="w-3 h-3 rounded-full" style={{ backgroundColor: '#ff2a2a' }} />
            <div className="w-3 h-3 rounded-full" style={{ backgroundColor: '#ffb800' }} />
            <div className="w-3 h-3 rounded-full" style={{ backgroundColor: '#00ff88' }} />
            <span className="ml-2 text-xs" style={{ color: '#8b8b9a', fontFamily: 'monospace' }}>
              {activeTab === 'url' ? 'target_url.sh' : activeTab === 'email' ? 'raw_email.eml' : 'visual_input.bin'}
            </span>
          </div>

          {activeTab === 'visual' ? (
            <div className="p-8 text-center" style={{ minHeight: '200px' }}>
              {droppedImage ? (
                <div className="space-y-3">
                  <Image className="w-12 h-12 mx-auto" style={{ color: '#00f0ff' }} />
                  <p style={{ color: '#e4e4f0', fontFamily: 'monospace', fontSize: '14px' }}>
                    {droppedImage.name}
                  </p>
                  <p style={{ color: '#8b8b9a', fontFamily: 'monospace', fontSize: '12px' }}>
                    {(droppedImage.size / 1024).toFixed(1)} KB · Ready to scan
                  </p>
                  <button
                    onClick={() => { setDroppedImage(null); setInput(''); }}
                    className="text-xs underline"
                    style={{ color: '#ff2a2a', fontFamily: 'monospace' }}
                  >
                    Remove
                  </button>
                </div>
              ) : (
                <>
                  <Upload className="w-12 h-12 mx-auto mb-4" style={{ color: 'rgba(0, 240, 255, 0.3)' }} />
                  <p style={{ color: '#8b8b9a', fontFamily: 'monospace', fontSize: '14px' }}>
                    Drop image here or click to browse
                  </p>
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleFileSelect}
                    className="hidden"
                    id="visual-file-input"
                  />
                  <label
                    htmlFor="visual-file-input"
                    className="inline-block mt-4 px-4 py-2 rounded-lg border cursor-pointer text-xs transition-colors hover:bg-white/5"
                    style={{ color: '#00f0ff', borderColor: 'rgba(0, 240, 255, 0.3)', fontFamily: 'monospace' }}
                  >
                    Browse Files
                  </label>
                  <p className="mt-3 text-xs" style={{ color: '#8b8b9a', fontFamily: 'monospace' }}>
                    Or paste base64 data below
                  </p>
                  <textarea
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Paste base64 image data..."
                    className="w-full mt-2 px-4 py-3 rounded-lg border text-xs outline-none focus:border-cyan/50 transition-colors resize-none"
                    style={{
                      backgroundColor: 'rgba(10, 10, 15, 0.8)',
                      borderColor: 'rgba(30, 30, 46, 0.6)',
                      color: '#e4e4f0',
                      fontFamily: 'monospace',
                      minHeight: '80px',
                    }}
                  />
                </>
              )}
            </div>
          ) : (
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder={currentTab.placeholder}
              className="w-full p-4 outline-none resize-none text-sm"
              style={{
                backgroundColor: 'rgba(10, 10, 15, 0.8)',
                color: '#e4e4f0',
                fontFamily: 'monospace',
                minHeight: activeTab === 'email' ? '280px' : '120px',
                border: 'none',
              }}
            />
          )}

          <div className="flex items-center justify-between px-4 py-3 border-t" style={{ borderColor: 'rgba(30, 30, 46, 0.4)', backgroundColor: 'rgba(10, 10, 15, 0.5)' }}>
            <span className="text-xs" style={{ color: '#8b8b9a', fontFamily: 'monospace' }}>
              {activeTab === 'visual' && droppedImage ? `${droppedImage.name}` : `${input.length} chars`}
            </span>
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={handleScan}
              disabled={scanning || (!input.trim() && !droppedImage)}
              className="flex items-center gap-2 px-6 py-2 rounded-lg font-medium text-sm transition-all disabled:opacity-40"
              style={{
                backgroundColor: scanning ? 'rgba(255, 184, 0, 0.2)' : 'rgba(0, 240, 255, 0.15)',
                color: '#00f0ff',
                border: '1px solid rgba(0, 240, 255, 0.3)',
                fontFamily: 'monospace',
              }}
            >
              {scanning ? <Loader2 className="w-4 h-4 animate-spin" /> : <Zap className="w-4 h-4" />}
              {scanning ? 'SCANNING...' : 'EXECUTE SCAN'}
            </motion.button>
          </div>
        </div>
      </motion.div>

      {/* Error */}
      <AnimatePresence>
        {error && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="p-4 border rounded-lg"
            style={{ backgroundColor: 'rgba(255, 42, 42, 0.1)', borderColor: 'rgba(255, 42, 42, 0.3)' }}
          >
            <p className="text-sm flex items-center gap-2" style={{ color: '#ff2a2a', fontFamily: 'monospace' }}>
              <AlertTriangle className="w-4 h-4" /> {error}
            </p>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Terminal */}
      <AnimatePresence>
        {terminalLines.length > 0 && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="border rounded-lg overflow-hidden"
            style={{
              backgroundColor: 'rgba(10, 10, 15, 0.95)',
              borderColor: 'rgba(0, 240, 255, 0.15)',
              fontFamily: 'monospace',
              fontSize: '12px',
            }}
          >
            <div className="px-4 py-2 border-b flex items-center justify-between" style={{ borderColor: 'rgba(0, 240, 255, 0.1)' }}>
              <span style={{ color: '#00f0ff' }}>phishpulse@parrot:~$ scan --verbose</span>
              <span className="text-xs" style={{ color: '#8b8b9a' }}>{terminalLines.length} lines</span>
            </div>
            <div ref={terminalRef} className="p-4 space-y-1 max-h-56 overflow-y-auto">
              {terminalLines.map((line, i) => (
                <motion.p
                  key={i}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="truncate"
                  style={{ color: line.includes('COMPLETE') || line.includes('Clean') ? '#00ff88' : line.includes('ERROR') || line.includes('Critical') || line.includes('Malicious') ? '#ff2a2a' : line.includes('Suspicious') ? '#ffb800' : '#8b8b9a' }}
                >
                  <span style={{ color: 'rgba(0, 240, 255, 0.5)' }}>❯</span> {line}
                </motion.p>
              ))}
              {scanning && <motion.span animate={{ opacity: [0, 1, 0] }} transition={{ repeat: Infinity, duration: 0.8 }} style={{ color: '#00f0ff' }}>_</motion.span>}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Result */}
      <AnimatePresence>
        {result && (
          <motion.div
            initial={{ opacity: 0, y: 30, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            transition={{ duration: 0.5, ease: 'easeOut' }}
            className="space-y-6"
          >
            {/* Verdict */}
            <div
              className="border rounded-xl overflow-hidden"
              style={{
                backgroundColor: 'rgba(20, 20, 31, 0.9)',
                borderColor: getScoreColor(getScore()) + '40',
                boxShadow: getScore() > 60 ? '0 0 40px rgba(255, 42, 42, 0.1)' : getScore() > 30 ? '0 0 40px rgba(255, 184, 0, 0.1)' : '0 4px 24px rgba(0, 0, 0, 0.4)',
              }}
            >
              <div className="p-6 flex items-center gap-6">
                <RiskGauge score={getScore()} size={160} />
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    {getScore() > 60 ? <Skull className="w-6 h-6" style={{ color: '#ff2a2a' }} /> : getScore() > 30 ? <AlertTriangle className="w-6 h-6" style={{ color: '#ffb800' }} /> : <ShieldCheck className="w-6 h-6" style={{ color: '#00ff88' }} />}
                    <span className="text-2xl font-bold" style={{ color: getScoreColor(getScore()), fontFamily: 'Space Grotesk, sans-serif' }}>
                      {getClassification().toUpperCase()}
                    </span>
                  </div>
                  <p className="text-sm mb-3" style={{ color: '#8b8b9a', fontFamily: 'monospace' }}>
                    Scan ID: {getScanId()}
                  </p>
                  <div className="flex gap-2">
                    <button 
                      onClick={() => navigator.clipboard.writeText(JSON.stringify(result, null, 2))}
                      className="flex items-center gap-1.5 px-3 py-1.5 rounded text-xs border transition-colors hover:bg-white/5"
                      style={{ color: '#8b8b9a', borderColor: 'rgba(30, 30, 46, 0.6)', fontFamily: 'monospace' }}
                    >
                      <Copy className="w-3 h-3" /> Copy JSON
                    </button>
                    {result.report_url && (
                      <a 
                        href={result.report_url}
                        className="flex items-center gap-1.5 px-3 py-1.5 rounded text-xs border transition-colors hover:bg-white/5"
                        style={{ color: '#8b8b9a', borderColor: 'rgba(30, 30, 46, 0.6)', fontFamily: 'monospace' }}
                      >
                        <Download className="w-3 h-3" /> PDF
                      </a>
                    )}
                  </div>
                </div>
              </div>
            </div>

            {/* Indicators + Model Consensus */}
            <div className="grid grid-cols-2 gap-6">
              {/* Left: Indicators + Mitigation */}
              <div className="p-6 border rounded-xl" style={{ backgroundColor: 'rgba(20, 20, 31, 0.8)', borderColor: 'rgba(30, 30, 46, 0.4)' }}>
                <h3 className="text-xs uppercase tracking-wider mb-4 flex items-center gap-2" style={{ color: '#8b8b9a', fontFamily: 'monospace' }}>
                  <AlertTriangle className="w-4 h-4" /> Threat Indicators
                </h3>
                <div className="space-y-2">
                  {getIndicators().map((ind, i) => (
                    <motion.div
                      key={i}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: i * 0.1 }}
                      className="flex items-start gap-3 p-3 rounded-lg"
                      style={{ backgroundColor: 'rgba(255, 42, 42, 0.05)', border: '1px solid rgba(255, 42, 42, 0.1)' }}
                    >
                      <span className="text-xs font-bold mt-0.5" style={{ color: '#ff2a2a', fontFamily: 'monospace' }}>{String(i + 1).padStart(2, '0')}</span>
                      <span className="text-sm" style={{ color: '#e4e4f0' }}>{ind}</span>
                    </motion.div>
                  ))}
                  {getIndicators().length === 0 && (
                    <p className="text-sm" style={{ color: '#8b8b9a' }}>No indicators generated.</p>
                  )}
                </div>

                {getMitigation().length > 0 && (
                  <div className="mt-4 pt-4 border-t" style={{ borderColor: 'rgba(30, 30, 46, 0.4)' }}>
                    <h4 className="text-xs uppercase tracking-wider mb-3 flex items-center gap-2" style={{ color: '#8b8b9a', fontFamily: 'monospace' }}>
                      <ShieldCheck className="w-3 h-3" /> Mitigation
                    </h4>
                    <div className="space-y-1">
                      {getMitigation().map((step, i) => (
                        <p key={i} className="text-xs" style={{ color: '#00ff88', fontFamily: 'monospace' }}>
                          ✓ {step}
                        </p>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* Right: Model Consensus */}
              <div className="p-6 border rounded-xl" style={{ backgroundColor: 'rgba(20, 20, 31, 0.8)', borderColor: 'rgba(30, 30, 46, 0.4)' }}>
                <h3 className="text-xs uppercase tracking-wider mb-4 flex items-center gap-2" style={{ color: '#8b8b9a', fontFamily: 'monospace' }}>
                  <Activity className="w-4 h-4" /> Model Consensus
                </h3>
                <div className="space-y-4">
                  {Object.entries(getModelBreakdown()).map(([key, data], i) => {
                    if (!data || data.score === null || data.score === undefined) return null;
                    return (
                      <motion.div
                        key={key}
                        initial={{ opacity: 0, x: 10 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: i * 0.15 }}
                      >
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-sm" style={{ color: '#e4e4f0' }}>
                            {key === 'url_analyzer' ? 'URL Lexical (A)' : key === 'email_forensics' ? 'Email Forensic (B)' : key === 'visual_detector' ? 'Visual Detector (C)' : key}
                          </span>
                          <span className="text-xs" style={{ color: '#8b8b9a', fontFamily: 'monospace' }}>
                            Weight: {data.weight ? (data.weight * 100).toFixed(0) : 'N/A'}%
                          </span>
                        </div>
                        <div className="h-2 rounded-full overflow-hidden" style={{ backgroundColor: 'rgba(30, 30, 46, 0.6)' }}>
                          <motion.div
                            initial={{ width: 0 }}
                            animate={{ width: `${data.score || 0}%` }}
                            transition={{ duration: 1, delay: 0.5 + i * 0.2 }}
                            className="h-full rounded-full"
                            style={{ backgroundColor: getScoreColor(data.score || 0) }}
                          />
                        </div>
                        <div className="flex items-center justify-between mt-1">
                          <span className="text-xs" style={{ color: '#8b8b9a', fontFamily: 'monospace' }}>Contribution: {data.contribution?.toFixed(1) || 0}</span>
                          <span className="text-xs font-bold" style={{ color: getScoreColor(data.score || 0), fontFamily: 'monospace' }}>{data.score || 0}/100</span>
                        </div>
                      </motion.div>
                    );
                  })}
                  {Object.keys(getModelBreakdown()).length === 0 && (
                    <p className="text-sm" style={{ color: '#8b8b9a' }}>No model breakdown available.</p>
                  )}
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.8 }}
                    className="pt-3 border-t"
                    style={{ borderColor: 'rgba(30, 30, 46, 0.4)' }}
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium" style={{ color: '#00f0ff' }}>Risk Fusion Engine (D)</span>
                      <span className="text-lg font-bold" style={{ color: '#00f0ff', fontFamily: 'Space Grotesk, sans-serif' }}>{getScore()}/100</span>
                    </div>
                    {result.confidence_interval && (
                      <p className="text-xs mt-1" style={{ color: '#8b8b9a', fontFamily: 'monospace' }}>
                        Confidence: [{result.confidence_interval[0]?.toFixed(2)}, {result.confidence_interval[1]?.toFixed(2)}]
                      </p>
                    )}
                  </motion.div>
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
