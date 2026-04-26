import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Scan API
export const scanAPI = {
  createScan: (type, target, options = {}) => 
    api.post('/scan/', { type, target, options }),
  
  getScan: (scanId) => 
    api.get(`/scan/${scanId}`),
  
  listScans: (skip = 0, limit = 100) => 
    api.get(`/scan/?skip=${skip}&limit=${limit}`)
}

// Report API
export const reportAPI = {
  downloadReport: (scanId) => 
    api.get(`/reports/download/${scanId}`, { responseType: 'blob' }),
  
  generateReport: (scanId) => 
    api.post(`/reports/generate/${scanId}`),
  
  listReports: (skip = 0, limit = 100) => 
    api.get(`/reports/?skip=${skip}&limit=${limit}`)
}

// Health API
export const healthAPI = {
  checkHealth: () => 
    api.get('/health/'),
  
  getDetailedHealth: () => 
    api.get('/health/detailed'),
  
  getStatistics: () => 
    api.get('/health/statistics'),
  
  getModelInfo: () => 
    api.get('/health/model-info')
}

export default api
