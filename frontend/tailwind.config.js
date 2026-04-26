/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'phishpulse': {
          navy: '#1e3a8a',
          amber: '#f59e0b',
          crimson: '#dc2626',
          safe: '#28a745',
          warning: '#ffc107',
          danger: '#dc3545',
        }
      }
    },
  },
  plugins: [],
}
