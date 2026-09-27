# landing-base-3d

Base de landing page com **hero de frame-sequence dirigida por scroll** (Next.js
16 + React 19 + Tailwind v4 + Lenis + Framer Motion). Cada novo projeto parte
deste repo. A hero já está pronta; o trabalho é trocar frames, copy e adicionar
seções.

## Modelo mental da hero (não esquecer)

A sensação "3D" **não é WebGL**. É uma sequência de imagens pré-renderizadas que
um `<canvas>` percorre conforme o scroll. Seção externa alta (`400vh`) cria a
distância; wrapper interno `sticky top-0` fica fixo. O handler de scroll faz 4
coisas: calcula progresso (0→1), escolhe o frame, desenha com cover-fit, e
liga/desliga os cards de annotation.

## Regras de performance (NÃO COMPROMETER)

- `requestAnimationFrame` + `tickingRef` — 1 update por frame, nunca síncrono.
- Canvas e opacidades atualizam **direto via ref**, nunca via React state.
- React state só para o conjunto de cards visíveis, e só quando o conjunto muda
  (diff por string de ids ordenados).
- Pré-carregar todos os frames com barra de loading antes de animar.
- Canvas escalado por `devicePixelRatio` **limitado a 2** (retina sem custo excessivo).
- Listener de scroll `{ passive: true }`.
- Lenis com defaults Safari-safe (`lerp: 0.1`, `syncTouch: false`), **desligado em
  `prefers-reduced-motion`**.

## Componentes de UI reutilizáveis (`src/components/ui/`)

- `AnimatedSection` / `AnimatedItem` — reveal escalonado no scroll (Framer).
- `Button` — CTA (variants `primary`/`outline`/`link`), usa os tokens do tema.
- `SectionLabel` — eyebrow (traço + mono caixa alta).
- `Placeholder` — `MediaPlaceholder` / `LogoPlaceholder` (espaços marcados de mídia).
- `VideoMedia` — vídeo de preenchimento com **play no hover** (sem autoplay);
  poster-only em reduced-motion. O card-pai deve ser `relative overflow-hidden`.
- `ScrollRevealText` — texto que revela a cor (`--muted` → `--foreground`) conforme
  o scroll; cores e alinhamento configuráveis por props.
- `EyebrowBadge` / `HudFrame` — chips/cantos estilo HUD (decorativos).

## Acessibilidade / motion (já embutidos em `globals.css` + provider)

- Foco visível por teclado (`:focus-visible`), `touch-action: manipulation`.
- `prefers-reduced-motion`: corta transições/animações e o smooth-scroll do Lenis;
  `MotionConfig reducedMotion="user"` faz o Framer respeitar automaticamente.

## Onde mexer

- Frames → `public/frames/` (`frame_0001.webp`/`.jpg`…) + `FRAME_COUNT`/`framePath`
  em `src/lib/hero.ts`. Como extrair de um vídeo: ver `public/frames/README.md`.
- Copy/rótulos da hero → comentários em `src/components/sections/Hero.tsx`.
- Tema/cores → `:root` em `src/app/globals.css`.
- Duração da animação → altura de `.scroll-animation` em `globals.css`.
- Seções novas → `src/app/page.tsx` com `<AnimatedSection>`/`<AnimatedItem>`.

## Convenções Next.js / React

- Componentes com hooks ou Framer Motion precisam de `"use client"`.
- Alias de import: `@/` → `src/`.
- Next 16 tem mudanças em relação a 14/15 — confira `node_modules/next/dist/docs/`
  antes de escrever rotas/metadata se tiver dúvida.

## Processo criativo (`intelligence/`)

Ao criar uma landing nova a partir desta base, siga `intelligence/README.md`:
persona, briefing, pipeline (direção → estrutura → hero → copy → build → QA) e o
portão de qualidade em `intelligence/reference/quality-checklist.md`. Em conflito
técnico, vale este CLAUDE.md.

## Comandos

`npm run dev` (`:3000`) · `npm run build` · `npm start` · `npm run lint`.
