# PASS 00 · Audit

**Projeto:** Gávea Green · Drone Inspection
**Direção:** `GAVEA_GREEN_DRONE_MASTER_BRIEF_V2_10-10.md` (lido inteiro)
**Data:** 02/10/2026
**Escopo desta rodada:** auditoria e proposta. Nenhum arquivo de código foi alterado.

Evidências visuais desta auditoria:

- `docs/pass00/contato-fotos-pdf.jpg` · folha de contato das fotos do PDF + fundo gerado
- `docs/pass00/comparacao-detalhes-drone.jpg` · recortes comparando LiDAR, ferramenta frontal, câmera e luz entre fotos

---

## 1. Current state

### O que existe

O projeto é uma cópia da base `new-3d-landbase` (commit `2028476`) com **11 arquivos modificados e não commitados** e um protótipo de landing já construído por cima.

| Item | Estado |
|---|---|
| `src/app/page.tsx` | Renderiza só `<Hero />` |
| `src/components/sections/Hero.tsx` | 270 linhas. Uma seção `500vh` com wrapper `sticky`, 5 cenas sobrepostas (`absolute`) que trocam por **crossfade de opacidade**, e um PNG do drone movido por `translate3d + scale + rotate` em 8 keyframes |
| `src/app/globals.css` | 204 linhas de CSS próprio (`.flight-*`, `.scene-*`). Tailwind importado, praticamente não usado |
| `src/lib/hero.ts` | **Apagado.** Era o motor de frame-sequence da base (canvas + preload). Recuperável via `git show HEAD:src/lib/hero.ts` |
| `public/frames/` | Apagado (só tinha README) |
| UI da base (`AnimatedSection`, `Button`, `HudFrame`, `EyebrowBadge`, `ScrollRevealText`, `VideoMedia`, `Placeholder`, `SectionLabel`) | Presentes, **nenhum é usado** pela página atual |
| `npm run lint` / `tsc --noEmit` | Passam sem erros |
| Docs no projeto | `BRIEF-CRIACAO-LANDING-DRONE.md` (brief V1 detalhado), `DIRECAO-CRIATIVA.md` (marcado como substituído) |

### Como o protótipo atual se move

- Progresso = `-rect.top / (altura - viewport)`, calculado em `scroll` passivo + `requestAnimationFrame`. Escrita direta em `style` via ref. Tecnicamente limpo.
- O drone é **um único `<Image>` 2D**. Ele muda posição, escala (1 → 0.1) e rotação **no plano da tela** (-15° a +24°). Isso é exatamente o "PNG deslizando" que o brief proíbe como acabamento.
- Pairar: `@keyframes drone-hover` em CSS (±9px, ±1°) sobre a imagem inteira. Hélices paradas.
- A troca de cena é **dissolve entre slides** (opacidade), o oposto de "consequência física do voo".
- O drone **some** (opacity 0 entre 64% e 76%) em vez de entrar em algum lugar.
- Halo verde-limão com `blur(38px)` sob o drone: glow gratuito.

### Conflitos do protótipo atual com o master brief

| Ponto | Situação atual | Brief V2 |
|---|---|---|
| Paleta | `--ink #071714`, `--paper #eeeee8`, `--acid #bde85e` | `#009F4A`, `#007A38`, `#FFFFFF`, `#F7F7F8`, `#1A1A2E`, `#555565` |
| Marca | `gavea-green-tech-logo.png` (é o `p01_simbolo_gavea_green_x13` do PDF) e "Gávea Green Tech" no metadata | Assinatura Gávea Green da referência MERUS |
| Tipografia | Geist, títulos em caixa alta ("PRIMEIRO, O DRONE.") | Space Grotesk / Inter (a confirmar), sentence case |
| Capítulos | 5 cenas | 4 capítulos, 5 a 7 alturas de tela |
| Copy | Própria do protótipo | Copy de trabalho do brief |
| Header | `backdrop-filter: blur(16px)` + label + CTA "Falar sobre um ativo" | Mínimo: assinatura + `Falar com a Gávea` |
| Integridade | Cena 3 usa `drone-em-tubulacao.jpg` com alt "Drone inspecionando a parede interna de um ativo". O arquivo é o `p03_robo_em_tubulacao_x97.jpg`, equipamento **não confirmado** como o protagonista. Cena 2 usa `industrial-vessel-empty.png` (gerado) sem identificação | Não atribuir equipamento nem operação sem validação |
| Copy com claim | "POUCA LUZ. SEM GPS. COM VISÃO." | Claims por equipamento: `REQUIRES_GAVEA_VALIDATION` |
| Microcopy | "SCROLL TO EXPLORE ↓" em inglês | PT-BR |

**Leitura:** a arquitetura de scroll (sticky + progresso + escrita por ref) é aproveitável. A camada visual, a paleta, a marca e o modelo de transição não são. O PASS 01 deve começar numa rota isolada, sem tentar remendar o `Hero.tsx`.

### Observações técnicas do código

