import { Routes, Route, NavLink } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import Reports from './pages/Reports'
import Settings from './pages/Settings'

function App() {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="bg-phishpulse-navy text-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 bg-white rounded-full flex items-center justify-center">
                <span className="text-phishpulse-navy font-bold">P</span>
              </div>
              <h1 className="text-xl font-bold">PhishPulse</h1>
              <span className="text-sm opacity-70">v2.0</span>
            </div>
            <nav className="flex gap-4">
              <NavLink 
                to="/" 
                className={({ isActive }) => 
                  `px-3 py-2 rounded-md transition-colors ${
                    isActive ? 'bg-blue-800' : 'hover:bg-blue-800'
                  }`
                }
              >
                Dashboard
              </NavLink>
              <NavLink 
                to="/reports" 
                className={({ isActive }) => 
                  `px-3 py-2 rounded-md transition-colors ${
                    isActive ? 'bg-blue-800' : 'hover:bg-blue-800'
                  }`
                }
              >
                Reports
              </NavLink>
              <NavLink 
                to="/settings" 
                className={({ isActive }) => 
                  `px-3 py-2 rounded-md transition-colors ${
                    isActive ? 'bg-blue-800' : 'hover:bg-blue-800'
                  }`
                }
              >
                Settings
              </NavLink>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/reports" element={<Reports />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-4">
        <div className="max-w-7xl mx-auto px-4 text-center text-sm">
          PhishPulse v2.0 | PhantomSecDy Research Initiative | Detect the Undetectable
        </div>
      </footer>
    </div>
  )
}

export default App
