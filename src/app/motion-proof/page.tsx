import type { Metadata } from "next";
import { DroneSequence } from "@/components/motion/DroneSequence";
import { display, text } from "@/lib/fonts";
import "@/styles/sequence.css";

export const metadata: Metadata = {
  title: "Motion proof · Gávea Green",
  robots: { index: false, follow: false },
};

export default function MotionProof() {
  return (
    <main className={`mp ${display.variable} ${text.variable}`}>
      <DroneSequence
        label="Drone de inspeção: aproximação e entrada em espaço confinado"
        reveal={
          <>
            <p className="mp-eyebrow">Drones para inspeção industrial</p>
            <h1 className="mp-title">O drone entra.<br />A evidência aparece.</h1>
            <p className="mp-support">
              Inspeção visual em espaços confinados, com imagens de alta resolução e acompanhamento da operação.
            </p>
          </>
        }
        enter={
          <>
            <p className="mp-eyebrow mp-eyebrow--dark">01 / Acesso</p>
            <h2 className="mp-title mp-title--dark">Acesse o que é difícil inspecionar.</h2>
          </>
        }
      />
      <section className="mp-after">
        <p>Fim do motion proof. Simulação visual: drone reconstruído a partir da foto do material da Gávea, ambiente modelado.</p>
      </section>
    </main>
  );
}
