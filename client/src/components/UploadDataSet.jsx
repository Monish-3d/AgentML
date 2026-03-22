import { useRef, useState } from "react";
import { Upload, FileSpreadsheet, Loader } from "lucide-react";

export function UploadDataset({ onFileUpload, loading }) {
  const fileInputRef = useRef(null);
  const [fileName, setFileName] = useState(null);
  const [dragActive, setDragActive] = useState(false);

  const handleClick = () => {
    if (!loading) fileInputRef.current.click();
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFileName(file.name);
      if (onFileUpload) onFileUpload(file);
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (loading) return;
    const file = e.dataTransfer.files[0];
    if (file) {
      setFileName(file.name);
      if (onFileUpload) onFileUpload(file);
    }
  };

  return (
    <div className="retro-card">
      <h2 className="font-mono text-sm text-retro-green font-bold uppercase tracking-wider mb-4">
        ▸ Upload Dataset
      </h2>

      <div
        className={`border-2 border-dashed rounded cursor-pointer transition-all duration-200 p-8 text-center
          ${loading ? "opacity-50 pointer-events-none" : ""}
          ${dragActive
            ? "border-retro-green bg-retro-green/5 shadow-[0_0_20px_rgba(57,255,20,0.1)]"
            : "border-retro-border hover:border-retro-green/50"
          }`}
        onClick={handleClick}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        {loading ? (
          <div className="flex flex-col items-center gap-3">
            <Loader className="w-10 h-10 text-retro-green animate-spin" />
            <p className="font-mono text-sm text-retro-green">Uploading...</p>
          </div>
        ) : fileName ? (
          <div className="flex flex-col items-center gap-3">
            <FileSpreadsheet className="w-10 h-10 text-retro-green" />
            <p className="font-mono text-sm text-retro-green">{fileName}</p>
            <p className="font-mono text-xs text-retro-muted">Click to replace</p>
          </div>
        ) : (
          <div className="flex flex-col items-center gap-3">
            <Upload className="w-10 h-10 text-retro-muted" />
            <p className="font-mono text-sm text-retro-text">
              Drop your dataset here or click to browse
            </p>
            <p className="font-mono text-xs text-retro-muted">
              Supports .csv and .xlsx files
            </p>
          </div>
        )}
      </div>

      <input
        type="file"
        accept=".csv,.xlsx"
        ref={fileInputRef}
        hidden
        onChange={handleFileChange}
        style={{ display: "none" }}
      />
    </div>
  );
}