- `html { scroll-behavior: smooth }` junto com Lenis: o Lenis recomenda remover, porque briga com âncoras e com o próprio smoothing.
- `height: 100dvh` no sticky: no iOS a barra de endereço muda o `dvh` durante o scroll e gera salto de layout. Para cena pinada, usar `100svh` ou altura capturada no load.
- `getBoundingClientRect()` por frame é ok numa única seção.
- O projeto tem `.git` próprio copiado da base (mesmo histórico, sem remote). A pasta `GAVEA TECH` em si cai no repo acidental da HOME. **Não commitar lá.** Antes do PASS 01, decidir se este projeto mantém o histórico da base ou começa um repo novo.

---

## 2. Stack

| Camada | Versão | Observação |
|---|---|---|
| Next.js | 16.2.2 | `turbopack.root` já fixado no `next.config.ts` (evita CSS defasado e fork storm por causa do `~/package-lock.json`) |
| React / React DOM | 19.2.4 | |
| Tailwind | v4 (`@tailwindcss/postcss`) | Quase sem uso na página atual |
| Lenis | 1.3.25 | `lerp 0.1`, `syncTouch: false`, desligado em reduced motion |
| Framer Motion | 12.38 | Só usado no provider (`MotionConfig reducedMotion="user"`) |
| Fontes | `geist` | Trocar por Space Grotesk / Inter via `next/font/google` quando a identidade for confirmada |
| Build | `next build --webpack` | Script força webpack no build |
| 3D / WebGL | **nenhum** | Sem `three`, `@react-three/*`, `gsap` |
| Ferramentas locais | Python 3 + Pillow + NumPy, ffmpeg/ffprobe | **Blender não está instalado.** Nenhum arquivo `.glb/.gltf/.blend/.step/.stl/.obj` no Desktop |
| Máquina | Apple M1, 8 GB | Render 3D local é possível com Blender, mas lento em Cycles |

**Arquitetura que a base oferece (e que foi apagada):** hero de frame-sequence em `<canvas>`, frames pré-renderizados, preload com barra, `devicePixelRatio` limitado a 2, cover-fit. É a arquitetura mais adequada para o que o brief pede, desde que exista um asset que gere esses frames (ver seção 7).

---

## 3. Drone asset audit

### Identidade do arquivo

`public/media/drone-cutout.png` é **byte a byte** o `03_PNGs_com_transparencia/p04_drone_recortado_x139.png` (sha256 `a3da35c1…`). Esse PNG é o JPEG do PDF (`x139`) com a máscara de alpha do próprio PDF aplicada. Não houve tratamento de pixel. Classificação: `ORIGINAL_PDF`.

### Medidas

| Medida | Valor |
|---|---|
| Canvas | 1000 × 667 px, RGBA |
| Bounding box do drone | **758 × 604 px** |
| Cobertura do alpha dentro da bbox | 38% (proteções vazadas, raios finos) |
| Alpha | 256 níveis, borda suave (máscara do PDF) |
| Halo claro na borda | ~4,5% dos pixels de borda com luminância > 200 (resto do fundo branco de estúdio) |
| Peso | 495 KB |

### O que a imagem mostra

Vista única em ¾ frontal de cima, câmera ~35° acima do plano das hélices. Corpo preto em carbono, **quatro proteções circulares com raios** (três inteiras visíveis, uma parcial atrás), LiDAR inclinado no topo (cilindro preto e branco com marca "II"), módulo frontal com rolo/escova e roda, **cabos azuis** em tubo transparente, dois módulos de luz vermelhos nas bordas das proteções. Hélices **paradas**. Luz de estúdio high-key, suave, sem direção forte.

### O que esse asset permite e o que não permite

| Exigência do brief | Com o PNG atual | Por quê |
|---|---|---|
| Aproximação convincente | **Limitada** | No desktop (1440 px, DPR 2), o drone a 50vw já está ~1,9× ampliado. A 85vw passa de 3×. Fica mole |
| Close de câmera / rotores / proteções (macro ZRK) | **Não** | O módulo de câmera ocupa ~120 px no original. Para preencher 40vw em DPR 2, precisa ~10× de ampliação |
| Mudança de perspectiva 30–60° | **Não** | Existe uma vista só. Qualquer giro inventa o outro lado |
| Sensação de profundidade | **Parcial** | Escala, blur de foco e paralaxe de camadas ajudam. O objeto em si continua chapado |
| Iluminação respondendo ao ambiente | **Não de forma crível** | Luz de estúdio difusa está "assada" no pixel. Sombra, rim light ou feixe por cima viram filtro. A luz das próprias lanternas do drone não tem como acender |
| Oclusão | **Sim** | Camadas de primeiro plano (borda de chapa, boca de visita) passando na frente funcionam bem com qualquer asset |
| Entrada em ambiente industrial | **Parcial** | Dá para encenar a passagem por oclusão. O drone entra "achatado" e com luz de estúdio dentro do escuro |
| Continuidade visual em movimento | **Parcial** | É sempre o mesmo pixel, então é o mesmo drone. Mas o único movimento possível é 2D, que é o que o brief reprova |
| Rotores vivos | **Não** | As hélices estão paradas na foto. Pintar blur por cima de hélice parada é falsificação visível |
| Fundo escuro | **Com cuidado** | O halo branco da borda aparece em fundo escuro. Precisa de defringe/choke (tratamento `TREATED_ORIGINAL`) |
| Desktop / mobile | **Sim, estático** | Funciona bem como still em qualquer tamanho até ~1,5× |

