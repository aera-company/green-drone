# Reference · Princípios de design

O "gosto" aplicado. Use na Etapa 1 (direção criativa) e na Etapa 5 (build).

## Tipografia

- **Escala modular.** Display / H1 / H2 / corpo / legenda com salto perceptível
  (razão ~1.25–1.333). Contraste de tamanho cria hierarquia sem esforço.
- **Poucos pesos.** 2–3 pesos bastam (ex.: 400 corpo, 600 títulos, 700 display).
- **Medida de leitura.** Corpo entre 55–75 caracteres (`max-w-[55ch]`/`max-w-prose`).
  Títulos com `max-w-[18ch]` quebram melhor.
- **Altura de linha.** ~1.5 no corpo (`leading-relaxed`), apertada em displays
  (`leading-[1.05]`) com `tracking-tighter`.
- **Balanceamento.** `text-balance` em títulos, `text-pretty` em parágrafos.
- **Caixa.** Sentence case em títulos e frases de impacto. Caps só em marcas e em
  microlabels mono (eyebrow, HUD), com tracking ≤ 0.08em.
- **Fontes.** Sempre via `next/font` (self-host, sem layout shift). Sans para texto, mono
  para rótulos técnicos/HUD.

## Cor

- **Base neutra + 1 destaque.** Fundo, texto e neutros fazem 90% da página; `--accent`
  aparece pouco e por isso converte.
- **Contraste AA+.** Texto normal ≥ 4.5:1, grande ≥ 3:1. `--muted` sobre `--background` é
  o ponto mais frágil: teste.
- **Significado.** `--accent` = ação, links, foco, progresso. Não desperdice em decoração.
- **Texto sobre a hero.** A imagem muda a cada frame; a legibilidade vem da vinheta do
  `Hero.tsx` e dos cards glass, não da sorte. Teste o texto no frame mais claro da sequência.
- **Dark ou light com intenção.** Escuro premium pede neutros frios, grão e glow contido;
  claro pede sombras suaves, bastante respiração e revisão da vinheta/grão.

## Espaço e ritmo

- **Respiração é design.** Seções com `py-24 md:py-32` ou mais; margens generosas fazem a
  página parecer cara. Aperto faz parecer template.
- **Escala consistente.** Use a escala do Tailwind (múltiplos de 4px), não valores soltos.
- **Ritmo vertical.** A hero é densa em movimento; a seção seguinte deve respirar. Depois
  alterne: respirada → densa → respirada.
- **Container.** `mx-auto max-w-[1100px]` + `px-6 md:px-12` como padrão da base.

## Composição

- **Grid e alinhamento.** Tudo se alinha a um eixo.
- **Um foco por fold.** Um título, uma ação. O resto suporta.
- **Direção do olho.** Tamanho, cor e posição conduzem para o CTA.
- **Assinatura visual.** Um motivo recorrente dá unidade. A base traz grão (`.grain`),
  HUD (`HudFrame`, `.hud-tick`) e cards glass (`.card-surface`): use em diálogo com a hero.

## Movimento

- **A hero já é o espetáculo.** O resto da página pede movimento discreto: reveal
  escalonado (`AnimatedSection`), `ScrollRevealText` para uma frase-manifesto, hover curto.
- **Uma ideia de movimento por seção.** Nada de parallax + reveal + marquee no mesmo bloco.
- **Framer para orquestração, CSS para hover.** Transições simples ficam em Tailwind.
- **Nunca brigue com o Lenis.** Nada de `scroll-behavior: smooth` nem outra lib de scroll.
- **`prefers-reduced-motion` sempre.** Já embutido (CSS + `MotionConfig` + Lenis off);
  animação nova precisa continuar fazendo sentido com ela desligada.

## Responsividade

- **Mobile primeiro.** Desenhe o fold 1 para 360px e expanda.
- **Hero no mobile.** Scroll menor (300vh), crop central com zoom 1.3x e annotations
  empilhadas: confirme que o assunto e o texto continuam legíveis.
- **Tipografia fluida.** Breakpoints do Tailwind (`text-4xl md:text-6xl`) ou `clamp()`.
- **Toque.** Alvos ≥ 44px, espaçados.
