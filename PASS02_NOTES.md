# PASS 02 · Casca narrativa

**Data:** 04/10/2026 · **Rota:** `/` (local) · **Status:** aguardando aprovação

Quatro capítulos com conteúdo mínimo, para validar duração, scroll, clareza e desktop/mobile. Arte final, transições entre capítulos, progresso e microinterações ficam para o PASS 04; integração cuidadosa das evidências para o PASS 03.

## Rotas

| Rota | O que é |
|---|---|
| `/` | Landing (casca narrativa) |
| `/motion-proof` | PASS 01, só a tomada |
| `/prototipo-v1` | Protótipo anterior ao brief V2, preservado para comparação (`noindex`) |

## Estrutura

| Capítulo | Onde acontece | Conteúdo |
|---|---|---|
| 01 Revelar | Início da tomada (fundo claro) | Eyebrow, H1 "O drone entra. A evidência aparece.", apoio, CTA "Avaliar meu ativo" |
| 02 Acesso | Fim da tomada (escuro, lanternas) | "Acesse o que é difícil inspecionar." + tanques, silos, chaminés, galerias e caldeiras |
| 03 Registro | Seção escura contínua | "Veja durante o voo. Revise depois." + 3 registros originais do PDF com legenda e procedência |
| 04 Próximo passo | Retorno à luz | "Qual ativo você precisa inspecionar?", "Falar sobre meu projeto" (WhatsApp) e "Enviar e-mail", drone de volta ao fundo claro |

Cabeçalho mínimo: assinatura Gávea Green + "Falar com a Gávea". Troca sozinho entre versão clara e escura; sobre a tomada é transparente, fora dela ganha faixa sólida na cor do trecho (sem vidro nem desfoque).

## Medições

| | Desktop 1440×900 | Mobile 375×812 |
|---|---|---|
| Altura total | **6,8 telas** | **6,2 telas** |
| Alvo do brief | 5 a 7 telas, incluindo fechamento | composição própria |

## Clareza (teste do brief, seção 18)

- **Só imagem:** um drone se aproxima, gira, entra por uma abertura e some no escuro; depois aparecem telas de registro; por fim o drone volta à luz. Lê como "entra em lugar difícil, registra, traz de volta".
- **Só texto:** serviço (drones para inspeção industrial), onde atua (espaços confinados, tanques etc.), o que entrega (ver durante o voo, revisar depois) e próximo passo (qual ativo, falar sobre meu projeto). Entendido em poucos segundos.

## Decisões tomadas nesta passada

- Eyebrows em sentence case (sem caixa alta), coerente com a preferência de tipografia.
- Verde só em ação (CTA) e reconhecimento (assinatura, eyebrows).
- Assinatura Gávea Green: `LOGO_Gavea-Green_Cor.png` e `_BCO.png` do acervo GAVEA PLAN27, apenas recortadas pela margem transparente. **Confirmar que é a assinatura oficial.**
- Imagem nova no projeto: `public/media/captura-e-representacao.jpg` = `p03_tela_de_termografia_x95.jpg` (cópia idêntica, hash conferido). Nome trocado porque a imagem não é termografia.
- Metadata da página atualizada para "Gávea Green" com a frase de apoio do brief (sem claim novo).

## Pendências e validações

| Item | Situação |
|---|---|
| Contato (André Barbosa, e-mail e WhatsApp da p. 8 do PDF) | `REQUIRES_GAVEA_VALIDATION` antes de publicar |
| Legendas das 3 imagens de registro | Provisórias e genéricas; validar com a equipe técnica |
| Claims do capítulo 02 (baixa iluminação, sem GPS etc.) | Vêm do PDF; validar por equipamento |
| Fonte (Space Grotesk / Inter) | Referência MERUS; confirmar identidade oficial |
| Registros no capítulo 03 | Entram como lista simples. A ideia de "evidências encontradas durante a jornada" é do PASS 03 |
| Transição tomada → registro | Hoje é corte seco do escuro para o escuro. Ligação visual (módulo óptico → captura) é PASS 03/04 |
| Progresso discreto | Não incluído (opcional no brief); PASS 04 |
| Movimento reduzido | Implementado e não testado com a preferência ligada no navegador desta sessão |
| Âncoras + Lenis | `html { scroll-behavior: smooth }` herdado da base convive com Lenis; revisar no PASS 06 |
