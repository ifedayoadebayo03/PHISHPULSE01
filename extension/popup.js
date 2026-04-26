/**
 * PhishPulse Browser Extension - Popup Script
 * 
 * Handles popup UI interactions and current page scanning.
 */

// DOM Elements
const urlDisplay = document.getElementById('url-display');
const scanBtn = document.getElementById('scan-btn');
const scanResult = document.getElementById('scan-result');
const riskScore = document.getElementById('risk-score');
const riskClassification = document.getElementById('risk-classification');
const riskIndicators = document.getElementById('risk-indicators');
const recentScans = document.getElementById('recent-scans');
const apiUrlInput = document.getElementById('api-url');
const autoScanCheckbox = document.getElementById('auto-scan');
const saveSettingsBtn = document.getElementById('save-settings');
const clearCacheLink = document.getElementById('clear-cache');

// Current tab URL
let currentUrl = '';

/**
 * Initialize popup
 */
async function init() {
  // Get current tab URL
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    currentUrl = tab.url;
    urlDisplay.textContent = currentUrl;
  } catch (e) {
    urlDisplay.textContent = 'Unable to get current URL';
    scanBtn.disabled = true;
  }
  
  // Load settings
  loadSettings();
  
  // Load recent scans
  loadRecentScans();
  
  // Setup event listeners
  scanBtn.addEventListener('click', scanCurrentPage);
  saveSettingsBtn.addEventListener('click', saveSettings);
  clearCacheLink.addEventListener('click', clearCache);
}

/**
 * Load settings from storage
 */
async function loadSettings() {
  try {
    const settings = await chrome.runtime.sendMessage({ action: 'getSettings' });
    if (settings.success) {
      apiUrlInput.value = settings.data.apiUrl || 'http://localhost:8000';
      autoScanCheckbox.checked = settings.data.autoScan || false;
    }
  } catch (e) {
    console.error('Error loading settings:', e);
  }
}

/**
 * Save settings to storage
 */
async function saveSettings() {
  const settings = {
    apiUrl: apiUrlInput.value.trim(),
    autoScan: autoScanCheckbox.checked
  };
  
  try {
    const result = await chrome.runtime.sendMessage({
      action: 'saveSettings',
      data: settings
    });
    
    if (result.success) {
      showMessage('Settings saved!', 'success');
    } else {
      showMessage('Failed to save settings', 'error');
    }
  } catch (e) {
    showMessage('Error saving settings', 'error');
  }
}

/**
 * Scan current page
 */
async function scanCurrentPage() {
  scanBtn.disabled = true;
  scanBtn.textContent = 'Scanning...';
  
  try {
    const result = await chrome.runtime.sendMessage({
      action: 'scanURL',
      data: { url: currentUrl }
    });
    
    if (result.success) {
      displayResult(result.data);
      addToRecentScans(result.data);
    } else {
      showMessage('Scan failed: ' + result.error, 'error');
    }
  } catch (e) {
    showMessage('Error: ' + e.message, 'error');
  } finally {
    scanBtn.disabled = false;
    scanBtn.textContent = 'Scan Current Page';
  }
}

/**
 * Display scan result
 */
function displayResult(result) {
  scanResult.classList.remove('hidden');
  
  const score = result.final_score;
  riskScore.textContent = score;
  riskClassification.textContent = result.classification;
  
  // Color code the score
  riskScore.className = '';
  if (score <= 30) {
    riskScore.classList.add('phishpulse-safe');
  } else if (score <= 60) {
    riskScore.classList.add('phishpulse-warning');
  } else if (score <= 85) {
    riskScore.classList.add('phishpulse-danger');
  } else {
    riskScore.classList.add('phishpulse-critical');
  }
  
  // Display indicators
  riskIndicators.innerHTML = '';
  if (result.indicators && result.indicators.length > 0) {
    const ul = document.createElement('ul');
    result.indicators.slice(0, 5).forEach(indicator => {
      const li = document.createElement('li');
      li.textContent = indicator;
      ul.appendChild(li);
    });
    riskIndicators.appendChild(ul);
  } else {
    riskIndicators.textContent = 'No specific indicators';
  }
}

/**
 * Add scan to recent scans list
 */
function addToRecentScans(result) {
  // Get existing recent scans
  chrome.storage.local.get('recentScans').then(data => {
    let scans = data.recentScans || [];
    
    // Add new scan
    scans.unshift({
      url: currentUrl,
      score: result.final_score,
      classification: result.classification,
      timestamp: Date.now()
    });
    
    // Keep only last 10
    scans = scans.slice(0, 10);
    
    // Save
    chrome.storage.local.set({ recentScans: scans });
    
    // Refresh display
    loadRecentScans();
  });
}

/**
 * Load and display recent scans
 */
async function loadRecentScans() {
  try {
    const data = await chrome.storage.local.get('recentScans');
    const scans = data.recentScans || [];
    
    if (scans.length === 0) {
      recentScans.innerHTML = '<p class="phishpulse-empty">No recent scans</p>';
      return;
    }
    
    recentScans.innerHTML = '';
    scans.forEach(scan => {
      const item = document.createElement('div');
      item.className = 'phishpulse-recent-item';
      
      const urlShort = scan.url.length > 40 ? scan.url.substring(0, 40) + '...' : scan.url;
      
      item.innerHTML = `
        <span class="phishpulse-recent-url" title="${scan.url}">${urlShort}</span>
        <span class="phishpulse-recent-score ${getScoreClass(scan.score)}">${scan.score}</span>
      `;
      
      recentScans.appendChild(item);
    });
  } catch (e) {
    console.error('Error loading recent scans:', e);
  }
}

/**
 * Get CSS class for score
 */
function getScoreClass(score) {
  if (score <= 30) return 'phishpulse-safe';
  if (score <= 60) return 'phishpulse-warning';
  if (score <= 85) return 'phishpulse-danger';
  return 'phishpulse-critical';
}

/**
 * Clear scan cache
 */
async function clearCache(e) {
  e.preventDefault();
  
  try {
    await chrome.runtime.sendMessage({ action: 'clearCache' });
    await chrome.storage.local.remove('recentScans');
    loadRecentScans();
    showMessage('Cache cleared', 'success');
  } catch (e) {
    showMessage('Error clearing cache', 'error');
  }
}

/**
 * Show message
 */
function showMessage(message, type) {
  // Create temporary message element
  const msg = document.createElement('div');
  msg.className = `phishpulse-message phishpulse-message-${type}`;
  msg.textContent = message;
  
  document.body.appendChild(msg);
  
  setTimeout(() => {
    msg.remove();
  }, 3000);
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', init);
