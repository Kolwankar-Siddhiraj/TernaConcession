/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js}"],
  theme: {
    fontFamily: {
      sans: ['Poppins', 'sans-serif'],
    },
    extend: {
      colors: {
        accent: "#344DA0",
        textaccent: "#F3811F",
        secondary: '#edd342',
        dark: '#0C0E12',
        light: 'white',
        lightGray: '#a0a0a0',
        descriptive: '#737373',
        button_trans: 'rgba(150, 160, 193, 22%)',
      },
      fontFamily: {
        sans: ['Kanit', 'sans-serif']
      },
      backgroundImage: {
        'logo-white': "url('/src/assets/images/logo-white.svg')",
        'arrow': "url('/src/assets/images/arrow.png')",
        'hero': "url('/src/assets/images/hero.png')",
      },
    },
  },
  plugins: [],
}