import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts'

function RiskGauge({ score, size = 200 }) {
  // Determine color based on score
  const getColor = () => {
    if (score <= 30) return '#28a745' // Safe - Green
    if (score <= 60) return '#ffc107' // Warning - Yellow
    if (score <= 85) return '#dc3545' // Danger - Red
    return '#721c24' // Critical - Dark Red
  }

  // Data for gauge
  const data = [
    { value: score },
    { value: 100 - score }
  ]

  const COLORS = [getColor(), '#e5e7eb']

  return (
    <div className="relative" style={{ width: size, height: size * 0.6 }}>
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="100%"
            startAngle={180}
            endAngle={0}
            innerRadius={size * 0.5}
            outerRadius={size * 0.6}
            paddingAngle={0}
            dataKey="value"
            stroke="none"
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index]} />
            ))}
          </Pie>
        </PieChart>
      </ResponsiveContainer>
      
      {/* Score Display */}
      <div 
        className="absolute inset-0 flex flex-col items-center justify-end pb-4"
        style={{ top: '40%' }}
      >
        <span 
          className="text-4xl font-bold"
          style={{ color: getColor() }}
        >
          {score}
        </span>
        <span className="text-sm text-gray-500">/ 100</span>
      </div>
    </div>
  )
}

export default RiskGauge