**Conclusão do asset:** o PNG é um **master de forma excelente** (fiel, com alpha limpo da origem) e um **still de fallback** sólido. Ele não é um asset de movimento. Com ele, o máximo honesto é uma coreografia 2.5D sem giro. Isso o próprio brief chama de opção D, "fallback temporário, nunca acabamento final".

### Coisas que NÃO resolvem e devem ser recusadas

- `rotateY` em CSS 3D sobre o PNG: vira cartão girando.
- Espelhar o PNG para "ver o outro lado": o drone é assimétrico (ferramenta frontal à esquerda, LiDAR deslocado). Espelhado vira outra configuração.
- Crossfade entre duas vistas geradas: é morph.
- Depth map + displacement (paralaxe 2.5D por profundidade): os raios finos das proteções e os vazados esticam visivelmente acima de ~6–8°. Lê como deformação.
- Usar `p05_drone_em_voo`, `p07_drone_em_gaiola`, `p05_drone_em_duto`, `p07_drone_em_estrutura` como outros ângulos: são outros equipamentos.

---

## 4. Available media

### Em `public/media/`

| Arquivo no projeto | Origem real (hash conferido) | Resolução | Classificação | Papel possível |
|---|---|---|---|---|
| `drone-cutout.png` | `p04_drone_recortado_x139.png` | 1000×667, alpha | `ORIGINAL_PDF` | Master de forma, still de fallback e reduced motion, referência de validação do 3D |
| `drone-em-tubulacao.jpg` | **`p03_robo_em_tubulacao_x97.jpg`** (nome no projeto induz a erro) | 2048×1179 | `ORIGINAL_PDF` · equipamento `REQUIRES_GAVEA_VALIDATION` | Ver análise abaixo. Hoje está publicado com alt que afirma o que não está confirmado |
| `monitoramento.jpg` | `p02_tela_de_monitoramento_x53.jpg` | 2048×858 | `ORIGINAL_PDF` | PASS 03, evidência de monitoramento. Pixels da tela intocáveis |
| `resultados-inspecao.jpg` | `p04_resultados_de_inspecao_termica_x135.jpg` | 1500×797 | `ORIGINAL_PDF` · legenda `REQUIRES_GAVEA_VALIDATION` | PASS 03. Não chamar de térmica: a imagem mostra captura + nuvem de pontos |
| `industrial-vessel-empty.png` | Gerado (não vem do PDF) | 1672×941 | `GENERATED_ILLUSTRATION` | Referência de atmosfera para o ambiente. Em tela cheia 1440 DPR 2 fica ~1,7× ampliado. Nunca como operação real |
| `gavea-green-tech-logo.png` | `p01_simbolo_gavea_green_x13.png` | 2048×593 | `ORIGINAL_PDF` | **Não usar** (brief: identidade Green Tech do PDF fora) |

### Fotos do PDF que importam para o drone

Ver `docs/pass00/contato-fotos-pdf.jpg` e `docs/pass00/comparacao-detalhes-drone.jpg`.

| Arquivo | Res. | Classificação | O que a auditoria encontrou |
|---|---|---|---|
| `p02_drone_em_espaco_confinado_x56.jpg` | 2048×1537 | `ORIGINAL_PDF` · `REQUIRES_GAVEA_VALIDATION` | O drone aparece **exatamente na mesma pose, perspectiva, roteamento de cabo e posição das luzes** do recorte master. Com luz de estúdio dentro de um poço escuro. Isso é forte indício de **composição do recorte sobre um fundo**, não de uma segunda foto. Não é uma vista adicional. Também não deve ser tratada como registro de operação até a Gávea confirmar a origem |
| `p04_drone_com_iluminacao_x138.jpg` | 1000×419 | `ORIGINAL_PDF` · `REQUIRES_GAVEA_VALIDATION` | Vista baixa, por baixo do drone, luzes acesas, proteção com raios, tubo claro/azulado. As duas fontes de luz ficam onde estariam os módulos de luz das proteções. **Provável mesmo equipamento.** É a melhor referência existente de como o drone fica **no escuro com as lanternas acesas**. Alta luz estourada, geometria oculta: serve de referência de luz, não de forma |
| `p03_robo_em_tubulacao_x97.jpg` | 2048×1179 | `ORIGINAL_PDF` · `REQUIRES_GAVEA_VALIDATION` | **Perfil lateral.** O LiDAR tem o mesmo formato, a mesma inclinação e a mesma marca "II" do master. Frame de carbono, proteções vistas de lado como anéis planos, ferramenta frontal com roda encostada na parede. Diferenças: **cabo de amarração (tether) amarelo**, tubos sem o azul, ferramenta frontal com outro acabamento. Hipótese: mesma plataforma em outra configuração de payload, ou modelo irmão |
| `p02_robo_em_tunel_x50.jpg` | 2048×1196 | `ORIGINAL_PDF` · `REQUIRES_GAVEA_VALIDATION` | **Vista frontal.** LiDAR no topo, módulo de câmera central, duas luzes fortes nas laterais, tether. Coerente com a mesma família. Muita luz estourada e grading pesado |
| `p05_drone_recortado_x167.jpg` | 1000×667 | `ORIGINAL_PDF` | Repete o ângulo do master, sem alpha. Não é multivista |
| `p03_tela_de_termografia_x95.jpg`, `p03_tela_de_inspecao_x92.jpg` | 2048×1018, 1000×419 | `ORIGINAL_PDF` | PASS 03. Fora do motion proof |
| `p05_drone_em_voo_x166`, `p07_drone_em_gaiola_x204`, `p05_drone_em_duto_x168`, `p07_drone_em_estrutura_x201`, ROVs (p06) | | `ORIGINAL_PDF` | **Excluídos** do protagonista (outros equipamentos; dois deles vetados nominalmente pelo brief) |

