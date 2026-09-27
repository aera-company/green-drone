import type { ReactNode } from "react";

type Variant = "primary" | "outline" | "link";

type Props = {
  children: ReactNode;
  href?: string;
  variant?: Variant;
  className?: string;
};

/* CTA reutilizável, baseado nos tokens do tema (--accent/--foreground). */
export function Button({
  children,
  href = "#",
  variant = "primary",
  className = "",
}: Props) {
  const base =
    "inline-flex items-center justify-center gap-2 rounded-full text-sm font-medium tracking-tight transition-all duration-200 ease-out active:scale-[0.97]";

  const variants: Record<Variant, string> = {
    primary:
      "bg-accent text-background px-6 py-3 hover:-translate-y-0.5 hover:brightness-110",
    outline:
      "border border-foreground/25 text-foreground px-6 py-3 hover:-translate-y-0.5 hover:border-foreground hover:bg-foreground/5",
    link: "text-muted px-1 py-1 hover:text-accent underline-offset-4 hover:underline",
  };

  return (
    <a href={href} className={`${base} ${variants[variant]} ${className}`}>
      {children}
      {variant !== "link" && (
        <span aria-hidden className="text-[1.1em] leading-none">
          &rarr;
        </span>
      )}
    </a>
  );
}
