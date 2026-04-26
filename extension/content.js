/**
 * PhishPulse Browser Extension - Content Script
 * 
 * Extracts email content from Gmail and Outlook for analysis.
 * Injects risk indicators into email headers.
 */

// Platform detection
const PLATFORM = {
  GMAIL: 'gmail',
  OUTLOOK: 'outlook',
  OUTLOOK_LIVE: 'outlook_live',
  UNKNOWN: 'unknown'
};

let currentPlatform = PLATFORM.UNKNOWN;
let observer = null;

/**
 * Initialize content script
 */
function init() {
  console.log('PhishPulse content script initializing...');
  
  // Detect platform
  currentPlatform = detectPlatform();
  console.log('Detected platform:', currentPlatform);
  
  if (currentPlatform === PLATFORM.UNKNOWN) {
    console.log('Unknown platform, not activating');
    return;
  }
  
  // Initial scan
  scanVisibleEmails();
  
  // Set up mutation observer for SPA navigation
  setupMutationObserver();
}

/**
 * Detect email platform based on URL and DOM
 */
function detectPlatform() {
  const url = window.location.href;
  
  if (url.includes('mail.google.com')) {
    return PLATFORM.GMAIL;
  } else if (url.includes('outlook.office.com')) {
    return PLATFORM.OUTLOOK;
  } else if (url.includes('outlook.live.com')) {
    return PLATFORM.OUTLOOK_LIVE;
  }
  
  return PLATFORM.UNKNOWN;
}

/**
 * Set up mutation observer to handle SPA navigation
 */
function setupMutationObserver() {
  const targetNode = document.body;
  const config = { childList: true, subtree: true };
  
  let debounceTimer = null;
  
  observer = new MutationObserver((mutations) => {
    // Debounce to avoid excessive scans
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      scanVisibleEmails();
    }, 1000);
  });
  
  observer.observe(targetNode, config);
}

/**
 * Scan all visible emails
 */
function scanVisibleEmails() {
  const emails = extractEmails();
  
  emails.forEach(email => {
    if (!email.element.dataset.phishpulseScanned) {
      scanEmail(email);
    }
  });
}

/**
 * Extract emails from current page
 */
function extractEmails() {
  switch (currentPlatform) {
    case PLATFORM.GMAIL:
      return extractGmailEmails();
    case PLATFORM.OUTLOOK:
    case PLATFORM.OUTLOOK_LIVE:
      return extractOutlookEmails();
    default:
      return [];
  }
}

/**
 * Extract emails from Gmail
 */
function extractGmailEmails() {
  const emails = [];
  
  // Gmail email containers
  const selectors = [
    'div[role="listitem"][data-message-id]',
    '.h7',
    '.gs'
  ];
  
  for (const selector of selectors) {
    const containers = document.querySelectorAll(selector);
    
    containers.forEach(container => {
      try {
        // Extract sender
        const senderEl = container.querySelector('span[email]');
        const sender = senderEl ? senderEl.getAttribute('email') : 'unknown';
        
        // Extract subject
        const subjectEl = container.querySelector('h2[data-legacy-thread-id]');
        const subject = subjectEl ? subjectEl.textContent.trim() : '';
        
        // Extract body
        const bodyEl = container.querySelector('.a3s.aiL');
        const body = bodyEl ? bodyEl.innerText : '';
        
        // Extract links
        const links = Array.from(container.querySelectorAll('a[href]')).map(a => ({
          href: a.href,
          text: a.textContent
        }));
        
        emails.push({
          element: container,
          sender,
          subject,
          body,
          links,
          platform: PLATFORM.GMAIL
        });
      } catch (e) {
        console.error('Error extracting Gmail email:', e);
      }
    });
  }
  
  return emails;
}

/**
 * Extract emails from Outlook
 */
function extractOutlookEmails() {
  const emails = [];
  
  // Outlook email containers
  const selectors = [
    'div[data-conversation-id]',
    '.customScrollBar',
    '[role="region"]'
  ];
  
  for (const selector of selectors) {
    const containers = document.querySelectorAll(selector);
    
    containers.forEach(container => {
      try {
        // Extract sender
        const senderEl = container.querySelector('div[role="heading"]');
        const sender = senderEl ? senderEl.textContent.trim() : 'unknown';
        
        // Extract subject (usually in h1 or specific class)
        const subjectEl = container.querySelector('h1, .subject, [role="heading"]');
        const subject = subjectEl ? subjectEl.textContent.trim() : '';
        
        // Extract body
        const bodyEl = container.querySelector('[id*="UniqueBody"], .x_readMsgBody, [role="region"]');
        const body = bodyEl ? bodyEl.innerText : '';
        
        // Extract links
        const links = Array.from(container.querySelectorAll('a[href]')).map(a => ({
          href: a.href,
          text: a.textContent
        }));
        
        emails.push({
          element: container,
          sender,
          subject,
          body,
          links,
          platform: PLATFORM.OUTLOOK
        });
      } catch (e) {
        console.error('Error extracting Outlook email:', e);
      }
    });
  }
  
  return emails;
}

