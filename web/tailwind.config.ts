import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        navy: {
          950: "#0a1224",
          900: "#0e1a2e",
          800: "#142239",
          700: "#1a2c47",
          600: "#22385a"
        },
        gold: {
          400: "#e0c074",
          500: "#d4a853",
          600: "#bf922f",
          700: "#9a7424"
        }
      },
      fontFamily: {
        display: ['"Playfair Display"', "serif"],
        sans: ['"Inter"', "system-ui", "sans-serif"]
      }
    }
  },
  plugins: []
};

export default config;
