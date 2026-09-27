# Reference · Anatomia de seções

Catálogo de seções de landing page. Use na Etapa 2 para montar a sequência. Nem toda página
usa todas: escolha o que serve à conversão. A espinha mínima é **Hero → Prova/Valor → CTA**.

## Essenciais

| Seção | Função | Notas | Base |
| ----- | ------ | ----- | ---- |
| **Hero** | Promessa em 5s + imersão | Headline de benefício, subhead, texto secundário no meio do scroll, annotations nos momentos-chave | `Hero.tsx` + `lib/hero.ts` (pronta) |
| **Prova social** | Reduzir risco | Depoimentos, logos, números, mídia. Específico > genérico | `LogoPlaceholder`, `.card-surface` |
| **Benefícios / Valor** | Traduzir features em ganhos | "O que você ganha", não "o que tem". Título + 1 linha | `SectionLabel` + `AnimatedItem` em grid |
| **Oferta / Pricing** | Tornar a decisão fácil | Preço claro, o que inclui, âncora, garantia, CTA repetido | `.card-surface` + `Button` |
| **CTA final** | Última chamada | Reforça promessa, remove fricção, ação | `Button` primary + outline |

## De apoio (use conforme a oferta)

| Seção | Quando usar | Base |
| ----- | ----------- | ---- |
| **Manifesto** | Logo após a hero, para ancorar o conceito numa frase | `ScrollRevealText` |
| **Como funciona** | Processo não óbvio, 3 a 4 passos | `AnimatedSection` + numeração mono |
| **Para quem é / não é** | Qualificar o público e aumentar identificação | duas colunas `.card-surface` |
| **Objeções / FAQ** | Dúvidas recorrentes que travam a compra | `<details>`/`<summary>` nativo (sem JS) |
| **Comparativo** | Mercado competitivo; diferencial lado a lado | tabela semântica |
| **Demonstração / Preview** | Produto visual (screens, vídeo, antes/depois) | `VideoMedia`, `MediaPlaceholder` |
| **Sobre / Autoridade** | A credibilidade de quem oferece é parte da venda | `next/image` + `SectionLabel` |
| **Garantia / Risco zero** | Diminuir o medo da decisão | `EyebrowBadge` + texto curto |
| **Bônus / Urgência** | Lançamentos com prazo ou estoque | `EyebrowBadge`, `HudFrame` |

## Regras de sequência

1. A hero entrega a promessa **antes de rolar** (texto principal no primeiro frame).
2. Logo depois da hero, uma seção que **respira** e ancora o conceito (manifesto ou valor).
3. Cada bloco de fricção (preço, formulário) vem **depois** de prova suficiente.
4. Repita o CTA a cada ~2–3 seções: quem decidir não deve precisar rolar de volta.
5. Termine sempre com uma ação clara, nunca em um parágrafo solto.

## No código

Cada seção = um componente em `src/components/sections/` (ex.: `Pricing.tsx`), composto em
`src/app/page.tsx` depois de `<Hero />`. Estrutura típica:

```tsx
<section id="oferta" className="px-6 py-24 md:px-12 md:py-32">
  <AnimatedSection className="mx-auto flex max-w-[1100px] flex-col gap-6">
    <AnimatedItem><SectionLabel>Oferta</SectionLabel></AnimatedItem>
    <AnimatedItem><h2 className="...">Título em sentence case.</h2></AnimatedItem>
    <AnimatedItem><Button href="#">Ação com valor</Button></AnimatedItem>
  </AnimatedSection>
</section>
```

A seção de exemplo que vem em `page.tsx` é descartável: substitua pela primeira seção real.
