import { useState } from "react";
import HealthScore from "../components/HealthScore";
import StatisticsPanel from "../components/StatisticsPanel";
import { UploadDataset } from "../components/UploadDataSet";
import DatasetPreview from "../components/DatasetPreview";
import AnalysisControls from "../components/AnalysisControls";
import SummaryPanel from "../components/SummaryPanel";
import CorrelationMatrix from "../components/CorrelationMatrix";
import HistogramCharts from "../components/HistogramCharts";
import AskQuestion from "../components/AskQuestion";
import { uploadDataset, runAnalysis } from "../services/api";

const STEPS = [
  { num: 1, label: "Upload Dataset", key: "upload" },
  { num: 2, label: "Configure & Run", key: "configure" },
  { num: 3, label: "Explore Results", key: "results" },
];

export function Dashboard() {
  const [uploadData, setUploadData] = useState(null);
  const [analysisData, setAnalysisData] = useState(null);
  const [target, setTarget] = useState("");
  const [problemType, setProblemType] = useState("classification");
  const [loading, setLoading] = useState({ upload: false, analysis: false });
  const [error, setError] = useState(null);

  const currentStep = analysisData ? 3 : uploadData ? 2 : 1;

  const handleFileUpload = async (file) => {
    setError(null);
    setLoading((l) => ({ ...l, upload: true }));
    setAnalysisData(null);
    try {
      const data = await uploadDataset(file);
      setUploadData(data);
      setTarget(data.columns[data.columns.length - 1]);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading((l) => ({ ...l, upload: false }));
    }
  };

  const handleRunAnalysis = async () => {
    if (!uploadData) return;
    setError(null);
    setLoading((l) => ({ ...l, analysis: true }));
    try {
      const data = await runAnalysis(uploadData.session_id, target, problemType);
      setAnalysisData(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading((l) => ({ ...l, analysis: false }));
    }
  };

  return (
    <div className="scanlines min-h-screen bg-retro-bg">
      {/* Header */}
      <header className="border-b border-retro-border bg-retro-card">
        <div className="max-w-6xl mx-auto px-6 py-6">
          <div className="flex items-center gap-3">
            <div className="w-3 h-3 bg-retro-green rounded-full shadow-[0_0_8px_rgba(57,255,20,0.6)]" />
            <h1 className="font-pixel text-xl text-retro-green glow-green tracking-wider">
              AgentML
            </h1>
          </div>
          <p className="font-mono text-sm text-retro-muted mt-2 ml-6">
            ▸ Intelligent Dataset Analysis &amp; AI Insights Engine
          </p>
          <p className="font-mono text-xs text-retro-muted mt-1 ml-6">
            Upload a dataset → Get automatic analysis → Ask questions in plain English
          </p>
        </div>
      </header>

      {/* Steps indicator */}
      <div className="max-w-6xl mx-auto px-6 pt-6">
        <div className="flex items-center gap-2 mb-6">
          {STEPS.map((step, i) => (
            <div key={step.key} className="flex items-center gap-2">
              <div
                className={`w-7 h-7 rounded-full flex items-center justify-center font-mono text-xs font-bold border-2 transition-colors ${
                  currentStep >= step.num
                    ? "border-retro-green text-retro-green"
                    : "border-retro-border text-retro-muted"
                }`}
              >
                {step.num}
              </div>
              <span
                className={`font-mono text-xs hidden sm:inline ${
                  currentStep >= step.num ? "text-retro-green" : "text-retro-muted"
                }`}
              >
                {step.label}
              </span>
              {i < STEPS.length - 1 && (
                <div
                  className={`w-8 h-px ${
                    currentStep > step.num ? "bg-retro-green" : "bg-retro-border"
                  }`}
                />
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Main */}
      <main className="max-w-6xl mx-auto px-6 pb-8 space-y-6">
        {error && (
          <div className="retro-card border-retro-red/50">
            <p className="font-mono text-sm text-retro-red">⚠ {error}</p>
          </div>
        )}

        {/* Step 1 */}
        <UploadDataset onFileUpload={handleFileUpload} loading={loading.upload} />

        {/* Step 2 */}
        {uploadData && (
          <>
            <DatasetPreview
              preview={uploadData.preview}
              columns={uploadData.columns}
              rows={uploadData.rows}
              cols={uploadData.cols}
              filename={uploadData.filename}
            />
            <AnalysisControls
              columns={uploadData.columns}
              target={target}
              problemType={problemType}
              onTargetChange={setTarget}
              onProblemTypeChange={setProblemType}
              onRunAnalysis={handleRunAnalysis}
              loading={loading.analysis}
            />
          </>
        )}

        {/* Loading */}
        {loading.analysis && (
          <div className="retro-card text-center">
            <div className="retro-loader mx-auto mb-3" />
            <p className="font-mono text-sm text-retro-green glow-green">
              Analyzing dataset... This may take a moment.
            </p>
          </div>
        )}

        {/* Step 3: Results */}
        {analysisData && (
          <>
            <div className="border-t border-retro-border pt-6">
              <p className="font-mono text-xs text-retro-green mb-2 glow-green">
                ▸ ANALYSIS COMPLETE — DISPLAYING RESULTS
              </p>
              {analysisData.preprocessing_logs.length > 0 && (
                <div className="retro-card mt-4">
                  <h3 className="font-mono text-sm text-retro-amber font-bold uppercase tracking-wider mb-3">
                    ▸ Preprocessing Applied
                  </h3>
                  <ul className="space-y-1">
                    {analysisData.preprocessing_logs.map((log, i) => (
                      <li key={i} className="font-mono text-xs text-retro-text">
                        • {log}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            <SummaryPanel
              summary={analysisData.summary}
              schema={analysisData.schema}
              missingValues={analysisData.missing_values}
              skewness={analysisData.skewness}
            />

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2">
                <StatisticsPanel statistics={analysisData.statistics} />
              </div>
              <div>
                <HealthScore
                  score={analysisData.health_score}
                  missingValues={analysisData.missing_values}
                  skewness={analysisData.skewness}
                />
              </div>
            </div>

            <CorrelationMatrix
              correlations={analysisData.correlations}
              heatmapImage={analysisData.correlation_heatmap}
            />

            <HistogramCharts histograms={analysisData.histograms} />

            {analysisData.ai_explanation && (
              <div className="retro-card">
                <h3 className="font-mono text-sm text-retro-cyan font-bold uppercase tracking-wider mb-3">
                  ▸ AI Insights
                </h3>
                <p className="font-mono text-xs text-retro-muted mb-2">
                  Beginner-friendly explanation of your dataset quality
                </p>
                <div className="p-4 bg-retro-bg border border-retro-border rounded">
                  <p className="font-mono text-sm text-retro-text whitespace-pre-wrap leading-relaxed">
                    {analysisData.ai_explanation}
                  </p>
                </div>
              </div>
            )}

            <AskQuestion sessionId={uploadData.session_id} />
          </>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-retro-border mt-12">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <p className="font-mono text-xs text-retro-muted text-center">
            AgentML v1.0 — Intelligent Dataset Analysis &amp; AI Insights
          </p>
        </div>
      </footer>
    </div>
  );
}