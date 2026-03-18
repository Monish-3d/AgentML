import { Zap } from "lucide-react";

const getCorrelationColor = (value) => {
  const absValue = Math.abs(value);
  if (absValue > 0.7) return { text: "text-retro-red", bar: "bg-retro-red" };
  if (absValue > 0.5) return { text: "text-retro-amber", bar: "bg-retro-amber" };
  if (absValue > 0.3) return { text: "text-retro-cyan", bar: "bg-retro-cyan" };
  return { text: "text-retro-green", bar: "bg-retro-green" };
};

export default function CorrelationMatrix({ correlations, heatmapImage }) {
  if (!correlations || correlations.length === 0) return null;

  return (
    <div className="space-y-6">
      <div className="retro-card">
        <div className="flex items-center gap-2 mb-1">
          <Zap className="w-4 h-4 text-retro-purple" />
          <h3 className="font-mono text-sm text-retro-purple font-bold uppercase tracking-wider">
            ▸ Correlation Analysis
          </h3>
        </div>
        <p className="font-mono text-xs text-retro-muted mb-6">
          Pairwise feature correlations (Pearson coefficient)
        </p>

        <div className="space-y-2">
          {correlations.map((corr, idx) => {
            const colors = getCorrelationColor(corr.value);
            return (
              <div
                key={idx}
                className="flex items-center justify-between p-3 rounded border border-retro-border hover:bg-retro-green/5 transition"
              >
                <div className="flex items-center gap-2 flex-1 min-w-0">
                  <span className="font-mono text-xs text-retro-text">{corr.col1}</span>
                  <span className="font-mono text-xs text-retro-muted">↔</span>
                  <span className="font-mono text-xs text-retro-text">{corr.col2}</span>
                </div>

                <div className="flex items-center gap-3">
                  <div className="w-24 h-1.5 bg-retro-border rounded-full overflow-hidden">
                    <div
                      className={`h-full transition-all ${colors.bar}`}
                      style={{ width: `${Math.abs(corr.value) * 100}%` }}
                    />
                  </div>
                  <span className={`font-mono text-xs font-bold w-12 text-right ${colors.text}`}>
                    {corr.value.toFixed(2)}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Heatmap image from server */}
      {heatmapImage && (
        <div className="retro-card">
          <h3 className="font-mono text-sm text-retro-purple font-bold uppercase tracking-wider mb-4">
            ▸ Correlation Heatmap
          </h3>
          <div className="flex justify-center">
            <img
              src={`data:image/png;base64,${heatmapImage}`}
              alt="Correlation heatmap"
              className="max-w-full rounded border border-retro-border"
            />
          </div>
        </div>
      )}

      {/* Interpretation Guide */}
      <div className="retro-card">
        <h3 className="font-mono text-sm text-retro-text font-bold uppercase tracking-wider mb-4">
          Interpretation Guide
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {[
            { label: "Weak", range: "0.0 – 0.3", desc: "Features are mostly independent", color: "border-retro-green/30 text-retro-green" },
            { label: "Moderate", range: "0.3 – 0.5", desc: "Some relationship exists", color: "border-retro-cyan/30 text-retro-cyan" },
            { label: "Strong", range: "0.5 – 0.7", desc: "Features are related", color: "border-retro-amber/30 text-retro-amber" },
            { label: "Very Strong", range: "> 0.7", desc: "Multicollinearity risk", color: "border-retro-red/30 text-retro-red" },
          ].map((item) => (
            <div key={item.label} className={`p-3 rounded border ${item.color}`}>
              <p className="font-mono text-xs font-bold">{item.label}</p>
              <p className="font-mono text-xs text-retro-muted mt-1">
                {item.range}: {item.desc}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
