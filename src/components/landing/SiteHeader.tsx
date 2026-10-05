"use client";

import Image from "next/image";
import { useEffect, useRef } from "react";

/**
 * Cabeçalho mínimo: assinatura Gávea Green + "Falar com a Gávea".
 * Troca entre versão clara e escura conforme o trecho que está sob ele:
 * qualquer elemento com data-tone="light|dark" (a tomada atualiza o próprio valor).
 * Sobre cenas de tela cheia (tomada, data-header="clear" ou "clear-wide" em paisagem) fica transparente.
 * Uma linha fina na base marca o progresso da página.
 */
export function SiteHeader() {
  const ref = useRef<HTMLElement | null>(null);
  const barRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const header = ref.current;
    if (!header) return;
    let ticking = false;
    const update = () => {
      ticking = false;
      const line = header.offsetHeight / 2;
      const mid = window.innerWidth / 2;
      // "clear-wide": cena de tela cheia só em paisagem (no retrato vira conteúdo corrido)
      const wide = !window.matchMedia("(max-aspect-ratio: 1/1), (prefers-reduced-motion: reduce)").matches;
      let tone = "light";
      let clear = false;
      document.querySelectorAll<HTMLElement>("[data-tone]:not(.gg-header)").forEach((el) => {
        const r = el.getBoundingClientRect();
        // também na horizontal: painéis de uma faixa lateral só contam quando estão no centro
        if (r.top <= line && r.bottom > line && r.left <= mid && r.right > mid) {
          tone = el.dataset.tone ?? tone;
          clear =
            clear ||
            el.classList.contains("mp-story") ||
            el.dataset.header === "clear" ||
            (el.dataset.header === "clear-wide" && wide);
        }
      });
      header.dataset.tone = tone;
      // sobre cenas de tela cheia o cabeçalho é transparente; fora delas, faixa sólida na cor do trecho
      header.dataset.solid = clear ? "false" : "true";
      const max = document.documentElement.scrollHeight - window.innerHeight;
      if (barRef.current) barRef.current.style.transform = `scaleX(${max > 0 ? Math.min(1, window.scrollY / max) : 0})`;
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
    window.addEventListener("gg:tone", update);
    return () => {
      window.removeEventListener("gg:tone", update);
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", onScroll);
    };
  }, []);

  return (
    <header ref={ref} className="gg-header" data-tone="light">
      <a href="#inicio" className="gg-brand" aria-label="Gávea Green, início">
        <Image className="gg-brand-color" src="/brand/gavea-green.png" alt="" width={720} height={374} priority />
        <Image className="gg-brand-white" src="/brand/gavea-green-branco.png" alt="" width={720} height={374} priority />
      </a>
      <a href="#contato" className="gg-header-cta">Falar com a Gávea</a>
      <div className="gg-progress" aria-hidden="true"><div ref={barRef} /></div>
    </header>
  );
}
