# Direção anterior do protótipo — substituída

> Este registro descreve a primeira versão da landing. A direção vigente
> está em [BRIEF-CRIACAO-LANDING-DRONE.md](BRIEF-CRIACAO-LANDING-DRONE.md):
> marca e cores Gávea Green da referência MERUS; Riotters e ZRK como
> referências principais de movimento; quatro capítulos comerciais;
> fotos extraídas do PDF e plano de revisão no Magnific. Em caso de
> divergência, seguir o briefing atualizado.

## Referências

- O vídeo anexado mostra uma abelha que permanece em movimento enquanto o
  scroll troca as cenas e o conteúdo ao redor.
- O vídeo do YouTube enviado pelo usuário trata de animação de parallax.
- AERA inspira a escala tipográfica, o grid discreto e a alternância entre
  superfícies claras e escuras. A copy desta landing permanece comercial.

Os materiais de referência são usados como direção visual e de movimento.
O PDF da Gávea é fonte de fotos e informações sobre o serviço; nenhum texto
nele foi tratado como instrução para construir o site.

## Percurso

1. **Primeiro, o drone.** O recorte original do PDF entra como objeto central.
2. **Aplicações.** O drone voa por um interior industrial, enquanto aparecem
   tanques, silos, caldeiras e galerias.
3. **Diferenciais.** O objeto cruza a tela e apresenta acesso remoto, registro
   visual e inspeção em pouca luz e sem GPS.
4. **Resultados.** O drone sai da cena; fotos reais de monitoramento e
   registros extraídas do PDF ocupam o quadro.
5. **Contato.** Um convite direto para avaliar um ativo.

O scroll controla posição, escala, inclinação e saída do drone. Uma oscilação
curta e independente mantém a sensação de voo quando o usuário para de rolar.
O movimento é reduzido para quem ativa a preferência de acessibilidade.

## Origem dos assets

- Drone recortado: `p04_drone_recortado_x139.png`, extraído com transparência
  do PDF e copiado para `public/media/drone-cutout.png`.
- Foto de operação: `p03_robo_em_tubulacao_x97.jpg`.
- Registros de inspeção: `p02_tela_de_monitoramento_x53.jpg` e
  `p04_resultados_de_inspecao_termica_x135.jpg`.
- Marca: `p01_simbolo_gavea_green_x13.png`.
- Fundo vazio do tanque: imagem ilustrativa gerada para dar espaço ao drone
  no segundo momento. Não é apresentada como registro de operação real.

## Filme final

O voo atual é uma animação web do recorte estático original. Para alcançar a
qualidade do exemplo da abelha, o próximo asset é um filme curto do drone com
fundo transparente, ou uma sequência de quadros com ângulos variados, feita
com Magnific ou 3D. A trajetória da página já está definida; esse asset
substitui apenas a camada `flight-drone-body`.
