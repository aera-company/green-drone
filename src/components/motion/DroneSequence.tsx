"use client";

import Image from "next/image";
import { useEffect, useRef, type ReactNode } from "react";

/**
 * Tomada contínua do drone (REVEAL → APPROACH → TURN → ENTRY → DARK) percorrida pelo
 * scroll num <canvas>. Quadros renderizados em 3D: drone reconstruído com a foto do
 * PDF projetada; ambiente modelado (simulação visual).
 *
 * Regras de performance da base: rAF + ticking, escrita direta por ref, DPR ≤ 2,
 * scroll passivo. Carga progressiva: o primeiro quadro aparece logo; os demais entram
 * em segundo plano e o canvas desenha o mais próximo já carregado.
 *
 * `reveal` e `enter` são os blocos de texto (HTML acessível) dos dois capítulos que
 * acontecem dentro da tomada. A seção expõe `data-tone` (light/dark) para o cabeçalho.
 */

type Source = { count: number; path: (i: number) => string };

const pad = (n: number) => String(n).padStart(4, "0");

const DESKTOP: Source = { count: 160, path: (i) => `/motion-proof/desktop/f${pad(i)}.webp` };
const MOBILE: Source = { count: 100, path: (i) => `/motion-proof/mobile/f${pad(i)}.webp` };

// Fronteiras dos beats em progresso (0–1), coerentes com 3d/shot.py (160 quadros).
const BEATS = [
  { id: "reveal", label: "Reveal", at: 0 },
  { id: "approach", label: "Approach", at: 24 / 159 },
  { id: "turn", label: "Turn", at: 56 / 159 },
  { id: "entry", label: "Entry", at: 88 / 159 },
  { id: "dark", label: "Dark", at: 124 / 159 },
];
// a partir deste ponto o quadro fica escuro (câmera já na sombra da antepara)
const DARK_FROM = 116 / 159;

const clamp = (n: number) => Math.min(1, Math.max(0, n));
const ramp = (n: number, a: number, b: number) => clamp((n - a) / (b - a));

type Props = {
  reveal: ReactNode;
  enter: ReactNode;
  label: string;
  mobileFrames?: boolean;
};