**Achado relevante:** o PDF parece ter **três vistas reais da mesma família de equipamento** (¾ de cima no master, perfil em `p03_robo_em_tubulacao`, frontal em `p02_robo_em_tunel`) e **uma referência de luz no escuro** (`p04_drone_com_iluminacao`). Elas não servem como frames de animação: a configuração muda entre elas (tether, cor dos tubos, ferramenta). Mas, se a Gávea confirmar que é o mesmo modelo, servem como **referência de modelagem 3D e como teste de validação** de qualquer vista nova. Até essa confirmação, ficam como `REQUIRES_GAVEA_VALIDATION` e não entram em nenhuma composição.

### Outros materiais encontrados

- `Imagens da apresentacao Gavea Green Tech/catalogo.csv`: página, dimensões, objeto PDF e sha256 de cada imagem. Rastreabilidade boa.
- Marca Gávea Green em alta, fora do projeto: `~/Desktop/GAVEA PLAN27/APRESENTAÇÃO  G A V E A/GAVEA_TEASER/ASSETS DIVERSOS GAVEA/01_GAVEA-GROUP/04_LOGOS/01_GAVEA-GROUP/LOGO_Gavea-Green_Cor.png` e `LOGO_Gavea-Green_BCO.png`. Confirmar que são a assinatura oficial antes de usar.
- `landing-drone NÃO CONSIDERAR/` e `landing-drone-prototipo.zip`: ignorados, conforme o nome.
- **Nenhum vídeo** do drone, **nenhum CAD**, **nenhum modelo 3D**, **nenhuma foto adicional** do equipamento em qualquer pasta do Desktop.
- O PDF não traz fabricante nem modelo do drone. O equipamento tem cara de produto comercial de terceiro (LiDAR com marca própria, ferramenta de contato modular). **Se for de fabricante, o caminho mais curto para CAD, renders oficiais ou fotos 360° é o fabricante.** `REQUIRES_GAVEA_VALIDATION`.

---

## 5. Motion feasibility

Sequência pedida: **REVEAL → APPROACH → TURN → ENTRY → DARK**.

| Beat | O que o beat exige | Viável com o que existe? | Bloqueio |
|---|---|---|---|
| REVEAL | Drone em fundo claro, presença, rotores vivos, micro-pairar | **Parcial** | Rotores parados no pixel |
| APPROACH | Câmera avança, drone ocupa 70–90% do quadro, foco desloca para proteção/câmera | **Parcial** | Resolução: acima de ~1,5× amolece; macro impossível |
| TURN | Guinada de 30–60°, com banking físico, revelando perfil do LiDAR e ferramenta | **Não** | Uma única vista. Qualquer solução 2D vira cartão, morph ou drone inventado |
| ENTRY | Passa por abertura industrial, oclusão por primeiro plano, reaparece em profundidade | **Sim (encenação)** · **Parcial (drone)** | A oclusão funciona com camadas. O drone continua chapado e com luz de estúdio |
| DARK | Escuro, lanternas do drone acesas iluminando a superfície, névoa, luz respondendo | **Não** | Não há como acender as luzes do drone num PNG de estúdio nem projetar a luz dele no ambiente de forma coerente |

**Resultado:** dos cinco beats, **TURN e DARK estão bloqueados por asset**, e APPROACH só funciona até um plano médio. O gate do brief (seção 09) seria **FAIL** com o material atual: o critério "parece PNG" se confirmaria no TURN.

Para não parecer PNG deslizando, zoom CSS, cartão, morph, objeto deformado ou outro drone, o asset precisa ter quatro propriedades ao mesmo tempo:

1. **Geometria consistente em qualquer ângulo** (resolve TURN, morph e "outro drone").
2. **Resolução ou detalhe sob demanda** (resolve APPROACH e macro).
3. **Luz recalculável** (resolve DARK e luz respondendo ao ambiente).
4. **Hélices com movimento real ou motion blur fotográfico** (resolve rotores vivos).

Só um modelo 3D fiel tem as quatro. Vídeo real filmado tem as quatro só no movimento que foi filmado.

---

## 6. Technical options

Avaliação pelo resultado visual, não pela sofisticação.

