"use client";

import { useEffect, useRef, useState } from "react";

/* Vídeo de preenchimento (mudo, loop) com poster e cover-fit.
   Renderiza só a mídia (sem wrapper) — o card-pai controla tamanho e deve
   ser `relative overflow-hidden`. Toca no HOVER do card (sem autoplay):
   ao entrar o ponteiro dá play; ao sair, pausa e volta ao início.
   `prefers-reduced-motion` → só o poster. */
type Props = {
  src: string;
  poster: string;
  label: string;
  className?: string;
};

export function VideoMedia({ src, poster, label, className = "" }: Props) {
  const ref = useRef<HTMLVideoElement | null>(null);
  const [reduced, setReduced] = useState(false);

  useEffect(() => {
    setReduced(window.matchMedia("(prefers-reduced-motion: reduce)").matches);
  }, []);

  // Play no hover do card-pai (o overlay costuma cobrir o vídeo).
  useEffect(() => {
    const el = ref.current;
    if (!el || reduced) return;
    const host = el.parentElement;
    if (!host) return;
    const onEnter = () => el.play().catch(() => {});
    const onLeave = () => {
      el.pause();
      el.currentTime = 0;
    };
    host.addEventListener("pointerenter", onEnter);
    host.addEventListener("pointerleave", onLeave);
    return () => {
      host.removeEventListener("pointerenter", onEnter);
      host.removeEventListener("pointerleave", onLeave);
    };
  }, [reduced]);

  if (reduced) {
    return (
      // eslint-disable-next-line @next/next/no-img-element
      <img
        src={poster}
        alt={label}
        className={`absolute inset-0 h-full w-full object-cover ${className}`}
      />
    );
  }

  return (
    <video
      ref={ref}
      className={`absolute inset-0 h-full w-full object-cover ${className}`}
      poster={poster}
      muted
      loop
      playsInline
      preload="metadata"
      aria-label={label}
    >
      <source src={src} type="video/mp4" />
    </video>
  );
}
