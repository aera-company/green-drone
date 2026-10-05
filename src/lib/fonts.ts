import { Inter, Space_Grotesk } from "next/font/google";

// Space Grotesk / Inter: referência de trabalho do brief (MERUS), a confirmar com a identidade oficial.
export const display = Space_Grotesk({ subsets: ["latin"], weight: ["500", "600"], variable: "--font-display" });
export const text = Inter({ subsets: ["latin"], weight: ["400", "500"], variable: "--font-text" });
