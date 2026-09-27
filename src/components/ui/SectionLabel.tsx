type Props = { children: React.ReactNode; className?: string };

/* Rótulo de seção (eyebrow): traço curto + texto mono em caixa alta. */
export function SectionLabel({ children, className = "" }: Props) {
  return (
    <span
      className={`inline-flex items-center gap-3 font-mono text-[11px] uppercase tracking-[0.28em] text-muted ${className}`}
    >
      <span aria-hidden className="h-px w-7 bg-accent" />
      {children}
    </span>
  );
}
