import { useState } from "react";
import { MessageCircle, Send, Loader } from "lucide-react";
import { askQuestion } from "../services/api";

export default function AskQuestion({ sessionId }) {
  const [question, setQuestion] = useState("");
  const [conversation, setConversation] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!question.trim() || loading) return;

    const q = question.trim();
    setConversation((prev) => [...prev, { type: "question", text: q }]);
    setQuestion("");
    setLoading(true);

    try {
      const data = await askQuestion(sessionId, q);
      setConversation((prev) => [...prev, { type: "answer", text: data.answer }]);
    } catch (err) {
      setConversation((prev) => [
        ...prev,
        { type: "answer", text: `Error: ${err.message}` },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleAsk();
    }
  };

  return (
    <div className="retro-card">
      <div className="flex items-center gap-2 mb-1">
        <MessageCircle className="w-4 h-4 text-retro-green" />
        <h3 className="font-mono text-sm text-retro-green font-bold uppercase tracking-wider">
          ▸ Ask About Your Data
        </h3>
      </div>
      <p className="font-mono text-xs text-retro-muted mb-4">
        Ask any question about your dataset in plain English
      </p>

      {/* Conversation history */}
      {conversation.length > 0 && (
        <div className="space-y-3 mb-4 max-h-96 overflow-y-auto">
          {conversation.map((msg, idx) => (
            <div
              key={idx}
              className={`p-3 rounded border ${msg.type === "question"
                  ? "border-retro-green/30 bg-retro-green/5"
                  : "border-retro-border bg-retro-bg"
                }`}
            >
              <p className="font-mono text-xs text-retro-muted mb-1 uppercase">
                {msg.type === "question" ? "▸ You" : "▸ AgentML"}
              </p>
              <p className="font-mono text-sm text-retro-text whitespace-pre-wrap leading-relaxed">
                {msg.text}
              </p>
            </div>
          ))}
          {loading && (
            <div className="p-3 rounded border border-retro-border bg-retro-bg">
              <p className="font-mono text-xs text-retro-muted mb-1 uppercase">▸ AgentML</p>
              <Loader className="w-4 h-4 text-retro-green animate-spin" />
            </div>
          )}
        </div>
      )}

      {/* Input */}
      <div className="flex gap-3">
        <input
          type="text"
          className="retro-input flex-1"
          placeholder="e.g. What are the most important features?"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={loading}
        />
        <button
          className="retro-btn flex items-center gap-2"
          onClick={handleAsk}
          disabled={loading || !question.trim()}
        >
          {loading ? (
            <Loader className="w-4 h-4 animate-spin" />
          ) : (
            <Send className="w-4 h-4" />
          )}
          Ask
        </button>
      </div>
    </div>
  );
}