| Opção | TURN 30–60° | Macro | Luz no escuro | Rotores | Risco "falso" | Peso / perf | Asset necessário | Veredito |
|---|---|---|---|---|---|---|---|---|
| **A. PNG + transformações (2.5D)** | ✗ | ✗ | ✗ | ✗ | Alto: é o que o brief reprova | Leve | Já existe | Só fallback e reduced motion |
| **B. PNG + depth map + displacement (WebGL)** | ✗ (máx. ~6–8°) | ✗ | Fraco (normal map estimado) | ✗ | Alto: raios finos esticam | Médio | Depth/normal estimados por IA | Recusar |
| **C. Multiview gerada por IA (Change Camera etc.)** | Só em degraus discretos | ✗ | ✗ | ✗ | Alto: raios, cabos e LiDAR mudam entre vistas; precisa crossfade = morph | Leve | Upload do master para serviço externo | Só como exploração rotulada |
| **D. Vídeo image-to-video por IA (start/end frame)** | ✓ aparente | Parcial | Parcial | ✓ aparente | **Muito alto**: deriva de geometria nos frames intermediários, sem alpha, difícil de recortar (estrutura vazada) | Médio | Upload externo + muitas iterações | Plano B emergencial, `MOTION_SIMULATION` |
| **E. Vídeo real filmado do drone** | ✓ (no movimento filmado) | ✓ (se filmado em 4K/macro) | ✓ (se filmado no escuro) | ✓ | Baixo | Médio | Sessão de filmagem com o equipamento | Excelente para planos, ruim para coreografia contínua com o DOM (sem alpha, sem controle de câmera) |
| **F. Image-to-3D por IA (uma imagem → GLB)** | ✓ geometricamente | ✗ | ✓ | ✓ | **Muito alto**: inventa o lado oculto, estrutura vazada vira bolha | Médio | Upload externo | Recusar como master. Talvez como base de modelagem |
| **G. Modelo 3D fiel → render offline → sequência de frames em canvas** | ✓ | ✓ | ✓ (luz real, volumétrico, sombras) | ✓ (motion blur real) | **Baixo**, se o modelo passar no teste de pose | Médio: 8–15 MB desktop, 4–7 MB mobile, com carga progressiva | CAD do fabricante **ou** modelagem por artista a partir de fotos reais | **Recomendado** |
| **H. Modelo 3D fiel → Three.js em tempo real** | ✓ | ✓ | Médio (tempo real em mobile limita sombra, AO, DOF, volumétrico) | ✓ | Médio: tende ao "Three.js demo" que o brief rejeita | GLB 3–8 MB + ~150 KB de lib + GPU no mobile | Mesmo modelo de G | Alternativa se for preciso interatividade livre |
| **I. Híbrido DOM + frames (G) + fotos reais** | ✓ | ✓ | ✓ | ✓ | Baixo | Médio | G + fotos do PDF nos PASS 03+ | É a arquitetura da página inteira, com G como coração |

### Por que G (render offline) e não H (Three.js em tempo real)

- A referência ZRK é sobre **luz**: rim light, falloff, névoa atravessada por feixe, profundidade de campo. Isso sai melhor e mais barato em render offline (Cycles) do que em WebGL em tempo real, principalmente no mobile.
- Carbono fosco, raios finos e tubo translúcido azul são materiais difíceis em tempo real. Em render offline ficam fotográficos.
- A base já tem a arquitetura de frame-sequence em canvas (apagada, recuperável do commit `2028476`). É código provado, sem dependência nova.
- O scroll em frame-sequence é determinístico: o frame 73 é sempre o mesmo. Fácil de aprovar por screenshots, que é exatamente o que o gate pede.
- Custo de H vale a pena só se a página precisar de câmera livre (arrastar, orbitar). O brief não pede isso.

**Limitação de G:** quando o scroll para, os frames congelam. Solução proposta: renderizar o drone em **camada separada com alpha**, sobre a camada de ambiente. Em repouso, só a camada do drone recebe o micro-pairar (±2–3 px, ±0,3°), e as hélices já saem com motion blur, então leem como girando mesmo paradas. O deslocamento é pequeno o suficiente para não descolar da luz do ambiente.

---

## 7. Recommended motion strategy

### Estratégia

**Modelo 3D fiel ao equipamento real → render offline em Blender (Cycles) → duas sequências de frames (ambiente opaco + drone com alpha) dirigidas por scroll em `<canvas>` → texto e CTA em DOM acessível por cima.**

Fallback em todos os níveis: o PNG master original como still.

### Vantagens

- Mesmo objeto físico do primeiro ao último frame, por construção.
- Qualquer câmera: wide, medium, macro na câmera, close nas proteções, contraplongée sob as lanternas.
- Luz física: as lanternas do drone acendem e iluminam a chapa, a névoa e a borda da abertura. É a cena "escuro = confinamento, luz = inspeção" do brief.
- Hélices com motion blur real.
- Oclusão real: a borda da boca de visita passa na frente do drone na geometria, não como máscara.
- Mobile ganha **renders próprios** (enquadramento vertical, câmera diferente), não um corte do desktop.
- Os stills do reduced motion saem do mesmo 3D: coerência total.

### Limitações

- Depende de um asset que **não existe hoje** (seção 8).
- O ambiente (boca de visita, chapa, interior do tanque) será modelado: é `MOTION_SIMULATION`, não registro de operação real. Precisa estar internamente identificado assim e não pode ser legendado como foto.
- Mudança de coreografia exige re-render (minutos a horas, não segundos). Por isso o timing precisa ser travado num animatic antes do render final.
- Blender não está instalado na máquina; render em Cycles num M1 8 GB é viável, mas lento para 2 sequências × 2 formatos. Pode ser necessário render fora (artista 3D ou render farm).