export function DroneSequence({ reveal, enter, label, mobileFrames = true }: Props) {
  const sectionRef = useRef<HTMLElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const revealRef = useRef<HTMLDivElement | null>(null);
  const enterRef = useRef<HTMLDivElement | null>(null);
  const debugRef = useRef<HTMLDivElement | null>(null);
  const loadRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const section = sectionRef.current;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      if (section) section.dataset.tone = "light";
      return;
    }

    const canvas = canvasRef.current;
    if (!canvas || !section) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // retrato (celular ou tablet em pé) usa a tomada vertical própria
    const useMobile = mobileFrames && window.matchMedia("(max-aspect-ratio: 1/1)").matches;
    const src = useMobile ? MOBILE : DESKTOP;
    const imgs: (HTMLImageElement | null)[] = new Array(src.count).fill(null);
    const ready: boolean[] = new Array(src.count).fill(false);
    let loaded = 0;
    let current = -1;
    let ticking = false;
    let cancelled = false;
    const debug = new URLSearchParams(window.location.search).has("debug");
    if (debugRef.current) debugRef.current.hidden = !debug;

    const nearestReady = (i: number) => {
      if (ready[i]) return i;
      for (let d = 1; d < src.count; d++) {
        if (i - d >= 0 && ready[i - d]) return i - d;
        if (i + d < src.count && ready[i + d]) return i + d;
      }
      return -1;
    };

    const draw = (i: number) => {
      const k = nearestReady(i);
      const img = k >= 0 ? imgs[k] : null;
      if (!img) return;
      const cw = canvas.width;
      const ch = canvas.height;
      const ir = img.naturalWidth / img.naturalHeight;
      const cr = cw / ch;
      let w: number, h: number;
      if (cr > ir) { w = cw; h = cw / ir; } else { h = ch; w = ch * ir; }
      // Tela mais estreita que 16:9: no REVEAL o drone está à direita (âncora à direita);
      // depois da abertura ele vem para o centro, e a âncora migra junto.
      const t = i / (src.count - 1);
      const anchor = 1 - 0.5 * ramp(t, 0.12, 0.32);
      const x = cr < ir && !useMobile ? (cw - w) * anchor : (cw - w) / 2;
      const y = (ch - h) / 2;
      ctx.drawImage(img, x, y, w, h);
    };

    const resize = () => {
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = Math.round(canvas.clientWidth * dpr);
      canvas.height = Math.round(canvas.clientHeight * dpr);
      if (current >= 0) draw(current);
    };

    const fade = (el: HTMLElement | null, o: number, dy: number) => {
      if (!el) return;
      el.style.opacity = String(o);
      el.style.transform = `translate3d(0, ${dy}px, 0)`;
      el.style.visibility = o < 0.01 ? "hidden" : "visible";
      el.inert = o < 0.5;
    };

    const update = () => {
      ticking = false;
      const range = Math.max(1, section.offsetHeight - window.innerHeight);
      const p = clamp(-section.getBoundingClientRect().top / range);
      const i = Math.min(src.count - 1, Math.floor(p * (src.count - 1) + 0.5));
      if (i !== current) {
        current = i;
        draw(i);
      }
      const tone = p >= DARK_FROM ? "dark" : "light";
      if (section.dataset.tone !== tone) {
        section.dataset.tone = tone;
        window.dispatchEvent(new Event("gg:tone"));   // cabeçalho reavalia no mesmo quadro
      }
      // REVEAL some quando a câmera avança; o capítulo de acesso entra no escuro
      const o1 = 1 - ramp(p, 0.07, 0.15);
      fade(revealRef.current, o1, (1 - o1) * -24);
      const o2 = ramp(p, 0.8, 0.88);
      fade(enterRef.current, o2, (1 - o2) * 24);
      if (debug && debugRef.current) {
        const beat = [...BEATS].reverse().find((b) => p >= b.at);
        debugRef.current.textContent = `${beat?.label ?? ""} · quadro ${i + 1}/${src.count} · ${(p * 100).toFixed(1)}%`;
      }
    };

    const onScroll = () => {
      if (!ticking) {
        ticking = true;
        requestAnimationFrame(update);
      }
    };

    // carga: primeiro quadro na frente, depois pontos dos beats, depois o resto
    const order = [0, ...BEATS.map((b) => Math.round(b.at * (src.count - 1))), src.count - 1];
    for (let i = 0; i < src.count; i++) if (!order.includes(i)) order.push(i);
    order.forEach((i) => {
      const img = new window.Image();
      img.decoding = "async";
      img.src = src.path(i);
      img.onload = () => {
        if (cancelled) return;
        ready[i] = true;
        loaded++;
        if (loadRef.current) loadRef.current.style.transform = `scaleX(${loaded / src.count})`;
        if (loaded === src.count && loadRef.current) loadRef.current.style.opacity = "0";
        if (current < 0) current = 0;
        if (Math.abs(i - current) <= 2) draw(current);
      };
      imgs[i] = img;
    });

    resize();
    update();
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", resize);
    return () => {
      cancelled = true;
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", resize);
    };
  }, [mobileFrames]);

  return (
    <section ref={sectionRef} className="mp-story" data-tone="light" aria-label={label}>
      <div className="mp-stage">
        <canvas ref={canvasRef} className="mp-canvas" aria-hidden="true" />
        <div ref={revealRef} className="mp-copy mp-copy--reveal">{reveal}</div>
        <div ref={enterRef} className="mp-copy mp-copy--dark">{enter}</div>
        <div className="mp-load" aria-hidden="true"><div ref={loadRef} /></div>
        <div ref={debugRef} className="mp-debug" hidden />
      </div>

      {/* prefers-reduced-motion: sequência estática do mesmo material */}
      <div className="mp-still">
        <figure>
          <Image src="/motion-proof/still-reveal.webp" alt="Drone de inspeção com proteções nas hélices, sobre fundo claro" width={1280} height={720} sizes="100vw" />
        </figure>
        <figure>
          <Image src="/motion-proof/still-turn.webp" alt="O mesmo drone em giro, mostrando a lateral e o módulo de escova" width={1280} height={720} sizes="100vw" />
        </figure>
        <figure>
          <Image src="/motion-proof/still-dark.webp" alt="O drone dentro de um tanque escuro, com as lanternas acesas" width={1280} height={720} sizes="100vw" />
        </figure>
      </div>
    </section>
  );
}
