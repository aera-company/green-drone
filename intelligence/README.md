# intelligence/

A **inteligência de criação de landing pages** deste projeto: prompts e instruções para uma
IA (Claude) dirigir e construir páginas sobre esta base (Next.js 16 + React 19 + Tailwind v4
+ Lenis + Framer Motion, com hero de frame-sequence dirigida por scroll).

É **referência**, não código. Nada aqui é importado pelo app; a pasta fica fora de `src/` e
não entra no build.

## Hierarquia de fontes

1. [`../CLAUDE.md`](../CLAUDE.md) manda nas **regras técnicas** (performance da hero, Lenis,
   a11y, onde mexer). Se algo aqui contradizer o CLAUDE.md, vale o CLAUDE.md.
2. Esta pasta manda no **processo criativo** (briefing, direção, copy, estrutura, QA).

## Como a IA deve usar isto

Ao receber um pedido de landing page neste repositório, o Claude deve:

1. Ler [`system-prompt.md`](system-prompt.md): persona e regras inegociáveis.
2. Coletar o briefing com [`brief-template.md`](brief-template.md).
3. Seguir o fluxo em [`pipeline.md`](pipeline.md): briefing, direção criativa, estrutura,
   hero, copy, build, QA.
4. Consultar `reference/` durante cada etapa.
5. Só entregar após passar por [`reference/quality-checklist.md`](reference/quality-checklist.md).

## Índice

| Arquivo | Para quê |
| ------- | -------- |
| [`system-prompt.md`](system-prompt.md) | Persona e princípios não negociáveis |
| [`pipeline.md`](pipeline.md) | Passo a passo do briefing à entrega |
| [`brief-template.md`](brief-template.md) | Questionário de intake de um novo pedido |
| [`reference/design-principles.md`](reference/design-principles.md) | Tipografia, cor, espaço, ritmo, movimento: o "gosto" |
| [`reference/section-anatomy.md`](reference/section-anatomy.md) | Catálogo de seções, quando usar e com qual componente da base |
| [`reference/hero-frames.md`](reference/hero-frames.md) | Como produzir, extrair e configurar a sequência da hero |
| [`reference/quality-checklist.md`](reference/quality-checklist.md) | Portão de qualidade antes do ship |

## Relação com a base de código

A base já entrega: hero de frame-sequence performática, smooth scroll Safari-safe,
componentes de UI reutilizáveis e acessibilidade/reduced-motion embutidos. O trabalho de
cada projeto é **trocar frames, copy e tema, e compor seções novas** sem quebrar essas
garantias.
