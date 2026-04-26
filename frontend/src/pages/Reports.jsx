import { useState } from 'react'
import { useQuery } from 'react-query'
import { format } from 'date-fns'
import { reportAPI } from '../services/api'

function Reports() {
  const [page, setPage] = useState(0)
  const limit = 10

  const { data, isLoading } = useQuery(
    ['reports', page],
    () => reportAPI.listReports(page * limit, limit).then(res => res.data)
  )

  const handleDownload = async (scanId) => {
    try {
      const response = await reportAPI.downloadReport(scanId)
      const blob = new Blob([response.data], { type: 'application/pdf' })
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `phishpulse_report_${scanId}.pdf`
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
    } catch (error) {
      alert('Download failed: ' + error.message)
    }
  }

  const getScoreColor = (score) => {
    if (score <= 30) return 'text-green-600'
    if (score <= 60) return 'text-yellow-600'
    if (score <= 85) return 'text-red-600'
    return 'text-red-900 font-bold'
  }

  return (
    <div className="card">
      <h2 className="text-lg font-bold mb-4">Generated Reports</h2>
      
      {isLoading ? (
        <p className="text-gray-500">Loading...</p>
      ) : data?.reports?.length === 0 ? (
        <p className="text-gray-500">No reports generated yet.</p>
      ) : (
        <>
          <table className="w-full">
            <thead>
              <tr className="border-b">
                <th className="text-left py-3 px-2">Scan ID</th>
                <th className="text-left py-3 px-2">Created</th>
                <th className="text-left py-3 px-2">Actions</th>
              </tr>
            </thead>
            <tbody>
              {data?.reports?.map((report) => (
                <tr key={report.report_id} className="border-b hover:bg-gray-50">
                  <td className="py-3 px-2 font-mono text-sm">
                    {report.scan_id.substring(0, 8)}...
                  </td>
                  <td className="py-3 px-2">
                    {format(new Date(report.created_at), 'MMM d, yyyy HH:mm')}
                  </td>
                  <td className="py-3 px-2">
                    <button
                      onClick={() => handleDownload(report.scan_id)}
                      className="text-phishpulse-navy hover:underline text-sm"
                    >
                      Download PDF
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {/* Pagination */}
          <div className="flex justify-between items-center mt-4">
            <button
              onClick={() => setPage(p => Math.max(0, p - 1))}
              disabled={page === 0}
              className="btn-secondary disabled:opacity-50"
            >
              Previous
            </button>
            <span className="text-gray-600">Page {page + 1}</span>
            <button
              onClick={() => setPage(p => p + 1)}
              disabled={!data?.reports || data.reports.length < limit}
              className="btn-secondary disabled:opacity-50"
            >
              Next
            </button>
          </div>
        </>
      )}
    </div>
  )
}

export default Reports
