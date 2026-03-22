import { BarChart2 } from "lucide-react";

export default function HistogramCharts({ histograms }) {
    if (!histograms || histograms.length === 0) return null;

    return (
        <div className="retro-card">
            <div className="flex items-center gap-2 mb-1">
                <BarChart2 className="w-4 h-4 text-retro-cyan" />
                <h3 className="font-mono text-sm text-retro-cyan font-bold uppercase tracking-wider">
                    ▸ Distribution Histograms
                </h3>
            </div>
            <p className="font-mono text-xs text-retro-muted mb-6">
                Shows how values are distributed across each numeric feature
            </p>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {histograms.map((img, idx) => (
                    <div key={idx} className="border border-retro-border rounded overflow-hidden">
                        <img
                            src={`data:image/png;base64,${img}`}
                            alt={`Histogram ${idx + 1}`}
                            className="w-full"
                        />
                    </div>
                ))}
            </div>
        </div>
    );
}