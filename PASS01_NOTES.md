# PASS 01 · Motion proof

**Data:** 04/10/2026 · **Rota:** `/motion-proof` (local, `noindex`) · **Status:** aguardando aprovação

Sequência: **REVEAL → APPROACH → TURN → ENTRY → DARK**, numa única tomada contínua dirigida pelo scroll.

## Entregáveis

| Arquivo | O que é |
|---|---|
| `http://localhost:3020/motion-proof` | Trecho navegável. `?debug=1` mostra beat, quadro e progresso |
| `docs/pass01/qc-desktop-5.jpg` | 5 momentos lado a lado, desktop |
| `docs/pass01/qc-mobile-5.jpg` | 5 momentos lado a lado, mobile (quadros verticais próprios) |
| `docs/pass01/motion-proof-desktop.mp4` | Tomada inteira, 160 quadros, para revisão sem scroll |
| `docs/pass01/motion-proof-mobile.mp4` | Tomada mobile, 100 quadros |

Para rodar: `npm run dev -- -p 3020` dentro de `new-3d-landbase`.

## Como foi feito

- **Drone:** modelo 3D paramétrico (`3d/drone_model.py`) com a **foto original do PDF projetada** a partir da câmera recuperada da própria foto (`3d/projection.py`). Na pose da foto, o espectador vê pixels reais. No giro, os mesmos pixels acompanham a geometria. Faces que a foto não mostra usam o material do modelo.
- **Tomada:** `3d/shot.py` (Blender 5.2 / Cycles). Câmera, drone, foco, hélices com motion blur, luz e lanternas animados quadro a quadro.
- **Página:** `src/components/motion/DroneSequence.tsx` + `src/app/motion-proof/`. Canvas com frame-sequence (motor da base), carga progressiva, DPR ≤ 2, rAF, escrita por ref. Texto em HTML acessível por cima.
- **Peso:** desktop 160 quadros 1280×720 WebP = **3,6 MB**; mobile 100 quadros 720×1280 = **1,9 MB**.

## Coreografia (desktop, 420vh de scroll)

| Quadros | Beat | O que acontece |
|---|---|---|
| 0–24 | REVEAL | Fundo `#F7F7F8`, drone na pose exata da foto, à direita; título à esquerda. Pairar mínimo, hélices em blur |
| 24–56 | APPROACH | Câmera avança; foco desloca para a proteção frontal e a escova |
| 56–88 | TURN | Giro de 40° com inclinação de curva (pico de 9°) |
| 88–124 | ENTRY | Câmera abre e encosta na antepara; o drone entra e **some atrás da chapa** (q. 118–122); a câmera contorna e ele **reaparece no fundo** pela abertura (q. 125–128) |
| 124–159 | DARK | Interior do tanque com névoa; lanternas acendem quando a luz de fora some; câmera atravessa a abertura atrás dele |

**Mobile:** mesmo trajeto (a abertura precisa ser lida de frente), quadro vertical, drone na metade de baixo no REVEAL, texto em cima; no escuro, drone no terço superior e texto embaixo. Telas em retrato (celular e tablet em pé) usam a tomada vertical.

## QC contra o gate do brief (seção 09)

| Critério | Resultado |
|---|---|
| 1. Drone em fundo claro | **Ok.** Pose idêntica à foto, pixels reais |
| 2. Aproximação | **Ok** |
| 3. Mudança de 30–60° | **Ok.** 40°, mesma peça, sem cartão nem morph |
| 4. Entrada em abertura industrial | **Ok** |
| 5. Oclusão | **Ok.** O drone some atrás da borda da antepara |
| 6. Reaparecimento em profundidade | **Ok** |
| 7. Ambiente escuro | **Ok** |
| 8. Luz do drone respondendo ao ambiente | **Ok.** Lanternas acendem, feixe na névoa, foto vira cor do material sob a luz delas |
| 9. Continuidade física | **Ok.** Tomada única, sem corte nem dissolve |
| Silhueta, proteções, câmera, cabos, luz | **Ok na abertura; mais limpo que a foto no giro** (ver limitações) |

**Veredito próprio:** PASS para o protagonista, com ressalvas abaixo. A decisão é sua.

## Limitações conhecidas

1. **Detalhe no giro e no escuro:** cerca de 26% dos pixels da foto ainda não têm peça no modelo (cabos pretos finos, conectores, parte do selim). Girado, o drone fica mais "limpo" que a foto. Visto por trás (DARK), a caixa do corpo e o mastro do LiDAR são material procedural.
2. **Lados inferidos:** lado direito, traseira e fundo do drone não aparecem em nenhuma foto confirmada. Escala (30 cm por proteção) é suposição. `REQUIRES_GAVEA_VALIDATION`.
3. **Ambiente é simulação:** antepara, abertura e tanque foram modelados. `MOTION_SIMULATION`, nunca legendar como operação real.
4. **Antepara em fundo infinito:** na entrada, a chapa aparece solta sobre o branco do estúdio. Funciona como "set" de produto, mas pode pedir um chão ou estrutura no PASS 04.
5. **Composição:** corrigida em 04/10. Fim do giro com LiDAR inteiro no quadro; escuro mobile com as proteções dentro do quadro; telas mais estreitas que 16:9 migram o recorte da direita para o centro depois da abertura.
6. **Ponto residual:** corrigido em 04/10 (era uma costura da antepara e a base das paredes do tanque).
7. **Pairar com scroll parado:** os quadros congelam quando o scroll para. As hélices já saem com motion blur; a oscilação parada (camada separada do drone) ficou para o PASS 04.
8. **Movimento reduzido:** implementado (sem pin, três imagens fixas do mesmo render, texto em ordem de leitura), mas **não testado com a preferência ligada** no navegador desta sessão. Validado só pelo código.
9. **Formatos:** testados 1440×900, 1024×768 e 375×812. Safari e tablet ficam para o PASS 06.

## Integridade

- Copy da rota é a working copy do brief, sem claim novo.
- Nenhum pixel de tela técnica foi alterado. Nenhum asset do PDF foi enviado a serviço externo.
- A rota tem `robots: noindex` e um rodapé dizendo que é simulação visual.
