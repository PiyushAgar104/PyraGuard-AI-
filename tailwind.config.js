/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        fire: {
          50: '#fff1f2',
          100: '#ffe4e6',
          400: '#fb7185',
          500: '#f43f5e',
          600: '#e11d48',
          700: '#be123c',
          900: '#881337',
        },
        cyber: {
          bg: '#0a0d14',
          card: 'rgba(18, 24, 38, 0.75)',
          border: 'rgba(255, 75, 75, 0.2)',
          accent: '#ff3b3b',
          glow: 'rgba(255, 59, 59, 0.4)'
        }
      },
      animation: {
        'pulse-glow': 'pulseGlow 2s infinite',
        'flame-float': 'flameFloat 3s ease-in-out infinite',
      },
      keyframes: {
        pulseGlow: {
          '0%, 100%': { boxShadow: '0 0 15px rgba(255, 59, 59, 0.4)' },
          '50%': { boxShadow: '0 0 35px rgba(255, 59, 59, 0.9)' },
        },
        flameFloat: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-6px)' }
        }
      }
    },
  },
  plugins: [],
}
