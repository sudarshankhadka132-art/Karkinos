import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}'
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#ff6b35',
          50: '#fff5f0',
          100: '#ffe8db',
          200: '#ffd0b7',
          300: '#ffb089',
          400: '#ff8b57',
          500: '#ff6b35',
          600: '#f15a23',
          700: '#d7441a',
          800: '#aa3418',
          900: '#872c16'
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif']
      },
      spacing: {
        '18': '4.5rem'
      }
    }
  },
  plugins: []
};

export default config;
