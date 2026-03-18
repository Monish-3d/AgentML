import { Database, AlertTriangle, BarChart } from "lucide-react";

export default function SummaryPanel({ summary, schema, missingValues, skewness }) {
  if (!summary) return null;

  const missingEntries = missingValues
    ? Object.entries(missingValues).map(([col, count]) => ({ column: col, missing: count }))
    : [];

  const skewnessEntries = skewness
    ? Object.entries(skewness).map(([col, val]) => ({ column: col, value: val }))
    : [];

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Dataset Overview */}
      <div className="retro-card">
        <div className="flex items-center gap-2 mb-4">
          <Database className="w-4 h-4 text-retro-green" />
          <h3 className="font-mono text-sm text-retro-green font-bold uppercase tracking-wider">
            Dataset Summary
          </h3>
        </div>
        <div className="space-y-3">
          {[
            { label: "Rows", value: summary.rows?.toLocaleString() },
            { label: "Columns", value: summary.columns },
            { label: "Numeric", value: schema?.numeric?.length ?? 0 },
            { label: "Categorical", value: schema?.categorical?.length ?? 0 },
            { label: "Text", value: schema?.text?.length ?? 0 },
          ].map((item) => (
            <div key={item.label} className="flex justify-between items-center">
              <span className="font-mono text-xs text-retro-muted uppercase">{item.label}</span>
              <span className="font-mono text-sm text-retro-text font-bold">{item.value}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Missing Values */}
      <div className="retro-card">
        <div className="flex items-center gap-2 mb-4">
          <AlertTriangle className="w-4 h-4 text-retro-amber" />
          <h3 className="font-mono text-sm text-retro-amber font-bold uppercase tracking-wider">
            Missing Values
          </h3>
        </div>
        <div className="space-y-3">
          {missingEntries.length === 0 ? (
            <p className="font-mono text-xs text-retro-muted">No data available</p>
          ) : (
            missingEntries.map((item) => (
              <div key={item.column} className="flex justify-between items-center">
                <span className="font-mono text-xs text-retro-muted">{item.column}</span>
                <span
                  className={`font-mono text-sm font-bold ${
                    item.missing > 0 ? "text-retro-amber" : "text-retro-green"
                  }`}
                >
                  {item.missing}
                </span>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Skewness */}
      <div className="retro-card">
        <div className="flex items-center gap-2 mb-4">
          <BarChart className="w-4 h-4 text-retro-purple" />
          <h3 className="font-mono text-sm text-retro-purple font-bold uppercase tracking-wider">
            Skewness
          </h3>
        </div>
        <div className="space-y-3">
          {skewnessEntries.length === 0 ? (
            <p className="font-mono text-xs text-retro-muted">No numeric columns</p>
          ) : (
            skewnessEntries.map((item) => (
              <div key={item.column} className="flex justify-between items-center">
                <span className="font-mono text-xs text-retro-muted">{item.column}</span>
                <span
                  className={`font-mono text-sm font-bold ${
                    Math.abs(item.value) > 1 ? "text-retro-red" : "text-retro-green"
                  }`}
                >
                  {item.value.toFixed(2)}
                </span>
              </div>
            ))
          )}
          <div className="mt-2 pt-2 border-t border-retro-border">
            <p className="font-mono text-xs text-retro-muted">
              |skewness| &gt; 1 indicates high skew
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}