### Assets necessários

Ver seção 8. Em resumo: modelo 3D validado do drone (CAD do fabricante ou modelagem por artista a partir de fotos reais), mais medidas gerais.

### Risco visual

| Risco | Mitigação |
|---|---|
| Modelo "parecido mas diferente" | **Teste de pose obrigatório:** renderizar o 3D exatamente na câmera do master `p04_drone_recortado_x139` e sobrepor ao PNG com diferença de silhueta. Contagem de raios, posição do LiDAR, roteamento do cabo azul e luzes precisam bater. Se a Gávea confirmar o perfil e a frontal, repetir o teste nessas duas vistas |
| Ficar com cara de render (CG limpo demais) | Grão leve, aberração mínima, DOF de lente real (50–85 mm equivalente), sujeira sutil no carbono, sem bloom. Referência de luz: `p04_drone_com_iluminacao` |
| Ambiente inventado parecer documental | Ambiente estilizado e genérico (chapa, solda, boca de visita), sem logo, sem placa, sem pessoa, sem dado. Registro interno `MOTION_SIMULATION` |
| Lado oculto inventado | O TURN é limitado a 30–45° na direção que as fotos reais cobrem (do ¾ do master para o perfil). Nada de mostrar a traseira sem referência |

### Impacto em performance

| Item | Desktop | Mobile |
|---|---|---|
| Frames | ~120 por camada, 1600 px de largura, WebP (AVIF opcional) | ~80, render vertical 900×1600, **uma camada só** (drone e ambiente juntos) |
| Peso estimado | ~8–15 MB total | ~4–7 MB |
| Carga | Poster + primeiros 15 frames antes de liberar o scroll (< 1,5 MB). Resto em background, por trecho | Idem, com trecho menor |
| Runtime | 1 `drawImage` por camada por frame, DPR ≤ 2, rAF + escrita por ref (regras da base) | Igual |
| Lenis | Mantido. Remover `scroll-behavior: smooth` do `html` | `syncTouch: false` (já está) |

### Desktop

Coreografia completa, 5 beats, ~300vh de scroll para o motion proof. Drone com camada própria para o pairar em repouso. Texto do REVEAL em DOM, na área de respiro que o render reserva.

### Mobile

Não é o desktop reduzido.

- Render vertical próprio, câmera mais alta e mais distante: o drone ocupa a metade de baixo, o texto a metade de cima.
- TURN reduzido a ~25–30° (menos tempo de tela para ler a rotação).
- ENTRY por **corte de oclusão mais seco**: a chapa cruza o quadro inteiro e revela o interior. Menos travelling, mais clareza.
- Sem camada separada de drone (economia de peso). Pairar só na fase clara.
- ~260vh de scroll.
- Prioridade do brief: clareza → legibilidade → movimento → performance.

### Fallback

- Sem JS ou carga lenta: poster (frame 1 do render) com o texto completo em DOM.
- Enquanto o 3D não existe: PNG master como still, sem coreografia de giro.
- Navegador que falhe ao decodificar WebP com alpha (raro): sequência única opaca.

### `prefers-reduced-motion`

- Sem pin, sem sequência, Lenis desligado (já está no provider).
- Capítulos empilhados em fluxo normal, cada um com **um still renderizado do mesmo 3D** (REVEAL claro, TURN em perfil, DARK com lanternas).
- Todo o conteúdo e CTA acessíveis em ordem de leitura.
- Botão "Pausar animação" previsto no storyboard para quem não ativou a preferência (PASS 05).

---

## 8. Missing assets

Nada abaixo deve ser inventado ou gerado como substituto silencioso.

### Bloqueadores do motion proof (precisa de pelo menos um caminho)

**Caminho A1, o mais rápido se existir:**

1. **Fabricante e modelo exatos do drone** `REQUIRES_GAVEA_VALIDATION`.
2. **CAD, modelo 3D, renders oficiais ou press kit 360°** do fabricante.

**Caminho A2, se não houver CAD:**

3. **Fotos reais do equipamento** na configuração que vai aparecer (com cabos azuis, ferramenta frontal com escova, sem tether ou com tether, a decidir):
   - frente, ¾ frontal esquerdo, ¾ frontal direito, perfil esquerdo, perfil direito, traseira, topo e baixo;
   - giro de 360° em degraus de 15–20°, em duas alturas de câmera (nível e +35°, que é a altura do master);
   - fundo neutro, luz difusa, RAW ou JPEG em máxima resolução;
   - closes: câmera/óptica, um módulo de luz vermelho (aceso e apagado), uma proteção com raios, LiDAR, ferramenta frontal, cabo azul.
4. **Vídeo de referência** do drone voando com as luzes acesas, mesmo de celular, para timing de pairar, inclinação e cor da luz.
5. **Medidas gerais:** diâmetro das proteções, distância entre eixos, largura total, altura com LiDAR. Garante escala física correta contra a abertura industrial.

Com A2, um artista 3D modela o equipamento a partir das fotos (hard-surface). Fotogrametria pura não resolve bem estrutura vazada de carbono.

**Caminho A3, mínimo e com risco:**

