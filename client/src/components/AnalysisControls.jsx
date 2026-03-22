import { Play, Target, Settings, Loader } from "lucide-react";

export default function AnalysisControls({
  columns,
  target,
  problemType,
  onTargetChange,
  onProblemTypeChange,
  onRunAnalysis,
  loading,
}) {
  if (!columns) return null;

  return (
    <div className="retro-card">
      <div className="flex items-center gap-2 mb-4">
        <Settings className="w-4 h-4 text-retro-amber" />
        <h3 className="font-mono text-sm text-retro-amber font-bold uppercase tracking-wider">
          ▸ Analysis Configuration
        </h3>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div>
          <label className="font-mono text-xs text-retro-muted block mb-2 uppercase tracking-wider">
            <Target className="w-3 h-3 inline mr-1" />
            Target Column
          </label>
          <select
            className="retro-select w-full"
            value={target}
            onChange={(e) => onTargetChange(e.target.value)}
          >
            {columns.map((col) => (
              <option key={col} value={col}>{col}</option>
            ))}
          </select>
        </div>

        <div>
          <label className="font-mono text-xs text-retro-muted block mb-2 uppercase tracking-wider">
            Problem Type
          </label>
          <select
            className="retro-select w-full"
            value={problemType}
            onChange={(e) => onProblemTypeChange(e.target.value)}
          >
            <option value="classification">Classification</option>
            <option value="regression">Regression</option>
          </select>
        </div>
      </div>

      <button
        className="retro-btn flex items-center gap-2"
        onClick={onRunAnalysis}
        disabled={loading}
      >
        {loading ? (
          <Loader className="w-4 h-4 animate-spin" />
        ) : (
          <Play className="w-4 h-4" />
        )}
        {loading ? "Analyzing..." : "Run Analysis"}
      </button>
    </div>
  );
}