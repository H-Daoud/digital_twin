import { useState } from "react";

export default function Upload() {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://127.0.0.1:8000/analyze-upload/", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setResponse(data);
    } catch (err) {
      console.error("Upload failed:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ marginTop: "2rem" }}>
      <h2>📤 Upload Finanzdokument (PDF, JPG, Excel)</h2>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <br />
      <button onClick={handleUpload} disabled={loading}>
        {loading ? "⏳ Analyse läuft..." : "📄 Hochladen & Analysieren"}
      </button>

      {response && (
        <div style={{ marginTop: "1rem" }}>
          <h3>🧠 Interpretation:</h3>
          <p><strong>Dateiname:</strong> {response.filename}</p>
          <p><strong>OCR Text:</strong></p>
          <pre style={{ whiteSpace: "pre-wrap" }}>{response.extracted_text}</pre>
          <p><strong>LLM Analyse:</strong></p>
          <pre style={{ whiteSpace: "pre-wrap" }}>{response.llm_interpretation}</pre>
        </div>
      )}
    </div>
  );
}

