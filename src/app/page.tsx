import Image from "next/image";
import { DroneSequence } from "@/components/motion/DroneSequence";
import { AmbientVideo } from "@/components/motion/AmbientVideo";
import { ScrollScene } from "@/components/motion/ScrollScene";
import { SiteHeader } from "@/components/landing/SiteHeader";
import { display, text } from "@/lib/fonts";
import "@/styles/sequence.css";
import "@/styles/landing.css";

// Contato confirmado pela Gávea em 05/10: só nome e e-mail (sem telefone/WhatsApp).
const PERSON = "André Barbosa";
const EMAIL = "andre.barbosa@gaveagroup.com";
const MAILTO = `mailto:${EMAIL}?subject=${encodeURIComponent("Inspeção com drone")}`;
const SOURCE = "Imagem do material da Gávea";

// Todo o texto abaixo vem da apresentação Gávea Green Tech (PDF, pp. 2–7), resumido.
// Capacidades e serviços: REQUIRES_GAVEA_VALIDATION por equipamento antes de publicar.

const PLACES = ["Tanques", "Silos", "Chaminés", "Galerias", "Caldeiras"];

const INSIDE = ["Sistema de voo anticolisão", "Sistema de iluminação embarcado", "Tempo de voo ilimitado"];

const CONFINED_SERVICES = [
  "Medição de espessura por ultrassom (UT)",
  "Inspeção visual de alta resolução (RVI)",
  "Inspeção de gases",
  "Termografia",
  "Inspeção de radiação (NORM)",
  "Modelagem LiDAR 3D (digital twin)",
];

// Registros originais do PDF, sem edição de pixels. Legendas descrevem só o que se vê.
const RECORD = [
  {
    t: "Capturar",
    d: "Vídeo em alta resolução (4K) e coleta estruturada de dados confiáveis.",
    src: "/media/captura-e-representacao.jpg", w: 2048, h: 1018,
    caption: "Imagem da câmera e representação 3D lado a lado",
  },
  {
    t: "Acompanhar ao vivo",
    d: "Transmissão em tempo real durante o voo (live feed).",
    src: "/media/registro-tablet.jpg", w: 1000, h: 419,
    caption: "Tela de inspeção no tablet de operação",
  },
  {
    t: "Revisar em 3D",
    d: "Revisão interativa com trajetória de voo, pontos de interesse e coordenadas UTM.",
    src: "/media/resultados-inspecao.jpg", w: 1500, h: 797,
    caption: "Registro e representação espacial",
  },
  {
    t: "Guardar e compartilhar",
    d: "Dados gerenciados e armazenados com segurança na nuvem, prontos para revisão, análise e compartilhamento.",
    src: "/media/monitoramento.jpg", w: 2048, h: 858,
    caption: "Visualização dos dados no tablet",
  },
];

// Os seis serviços de altura (PDF p. 5), agrupados pela foto que melhor os mostra.
const HEIGHT_ROWS = [
  {
    t: "Dutos e tubulações",
    d: "Medição de espessura com o drone em contato com a superfície, sem andaimes nem acesso por corda.",
    services: ["Medição de espessura (UT, UT de alta temperatura, EMAT, PEC)"],
    src: "/media/altura-duto.jpg", alt: "Drone pousado sobre uma tubulação elevada, contra o céu azul",
  },
  {
    t: "Torres, chaminés e estruturas",
    d: "Imagem e geometria de estruturas altas, fachadas e pontes.",
    services: ["Inspeção visual de alta resolução (RVI)", "Aerofotogrametria 3D", "Mapeamento LiDAR 3D, nuvem de pontos e digital twin"],
    src: "/media/altura-chamine.jpg", alt: "Drone ao lado de uma chaminé industrial com fumaça",
  },
  {
    t: "Flares",
    d: "Leitura térmica e de gases a partir do ar.",
    services: ["Termografia aérea", "Inspeção de gases (sniffing)"],
    src: "/media/altura-flare.jpg", alt: "Imagem térmica de um flare em operação",
  },
];

