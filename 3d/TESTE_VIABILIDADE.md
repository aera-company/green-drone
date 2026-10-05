# Teste de viabilidade · modelo 3D do drone

**Data:** 02/10/2026 · **Status do modelo:** `MOTION_SIMULATION` · `REQUIRES_GAVEA_VALIDATION`
**Folha comparativa:** `docs/pass00/teste-modelo-3d.jpg`

## O que foi feito

- Blender 5.2.2 instalado (Homebrew). Cycles roda na GPU do M1 (Metal).
- Modelo paramétrico escrito em Python (`3d/drone_model.py`), sem malha importada nem IA.
- **Câmera do master recuperada** a partir de pontos físicos da foto (cubos e parafusos das proteções) e refinada por silhueta: 28 mm equivalente, 43° de elevação, azimute 138°. `3d/renders/camera_refined.json`.
- Proporções medidas por projeção inversa: espaçamento das proteções, altura do corpo, posição do LiDAR, alcance da ferramenta.

## Como rodar

```bash
cd "/Users/tiagolima/Desktop/GAVEA TECH/new-3d-landbase/3d"
blender -b --factory-startup --python render_tests.py -- master 160
blender -b --factory-startup --python render_tests.py -- turn 160
blender -b --factory-startup --python render_tests.py -- dark 200
```

Cada render leva de 10 a 45 s em 1000×667.

## Resultado

| Teste | Veredito | Por quê |
|---|---|---|
| A/B · mesma pose do master | **Proporção ok, acabamento não** | A silhueta cai sobre a foto (C). Lado a lado, o render parece um esboço limpo: falta a densidade de detalhe da foto (feixe de cabos, mecanismo da ferramenta, recortes dos gussets, trama de carbono, parafusos, LiDAR) |
| D · giro de 35° | **Funciona como movimento** | É o mesmo objeto por construção. Sem deformação, sem cartão. Inclinação de curva crível. Herda a falta de detalhe de B |
| E · escuro com lanternas | **O mais convincente** | Luz e névoa escondem a falta de detalhe. Lê como drone real dentro de um tanque. Linguagem ZRK possível |

## O que é inventado

- Lado direito, traseira e parte de baixo: nenhuma foto confirmada mostra.
- Varetas inferiores, encaixe do selim, mecanismo interno da ferramenta.
- Escala absoluta: proteção de 30 cm é suposição.

O perfil (`p03_robo_em_tubulacao`) pode servir de conferência, se a Gávea confirmar que é o mesmo modelo.

## Próximos passos possíveis

1. **Passe de detalhe:** cabos, ferramenta, selim, recortes, materiais. Melhora B e D. Teto: CG bom, com detalhes finos ainda inferidos.
2. **Projeção da foto real sobre o modelo:** como a câmera do master foi recuperada, os pixels da foto podem ser projetados sobre a geometria. Do REVEAL até ~20–25° de giro, o espectador vê a foto real com volume; o material procedural só aparece nas faces que a foto não mostra. Técnica clássica de VFX, usa pixels reais e não inventa superfície visível.
3. **DARK com o modelo atual:** já serve para o capítulo escuro.


---

## Rodada 2 · projeção da foto + passe de detalhe (03/10/2026)

**Arquivos:** `docs/pass00/teste-projecao-v2.jpg` (foto, 0°, 12°, 20°, 35°, escuro) e `docs/pass00/teste-giro-projecao.mp4` (giro 0→35° e volta).

### Projeção (`3d/projection.py`)
- A foto é projetada da câmera recuperada, presa ao drone: os pixels giram junto com o objeto.
- Mapa de profundidade do ponto de vista da foto decide o que ela realmente enxerga; o resto usa o material do modelo.
- Máscara de ângulo (faces vistas de lado pela foto não recebem pixels esticados) e corte da franja semitransparente do recorte.
- No escuro a foto entra como **cor do material** (não emissão), então responde às lanternas e à névoa.
- **Descartado:** a "casca de resíduo" que segurava o que o modelo não tinha. Ao sumir com o giro ela gerava imagens fantasmas, que é crossfade. A regra passou a ser: tudo o que a foto mostra precisa existir como peça.

### Passe de detalhe guiado pela foto
- Mapa "foto tem, modelo não" (`3d/unmodeled.py`) usado como lista de trabalho: de 38% para 26% dos pixels do drone sem geometria.
- Ajuste de cada proteção por IoU numa região, com o modelo inteiro presente (o critério anterior "escondia" anéis no corpo).
- Raios também no anel inferior de cada gaiola (vistos através da gaiola na foto).
- Ferramenta remontada com medidas da foto: o módulo da escova fica **alto** (z ~ +0,25 D), o que a foto de perfil confirma.
- Gaiola do LiDAR: um octógono grande no plano lateral do lado da câmera. O espelho do outro lado foi removido porque a foto o mostraria.
- Tubo azul extraído da foto por cor e levado a 3D pelo mapa de profundidade.
- Luzes vermelhas e pás das hélices na posição/ângulo medidos.

### Veredito da rodada
| Faixa | Resultado |
|---|---|
| 0° | Muito próximo da foto (pixels reais) |
| 12° a 35° | Mesmo objeto girando, textura real, sem fantasma nem mancha. Mais limpo que a foto: faltam cabos pretos finos e miudezas |
| Escuro | Silhueta e lanternas convincentes; drone pequeno e escuro demais no quadro, ajuste de direção de fotografia fica para o PASS 01 |

### O que ainda falta / é inferido
- 26% dos pixels sem geometria: feixe de cabos pretos, conectores, parte do selim e das sondas.
- Lado direito, traseira e fundo continuam inferidos. Escala (30 cm por proteção) é suposição.
- Ângulo das hélices FR/BR arbitrário (não aparecem na foto).
