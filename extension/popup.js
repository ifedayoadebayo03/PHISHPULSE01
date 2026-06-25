document.getElementById('scanBtn').addEventListener('click', async () => {
  const url = document.getElementById('urlInput').value;
  const result = document.getElementById('result');
  
  result.style.display = 'block';
  result.textContent = 'Scanning...';
  result.className = '';
  
  try {
    const res = await fetch('http://localhost:8000/api/v1/scan', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type: 'url', target: url, options: {} }),
    });
    const data = await res.json();
    
    result.className = data.classification.toLowerCase();
    result.innerHTML = `
      <div style="font-size: 24px; font-weight: bold; margin-bottom: 4px;">${data.final_score}/100</div>
      <div style="text-transform: uppercase; font-size: 12px; margin-bottom: 8px;">${data.classification}</div>
      <div style="font-size: 10px; opacity: 0.7;">${data.indicators?.[0] || 'No indicators'}</div>
    `;
  } catch (e) {
    result.textContent = 'Error: ' + e.message;
  }
});