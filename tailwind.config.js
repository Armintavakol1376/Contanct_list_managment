/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
      "./templates/*.html",
      "./static/*.js"
    ],
    theme: {
      extend: {
        colors: {
          'custom-green': '#008000',
          'custom-light-green': '#f0fff0',
        }
      },
    },
    plugins: [],
  }