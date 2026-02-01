import { Navigation } from "@/components/landing/Navigation";
import { Hero } from "@/components/landing/Hero";
import { Problem } from "@/components/landing/Problem";
import { BeforeAfter } from "@/components/landing/BeforeAfter";
import { HowItWorks } from "@/components/landing/HowItWorks";
import { Benefits } from "@/components/landing/Benefits";
import { UseCases } from "@/components/landing/UseCases";
import { CTA } from "@/components/landing/CTA";
import { Footer } from "@/components/landing/Footer";

export default function Home() {
    return (
        <main className="min-h-screen bg-dark-950">
            <Navigation />
            <Hero />
            <Problem />
            <BeforeAfter />
            <HowItWorks />
            <Benefits />
            <UseCases />
            <CTA />
            <Footer />
        </main>
    );
}
