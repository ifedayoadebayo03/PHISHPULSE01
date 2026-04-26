/**
 * PhishPulse Browser Extension - Background Script (Service Worker)
 * 
 * Handles:
 * - API communication with PhishPulse backend
 * - Message passing between content scripts and popup
 * - Scan result caching
 */

// Default API endpoint
const DEFAULT_API_URL = 'http://localhost:8000';

// Cache for scan results
const scanCache = new Map();
const CACHE_DURATION = 5 * 60 * 1000; // 5 minutes

/**
 * Initialize extension
 */
chrome.runtime.onInstalled.addListener((details) => {
  console.log('PhishPulse installed:', details.reason);
  
  // Set default settings
  chrome.storage.sync.set({
    apiUrl: DEFAULT_API_URL,
    autoScan: true,
    showIndicators: true,
    minRiskLevel: 30
  });
});

/**
 * Handle messages from content scripts and popup
 */
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log('Background received message:', request.action);
  
  switch (request.action) {
    case 'scanURL':
      handleScanURL(request.data)
        .then(result => sendResponse({ success: true, data: result }))
        .catch(error => sendResponse({ success: false, error: error.message }));
      return true; // Keep channel open for async
      
    case 'scanEmail':
      handleScanEmail(request.data)
        .then(result => sendResponse({ success: true, data: result }))
        .catch(error => sendResponse({ success: false, error: error.message }));
      return true;
      
    case 'getSettings':
      chrome.storage.sync.get(['apiUrl', 'autoScan', 'showIndicators', 'minRiskLevel'])
        .then(settings => sendResponse({ success: true, data: settings }))
        .catch(error => sendResponse({ success: false, error: error.message }));
      return true;
      
    case 'saveSettings':
      chrome.storage.sync.set(request.data)
        .then(() => sendResponse({ success: true }))
        .catch(error => sendResponse({ success: false, error: error.message }));
      return true;
      
    case 'clearCache':
      scanCache.clear();
      sendResponse({ success: true });
      return true;
      
    default:
      sendResponse({ success: false, error: 'Unknown action' });
      return false;
  }
});

/**
 * Scan a URL via PhishPulse API
 */
async function handleScanURL(data) {
  const { url } = data;
  
  // Check cache
  const cacheKey = `url:${url}`;
  const cached = scanCache.get(cacheKey);
  if (cached && (Date.now() - cached.timestamp) < CACHE_DURATION) {
    console.log('Returning cached result for:', url);
    return cached.result;
  }
  
  // Get API URL from settings
  const settings = await chrome.storage.sync.get('apiUrl');
  const apiUrl = settings.apiUrl || DEFAULT_API_URL;
  
  // Call API
  const response = await fetch(`${apiUrl}/api/v1/scan/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      type: 'url',
      target: url,
      options: {
        screenshot: false,
        generate_report: false
      }
    })
  });
  
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }
  
  const result = await response.json();
  
  // Cache result
  scanCache.set(cacheKey, {
    timestamp: Date.now(),
    result: result
  });
  
  return result;
}

/**
 * Scan an email via PhishPulse API
 */
async function handleScanEmail(data) {
  const { content, headers, links } = data;
  
  // Get API URL from settings
  const settings = await chrome.storage.sync.get('apiUrl');
  const apiUrl = settings.apiUrl || DEFAULT_API_URL;
  
  // Create email content with headers
  const fullEmail = headers ? `${headers}\n\n${content}` : content;
  
  // Call API
  const response = await fetch(`${apiUrl}/api/v1/scan/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      type: 'email',
      target: fullEmail,
      headers: headers,
      options: {
        screenshot: false,
        generate_report: false
      }
    })
  });
  
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }
  
  return await response.json();
}

/**
 * Clean old cache entries periodically
 */
setInterval(() => {
  const now = Date.now();
  for (const [key, value] of scanCache.entries()) {
    if (now - value.timestamp > CACHE_DURATION) {
      scanCache.delete(key);
    }
  }
}, CACHE_DURATION);

console.log('PhishPulse background script loaded');