/**
 * Scan a single email via background script
 */
async function scanEmail(email) {
  // Mark as scanned
  email.element.dataset.phishpulseScanned = 'true';
  
  try {
    // Send to background script for API call
    const response = await chrome.runtime.sendMessage({
      action: 'scanEmail',
      data: {
        content: `${email.subject}\n\n${email.body}`,
        headers: `From: ${email.sender}`,
        links: email.links
      }
    });
    
    if (response.success) {
      injectRiskIndicator(email.element, response.data);
    } else {
      console.error('Scan failed:', response.error);
    }
  } catch (e) {
    console.error('Error scanning email:', e);
  }
}

/**
 * Inject risk indicator badge into email header
 */
function injectRiskIndicator(element, result) {
  const score = result.final_score;
  const classification = result.classification;
  
  // Determine color
  let colorClass = 'phishpulse-safe';
  if (score > 85) {
    colorClass = 'phishpulse-critical';
  } else if (score > 60) {
    colorClass = 'phishpulse-danger';
  } else if (score > 30) {
    colorClass = 'phishpulse-warning';
  }
  
  // Create badge
  const badge = document.createElement('div');
  badge.className = `phishpulse-badge ${colorClass}`;
  badge.innerHTML = `
    <span class="phishpulse-score">${score}</span>
    <span class="phishpulse-label">${classification}</span>
  `;
  badge.title = `PhishPulse Risk Score: ${score}/100 - ${classification}`;
  
  // Add click handler to show details
  badge.addEventListener('click', (e) => {
    e.stopPropagation();
    showDetailsModal(result);
  });
  
  // Find insertion point
  const headerEl = element.querySelector('h1, h2, h3, .hP, [role="heading"]');
  if (headerEl && !headerEl.querySelector('.phishpulse-badge')) {
    headerEl.style.position = 'relative';
    headerEl.appendChild(badge);
  }
}

/**
 * Show details modal for scan result
 */
function showDetailsModal(result) {
  // Remove existing modal
  const existing = document.getElementById('phishpulse-modal');
  if (existing) {
    existing.remove();
  }
  
  // Create modal
  const modal = document.createElement('div');
  modal.id = 'phishpulse-modal';
  modal.className = 'phishpulse-modal';
  
  const indicatorsHtml = result.indicators.map(i => 
    `<li>${escapeHtml(i)}</li>`
  ).join('');
  
  const mitigationHtml = result.mitigation_steps.map(s => 
    `<li>${escapeHtml(s)}</li>`
  ).join('');
  
  modal.innerHTML = `
    <div class="phishpulse-modal-content">
      <div class="phishpulse-modal-header">
        <h2>PhishPulse Analysis</h2>
        <span class="phishpulse-close">&times;</span>
      </div>
      <div class="phishpulse-modal-body">
        <div class="phishpulse-score-display">
          <span class="phishpulse-big-score" style="color: ${getScoreColor(result.final_score)}">
            ${result.final_score}
          </span>
          <span class="phishpulse-classification">${result.classification}</span>
        </div>
        
        <h3>Indicators</h3>
        <ul>${indicatorsHtml || '<li>No specific indicators</li>'}</ul>
        
        <h3>Recommended Actions</h3>
        <ul>${mitigationHtml || '<li>No specific actions required</li>'}</ul>
        
        <div class="phishpulse-model-breakdown">
          <h3>Model Breakdown</h3>
          <table>
            <tr><td>URL Analysis</td><td>${result.model_breakdown?.url_analyzer?.score || 'N/A'}</td></tr>
            <tr><td>Email Analysis</td><td>${result.model_breakdown?.email_forensics?.score || 'N/A'}</td></tr>
            <tr><td>Visual Analysis</td><td>${result.model_breakdown?.visual_detector?.score || 'N/A'}</td></tr>
          </table>
        </div>
      </div>
    </div>
  `;
  
  // Add close handler
  modal.querySelector('.phishpulse-close').addEventListener('click', () => {
    modal.remove();
  });
  
  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.remove();
    }
  });
  
  document.body.appendChild(modal);
}

/**
 * Get color for score
 */
function getScoreColor(score) {
  if (score <= 30) return '#28a745';
  if (score <= 60) return '#ffc107';
  if (score <= 85) return '#dc3545';
  return '#721c24';
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