const SUBSEA_PLACES = ["Cascos", "Tanques e reservatórios", "Portos e amarras", "Barragens", "Tubulações e risers", "ETA/ETE"];

// MOTION_SIMULATION: gerados no Magnific a partir da foto do ROV no PDF.
const ROV_SCENES = [
  { src: "/media/rov-amarras.webp", caption: "Amarras", alt: "Simulação: o mini-ROV ilumina uma corrente de amarração coberta de ferrugem" },
  { src: "/media/rov-porto.webp", caption: "Estacas de píer", alt: "Simulação: o mini-ROV ilumina uma estaca de píer coberta de cracas" },
  { src: "/media/rov-reservatorio.webp", caption: "Reservatórios e tubulações", alt: "Simulação: o mini-ROV ilumina a boca de uma tubulação dentro de um reservatório" },
];

const SUBSEA_SERVICES = [
  "Inspeção de espessura",
  "Inspeção de potencial eletroquímico",
  "Inspeção visual (RVI)",
  "Limpeza subaquática",
  "Mapeamento 3D (digital twin)",
  "Inspeção ambiental",
];

const BENEFITS = [
  "Equipe fora do ambiente de risco",
  "Menor POB, com equipe reduzida",
  "Menos andaimes, escaladas e seguros",
  "Menor downtime",
  "Inspeções mais rápidas",
  "Maior precisão dos dados",
  "Análise preditiva de falhas estruturais e monitoramento de integridade",
  "Mais segurança operacional",
];

