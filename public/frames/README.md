# Frames da hero

Coloque aqui a sequência de imagens que a hero percorre durante o scroll.

## Convenção de nomes

```
frame_0001.jpg
frame_0002.jpg
frame_0003.jpg
...
```

- Zero-padding de 4 dígitos (`0001`), numeração começando em **1**.
- Mesma extensão para todos. **WebP recomendado** (mais nítido e mais leve que
  JPG no mesmo peso); JPG também funciona. PNG só se precisar de alpha.
- Resolução sugerida: 1920×1080 (desktop).

## Extrair frames de um vídeo (sem ffmpeg no sistema)

Use o `ffmpeg-static` via npm — traz um binário estático, sem instalar nada
global:

```bash
npx --yes ffmpeg-static -hide_banner -i video.mp4 \
  -vf "fps=18,scale=1920:-2:flags=lanczos" \
  -c:v libwebp -f image2 -q:v 82 -compression_level 6 \
  public/frames/frame_%04d.webp
```

- `-f image2` é **essencial**: sem ele o encoder WebP gera um único arquivo
  animado em vez de uma sequência de frames.
- `fps=18` ≈ 120 frames para ~6,7s (ajuste ao seu vídeo).
- `scale=...:lanczos` faz upscale limpo se o fonte for menor que 1920.
- Para JPG: troque por `-qscale:v 4 public/frames/frame_%04d.jpg`.

Depois **ajuste `framePath` (extensão) e `FRAME_COUNT`** em `src/lib/hero.ts`.

## Ao trocar a sequência

Edite [`src/lib/hero.ts`](../../src/lib/hero.ts):

- `FRAME_COUNT` = quantidade exata de arquivos nesta pasta.
- `framePath` = ajuste o caminho/extensão se necessário.

## De onde vêm os frames

A sensação "3D" é uma sequência **pré-renderizada** (Blender / Cinema 4D /
After Effects) exportada como imagens — não é WebGL em runtime. Mire ~4s de
animação a 24–30fps (≈96–120 frames). Sem frames, a página roda normalmente,
mas o canvas fica em branco até você adicioná-los.
