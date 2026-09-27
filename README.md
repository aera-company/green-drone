# landing-base-3d

Base para landing pages com **hero de frame-sequence dirigida por scroll** — uma
sequência de imagens pré-renderizadas que um `<canvas>` percorre conforme a
rolagem (a técnica das homepages premium, estilo Apple AirPods / agências).

Cada novo projeto parte deste repositório. A hero já vem montada; você troca os
frames, ajusta a copy e constrói as seções seguintes.

## Stack

- **Next.js 16** (App Router) + **React 19**
- **Tailwind CSS v4** (`@import "tailwindcss"`, tokens em `@theme inline`)
- **Lenis** — scroll suave (configuração Safari-safe)
- **Framer Motion** — reveals de seções pós-hero
- **Geist** — fontes sans + mono

## Comandos

| Comando           | Ação                                   |
| ----------------- | -------------------------------------- |
| `npm install`     | Instala as dependências                |
| `npm run dev`     | Servidor de desenvolvimento (`:3000`)  |
| `npm run build`   | Build de produção                      |
| `npm start`       | Sobe o build de produção               |
| `npm run lint`    | ESLint                                 |

## Estrutura

```
src/
├── app/
│   ├── layout.tsx          # fontes, metadata (SEO), SmoothScrollProvider
│   ├── page.tsx            # compõe as seções (Hero + exemplo)
│   └── globals.css         # design tokens + classes utilitárias
├── components/
│   ├── sections/Hero.tsx   # ⭐ motor de frame-sequence (o coração da base)
│   ├── ui/                 # EyebrowBadge, HudFrame, AnimatedSection
│   └── providers/          # SmoothScrollProvider (Lenis)
└── lib/hero.ts             # FRAME_COUNT, caminho dos frames, annotations
public/
├── frames/                 # ⬅️ coloque sua sequência aqui (ver frames/README.md)
├── favicon.svg
└── robots.txt
```

## Como customizar (passo a passo)

1. **Frames** — exporte sua animação como imagens em `public/frames/`
   (`frame_0001.jpg`…). Veja [`public/frames/README.md`](public/frames/README.md).
2. **Config da hero** — em [`src/lib/hero.ts`](src/lib/hero.ts), ajuste
   `FRAME_COUNT` e edite/remova os cards em `ANNOTATIONS`.
3. **Copy da hero** — títulos e rótulos estão marcados com comentários em
   [`src/components/sections/Hero.tsx`](src/components/sections/Hero.tsx).
4. **Tema** — troque as cores em `:root` no topo de
   [`src/app/globals.css`](src/app/globals.css) (`--accent`, `--background`…).
5. **Duração da animação** — a altura de `.scroll-animation` (400vh) define a
   distância de scroll; mais alto = animação mais lenta.
6. **Seções seguintes** — adicione em `page.tsx` usando `<AnimatedSection>` /
   `<AnimatedItem>` e a superfície `.card-surface`.

## Como a hero funciona

Seção externa de `400vh` cria a distância de scroll; o wrapper interno fica
`sticky top-0`. A cada frame de scroll: calcula-se o progresso (0→1), escolhe-se
o frame correspondente e desenha-se no canvas com *cover-fit*. Tudo via
`requestAnimationFrame`, canvas com `devicePixelRatio` (nítido em retina),
pré-carregamento de todos os frames com barra de loading e listener passivo.

## Deploy

Conectar o repositório no [Vercel](https://vercel.com/new) — detecção automática
do Next.js. Cada push publica.