6. **Confirmação da Gávea** de que `p03_robo_em_tubulacao_x97` (perfil) e `p02_robo_em_tunel_x50` (frente) mostram **o mesmo modelo** do master. Com isso, master + perfil + frente permitem uma modelagem de fidelidade média. Traseira e lado direito ficam sem referência: o TURN fica restrito ao arco coberto.

### Validações (não bloqueiam o rig, bloqueiam a publicação)

7. Origem de `p02_drone_em_espaco_confinado_x56`: foto real ou composição do recorte?
8. `p04_drone_com_iluminacao_x138` é o mesmo drone? As luzes são as do módulo vermelho?
9. Configuração oficial que a página mostra: com ou sem tether?
10. Capacidades por equipamento (luz embarcada, anticolisão, 4K, live feed, sem GPS): `REQUIRES_GAVEA_VALIDATION`.
11. Assinatura oficial Gávea Green (confirmar `LOGO_Gavea-Green_Cor.png` / `BCO.png`).
12. Tipografia oficial (Space Grotesk / Inter é referência de trabalho).

### Autorização pendente

13. O brief V1 proíbe enviar assets do PDF a serviço externo sem autorização. Qualquer caminho com IA (Magnific, Higgsfield, image-to-3D) **precisa de autorização explícita** antes de subir o master.

### Ferramenta

14. Blender (gratuito) instalado nesta máquina, ou render fora com artista 3D.

---

## 9. PASS 01 proposal · Motion proof

Objetivo único: **provar o protagonista.** Sem landing, sem registros, sem CTA final.

### Onde

- Rota isolada `src/app/motion-proof/page.tsx`. O protótipo atual (`Hero.tsx`) fica intocado para comparação.
- Componente `src/components/motion/DroneSequence.tsx`, recuperando o motor de frame-sequence da base (`git show HEAD:src/lib/hero.ts` + Hero original), adaptado para **duas camadas** e para fonte desktop/mobile separada.
- Tokens Gávea Green em `:root` (`#009F4A`, `#007A38`, `#FFFFFF`, `#F7F7F8`, `#1A1A2E`, `#555565`) desde o início, para julgar a luz contra a paleta real.
- Nenhuma dependência nova.

### Mapa de coreografia (desktop, ~300vh)

Lente equivalente 50 mm no wide, 85 mm no close. Fundo claro `#F7F7F8`. Drone com proporção física real.

| Progresso | Beat | Câmera | Drone | Luz | Teste |
|---|---|---|---|---|---|
| 0,00–0,15 | **REVEAL** | Wide fixo, leve contraplongée, muito espaço negativo à esquerda (reservado para H1) | ¾ frontal, mesma pose do master, ~40% da largura. Pairando, hélices em blur | Key suave de cima à esquerda, sombra de contato difusa no "chão" claro | 1 · drone em fundo claro |
| 0,15–0,35 | **APPROACH** | Dolly in + foco desloca do corpo para a proteção frontal e a câmera | Avança e cresce até ~85% do quadro. Leve pitch para frente ao acelerar | Mesma key. Rim aparece na borda do carbono | 2 · aproximação |
| 0,35–0,55 | **TURN** | Câmera recua um pouco para manter o drone inteiro no meio do giro | Guinada de **35–45°** em direção ao perfil (arco coberto pelas fotos reais), com **banking de 6–10°** na curva. LiDAR e ferramenta frontal revelam o perfil | A borda de uma chapa industrial entra no primeiro plano, fora de foco. A luz clara começa a ser cortada por ela | 3 · mudança crível de 30–60° |
| 0,55–0,72 | **ENTRY** | Câmera acompanha por trás e por cima. A boca de visita (abertura circular em chapa) atravessa o quadro | Drone mergulha pela abertura. **Oclusão total breve** (~3% do scroll) pela chapa | Exterior claro se fecha. Último fio de luz pela abertura | 4 · entrada na abertura · 5 · oclusão |
| 0,72–1,00 | **DARK** | Câmera dentro, estática ou deriva lenta. Drone reaparece **em profundidade**, ~25–30% do quadro | Lanternas acendem (os módulos vermelhos). O drone avança devagar para dentro do escuro | Feixes cortam névoa leve, iluminam a parede de chapa. O próprio drone recebe a luz que reflete. Quase preto em volta, sem preto puro | 6 · reaparecimento em profundidade · 7 · ambiente escuro · 8 · luz respondendo |

Teste 9 (continuidade física) é transversal: nenhum corte, nenhum dissolve, nenhum frame em que o drone mude de escala ou pose sem causa visível.

### Física do movimento

- Inércia: aceleração e desaceleração do drone em curva de ease com overshoot mínimo (drone real não para seco).
- Pitch para frente ao acelerar, para trás ao frear. Bank na curva.
- Pairar em repouso: ±2–3 px e ±0,3° na camada do drone, frequência ~0,4 Hz, só quando o scroll está parado (detectado por inatividade > 150 ms).
- Hélices sempre em motion blur.

### Mobile (versão simplificada, render próprio vertical, ~260vh)

| Beat | Diferença em relação ao desktop |
|---|---|
| REVEAL | Drone na metade de baixo, texto em cima. Câmera mais alta |
| APPROACH | Aproximação menor (até ~70% da largura) |
| TURN | 25–30° apenas |
| ENTRY | Corte por oclusão mais seco: a chapa varre o quadro inteiro |
| DARK | Drone um pouco maior que no desktop, para manter legível |

