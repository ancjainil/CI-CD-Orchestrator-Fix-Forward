import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        border: "hsl(215 16% 27%)",
        input: "hsl(216 34% 17%)",
        ring: "hsl(199 100% 50%)",
        background: "#060a12",
        foreground: "#e5e7eb",
        muted: {
          DEFAULT: "#6b7280",
          foreground: "#9ca3af",
        },
        card: {
          DEFAULT: "#0b1220",
          foreground: "#e5e7eb",
        },
        accent: {
          DEFAULT: "#0ea5e9",
          foreground: "#0b1220",
        },
        success: "#22c55e",
        warning: "#f59e0b",
        danger: "#ef4444",
      },
      borderRadius: {
        lg: "12px",
        md: "10px",
        sm: "8px",
      },
      boxShadow: {
        card: "0 20px 60px rgba(0,0,0,0.35)",
      },
    },
  },
  plugins: [],
};

export default config;
