type MediaProps = {
  label?: string;
  className?: string;
  ratio?: string; // ex.: "16/9", "4/5"
};

/* Marcação de ESPAÇO DE IMAGEM/VÍDEO a inserir depois. Mantém o layout
   e deixa explícito o que falta de material. */
export function MediaPlaceholder({
  label = "Espaço para imagem",
  className = "",
  ratio,
}: MediaProps) {
  return (
    <div
      className={`placeholder-media flex items-center justify-center overflow-hidden rounded-xl ${className}`}
      style={ratio ? { aspectRatio: ratio } : undefined}
      role="img"
      aria-label={`${label} (placeholder)`}
    >
      <span className="px-4 text-center font-mono text-[11px] uppercase tracking-[0.24em] text-muted">
        {label}
      </span>
    </div>
  );
}

type LogoProps = { className?: string };

/* Marcação de ESPAÇO DE LOGO a inserir. */
export function LogoPlaceholder({ className = "" }: LogoProps) {
  return (
    <div
      className={`placeholder-media flex h-16 items-center justify-center rounded-lg ${className}`}
      role="img"
      aria-label="Logo (placeholder)"
    >
      <span className="font-mono text-[11px] uppercase tracking-[0.24em] text-muted">
        Logo
      </span>
    </div>
  );
}