Camada única (sem drone separado). Pairar só no REVEAL, via CSS na camada inteira enquanto o fundo é liso.

### Reduced motion no proof

Três stills empilhados (REVEAL, TURN, DARK), sem pin. Serve para validar desde já que a estratégia de acessibilidade funciona com o mesmo material.

### Entregáveis do PASS 01

1. Preview local navegável em `/motion-proof` (desktop e mobile).
2. Folha com **5 screenshots lado a lado** nas posições 0 · 0,25 · 0,5 · 0,75 · 1,0, desktop.
3. Mesma folha para mobile (390 px).
4. **Teste de pose:** render 3D na câmera do master sobreposto ao PNG original, com diferença de silhueta.
5. Notas de QC contra o gate: silhueta, proteções, câmera, cabos, iluminação, escala, perspectiva, luz.
6. Lista de limitações conhecidas.

Depois: **parar e aguardar aprovação.**

### Ordem de produção dentro do PASS 01

1. Animatic em blocos (formas simples no Blender) com o timing da tabela acima, exportado em frames leves e já rodando no canvas da rota. Trava o ritmo antes de gastar render.
2. Validação do modelo 3D pelo teste de pose.
3. Render final das duas camadas (desktop) e da camada única (mobile).
4. Integração, screenshots, notas.

### Se o 3D não chegar logo: duas saídas possíveis, sem fingir que passam no gate

- **PASS 01-R (rig):** construir agora a rota, o motor de duas camadas, os beats, a oclusão, a luz do ambiente, o mobile e o reduced motion, usando o **PNG master como placeholder declarado** (sem giro). Prova palco, ritmo e oclusão. **Não prova o protagonista** e não substitui o gate. Quando o 3D chegar, troca-se só a fonte de frames.
- **PASS 01-B (IA, emergencial):** vídeo image-to-video com frames de início e fim, ou image-to-3D, a partir do master. Requer autorização para subir o asset a serviço externo. Saída rotulada `MOTION_SIMULATION`, com QC frame a frame (raios, cabos, LiDAR). A expectativa honesta é de que o TURN falhe no QC pela estrutura vazada.

---

## Síntese

**CURRENT STATE**
Protótipo de 5 cenas funcional (lint e tsc ok), com scroll bem implementado, mas o drone é um PNG 2D com translate/scale/rotate, cenas trocam por dissolve, paleta e marca são da Green Tech, e uma foto de equipamento não confirmado está legendada como se fosse o protagonista. O motor de frame-sequence da base foi apagado, mas é recuperável do git.

**MAIN LIMITATION**
O protagonista existe em **uma única vista de 758×604 px** com luz de estúdio e hélices paradas. Isso impede o TURN de 30–60°, o macro, a luz respondendo no escuro e os rotores vivos. Não há vídeo, CAD, modelo 3D ou fotos adicionais confirmadas do equipamento.

**RECOMMENDED MOTION STRATEGY**
Modelo 3D fiel validado contra o master por teste de pose → render offline (Blender/Cycles) → frame-sequence em canvas com duas camadas (ambiente opaco + drone com alpha) → DOM por cima. Mobile com render vertical próprio. Reduced motion com stills do mesmo 3D. PNG master como fallback.

**MISSING ASSETS**
Fabricante e modelo do drone. CAD ou modelo 3D, **ou** fotos reais multivista (giro 360° em duas alturas + closes) e medidas gerais. Confirmação se `p03_robo_em_tubulacao` (perfil), `p02_robo_em_tunel` (frente) e `p04_drone_com_iluminacao` são o mesmo equipamento. Origem de `p02_drone_em_espaco_confinado` (indício de composição do recorte). Blender instalado ou artista 3D.

**PASS 01 PLAN**
Rota isolada `/motion-proof`, motor de frame-sequence recuperado da base em duas camadas, coreografia de ~300vh em 5 beats (tabela da seção 9), mobile vertical de ~260vh com TURN de 25–30° e corte por oclusão, reduced motion com 3 stills. Começa por animatic para travar ritmo, depois teste de pose, depois render. Entrega preview local, folhas de 5 screenshots desktop e mobile, teste de pose e notas de QC.

**READY FOR MOTION PROOF: NO**

Bloqueio: não existe asset que permita o TURN de 30–60° nem a luz no escuro sem inventar geometria. O gate da seção 09 do brief daria FAIL ("parece PNG") com o material atual. Desbloqueia com qualquer um destes: CAD/3D do fabricante (A1), fotos multivista reais para modelagem (A2), ou confirmação da Gávea de que perfil e frente do PDF são o mesmo equipamento (A3, fidelidade média).

Decisões que dependem de você:

1. Pedir à Gávea fabricante/modelo, CAD ou fotos (itens 1 a 6 da seção 8).
2. Autorizar ou não o PASS 01-R (rig com PNG placeholder, sem passar no gate) enquanto o 3D é produzido.
3. Autorizar ou não envio do master a serviço externo de IA (PASS 01-B).
4. Modelagem 3D: feita por artista externo, ou instalar Blender aqui e eu conduzo animatic e render a partir de um modelo recebido.
