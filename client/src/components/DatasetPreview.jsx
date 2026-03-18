import { FileText } from "lucide-react";

export default function DatasetPreview({ preview, columns, rows, cols, filename }) {
  if (!preview || !columns) return null;

  return (
    <div className="retro-card">
      <div className="flex items-center gap-2 mb-1">
        <FileText className="w-4 h-4 text-retro-cyan" />
        <h3 className="font-mono text-sm text-retro-cyan font-bold uppercase tracking-wider">
          ▸ Dataset Preview
        </h3>
      </div>
      <p className="font-mono text-xs text-retro-muted mb-4">
        {filename} — First {preview.length} rows of your dataset
      </p>

      <div className="overflow-x-auto">
        <table className="retro-table">
          <thead>
            <tr>
              {columns.map((col) => (
                <th key={col}>{col}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {preview.map((row, idx) => (
              <tr key={idx}>
                {columns.map((col) => (
                  <td key={col}>
                    <code className="font-mono text-xs">
                      {row[col] != null ? String(row[col]) : "—"}
                    </code>
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="mt-4 flex justify-between items-center font-mono text-xs text-retro-muted">
        <span>Showing {preview.length} rows</span>
        <span>Total: {rows?.toLocaleString()} rows × {cols} columns</span>
      </div>
    </div>
  );
}
