/* ============================================================
   CONFIGURAÇÃO DA HERO (frame-sequence)
   Ajuste estes valores ao trocar a sequência de imagens.
   ============================================================ */

// Quantos frames a sua animação tem (= nº de arquivos em /public/frames).
export const FRAME_COUNT = 169;

// Caminho de cada frame. Padrão: /public/frames/frame_0001.jpg ...
// Mantenha o zero-padding (0001) e a extensão consistentes.
export const framePath = (n: number) =>
  `/frames/frame_${String(n).padStart(4, "0")}.jpg`;

// Em que ponto (0–1 do scroll) o texto principal da hero termina de sumir.
export const HERO_TEXT_FADE_END = 0.08;

/* ------------------------------------------------------------
   ANNOTATIONS — cards que aparecem/somem em pontos do scroll.
   `show`/`hide` são frações do progresso (0 = topo, 1 = fim).
   Edite/remova livremente. Deixe a lista vazia para não usar.
   ------------------------------------------------------------ */
export type Annotation = {
  id: string;
  show: number;
  hide: number;
  quote: string;
  speaker: string;
  film: string; // rótulo curto à direita (ex.: categoria, ano, tag)
};

export const ANNOTATIONS: Annotation[] = [
  {
    id: "a1",
    show: 0.1,
    hide: 0.3,
    quote: "Sua primeira mensagem-chave aparece aqui.",
    speaker: "Legenda",
    film: "TAG 01",
  },
  {
    id: "a2",
    show: 0.35,
    hide: 0.55,
    quote: "Um segundo ponto, revelado conforme a rolagem avança.",
    speaker: "Legenda",
    film: "TAG 02",
  },
  {
    id: "a3",
    show: 0.6,
    hide: 0.8,
    quote: "E o argumento final, perto do fim da animação.",
    speaker: "Legenda",
    film: "TAG 03",
  },
];
