import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
    subsets: ["latin"],
    variable: "--font-inter",
});

export const metadata: Metadata = {
    title: "MAI - Marketing Artificial Intelligence",
    description:
        "Decisões de Marketing que Protegem Caixa e Aceleram Crescimento. IA Estratégica de Decisão para Marketing e Crescimento.",
    keywords: [
        "MAI",
        "Marketing AI",
        "Decision Intelligence",
        "Growth",
        "Marketing Strategy",
        "Capital Efficiency",
    ],
    authors: [{ name: "MAI Engineering", url: "https://mai.ai" }],
    openGraph: {
        title: "MAI - Marketing Artificial Intelligence",
        description:
            "Decisões de Marketing que Protegem Caixa e Aceleram Crescimento",
        url: "https://mai.ai",
        siteName: "MAI",
        locale: "pt_BR",
        type: "website",
    },
    twitter: {
        card: "summary_large_image",
        title: "MAI - Marketing Artificial Intelligence",
        description:
            "Decisões de Marketing que Protegem Caixa e Aceleram Crescimento",
    },
    robots: {
        index: true,
        follow: true,
    },
};

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="pt-BR" className={inter.variable}>
            <body className="antialiased bg-dark-950 text-white">{children}</body>
        </html>
    );
}
