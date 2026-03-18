import { BarChart3, TrendingUp } from "lucide-react";

export default function StatisticsPanel({ statistics }) {
  if (!statistics || Object.keys(statistics).length === 0) return null;

  const columns = Object.keys(statistics);

  return (
    <div className="retro-card">
      <div className="flex items-center gap-2 mb-1">
        <BarChart3 className="w-4 h-4 text-retro-cyan" />
        <h3 className="font-mono text-sm text-retro-cyan font-bold uppercase tracking-wider">
          ▸ Statistics
        </h3>
      </div>
      <p className="font-mono text-xs text-retro-muted mb-6">
        Descriptive statistics for numeric columns
      </p>

      <div className="space-y-6">
        {columns.map((col) => {
          const s = statistics[col];
          if (!s) return null;

          const items = [
            { label: "Mean", value: s.mean },
            { label: "Std Dev", value: s.std },
            { label: "Min", value: s.min },
            { label: "Max", value: s.max },
            { label: "Median", value: s["50%"] },
            { label: "Count", value: s.count },
          ].filter((item) => item.value != null);

          return (
            <div key={col}>
              <h4 className="font-mono text-sm text-retro-text font-bold mb-3 flex items-center gap-2">
                <TrendingUp className="w-3 h-3 text-retro-green" />
                {col}
              </h4>
              <div className="grid gap-3 grid-cols-2 lg:grid-cols-3">
                {items.map((item) => (
                  <div key={item.label} className="stat-card">
                    <p className="font-mono text-xs text-retro-muted mb-1 uppercase">{item.label}</p>
                    <p className="font-mono text-lg text-retro-text font-bold">
                      {typeof item.value === "number" ? item.value.toFixed(2) : item.value}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
