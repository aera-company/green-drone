# PASS 03 · Conteúdo do PDF e evidências

**Data:** 04/10/2026 · **Rota:** `/` (local) · **Status:** aguardando avaliação

Pedido: a hero ficou boa; as outras seções estavam fracas (pouca informação, poucas fotos, pouca experiência). Entraram o conteúdo e as fotos da `Apresentacao Gavea Green Tech.pdf` (pp. 2 a 8), com cenas dirigidas por scroll.

## Estrutura nova

| Trecho | Tom | O que acontece | Conteúdo (fonte no PDF) |
|---|---|---|---|
| Tomada (hero + 01 Acesso) | claro → escuro | sem mudança | |
| Abertura | escuro | a foto do drone no poço nasce como uma fresta (eco da abertura da tomada) e abre para tela cheia | "Sem entrada humana." + ambientes sem GPS, baixa iluminação, obstáculos (p. 3) |
| Onde atua | escuro | os cinco ambientes acendem um a um ao passar pelo meio da tela | tanques, silos, chaminés, galerias, caldeiras (p. 3) |
| Como trabalha lá dentro | escuro | fotos em túnel e na parede; lista fixa ao lado | anticolisão, iluminação embarcada, tempo de voo ilimitado (p. 3); 6 serviços em espaço confinado (p. 4) |
| 02 Registro | a luz acende | cena presa em 4 passos; cada passo troca a tela com uma máscara lateral | capturar (4K), acompanhar ao vivo (live feed), revisar em 3D (trajetória, pontos de interesse, UTM), guardar e compartilhar (nuvem) (p. 3) |
| 03 Aplicações | claro → escuro | faixa horizontal: do céu para debaixo d'água | em altura e áreas externas + 6 serviços (p. 5); mini-ROV + 6 serviços (p. 6) |
| 04 Resultado | escuro | foto da equipe em campo com paralaxe | "Inspeções mais seguras, inteligentes e eficientes", 8 benefícios (p. 7); quem é a Gávea Green, setores (p. 2) |
| 05 Próximo passo | claro | o drone volta à luz | o que contar (ativo, acesso, registro), CTAs, André Barbosa, telefone, e-mail (p. 8) |

Cabeçalho: ganhou uma linha fina de progresso; fica transparente sobre as cenas de tela cheia e escolhe o tom pelo painel que está no centro da faixa horizontal.

## Medições

| | Desktop 1440×900 | Mobile 375×812 |
|---|---|---|
| Altura total | **17,0 telas** (antes 6,8) | **18,9 telas** (antes 6,2) |

Passa bem do alvo de 5–7 telas do brief, por decisão do pedido (mais informação). Boa parte é cena presa (tomada, abertura, registro, faixa), que anda rápido no scroll. Se ficar longo, os primeiros cortes candidatos: "Como trabalha lá dentro" ou a faixa de aplicações.

## Mídia nova em `public/media/` (cópias idênticas, hash conferido com `catalogo.csv`)

| Arquivo | Origem | Classificação |
|---|---|---|
| `acesso-poco.jpg` | `p02_drone_em_espaco_confinado_x56` | `ORIGINAL_PDF` · origem (foto ou composição) `REQUIRES_GAVEA_VALIDATION` |
| `acesso-iluminacao.jpg` | `p04_drone_com_iluminacao_x138` | `ORIGINAL_PDF` |
| `acesso-tunel.jpg` | `p02_robo_em_tunel_x50` | `ORIGINAL_PDF` |
| `registro-tablet.jpg` | `p03_tela_de_inspecao_x92` | `ORIGINAL_PDF` · pixels intocados |
| `altura-duto.jpg` | `p05_drone_em_duto_x168` | `ORIGINAL_PDF` |
| `altura-chamine.jpg` | `p07_drone_em_estrutura_x201` | `ORIGINAL_PDF` |
| `altura-flare.jpg` | `p05_termografia_de_flare_x165` | `ORIGINAL_PDF` |
| `rov-amarelo.jpg` | `p06_rov_amarelo_fundo_preto_x182` | `ORIGINAL_PDF` |
| `rov-preto.png` | `p06_rov_preto_recortado_x179` (JPEG + máscara do próprio PDF) | `TREATED_ORIGINAL` · fora da página desde 05/10 |
| `equipe-campo.jpg` | `p07_trabalhador_em_inspecao_x200` | `ORIGINAL_PDF` |

