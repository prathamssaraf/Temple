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
                bg: '#030303',
                surface: '#09090b',
                border: '#27272a',
                accent: '#10b981',
                // Shifted Gray Scale for brighter text/ui
                gray: {
                    200: '#e4e4e7', // was 200
                    300: '#d4d4d8', // was 300
                    400: '#d4d4d8', // was 300 (lighter) - used for secondary text
                    500: '#a1a1aa', // was 400 (lighter) - used for muted text
                    600: '#71717a', // was 500 (lighter) - used for borders/icons
                    700: '#52525b', // was 600
                    800: '#3f3f46', // was 700
                    900: '#27272a', // was 800
                }
            },
            fontFamily: {
                sans: ['Inter', 'sans-serif'],
                header: ['Outfit', 'sans-serif'],
            },
            boxShadow: {
                'glow': '0px 0px 40px -10px rgba(16, 185, 129, 0.1)',
            },
            animation: {
                'spin-slow': 'spin 3s linear infinite',
                'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                'slide-up': 'slideUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards',
            },
            keyframes: {
                slideUp: {
                    '0%': { opacity: '0', transform: 'translateY(1rem)' },
                    '100%': { opacity: '1', transform: 'translateY(0)' },
                }
            }
        },
    },
    plugins: [],
}
