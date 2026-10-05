"use client";

import Image from "next/image";
import { useEffect, useRef } from "react";

type FlightPoint = { at: number; x: number; y: number; scale: number; rotate: number };

const desktopFlight: FlightPoint[] = [
  { at: 0, x: 69, y: 55, scale: 1, rotate: -7 },
  { at: 0.19, x: 72, y: 43, scale: 0.86, rotate: 7 },
  { at: 0.38, x: 78, y: 72, scale: 0.60, rotate: 13 },
  { at: 0.47, x: 34, y: 74, scale: 0.59, rotate: -15 },
  { at: 0.54, x: 30, y: 55, scale: 0.66, rotate: -12 },
  { at: 0.68, x: 57, y: 79, scale: 0.43, rotate: 10 },
  { at: 0.81, x: 87, y: 117, scale: 0.18, rotate: 24 },
  { at: 1, x: 105, y: 135, scale: 0.1, rotate: 24 },
];

const mobileFlight: FlightPoint[] = [
  { at: 0, x: 61, y: 70, scale: 0.78, rotate: -8 },
  { at: 0.19, x: 67, y: 69, scale: 0.66, rotate: 6 },
  { at: 0.38, x: 78, y: 86, scale: 0.46, rotate: 12 },
  { at: 0.54, x: 60, y: 86, scale: 0.50, rotate: -11 },
  { at: 0.68, x: 70, y: 91, scale: 0.34, rotate: 10 },
  { at: 0.81, x: 96, y: 118, scale: 0.14, rotate: 24 },
  { at: 1, x: 110, y: 135, scale: 0.08, rotate: 24 },
];

const clamp = (n: number) => Math.min(1, Math.max(0, n));
const ramp = (n: number, a: number, b: number) => clamp((n - a) / (b - a));
const mix = (a: number, b: number, t: number) => a + (b - a) * t;

function flightAt(progress: number, mobile: boolean): FlightPoint {
  const points = mobile ? mobileFlight : desktopFlight;
  for (let i = 0; i < points.length - 1; i++) {
    const from = points[i];
    const to = points[i + 1];
    if (progress <= to.at) {
      const t = ramp(progress, from.at, to.at);
      const eased = t * t * (3 - 2 * t);
      return {
        at: progress,
        x: mix(from.x, to.x, eased),
        y: mix(from.y, to.y, eased),
        scale: mix(from.scale, to.scale, eased),
        rotate: mix(from.rotate, to.rotate, eased),
      };
    }
  }
  return points[points.length - 1];
}

function sceneOpacity(progress: number, index: number) {
  switch (index) {
    case 0: return 1 - ramp(progress, 0.17, 0.25);
    case 1: return ramp(progress, 0.18, 0.26) * (1 - ramp(progress, 0.36, 0.44));
    case 2: return ramp(progress, 0.38, 0.46) * (1 - ramp(progress, 0.57, 0.65));
    case 3: return ramp(progress, 0.59, 0.68) * (1 - ramp(progress, 0.87, 0.90));
    default: return 1;
  }
}

function contentOpacity(progress: number, index: number) {
  switch (index) {
    case 0: return 1 - ramp(progress, 0.15, 0.20);
    case 1: return ramp(progress, 0.23, 0.29) * (1 - ramp(progress, 0.34, 0.39));
    case 2: return ramp(progress, 0.43, 0.49) * (1 - ramp(progress, 0.55, 0.60));
    case 3: return ramp(progress, 0.65, 0.70) * (1 - ramp(progress, 0.83, 0.88));
    default: return ramp(progress, 0.83, 0.89);
  }
}

const emailHref =
  "mailto:andre.barbosa@gaveagroup.com?subject=Avalia%C3%A7%C3%A3o%20de%20inspe%C3%A7%C3%A3o%20com%20drone";

