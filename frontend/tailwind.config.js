/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        sloth: {
          canvas: {
            light: '#FDFBF7',
            dark: '#181716',
          },
          card: {
            light: '#FFFFFF',
            dark: '#22201E',
          },
          border: {
            light: '#EBE5DC',
            dark: '#34302C',
          },
          sage: {
            50: '#F2F6F3',
            100: '#E1ECE3',
            500: '#4A6B53',
            600: '#3D5944',
            700: '#304736',
          },
          clay: {
            50: '#FAF5ED',
            100: '#F4E9D8',
            500: '#9C6528',
            600: '#835420',
          },
          charcoal: {
            800: '#2A2724',
            900: '#1C1A18',
          }
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        mono: ['ui-monospace', 'SFMono-Regular', 'Menlo', 'Monaco', 'Consolas', 'monospace'],
      }
    },
  },
  plugins: [],
}
