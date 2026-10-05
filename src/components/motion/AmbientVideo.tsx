"use client";

import { useEffect, useRef } from "react";

/**
 * Vídeo de ambiente: mudo, em loop, sem controles. Só toca quando está na tela
 * e nunca toca com prefers-reduced-motion (fica o poster).
 */
type Props = { src: string; poster: string; label: string; className?: string };

export function AmbientVideo({ src, poster, label, className }: Props) {
  const ref = useRef<HTMLVideoElement | null>(null);

  useEffect(() => {
    const video = ref.current;
    if (!video) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const io = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) video.play().catch(() => {});
        else video.pause();
      },
      { threshold: 0.15 },
    );
    io.observe(video);
    return () => io.disconnect();
  }, []);

  return (
    <video
      ref={ref}
      className={className}
      src={src}
      poster={poster}
      muted
      loop
      playsInline
      preload="metadata"
      aria-label={label}
    />
  );
}
