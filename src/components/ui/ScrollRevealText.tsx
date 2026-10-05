"use client";

import { useEffect, useRef } from "react";

/* Texto que revela a cor conforme o scroll: cada palavra transita da cor
   `from` (padrão --muted) para `to` (padrão --foreground) à medida que o
   seu centro sobe pela viewport, cruzando uma faixa de foco. O progresso é
   aplicado via ref (sem re-render). `prefers-reduced-motion` → tudo em `to`.

   Uso: <ScrollRevealText body="..." /> ou com lead + align="center". */
type Props = {
  lead?: string;
  body: string;
  className?: string;
  align?: "left" | "center";
  from?: string; // ex.: "var(--muted)"
  to?: string; // ex.: "var(--foreground)"
};

export function ScrollRevealText({
  lead,
  body,
  className = "",
  align = "left",
  from = "var(--muted)",
  to = "var(--foreground)",
}: Props) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const wordRefs = useRef<(HTMLSpanElement | null)[]>([]);
  const ticking = useRef(false);

  const leadWords = lead ? lead.split(" ") : [];
  const bodyWords = body.split(" ");
  const wordCount = leadWords.length + bodyWords.length;

  useEffect(() => {
    const reduced = window.matchMedia(
      "(prefers-reduced-motion: reduce)",
    ).matches;
    const words = wordRefs.current.slice(0, wordCount);

    if (reduced) {
      words.forEach((w) => w && (w.style.color = to));
      return;
    }

    const onScroll = () => {
      if (ticking.current) return;
      ticking.current = true;
      requestAnimationFrame(() => {
        ticking.current = false;
        const vh = window.innerHeight;
        // Cada palavra revela conforme o SEU centro sobe pela viewport,
        // cruzando a faixa entre 82% e 48% da altura.
        const start = vh * 0.82;
        const end = vh * 0.48;
        const span = start - end;
        for (let i = 0; i < words.length; i++) {
          const w = words[i];
          if (!w) continue;
          const r = w.getBoundingClientRect();
          const centerY = r.top + r.height / 2;
          const lit = Math.min(1, Math.max(0, (start - centerY) / span));
          w.style.color = `color-mix(in srgb, ${to} ${Math.round(
            lit * 100,
          )}%, ${from})`;
        }
      });
    };

    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
    return () => window.removeEventListener("scroll", onScroll);
  }, [lead, body, align, from, to, wordCount]);

  let idx = 0;
  const renderWords = (words: string[]) =>
    words.map((word) => {
      const i = idx++;
      return (
        <span
          key={i}
          ref={(el) => {
            wordRefs.current[i] = el;
          }}
          style={{ color: from }}
        >
          {word}{" "}
        </span>
      );
    });

  const hasLead = leadWords.length > 0;
  const justify = align === "center" ? "text-pretty text-center" : "";

  return (
    <div ref={containerRef} className={className}>
      {hasLead && (
        <p className="font-sans text-3xl font-semibold leading-[1.1] tracking-tight md:text-5xl">
          {renderWords(leadWords)}
        </p>
      )}
      <p
        className={`font-sans text-xl leading-relaxed md:text-3xl md:leading-[1.5] ${
          hasLead ? "mt-7 max-w-[64ch]" : ""
        } ${justify}`}
      >
        {renderWords(bodyWords)}
      </p>
    </div>
  );
}
