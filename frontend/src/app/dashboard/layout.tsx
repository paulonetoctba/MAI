import { Sidebar } from "@/components/dashboard/Sidebar";
import { Header } from "@/components/dashboard/Header";

export default function DashboardLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="min-h-screen bg-dark-950">
            {/* Sidebar */}
            <Sidebar />

            {/* Main Content */}
            <div className="pl-64 transition-all duration-300">
                <Header />
                <main className="p-6">{children}</main>
            </div>
        </div>
    );
}
