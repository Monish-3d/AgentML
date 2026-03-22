import { AlertCircle, CheckCircle2, Activity } from "lucide-react";

export default function HealthScore({ score, missingValues, skewness }) {
  if (score == null) return null;

  const status = score >= 80 ? "Excellent" : score >= 60 ? "Good" : "Needs Attention";
  const statusColor = score >= 80 ? "text-retro-green" : score >= 60 ? "text-retro-amber" : "text-retro-red";
  const barColor = score >= 80 ? "bg-retro-green" : score >= 60 ? "bg-retro-amber" : "bg-retro-red";

  const totalMissing = missingValues
    ? Object.values(missingValues).reduce((a, b) => a + b, 0)
    : 0;

  const skewedCols = skewness
    ? Object.entries(skewness).filter(([, v]) => Math.abs(v) > 1)
    : [];

  return (
    <div className="retro-card">
      <div className="flex items-center gap-2 mb-4">
        <Activity className="w-4 h-4 text-retro-amber" />
        <h3 className="font-mono text-sm text-retro-amber font-bold uppercase tracking-wider">
          Health Score
        </h3>
      </div>

      <div className="text-center mb-4">
        <span className={`font-pixel text-3xl font-bold ${statusColor}`}>{score}</span>
        <span className="font-mono text-sm text-retro-muted"> / 100</span>
      </div>

      <div className="retro-progress mb-3">
        <div
          className={`retro-progress-bar ${barColor}`}
          style={{ width: `${score}%` }}
        />
      </div>

      <p className={`font-mono text-xs text-center ${statusColor} mb-4 uppercase tracking-wider`}>
        Status: {status}
      </p>

      <div className="space-y-2 border-t border-retro-border pt-4">
        <div className="flex items-center gap-2">
          {totalMissing === 0 ? (
            <CheckCircle2 className="w-4 h-4 text-retro-green flex-shrink-0" />
          ) : (
            <AlertCircle className="w-4 h-4 text-retro-amber flex-shrink-0" />
          )}
          <span className="font-mono text-xs text-retro-muted">
            {totalMissing === 0
              ? "No missing values detected"
              : `${totalMissing} missing values found`}
          </span>
        </div>

        <div className="flex items-center gap-2">
          {skewedCols.length === 0 ? (
            <CheckCircle2 className="w-4 h-4 text-retro-green flex-shrink-0" />
          ) : (
            <AlertCircle className="w-4 h-4 text-retro-amber flex-shrink-0" />
          )}
          <span className="font-mono text-xs text-retro-muted">
            {skewedCols.length === 0
              ? "No highly skewed features"
              : `${skewedCols.length} highly skewed feature(s)`}
          </span>
        </div>
      </div>
    </div>
  );
}
