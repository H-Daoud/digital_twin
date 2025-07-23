import React, { useState } from 'react';
import Upload from './Upload.jsx';
import './App.css';

function App() {
  const [ocrText, setOcrText] = useState('');
  const [llmAnalysis, setLlmAnalysis] = useState('');
  const [ruleInput, setRuleInput] = useState('');
  const [structuredRule, setStructuredRule] = useState('');
  const [simInput, setSimInput] = useState('{\n  "steps": 5,\n  "blocks": {}\n}');
  const [simResult, setSimResult] = useState(null);
  const [error, setError] = useState('');

  // Upload handler
  const handleFileUpload = async (file) => {
    setError('');
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch('/analyze-upload/', {
      method: 'POST',
      body: formData,
    });
    if (res.ok) {
      const data = await res.json();
      setOcrText(data.text || '');
      setLlmAnalysis(data.llm_analysis || '');
    } else {
      setError('Error uploading file.');
    }
  };

  // Rule extraction handler
  const handleExtractRule = async () => {
    setError('');
    const res = await fetch('/extract-rule/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ rule: ruleInput }),
    });
    if (res.ok) {
      const data = await res.json();
      setStructuredRule(data.structured || '');
    } else {
      setError('Error extracting rule.');
    }
  };

  // Simulation handler
  const handleSimulate = async () => {
    setError('');
    try {
      const res = await fetch('/simulate/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: simInput,
      });
      if (res.ok) {
        const data = await res.json();
        setSimResult(data.results);
      } else {
        setError('Error running simulation.');
      }
    } catch (e) {
      setError('Invalid input or server error.');
    }
  };

  return (
    <div>
      <div className="app-header">STK Digital Twin Challenge</div>
      <div className="container">
        <h2>1. Document Upload (OCR + LLM)</h2>
        <Upload onFileUpload={handleFileUpload} />
        <div>
          <strong>OCR Text:</strong>
          <pre>{ocrText}</pre>
        </div>
        <div>
          <strong>LLM Analysis:</strong>
          <pre>{llmAnalysis}</pre>
        </div>
        <hr />
        <h2>2. Extract Simulation Rule from Natural Language</h2>
        <textarea
          rows={3}
          style={{ width: '100%' }}
          placeholder='e.g. "Wenn die Energiekosten über 200 €/MWh steigen, schieben wir die Produktion um eine Woche nach hinten."'
          value={ruleInput}
          onChange={e => setRuleInput(e.target.value)}
        />
        <button onClick={handleExtractRule}>Extract Rule</button>
        <div>
          <strong>Structured Rule:</strong>
          <pre>{structuredRule}</pre>
        </div>
        <hr />
        <h2>3. Run Simulation</h2>
        <textarea
          rows={5}
          style={{ width: '100%' }}
          value={simInput}
          onChange={e => setSimInput(e.target.value)}
        />
        <button onClick={handleSimulate}>Run Simulation</button>
        {simResult && (
          <div>
            <strong>Simulation Results:</strong>
            <pre>{JSON.stringify(simResult, null, 2)}</pre>
          </div>
        )}
        {error && <div style={{ color: 'red' }}>{error}</div>}
      </div>
    </div>
  );
}

export default App;
