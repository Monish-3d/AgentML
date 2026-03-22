/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        retro: {
          bg: '#0f1318',
          card: '#181d25',
          border: '#2a3140',
          green: '#39ff14',
          amber: '#ffb000',
          cyan: '#00e5ff',
          red: '#ff4444',
          purple: '#bc8cff',
          text: '#c5d1de',
          muted: '#5a6a7a',
        }
      },
      fontFamily: {
        pixel: ['"Press Start 2P"', 'monospace'],
        mono: ['"Space Mono"', 'monospace'],
      },
    },
  },
  plugins: [],
}