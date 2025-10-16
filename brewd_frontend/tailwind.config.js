/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        // Retro Loewe Theme
        retro: {
          primary: "#3E5C4B",
          secondary: "#8C5E3C",
          accent: "#C2A14D",
          bg: "#F4E7D4",
          surface: "#FAF6F0",
          textPrimary: "#3B2E26",
          textSecondary: "#5B4E44",
          error: "#A44B3E",
        },
        // Mykonos Theme
        mykonos: {
          primary: "#1E64C8",
          secondary: "#D63384",
          accent: "#E5C07B",
          bg: "#F9F9F9",
          surface: "#FFFFFF",
          textPrimary: "#1A2942",
          textSecondary: "#555B66",
          error: "#E63946",
        },
      },
    },
  },
  plugins: [],
};


