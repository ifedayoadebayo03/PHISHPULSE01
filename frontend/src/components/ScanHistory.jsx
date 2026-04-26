import { format } from 'date-fns'

function ScanHistory({ scans }) {
  const getScoreColor = (score) => {
    if (score <= 30) return 'bg-green-100 text-green-800'
    if (score <= 60) return 'bg-yellow-100 text-yellow-800'
    if (score <= 85) return 'bg-red-100 text-red-800'
    return 'bg-red-200 text-red-900'
  }

  const truncate = (str, length) => {
    if (!str) return ''
    return str.length > length ? str.substring(0, length) + '...' : str
  }

  if (scans.length === 0) {
    return <p className="text-gray-500">No scans yet.</p>
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full">
        <thead>
          <tr className="border-b">
            <th className="text-left py-3 px-2">Time</th>
            <th className="text-left py-3 px-2">Type</th>
            <th className="text-left py-3 px-2">Target</th>
            <th className="text-left py-3 px-2">Score</th>
            <th className="text-left py-3 px-2">Classification</th>
          </tr>
        </thead>
        <tbody>
          {scans.map((scan) => (
            <tr key={scan.scan_id} className="border-b hover:bg-gray-50">
              <td className="py-3 px-2 text-sm text-gray-600">
                {format(new Date(scan.timestamp), 'MMM d, HH:mm')}
              </td>
              <td className="py-3 px-2">
                <span className="uppercase text-xs font-medium bg-gray-100 px-2 py-1 rounded">
                  {scan.scan_type}
                </span>
              </td>
              <td className="py-3 px-2 text-sm">
                {truncate(scan.target, 50)}
              </td>
              <td className="py-3 px-2">
                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getScoreColor(scan.final_score)}`}>
                  {scan.final_score}
                </span>
              </td>
              <td className="py-3 px-2">
                <span className={`text-sm font-medium ${
                  scan.classification === 'Clean' ? 'text-green-600' :
                  scan.classification === 'Suspicious' ? 'text-yellow-600' :
                  scan.classification === 'Malicious' ? 'text-red-600' :
                  'text-red-900'
                }`}>
                  {scan.classification}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default ScanHistory
