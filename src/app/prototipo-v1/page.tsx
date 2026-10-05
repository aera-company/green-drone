import type { Metadata } from "next";
import { Hero } from "@/components/sections/Hero";

// Protótipo anterior ao master brief V2, preservado só para comparação.
export const metadata: Metadata = {
  title: "Protótipo v1 (arquivo)",
  robots: { index: false, follow: false },
};

export default function PrototipoV1() {
  return <main><Hero /></main>;
}
