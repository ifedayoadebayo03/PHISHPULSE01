import { useState, useEffect } from 'react'
import { useQuery } from 'react-query'
import { healthAPI } from '../services/api'

function Settings() {
  const [settings, setSettings] = useState({
    apiUrl: 'http://localhost:8000',
    autoScan: true,
    minRiskLevel: 30
  })
  const [saved, setSaved] = useState(false)

  const { data: modelInfo, isLoading: modelLoading } = useQuery(
    'modelInfo',
    () => healthAPI.getModelInfo().then(res => res.data)
  )

  const handleSave = () => {
    // Save to localStorage for demo
    localStorage.setItem('phishpulse_settings', JSON.stringify(settings))
    setSaved(true)
    setTimeout(() => setSaved(false), 3000)
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'loaded': return 'text-green-600'
      case 'untrained': return 'text-yellow-600'
      default: return 'text-gray-600'
    }
  }

  return (
    <div className="space-y-6">
      {/* Model Information */}
      <div className="card">
        <h2 className="text-lg font-bold mb-4">AI Models</h2>
        
        {modelLoading ? (
          <p className="text-gray-500">Loading model information...</p>
        ) : (
          <div className="space-y-4">
            {modelInfo?.models?.map((model, index) => (
              <div key={index} className="border rounded-lg p-4">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="font-semibold text-phishpulse-navy">{model.name}</h3>
                    <p className="text-sm text-gray-600">{model.algorithm}</p>
                    <p className="text-sm text-gray-500">Type: {model.type}</p>
                  </div>
                  <span className={`text-sm font-medium ${getStatusColor(model.status)}`}>
                    {model.status}
                  </span>
                </div>
                <div className="mt-2">
                  <p className="text-sm text-gray-600">
                    Weight: <span className="font-medium">{(model.weight * 100).toFixed(0)}%</span>
                    {model.brand_hashes !== undefined && (
                      <span className="ml-4">Brand hashes: {model.brand_hashes}</span>
                    )}
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Thresholds */}
      <div className="card">
        <h2 className="text-lg font-bold mb-4">Risk Thresholds</h2>
        <div className="grid grid-cols-4 gap-4">
          <div className="text-center p-4 bg-green-100 rounded-lg">
            <div className="text-2xl font-bold text-green-700">{modelInfo?.thresholds?.clean}</div>
            <div className="text-sm text-green-800">Clean</div>
          </div>
          <div className="text-center p-4 bg-yellow-100 rounded-lg">
            <div className="text-2xl font-bold text-yellow-700">{modelInfo?.thresholds?.suspicious}</div>
            <div className="text-sm text-yellow-800">Suspicious</div>
          </div>
          <div className="text-center p-4 bg-red-100 rounded-lg">
            <div className="text-2xl font-bold text-red-700">{modelInfo?.thresholds?.malicious}</div>
            <div className="text-sm text-red-800">Malicious</div>
          </div>
          <div className="text-center p-4 bg-red-200 rounded-lg">
            <div className="text-2xl font-bold text-red-900">{modelInfo?.thresholds?.critical}</div>
            <div className="text-sm text-red-900">Critical</div>
          </div>
        </div>
      </div>

      {/* General Settings */}
      <div className="card">
        <h2 className="text-lg font-bold mb-4">General Settings</h2>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              API URL
            </label>
            <input
              type="text"
              value={settings.apiUrl}
              onChange={(e) => setSettings({ ...settings, apiUrl: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-phishpulse-navy"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Minimum Risk Level for Alert
            </label>
            <input
              type="number"
              min="0"
              max="100"
              value={settings.minRiskLevel}
              onChange={(e) => setSettings({ ...settings, minRiskLevel: parseInt(e.target.value) })}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-phishpulse-navy"
            />
          </div>

          <div className="flex items-center">
            <input
              type="checkbox"
              id="autoScan"
              checked={settings.autoScan}
              onChange={(e) => setSettings({ ...settings, autoScan: e.target.checked })}
              className="w-4 h-4 text-phishpulse-navy border-gray-300 rounded focus:ring-phishpulse-navy"
            />
            <label htmlFor="autoScan" className="ml-2 text-sm text-gray-700">
              Enable automatic scanning
            </label>
          </div>

          <button
            onClick={handleSave}
            className="btn-primary"
          >
            Save Settings
          </button>

          {saved && (
            <p className="text-green-600 text-sm">Settings saved successfully!</p>
          )}
        </div>
      </div>
    </div>
  )
}

export default Settings
