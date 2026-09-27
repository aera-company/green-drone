# Reference · Frames da hero

Como transformar a fonte visual em sequência pronta. Use na Etapa 3. O passo a passo de
extração também está em [`../../public/frames/README.md`](../../public/frames/README.md).

## Modelo mental

Não é WebGL. É uma sequência de imagens pré-renderizadas que o `<canvas>` percorre conforme
o scroll: `.scroll-animation` (400vh desktop, 350vh tablet, 300vh mobile) cria a distância e
o wrapper `sticky top-0` fica fixo. Progresso 0→1 escolhe o frame, desenha com cover-fit e
liga/desliga os cards de annotation.

## Fonte

- **Melhor:** render 3D (Blender/C4D/AE) com câmera contínua e sem cortes. Movimento
  lento e constante lê melhor no scrub do que ação rápida.
- **Vídeo gerado ou filmado:** funciona, desde que seja um plano contínuo. Cortes secos
  viram "saltos" no scroll.
- **Corte trechos mortos** (pretos, fades, repetições) antes de extrair: cada frame inútil
  pesa no download e alonga o scroll sem conteúdo.
- **Enquadramento:** assunto centralizado. No mobile o canvas faz crop central com zoom 1.3x.

## Orçamento

| Parâmetro | Alvo |
| --------- | ---- |
| Quantidade | ~96–170 frames (mais que isso raramente compensa) |
| Resolução | 1920px de largura (desktop) |
| Formato | WebP, qualidade ~80 |
| Peso por frame | ~40–120 KB |
| Peso total | idealmente < 12 MB; acima de 20 MB, reduza fps ou qualidade |

Todos os frames são pré-carregados antes de animar: o peso total é o tempo de loading.

## Extração (sem ffmpeg global)

```bash
npx --yes ffmpeg-static -hide_banner -i video.mp4 \
  -vf "fps=18,scale=1920:-2:flags=lanczos" \
  -c:v libwebp -f image2 -q:v 82 -compression_level 6 \
  public/frames/frame_%04d.webp
```

- `-f image2` é essencial (sem ele sai um WebP animado único).
- Para cortar a fonte: `-ss 00:00:02 -to 00:00:09` antes do `-i`.
- Confira o total: `ls public/frames/*.webp | wc -l` e `du -sh public/frames`.

## Configuração em `src/lib/hero.ts`

- `FRAME_COUNT` = número exato de arquivos.
- `framePath` = ajuste a extensão (a base vem com `.jpg`; troque para `.webp`).
- `HERO_TEXT_FADE_END` = em que fração do scroll o texto principal some (padrão 0.08).
- `ANNOTATIONS` = cards com `show`/`hide` em fração do progresso. Posicione olhando a
  sequência: frame N aparece em `progresso ≈ (N - 1) / (FRAME_COUNT - 1)`. Lista vazia
  desliga os cards.

## Duração

A altura de `.scroll-animation` em `globals.css` define o ritmo. Poucos frames num scroll
longo = animação "engasgada"; muitos frames num scroll curto = rápida demais. Referência:
~40 frames por 100vh.

## Checagem

- Loading real (barra chega a 100%) e nenhum 404 de frame no console.
- Scrub liso de cima a baixo, sem saltos, no Chrome **e** no Safari.
- Texto legível no frame mais claro; assunto legível no mobile.
- Com `prefers-reduced-motion`, a página continua utilizável.