Continuam fora, como pede o brief: `p05_drone_em_voo_x166` e `p07_drone_em_gaiola_x204`. Nenhuma foto de outro equipamento foi usada como ângulo do drone protagonista: as fotos de altura e de ROV aparecem só na seção de outras aplicações, com legenda própria.

Apresentação sem tocar nos pixels: telas em `object-fit: contain` (nada cortado); ROVs com `mix-blend-mode: lighten` para o fundo preto da foto sumir no fundo da página.

## Copy

Todo texto vem do PDF, resumido. Ajustes por regra do brief:
- "Zero exposição ao risco" virou "Equipe fora do ambiente de risco" (o brief veta "zero risco").
- "Dados precisos de máxima confiabilidade" ficou fora; o parágrafo institucional fala em expertise técnica e acesso de alto risco.
- Caixa alta do PDF em sentence case.

## Validações (retorno da Gávea em 05/10)

| Item | Situação |
|---|---|
| Direito de uso das fotos | **Ok** |
| Capacidades por equipamento, serviços, benefícios | **Pode manter assim** |
| Gávea Group / gavea-group.com no rodapé | **Ok** |
| Contato | **Só André Barbosa + andre.barbosa@gaveagroup.com.** Telefone e WhatsApp saíram; o CTA "Falar sobre meu projeto" abre o e-mail |

## Vídeo do mini-ROV (05/10)

A frente subaquática estava simples perto do drone. Com autorização do Tiago, a foto `rov-amarelo.jpg` foi enviada ao Magnific:
1. Quadro-chave (Nano Banana Pro, foto do ROV como referência): ROV com as luzes acesas inspecionando o casco submerso de um navio. Conferido contra a foto: painel amarelo, frente preta, duas luzes, barra de sensores e propulsores com aro batem; a lente central entre as luzes não aparece.
2. Vídeo de 8 s em 1080p (Seedance 2.5) a partir desse quadro.

Na página: o filme ocupa a coluna e abre com máscara quando a faixa chega; a foto real do ROV entra embaixo como "o equipamento". Legenda: "Simulação visual a partir da foto do equipamento". Mudo, em loop, só toca na tela, poster fixo em movimento reduzido.

Classificação: `rov-casco.mp4` / `rov-casco.webp` = `MOTION_SIMULATION` (gerado por IA). Nunca legendar como operação real.

## Pendente

- Movimento reduzido: implementado (sem pins, tudo empilhado) e ainda não testado com a preferência ligada.
- Safari e tablet: PASS 06.
- A ligação "módulo óptico → captura" entre a tomada e o registro continua sendo um corte de cena, não um movimento contínuo.

## Rodada 05/10 (tarde): em altura, segunda abertura, detalhe do ROV

- **03 Em altura:** a colagem virou faixas que grudam e se empilham (referência price-pierce.co.uk, seção "Discover our Difference"). Foto grande à esquerda com o título, coluna branca à direita com o texto e os serviços. Os seis serviços da p. 5 agrupados pela foto: dutos e tubulações (espessura), torres, chaminés e estruturas (RVI, aerofotogrametria, LiDAR), flares (termografia aérea, gases). Cada faixa fica inteira por 40svh antes da próxima subir.
- **04 Subaquático, segunda abertura:** cena presa. O drone (foto original) está no claro com "No ar e em espaços confinados, o drone."; a água sobe de baixo (o filme do ROV entra por máscara, com uma linha d'água), o drone sobe e sai, e fica "Debaixo d'água, o mini-ROV." sobre o vídeo em tela cheia.
- **Detalhe do ROV:** o equipamento recortado (fundo removido no Magnific a partir da foto do PDF) fica fixo à esquerda; à direita, onde atua (lista que acende) e os seis serviços; embaixo, três cenas geradas: amarras, estacas de píer, reservatórios e tubulações.
- **06 Próximo passo:** drone e mini-ROV juntos, os dois a partir das fotos do PDF.
- Numeração: 01 Acesso, 02 Registro, 03 Em altura, 04 Subaquático, 05 Resultado, 06 Próximo passo.
- Altura: cerca de 23 telas no desktop, 25 no mobile.

Mídia nova: `rov-amarras.webp`, `rov-porto.webp`, `rov-reservatorio.webp` = `MOTION_SIMULATION` (Nano Banana Pro com a foto do ROV e o quadro do vídeo como referência; legenda "Simulação visual"). `rov-recorte.webp` = `TREATED_ORIGINAL` (só fundo removido). Créditos desta rodada: cerca de 230.