export function Hero() {
  const storyRef = useRef<HTMLElement | null>(null);
  const droneRef = useRef<HTMLDivElement | null>(null);
  const sceneRefs = useRef<(HTMLElement | null)[]>([]);
  const progressRef = useRef<HTMLDivElement | null>(null);
  const progressUiRef = useRef<HTMLDivElement | null>(null);
  const chapterRef = useRef<HTMLSpanElement | null>(null);
  const photoRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      sceneRefs.current.forEach((scene) => {
        if (!scene) return;
        scene.inert = false;
        scene.setAttribute("aria-hidden", "false");
      });
      return;
    }
    let scheduled = 0;

    const update = () => {
      scheduled = 0;
      const story = storyRef.current;
      const drone = droneRef.current;
      if (!story || !drone) return;

      const range = Math.max(1, story.offsetHeight - window.innerHeight);
      const progress = clamp(-story.getBoundingClientRect().top / range);
      const point = flightAt(progress, window.innerWidth < 720);
      drone.style.transform =
        "translate3d(" + point.x + "vw, " + point.y +
        "vh, 0) translate(-50%, -50%) scale(" + point.scale +
        ") rotate(" + point.rotate + "deg)";
      drone.style.opacity = String(1 - ramp(progress, 0.64, 0.76));

      sceneRefs.current.forEach((scene, index) => {
        if (!scene) return;
        const opacity = sceneOpacity(progress, index);
        const textOpacity = contentOpacity(progress, index);
        scene.style.opacity = String(opacity);
        if (index === 4) {
          scene.style.transform = "translate3d(0," + ((1 - ramp(progress, 0.78, 0.87)) * 100) + "%,0)";
        }
        scene.style.pointerEvents = textOpacity > 0.7 ? "auto" : "none";
        scene.inert = textOpacity < 0.7;
        scene.setAttribute("aria-hidden", textOpacity < 0.7 ? "true" : "false");
        const content = scene.querySelector<HTMLElement>(".scene-content");
        if (content) {
          content.style.opacity = String(textOpacity);
          content.style.transform = "translate3d(0," + ((1 - textOpacity) * 32) + "px,0)";
        }
        if (index === 0) {
          const note = scene.querySelector<HTMLElement>(".scene-side-note");
          if (note) note.style.opacity = String(textOpacity);
        }
        if (index === 3) {
          const gallery = scene.querySelector<HTMLElement>(".result-gallery");
          if (gallery) gallery.style.opacity = String(1 - ramp(progress, 0.83, 0.87));
        }
      });

      if (photoRef.current) {
        photoRef.current.style.transform =
          "scale(" + (1.04 + progress * 0.18) + ")";
      }
      const lightScene = progress < 0.18 || (progress > 0.44 && progress < 0.59) || progress > 0.78;
      if (progressUiRef.current) progressUiRef.current.style.color = lightScene ? "#34683f" : "#bde85e";
      if (progressRef.current) {
        progressRef.current.style.transform =
          (window.innerWidth < 720 ? "scaleX(" : "scaleY(") + progress + ")";
        progressRef.current.style.background = lightScene ? "#34683f" : "#bde85e";
      }
      const gallery = sceneRefs.current[3]?.querySelectorAll<HTMLElement>(".result-gallery figure");
      gallery?.forEach((figure, index) => {
        const reveal = ramp(progress, 0.62 + index * 0.035, 0.73 + index * 0.035);
        figure.style.transform = "translate3d(0," + ((1 - reveal) * (index ? 90 : 55)) + "px,0)";
      });
      if (chapterRef.current) {
        chapterRef.current.textContent =
          String(Math.min(5, Math.floor(progress * 5) + 1)).padStart(2, "0") + " / 05";
      }
    };

    const schedule = () => {
      if (!scheduled) scheduled = requestAnimationFrame(update);
    };
    window.addEventListener("scroll", schedule, { passive: true });
    window.addEventListener("resize", schedule);
    schedule();
    return () => {
      window.removeEventListener("scroll", schedule);
      window.removeEventListener("resize", schedule);
      if (scheduled) cancelAnimationFrame(scheduled);
    };
  }, []);

  return (
    <section ref={storyRef} id="inicio" className="flight-story" aria-label="Inspeção com drones da Gávea Green Tech">
      <div className="flight-sticky">
        <div className="flight-grid" aria-hidden="true" />
        <header className="flight-header">
          <a href="#inicio" className="flight-brand" aria-label="Gávea Green Tech, início">
            <Image src="/media/gavea-green-tech-logo.png" alt="" width={2048} height={593} priority />
          </a>
          <div className="flight-header-label">INSPEÇÃO ROBOTIZADA <span>/</span> INDÚSTRIA</div>
          <a className="flight-header-cta" href="#contato" aria-label="Falar sobre um ativo">Falar sobre um ativo <span aria-hidden="true">↗</span></a>
        </header>

        <article ref={(el) => { sceneRefs.current[0] = el; }} className="flight-scene scene-intro">
          <div className="scene-intro-glow" aria-hidden="true" />
          <div className="scene-content">
            <p className="scene-eyebrow"><span>01 / 05</span> Acesso que vira informação</p>
            <h1>PRIMEIRO,<br /><em>O DRONE.</em></h1>
            <p className="scene-lead">Inspeção de espaços confinados com imagens e dados para decidir antes da entrada da equipe.</p>
            <a href="#contato" className="scene-link">Solicitar avaliação técnica <span aria-hidden="true">↗</span></a>
          </div>
          <Image className="flight-static" src="/media/drone-cutout.png" alt="Drone de inspeção da Gávea Green Tech" width={1000} height={667} priority />
          <p className="scene-side-note">TANQUES · SILOS · CALDEIRAS · GALERIAS</p>
        </article>

        <article ref={(el) => { sceneRefs.current[1] = el; }} className="flight-scene scene-access" aria-hidden="true" inert>
          <div ref={photoRef} className="scene-access-photo">
            <Image src="/media/industrial-vessel-empty.png" alt="" fill sizes="100vw" />
          </div>
          <div className="scene-access-shade" />
          <div className="scene-content">
            <p className="scene-eyebrow"><span>02 / 05</span> Aplicações</p>
            <h2>O interior<br />não precisa<br /><em>esperar.</em></h2>
            <p>O drone leva a inspeção visual aos pontos de acesso complexo. Sua equipe vê o ativo antes de definir o próximo passo.</p>
            <div className="application-list" aria-label="Exemplos de ativos">
              <span>Tanques</span><span>Silos</span><span>Caldeiras</span><span>Galerias</span>
            </div>
          </div>
        </article>

        <article ref={(el) => { sceneRefs.current[2] = el; }} className="flight-scene scene-difference" aria-hidden="true" inert>
          <div className="scene-difference-image">
            <Image src="/media/drone-em-tubulacao.jpg" alt="Drone inspecionando a parede interna de um ativo" fill sizes="(max-width: 720px) 100vw, 50vw" />
          </div>
          <div className="scene-content">
            <p className="scene-eyebrow"><span>03 / 05</span> Diferenciais</p>
            <h2>POUCA LUZ.<br />SEM GPS.<br /><em>COM VISÃO.</em></h2>
            <p>Câmera e iluminação para registrar o interior em ambientes desafiadores, com operação remota e menor necessidade de acesso humano inicial.</p>
            <div className="difference-points"><span>01 / Acesso remoto</span><span>02 / Registro visual</span><span>03 / Base para análise</span></div>
          </div>
        </article>

        <article ref={(el) => { sceneRefs.current[3] = el; }} className="flight-scene scene-results" aria-hidden="true" inert>
          <div className="scene-content">
            <p className="scene-eyebrow"><span>04 / 05</span> Resultado da inspeção</p>
            <h2>O QUE ELE VÊ<br /><em>VIRA DECISÃO.</em></h2>
            <p>Capturas do interior e dados de inspeção ajudam a documentar a condição do ativo e orientar a análise técnica.</p>
          </div>
          <div className="result-gallery">
            <figure>
              <div className="result-image"><Image src="/media/monitoramento.jpg" alt="Tela de monitoramento e mapeamento espacial da inspeção" fill sizes="(max-width: 720px) 90vw, 46vw" /></div>
              <figcaption><span>01</span> Monitoramento</figcaption>
            </figure>
            <figure>
              <div className="result-image"><Image src="/media/resultados-inspecao.jpg" alt="Registro visual e representação espacial de uma inspeção" fill sizes="(max-width: 720px) 90vw, 35vw" /></div>
              <figcaption><span>02</span> Evidências do ativo</figcaption>
            </figure>
          </div>
        </article>

        <article ref={(el) => { sceneRefs.current[4] = el; }} className="flight-scene scene-contact" aria-hidden="true" inert>
          <div className="scene-content">
            <p className="scene-eyebrow"><span>05 / 05</span> Próximo passo</p>
            <h2>QUAL ATIVO<br />VOCÊ PRECISA<br /><em>ENXERGAR?</em></h2>
            <p>Conte o desafio de acesso. A Gávea Green Tech ajuda a definir a abordagem de inspeção.</p>
            <div className="contact-actions">
              <a href={emailHref} className="contact-main">Solicitar avaliação técnica <span aria-hidden="true">↗</span></a>
              <a href="https://wa.me/5521999115741" target="_blank" rel="noopener noreferrer" className="contact-alt">Conversar pelo WhatsApp ↗</a>
            </div>
          </div>
          <div className="contact-orbit" aria-hidden="true" />
          <footer>GÁVEA GREEN TECH <span>INSPEÇÃO ROBOTIZADA PARA ATIVOS CRÍTICOS</span></footer>
        </article>

        <div ref={droneRef} className="flight-drone" aria-hidden="true">
          <div className="flight-drone-body">
            <Image src="/media/drone-cutout.png" alt="" width={1000} height={667} priority />
          </div>
          <div className="flight-drone-halo" />
        </div>
        <div ref={progressUiRef} className="flight-progress" aria-hidden="true">
          <span ref={chapterRef}>01 / 05</span>
          <div className="flight-progress-track"><div ref={progressRef} /></div>
          <span>SCROLL TO EXPLORE ↓</span>
        </div>
      </div>
      <div id="contato" className="flight-contact-anchor" aria-hidden="true" />
    </section>
  );
}
