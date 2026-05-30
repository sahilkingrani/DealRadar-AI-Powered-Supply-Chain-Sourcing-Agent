import { useState } from "react";
import axios from "axios";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export default function App() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [logs, setLogs] = useState([]);

  const addLog = (msg) => setLogs((prev) => [...prev, msg]);

  const handleSearch = async () => {
    if (!query.trim()) return;
    setLoading(true);
    setResults(null);
    setLogs([]);

    addLog("🔍 Finder Agent: Searching suppliers across the web...");
    addLog("✅ Verifier Agent: Checking reviews and ratings...");
    addLog("💰 Margin Agent: Calculating profit margins...");

    try {
      const res = await axios.post(`${API_BASE}/api/search`, {
        query: query,
        max_results: 5,
      }, {
        timeout: 20000,
      });
      setResults(res.data);
      addLog("🎉 Done! Results ready.");
      setLoading(false);
    } catch (err) {
      addLog("❌ Error: " + (err.response?.data?.detail || err.message));
      setLoading(false);
    }
  };

  const getRiskColor = (risk) => {
    if (risk === "Low") return "text-green-600 bg-green-100";
    if (risk === "Medium") return "text-yellow-600 bg-yellow-100";
    return "text-red-600 bg-red-100";
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-4xl mx-auto">

        {/* Header */}
        <div className="text-center mb-10">
          <h1 className="text-4xl font-bold text-gray-800">📡 DealRadar</h1>
          <p className="text-gray-500 mt-2">AI-powered supplier intelligence agent</p>
        </div>

        {/* Search Bar */}
        <div className="flex gap-3 mb-6">
          <input
            className="flex-1 border border-gray-300 rounded-xl px-4 py-3 text-base outline-none focus:border-blue-500"
            placeholder='e.g. "leather phone cases under $2/unit"'
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSearch()}
          />
          <button
            onClick={handleSearch}
            disabled={loading}
            className="bg-blue-600 text-white px-6 py-3 rounded-xl font-medium hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? "Searching..." : "Search"}
          </button>
        </div>

        {/* Agent Live Feed */}
        {logs.length > 0 && (
          <div className="bg-gray-900 text-green-400 rounded-xl p-4 mb-6 font-mono text-sm">
            <p className="text-gray-400 text-xs mb-2">Agent activity feed</p>
            {logs.map((log, i) => (
              <p key={i} className="mb-1">{log}</p>
            ))}
            {loading && <span className="animate-pulse">▊</span>}
          </div>
        )}

        {/* Results */}
        {results && (
          <div>
            <h2 className="text-lg font-semibold text-gray-700 mb-4">{results.summary}</h2>
            <div className="grid gap-4">
              {results.suppliers.map((s, i) => (
                <div key={i} className="bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
                  <div className="flex justify-between items-start mb-3">
                    <div>
                      <h3 className="font-semibold text-gray-800 text-base">{s.name}</h3>
                      <a href={s.website} target="_blank" rel="noreferrer"
                        className="text-blue-500 text-sm hover:underline">{s.website}</a>
                    </div>
                    <span className={`text-xs font-medium px-3 py-1 rounded-full ${getRiskColor(s.risk_score)}`}>
                      {s.risk_score} Risk
                    </span>
                  </div>
                  <div className="grid grid-cols-2 gap-3 text-sm text-gray-600 mb-3">
                    <div><span className="font-medium">Price/unit:</span> {s.price_per_unit}</div>
                    <div><span className="font-medium">MOQ:</span> {s.moq}</div>
                    <div><span className="font-medium">Rating:</span> {s.rating}</div>
                    <div><span className="font-medium">Profit margin:</span> <span className="text-green-600 font-semibold">{s.profit_margin}</span></div>
                  </div>
                  <p className="text-sm text-gray-500 italic">{s.review_summary}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}