export default function Home() {
  return (
    <main id="inicio" className={`mp gg ${display.variable} ${text.variable}`}>
      <SiteHeader />

      {/* 01 Revelar + Acesso acontecem dentro da tomada do drone */}
      <DroneSequence
        label="Inspeção com drone: o equipamento se aproxima e entra em um espaço confinado"
        reveal={
          <>
            <p className="mp-eyebrow">Drones para inspeção industrial</p>
            <h1 className="mp-title">O drone entra.<br />A evidência aparece.</h1>
            <p className="mp-support">
              Inspeção visual em espaços confinados, com imagens de alta resolução e acompanhamento da operação.
            </p>
            <a href="#contato" className="gg-cta">Avaliar meu ativo</a>
          </>
        }
        enter={
          <>
            <p className="mp-eyebrow mp-eyebrow--dark">01 / Acesso</p>
            <h2 className="mp-title mp-title--dark">Acesse o que é difícil inspecionar.</h2>
            <p className="mp-support mp-support--dark">
              Tanques, silos, chaminés, galerias e caldeiras. Ambientes com pouco espaço, baixa iluminação, obstáculos ou sem GPS.
            </p>
          </>
        }
      />

      {/* 01 Acesso, continuação: a abertura vira a foto real do equipamento no poço */}
      <ScrollScene className="gg-opening" tone="dark" header="clear" labelledBy="sem-entrada">
        <div className="gg-opening-stage">
          <figure className="gg-opening-photo">
            <Image
              src="/media/acesso-poco.jpg" alt="Drone com proteções nas hélices dentro de um poço metálico escuro"
              fill sizes="100vw" />
            <figcaption className="gg-tag">{SOURCE}</figcaption>
          </figure>
          <div className="gg-opening-copy">
            <h2 id="sem-entrada" className="gg-h2 gg-h2--dark">Sem entrada humana.</h2>
            <p className="gg-lead gg-lead--dark">
              Soluções para ambientes confinados, sem sinal de GPS, com baixa iluminação e obstáculos complexos.
            </p>
          </div>
        </div>
      </ScrollScene>

      <section className="gg-access" data-tone="dark" aria-label="Onde o drone atua e o que ele registra">
        <ScrollScene className="gg-places-wrap" mode="through" tone="dark">
          <div className="gg-places">
            <p className="gg-kicker">Onde atua</p>
            <ul className="gg-places-list">
              {PLACES.map((p, i) => (
                <li key={p} style={{ ["--i" as string]: i }}>{p}</li>
              ))}
            </ul>
            <p className="gg-note">Inspeção sem necessidade de entrada humana.</p>
          </div>
          <figure className="gg-places-photo">
            <Image src="/media/acesso-iluminacao.jpg" alt="Drone visto de baixo com duas luzes fortes acesas no escuro"
              width={1000} height={419} sizes="(max-aspect-ratio: 1/1) 100vw, 48vw" />
            <figcaption><span>Iluminação embarcada no escuro</span><span className="gg-source">{SOURCE}</span></figcaption>
          </figure>
        </ScrollScene>

        <div className="gg-inside">
          <div className="gg-inside-photos">
            <figure className="gg-inside-a">
              <Image src="/media/acesso-tunel.jpg" alt="Drone de frente em um túnel, com duas luzes acesas e cabo de amarração"
                width={2048} height={1196} sizes="(max-aspect-ratio: 1/1) 100vw, 40vw" />
              <figcaption><span>Voo em galeria</span><span className="gg-source">{SOURCE}</span></figcaption>
            </figure>
            <figure className="gg-inside-b">
              <Image src="/media/drone-em-tubulacao.jpg" alt="Drone de perfil com a ferramenta frontal encostada em uma parede metálica"
                width={2048} height={1179} sizes="(max-aspect-ratio: 1/1) 100vw, 34vw" />
              <figcaption><span>Contato com a parede</span><span className="gg-source">{SOURCE}</span></figcaption>
            </figure>
          </div>
          <div className="gg-inside-copy">
            <p className="gg-kicker">Como trabalha lá dentro</p>
            <ul className="gg-facts">
              {INSIDE.map((f) => <li key={f}>{f}</li>)}
            </ul>
            <p className="gg-kicker gg-kicker--gap">O que mede e registra</p>
            <ol className="gg-services gg-services--dark">
              {CONFINED_SERVICES.map((s, i) => (
                <li key={s}><span>{String(i + 1).padStart(2, "0")}</span>{s}</li>
              ))}
            </ol>
          </div>
        </div>
      </section>

      {/* 02 Registro: cena presa, quatro passos, a luz acende ao entrar */}
      <ScrollScene className="gg-record" steps={RECORD.length} tone={{ from: "dark", to: "light", at: -0.14 }} labelledBy="registro">
        <div className="gg-record-stage">
          <div className="gg-record-copy">
            <p className="mp-eyebrow">02 / Registro</p>
            <h2 id="registro" className="gg-h2">Veja durante o voo.<br />Revise depois.</h2>
            <ol className="gg-steps">
              {RECORD.map((r, i) => (
                <li key={r.t} data-i={i}>
                  <span className="gg-step-n">{String(i + 1).padStart(2, "0")}</span>
                  <div>
                    <h3>{r.t}</h3>
                    <p>{r.d}</p>
                  </div>
                </li>
              ))}
            </ol>
          </div>
          <div className="gg-record-media">
            {RECORD.map((r, i) => (
              <figure key={r.src} data-i={i}>
                <div className="gg-record-frame">
                  <Image src={r.src} alt={r.caption} width={r.w} height={r.h} sizes="(max-aspect-ratio: 1/1) 100vw, 58vw" />
                </div>
                <figcaption><span>{r.caption}</span><span className="gg-source">{SOURCE}</span></figcaption>
              </figure>
            ))}
          </div>
        </div>
      </ScrollScene>

      {/* 03 Em altura: faixas que grudam e se empilham (referência: price-pierce.co.uk, seção 04) */}
      <section className="gg-height" data-tone="light" aria-labelledby="altura">
        <header className="gg-height-head">
          <p className="mp-eyebrow">03 / Em altura</p>
          <h2 id="altura" className="gg-h2">Em altura e áreas externas.</h2>
          <p className="gg-lead">
            Flares, torres, dutos e tubulações, fachadas, pontes e estruturas metálicas, sem andaimes nem acesso por corda.
          </p>
        </header>
        <div className="gg-rows">
          {HEIGHT_ROWS.map((r, i) => (
            <article key={r.t} className="gg-row">
              <figure className="gg-row-media">
                <Image src={r.src} alt={r.alt} fill sizes="(max-aspect-ratio: 1/1) 100vw, 66vw" />
                <h3>{r.t}</h3>
                <figcaption className="gg-tag">{SOURCE}</figcaption>
              </figure>
              <div className="gg-row-copy">
                <span className="gg-row-n">{String(i + 1).padStart(2, "0")}</span>
                <p>{r.d}</p>
                <ul className="gg-services gg-services--compact">
                  {r.services.map((x) => <li key={x}>{x}</li>)}
                </ul>
              </div>
            </article>
          ))}
        </div>
      </section>

      {/* 04 Subaquático: segunda abertura. A água sobe, o drone fica no ar, o ROV assume */}
      <ScrollScene className="gg-dive" tone={{ from: "light", to: "dark", at: 0.49 }} header="clear" labelledBy="subaquatico">
        <div className="gg-dive-stage">
          <div className="gg-dive-air" aria-hidden="true">
            <Image src="/media/drone-cutout.png" alt="" width={1000} height={667} sizes="(max-aspect-ratio: 1/1) 100vw, 56vw" />
          </div>
          <div className="gg-dive-copy gg-dive-copy--air">
            <p className="mp-eyebrow">Do ar para debaixo d&apos;água</p>
            <p className="gg-dive-line">No ar e em espaços confinados, o drone.</p>
          </div>
          <div className="gg-dive-water">
            {/* MOTION_SIMULATION: gerado no Magnific (Seedance 2.5) a partir da foto do ROV no PDF */}
            <AmbientVideo
              className="gg-dive-video" src="/media/rov-casco.mp4" poster="/media/rov-casco.webp"
              label="Simulação: mini-ROV com as luzes acesas inspeciona o casco submerso de um navio" />
            <span className="gg-tag">Simulação visual a partir da foto do equipamento</span>
          </div>
          <div className="gg-dive-copy gg-dive-copy--sea">
            <p className="mp-eyebrow mp-eyebrow--dark">04 / Subaquático</p>
            <h2 id="subaquatico" className="mp-title gg-dive-title">Debaixo d&apos;água,<br />o mini-ROV.</h2>
            <p className="mp-support mp-support--dark">
              Inspeção e monitoramento sub-sea de cascos, portos, barragens, reservatórios e risers.
            </p>
          </div>
        </div>
      </ScrollScene>

      {/* 04 Subaquático, detalhe do equipamento */}
      <section className="gg-rov" data-tone="dark" aria-label="O mini-ROV: onde atua e o que registra">
        <div className="gg-rov-top">
          <figure className="gg-rov-unit">
            <Image src="/media/rov-recorte.webp" alt="O mini-ROV preto e amarelo, com câmeras e luzes frontais e propulsores laterais"
              width={1047} height={644} sizes="(max-aspect-ratio: 1/1) 100vw, 50vw" />
            <figcaption><span>O equipamento</span><span className="gg-source">{SOURCE}</span></figcaption>
          </figure>
          <div className="gg-rov-copy">
            <ScrollScene className="gg-rov-places" mode="through" tone="dark">
              <p className="gg-kicker">Onde atua</p>
              <ul className="gg-places-list gg-places-list--sm">
                {SUBSEA_PLACES.map((p, i) => (
                  <li key={p} style={{ ["--i" as string]: i }}>{p}</li>
                ))}
              </ul>
            </ScrollScene>
            <p className="gg-kicker gg-kicker--gap">O que mede e registra</p>
            <ol className="gg-services gg-services--dark">
              {SUBSEA_SERVICES.map((x, i) => (
                <li key={x}><span>{String(i + 1).padStart(2, "0")}</span>{x}</li>
              ))}
            </ol>
          </div>
        </div>
        <div className="gg-rov-scenes">
          {ROV_SCENES.map((r) => (
            <figure key={r.src}>
              <Image src={r.src} alt={r.alt} width={928} height={1152} sizes="(max-aspect-ratio: 1/1) 100vw, 30vw" />
              <figcaption><span>{r.caption}</span><span className="gg-source">Simulação visual</span></figcaption>
            </figure>
          ))}
        </div>
      </section>

      {/* 05 Resultado */}
      <ScrollScene className="gg-results" mode="through" tone="dark" labelledBy="resultado">
        <figure className="gg-results-photo">
          <Image src="/media/equipe-campo.jpg" alt="Técnico com colete refletivo carregando uma maleta de equipamento em área industrial"
            width={1000} height={419} sizes="100vw" />
          <figcaption className="gg-tag">{SOURCE}</figcaption>
        </figure>
        <div className="gg-results-body">
          <div className="gg-results-head">
            <p className="mp-eyebrow mp-eyebrow--dark">05 / Resultado</p>
            <h2 id="resultado" className="gg-h2 gg-h2--dark">Inspeções mais seguras, inteligentes e eficientes.</h2>
            <p className="gg-lead gg-lead--dark">
              A Gávea Green une drones e ROVs à expertise técnica em inspeções e ensaios não destrutivos (END), onde o acesso humano é de alto risco ou logisticamente complexo.
            </p>
            <p className="gg-sectors">Óleo &amp; gás · Energia · Indústria</p>
          </div>
          <ul className="gg-benefits">
            {BENEFITS.map((b) => <li key={b}>{b}</li>)}
          </ul>
        </div>
      </ScrollScene>

      {/* 06 Próximo passo: drone e mini-ROV juntos, de volta à luz */}
      <section id="contato" className="gg-contact" data-tone="light" aria-labelledby="proximo-passo">
        <div className="gg-contact-copy">
          <p className="mp-eyebrow">06 / Próximo passo</p>
          <h2 id="proximo-passo" className="mp-title">Qual ativo você precisa inspecionar?</h2>
          <p className="mp-support">A equipe da Gávea avalia a aplicação. Para começar, conte:</p>
          <ol className="gg-brief-list">
            <li><span>01</span>O ativo e o ambiente</li>
            <li><span>02</span>Como é o acesso hoje</li>
            <li><span>03</span>O registro que você precisa</li>
          </ol>
          <div className="gg-contact-actions">
            <a href={MAILTO} className="gg-cta">Falar sobre meu projeto</a>
          </div>
          <address className="gg-person">
            <strong>{PERSON}</strong>
            <a href={MAILTO}>{EMAIL}</a>
          </address>
        </div>
        <div className="gg-contact-visual" aria-hidden="true">
          <Image className="gg-contact-drone" src="/media/drone-cutout.png" alt="" width={1000} height={667} sizes="(max-aspect-ratio: 1/1) 100vw, 50vw" />
          <Image className="gg-contact-rov" src="/media/rov-recorte.webp" alt="" width={1047} height={644} sizes="(max-aspect-ratio: 1/1) 60vw, 26vw" />
        </div>
      </section>

      <footer className="gg-footer" data-tone="light">
        <Image src="/brand/gavea-green.png" alt="Gávea Green" width={720} height={374} className="gg-footer-logo" />
        <p>
          <a href="https://gavea-group.com" target="_blank" rel="noopener noreferrer">gavea-group.com</a><br />
          Imagens do drone em movimento e do mini-ROV debaixo d&apos;água: simulação visual feita a partir de fotos dos equipamentos.
        </p>
      </footer>
    </main>
  );
}
