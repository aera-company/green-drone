import { Hero } from "@/components/sections/Hero";
import { AnimatedSection, AnimatedItem } from "@/components/ui/AnimatedSection";
import { SectionLabel } from "@/components/ui/SectionLabel";
import { Button } from "@/components/ui/Button";

export default function Home() {
  return (
    <main>
      <Hero />

      {/* Seção de exemplo pós-hero. Demonstra o reveal escalonado + os
          componentes de UI (SectionLabel, Button). Substitua conforme o projeto. */}
      <section className="px-6 py-24 md:px-12 md:py-32">
        <AnimatedSection className="mx-auto flex max-w-[1100px] flex-col gap-6">
          <AnimatedItem>
            <SectionLabel>Próxima seção</SectionLabel>
          </AnimatedItem>
          <AnimatedItem>
            <h2 className="max-w-[18ch] font-sans text-4xl font-semibold leading-[1.05] tracking-tighter text-foreground md:text-6xl">
              A partir daqui você constrói o resto da página.
            </h2>
          </AnimatedItem>
          <AnimatedItem>
            <p className="max-w-[55ch] font-sans text-base leading-relaxed text-muted">
              Use <code className="text-foreground">&lt;AnimatedSection&gt;</code> e{" "}
              <code className="text-foreground">&lt;AnimatedItem&gt;</code> para
              revelar conteúdo no scroll. Componentes prontos em{" "}
              <code className="text-foreground">src/components/ui</code>:{" "}
              <code className="text-foreground">Button</code>,{" "}
              <code className="text-foreground">SectionLabel</code>,{" "}
              <code className="text-foreground">Placeholder</code>,{" "}
              <code className="text-foreground">VideoMedia</code>,{" "}
              <code className="text-foreground">ScrollRevealText</code>.
            </p>
          </AnimatedItem>
          <AnimatedItem className="mt-2 flex flex-wrap gap-3">
            <Button href="#">Começar</Button>
            <Button href="#" variant="outline">
              Documentação
            </Button>
          </AnimatedItem>
        </AnimatedSection>
      </section>
    </main>
  );
}
