import { useState, useEffect } from 'react'
import { useQuery } from 'react-query'
import { scanAPI, healthAPI } from '../services/api'
import RiskGauge from '../components/RiskGauge'
import ScanHistory from '../components/ScanHistory'

function Dashboard() {
  const [scanUrl, setScanUrl] = useState('')
  const [scanResult, setScanResult] = useState(null)
  const [isScanning, setIsScanning] = useState(false)

  // Fetch statistics
  const { data: stats, isLoading: statsLoading } = useQuery(
    'statistics',
    () => healthAPI.getStatistics().then(res => res.data),
    { refetchInterval: 30000 }
  )

  // Fetch recent scans
  const { data: recentScans, refetch: refetchScans } = useQuery(
    'recentScans',
    () => scanAPI.listScans(0, 10).then(res => res.data),
    { refetchInterval: 10000 }
  )

  // Handle scan
  const handleScan = async (e) => {
    e.preventDefault()
    if (!scanUrl) return

    setIsScanning(true)
    try {
      const result = await scanAPI.createScan('url', scanUrl, {
        screenshot: false,
        generate_report: false
      })
      setScanResult(result.data)
      refetchScans()
    } catch (error) {
      alert('Scan failed: ' + error.message)
    } finally {
      setIsScanning(false)
    }
  }

  return (
    <div className="space-y-6">
      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="card">
          <h3 className="text-gray-500 text-sm font-medium">Total Scans</h3>
          <p className="text-3xl font-bold text-phishpulse-navy">
            {statsLoading ? '-' : stats?.total_scans || 0}
          </p>
        </div>
        <div className="card">
          <h3 className="text-gray-500 text-sm font-medium">Last 24h</h3>
          <p className="text-3xl font-bold text-phishpulse-navy">
            {statsLoading ? '-' : stats?.last_24h_scans || 0}
          </p>
        </div>
        <div className="card">
          <h3 className="text-gray-500 text-sm font-medium">Threats Detected</h3>
          <p className="text-3xl font-bold text-phishpulse-danger">
            {statsLoading ? '-' : (stats?.malicious_count || 0) + (stats?.critical_count || 0)}
          </p>
        </div>
        <div className="card">
          <h3 className="text-gray-500 text-sm font-medium">Avg Risk Score</h3>
          <p className="text-3xl font-bold text-phishpulse-amber">
            {statsLoading ? '-' : stats?.average_risk_score || 0}
          </p>
        </div>
      </div>

      {/* Quick Scan */}
      <div className="card">
        <h2 className="text-lg font-bold mb-4">Quick Scan</h2>
        <form onSubmit={handleScan} className="flex gap-4">
          <input
            type="url"
            value={scanUrl}
            onChange={(e) => setScanUrl(e.target.value)}
            placeholder="Enter URL to scan..."
            className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-phishpulse-navy"
            required
          />
          <button
            type="submit"
            disabled={isScanning}
            className="btn-primary disabled:opacity-50"
          >
            {isScanning ? 'Scanning...' : 'Scan'}
          </button>
        </form>

        {/* Scan Result */}
        {scanResult && (
          <div className="mt-6 p-6 bg-gray-50 rounded-lg">
            <div className="flex items-start gap-8">
              <div className="flex-shrink-0">
                <RiskGauge score={scanResult.final_score} size={200} />
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-4">
                  <span className="text-2xl font-bold">
                    {scanResult.classification}
                  </span>
                  <span className="text-gray-500">
                    (Score: {scanResult.final_score}/100)
                  </span>
                </div>
                
                <div className="mb-4">
                  <h4 className="font-semibold mb-2">Indicators:</h4>
                  <ul className="list-disc list-inside space-y-1 text-sm">
                    {scanResult.indicators?.map((indicator, i) => (
                      <li key={i} className="text-gray-700">{indicator}</li>
                    ))}
                  </ul>
                </div>

                <div className="mb-4">
                  <h4 className="font-semibold mb-2">Mitigation Steps:</h4>
                  <ul className="list-disc list-inside space-y-1 text-sm">
                    {scanResult.mitigation_steps?.map((step, i) => (
                      <li key={i} className="text-gray-700">{step}</li>
                    ))}
                  </ul>
                </div>

                {scanResult.report_url && (
                  <a
                    href={`http://localhost:8000${scanResult.report_url}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-phishpulse-navy hover:underline"
                  >
                    Download Full Report →
                  </a>
                )}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Recent Scans */}
      <div className="card">
        <h2 className="text-lg font-bold mb-4">Recent Scans</h2>
        <ScanHistory scans={recentScans?.scans || []} />
      </div>
    </div>
  )
}

export default Dashboard
