"use client";

import { useEffect, useRef, type ReactNode } from "react";

/**
 * Seção dirigida pelo scroll. Escreve o progresso em `--p` (0–1) no próprio elemento;
 * o CSS decide o que fazer com ele (máscaras, deslocamentos, opacidades).
 *
 * - `pin`: progresso enquanto o palco sticky interno está preso (topo da seção no topo
 *   da janela → fundo da seção no fundo da janela).
 * - `through`: progresso enquanto a seção atravessa a janela (entra por baixo, sai por cima).
 *
 * Opcional: `steps` escreve `data-step` (0…n-1); `tone` fixa `data-tone` ou troca o valor
 * num ponto do progresso e avisa o cabeçalho (`gg:tone`).
 *
 * Mesmas regras da tomada: rAF + ticking, escrita direta no DOM, scroll passivo.
 */

type Tone = "light" | "dark";

type Props = {
  children: ReactNode;
  className?: string;
  id?: string;
  mode?: "pin" | "through";
  steps?: number;
  tone?: Tone | { from: Tone; to: Tone; at: number };
  header?: "clear" | "clear-wide";
  labelledBy?: string;
};

const clamp = (n: number) => Math.min(1, Math.max(0, n));

export function ScrollScene({ children, className, id, mode = "pin", steps, tone, header, labelledBy }: Props) {
  const ref = useRef<HTMLElement | null>(null);
  const toneFrom = typeof tone === "string" ? tone : tone?.from;
  const toneTo = typeof tone === "string" ? undefined : tone?.to;
  const toneAt = typeof tone === "string" ? undefined : tone?.at;

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    let ticking = false;

    const update = () => {
      ticking = false;
      const r = el.getBoundingClientRect();
      const vh = window.innerHeight;
      if (r.bottom < -vh || r.top > 2 * vh) return;
      // sem clamp: o tom pode trocar antes do palco prender (valores negativos)
      const raw =
        mode === "pin"
          ? -r.top / Math.max(1, r.height - vh)
          : (vh - r.top) / (vh + r.height);
      const p = clamp(raw);
      el.style.setProperty("--p", p.toFixed(4));
      if (steps) {
        const s = String(Math.min(steps - 1, Math.floor(p * steps)));
        if (el.dataset.step !== s) el.dataset.step = s;
      }
      if (toneFrom && toneTo && toneAt !== undefined) {
        const t = raw >= toneAt ? toneTo : toneFrom;
        if (el.dataset.tone !== t) {
          el.dataset.tone = t;
          window.dispatchEvent(new Event("gg:tone"));
        }
      }
    };

    const onScroll = () => {
      if (!ticking) {
        ticking = true;
        requestAnimationFrame(update);
      }
    };

    update();
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    return () => {
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", onScroll);
    };
  }, [mode, steps, toneFrom, toneTo, toneAt]);

  return (
    <section
      ref={ref}
      id={id}
      className={className}
      data-tone={toneFrom}
      data-step={steps ? "0" : undefined}
      data-header={header}
      aria-labelledby={labelledBy}
    >
      {children}
    </section>
  );
}
