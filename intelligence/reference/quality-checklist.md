# Reference · Portão de qualidade

Rode antes de entregar qualquer página. Só ship com tudo ✓. A hero de frame-sequence tem
custo de download por natureza; o objetivo é **hero lisa + resto da página leve**, não
Lighthouse 100 a qualquer preço.

## Build

- [ ] `npm run build` passa sem erros nem warnings relevantes (inclusive sem o aviso
      "inferred your workspace root": `turbopack.root` fixado em `next.config.ts`).
- [ ] `npm run lint` limpo.
- [ ] Nenhuma dependência adicionada sem necessidade real.

## Hero

- [ ] Regras de performance do `CLAUDE.md` intactas: rAF + `tickingRef`, canvas/opacidades
      via ref, state só para o conjunto de cards (diff por ids), DPR ≤ 2, scroll `passive`.
- [ ] `FRAME_COUNT` bate com os arquivos; extensão de `framePath` correta; zero 404.
- [ ] Frames em WebP ~1920px; peso total anotado (alvo < 12 MB).
- [ ] Barra de loading chega a 100% e a animação só começa depois.
- [ ] Scrub liso sem saltos em Chrome e Safari (desktop e iOS).
- [ ] Texto principal legível no primeiro frame; annotations nos momentos certos.
- [ ] Mobile: assunto e texto legíveis com o crop/zoom; annotations empilhadas ok.

## Performance (fora da hero)

- [ ] Seções sem `"use client"` desnecessário.
- [ ] Imagens via `next/image` com dimensões e `sizes` (sem CLS).
- [ ] Vídeos via `VideoMedia` (sem autoplay, com poster).
- [ ] Fontes via `next/font`; no máximo 2 famílias.

## Acessibilidade e motion

- [ ] HTML semântico: um `<h1>`, hierarquia de headings correta, landmarks (`main`, `footer`).
- [ ] Contraste AA+ em textos e botões (atenção a `--muted` e a texto sobre a hero).
- [ ] Imagens com `alt` significativo (ou `alt=""` se decorativas); canvas decorativo com
      `aria-hidden` ou texto equivalente.
- [ ] Navegável por teclado; foco visível (`:focus-visible` da base); ordem lógica.
- [ ] `prefers-reduced-motion`: Lenis desliga, reveals reduzem, página continua usável.
- [ ] Formulários com `<label>` associado.

## Copy

- [ ] Títulos em sentence case (caps só em marcas e microlabels mono).
- [ ] Nenhum travessão (—) em texto visível, incluindo `metadata`.
- [ ] Nenhum texto placeholder da base sobrando ("Legenda", "TAG 01", "Próxima seção"…).

## SEO e boas práticas

- [ ] `metadata` em `layout.tsx`: `title` e `description` do projeto.
- [ ] `metadataBase` com o domínio de produção (não `localhost`).
- [ ] Open Graph / Twitter card (título, descrição, imagem 1200×630).
- [ ] `lang` correto no `<html>`; favicon trocado; `public/robots.txt` coerente.
- [ ] Sem erros no console; links externos com `rel="noopener"`.

## Responsividade

- [ ] Testado de **360px a ultrawide** sem quebra nem scroll horizontal.
- [ ] Alvos de toque ≥ 44px.
- [ ] Âncoras de navegação caem no lugar certo com Lenis ativo.

## Conversão

- [ ] Promessa clara no fold 1 sem rolar.
- [ ] Uma ação primária por fold; CTA repetido ao longo da página.
- [ ] Prova antes de cada ponto de fricção.
- [ ] Página termina em uma ação, não em texto solto.
