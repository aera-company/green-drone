# Pipeline · do briefing à entrega

Fluxo padrão para criar uma landing page nesta base. Cada etapa tem um objetivo, um prompt
e um artefato de saída. Não pule etapas.

---

## Etapa 0 · Briefing

**Objetivo:** entender oferta, público, objetivo, restrições e o material visual da hero.
**Prompt:** preencha [`brief-template.md`](brief-template.md) com o cliente/usuário. Se faltar
algo essencial (oferta, público, ação desejada, fonte da hero), pergunte antes de seguir.
**Saída:** briefing preenchido.

---

## Etapa 1 · Direção criativa

**Objetivo:** definir a ideia antes do layout. Consulte
[`reference/design-principles.md`](reference/design-principles.md).

Defina e escreva:

- **Conceito / ângulo:** a ideia central e a promessa em uma frase.
- **Tom:** 3–5 adjetivos (ex.: confiante, técnico, caloroso).
- **Paleta:** `--background`, `--foreground`, `--muted`, `--accent` (+ `--accent-soft`,
  `--card-bg`, `--card-border`, `--hud-line`). Justifique o contraste.
- **Sistema tipográfico:** família(s) via `next/font`, escala (display, corpo, legenda), pesos.
  A base usa Geist + Geist Mono; troque se a marca pedir.
- **Motivo/assinatura:** o elemento recorrente (grão, HUD, glow, linha, card glass). A base
  traz grão e HUD; mantenha, troque ou desligue com intenção.
- **Plano da hero:** o que a sequência mostra, o arco (início, meio, fim) e onde entram os
  3 momentos de texto (principal, secundário, annotations).
- **Anatomia de folds:** a lista ordenada de seções (ver Etapa 2).

**Saída:** um bloco de "Direção Criativa" em markdown.

---

## Etapa 2 · Estrutura (anatomia de folds)

**Objetivo:** decidir a sequência de seções que conduz à conversão.
**Prompt:** monte a ordem com o catálogo em
[`reference/section-anatomy.md`](reference/section-anatomy.md). Toda página precisa de:
hero → prova/benefício → oferta/CTA. O resto é a serviço disso.
**Saída:** lista ordenada de seções com a função e o componente-base de cada uma.

---

## Etapa 3 · Hero (frames)

**Objetivo:** produzir e configurar a sequência. Guia completo em
[`reference/hero-frames.md`](reference/hero-frames.md).

1. Obter a fonte (render 3D, vídeo gerado ou filmado) e cortar trechos mortos.
2. Extrair frames em WebP para `public/frames/` (`frame_0001.webp`…).
3. Ajustar `FRAME_COUNT` e a extensão de `framePath` em `src/lib/hero.ts`.
4. Ajustar a duração pela altura de `.scroll-animation` em `globals.css`.
5. Posicionar `HERO_TEXT_FADE_END` e os `show`/`hide` das `ANNOTATIONS` nos momentos certos
   da sequência (conferir rolando, não no olho).

**Saída:** hero rodando com a sequência nova, peso total dos frames anotado.

---

## Etapa 4 · Copy

**Objetivo:** escrever o texto de cada seção e da hero.

Diretrizes:

- **Headline da hero:** benefício concreto, não slogan vago. Subhead explica o "como/para quem".
- **Texto secundário e annotations:** acompanham o arco da sequência; cada card diz uma
  coisa só (quote curta + rótulo + tag).
- **Voz:** segue o tom da direção. Frases curtas. Sem jargão vazio.
- **Prova:** específica (números, nomes, resultados), não adjetivo.
- **CTA:** verbo de ação + valor ("Agendar diagnóstico" > "Enviar").
- **Escaneável:** títulos, bullets, ênfase. Ninguém lê parágrafo gigante em LP.
- **Regras da casa:** sentence case em títulos, sem travessão em texto visível.

**Saída:** copy por seção, pronta para entrar no layout.

---

## Etapa 5 · Build

**Objetivo:** implementar a página mantendo as garantias do [`../CLAUDE.md`](../CLAUDE.md).

Onde mexer:

| O quê | Onde |
| ----- | ---- |
| Tema/cores | `:root` em `src/app/globals.css` |
| Fontes | `next/font` em `src/app/layout.tsx` + `--font-sans`/`--font-mono` no `@theme` |
| Title, description, OG | `metadata` em `src/app/layout.tsx` (definir `metadataBase` com o domínio) |
| Copy da hero | blocos comentados em `src/components/sections/Hero.tsx` |
| Frames, annotations | `src/lib/hero.ts` |
| Seções novas | `src/components/sections/<Nome>.tsx`, compostas em `src/app/page.tsx` |

Regras de implementação:

- **Uma seção por arquivo** em `src/components/sections/`. Estilo com Tailwind usando os
  tokens do tema (`bg-background`, `text-foreground`, `text-muted`, `text-accent`), nunca
  cores soltas.
- **Server component por padrão.** Só marque `"use client"` quando houver hook ou Framer.
  `AnimatedSection`/`AnimatedItem` já são client; uma seção que só os usa pode continuar
  server.
- **Reveal:** envolva o conteúdo em `<AnimatedSection>` e cada bloco em `<AnimatedItem>`.
- **Reuse `src/components/ui/`:** `Button`, `SectionLabel`, `MediaPlaceholder`/`LogoPlaceholder`,
  `VideoMedia`, `ScrollRevealText`, `EyebrowBadge`, `HudFrame`, `.card-surface`.
- **Imagens:** `next/image` com `width`/`height` (ou `fill` + container com proporção) e
  `sizes`. Frames da hero não passam por `next/image`; ficam em `public/frames/`.
- **Vídeo:** `VideoMedia` (play no hover, poster em reduced-motion). Card-pai
  `relative overflow-hidden`.
- **Âncoras/navegação:** com Lenis ativo, links `#id` funcionam; confira o offset se houver
  header fixo.
- Next 16 tem mudanças em relação a 14/15: em dúvida sobre rotas/metadata, consulte
  `node_modules/next/dist/docs/`.

**Saída:** página funcionando em `npm run dev`, `npm run build` e `npm run lint` limpos.

---

## Etapa 6 · QA (portão de qualidade)

**Objetivo:** garantir hero lisa, página leve, acessível e responsiva antes de entregar.
**Prompt:** rode todos os itens de
[`reference/quality-checklist.md`](reference/quality-checklist.md). Só entregue com tudo ✓.
**Saída:** checklist preenchido + confirmação de build.
