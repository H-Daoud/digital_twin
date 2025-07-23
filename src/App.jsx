import { useState } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from "recharts";
import "./App.css";

function App() {
  const [inputs, setInputs] = useState({
    strompreis: 200,
    zoll: 10,
    co2: 50,
    lieferkosten: 1000,
    nachhaltigkeit: -200,
    kundenbindung: 300,
    fixkosten: 12000,
    variableKosten: 7000,
  });

  const [simulations, setSimulations] = useState([]);
  const [counter, setCounter] = useState(1);

  const inputFields = [
    { key: "strompreis", label: "⚡ Strompreis (€/MWh)" },
    { key: "zoll", label: "🌐 Zoll (%)" },
    { key: "co2", label: "🌱 CO₂-Kosten (€/t)" },
    { key: "lieferkosten", label: "🚚 Lieferkosten (€)" },
    { key: "nachhaltigkeit", label: "🍃 Nachhaltigkeitsbonus (€)" },
    { key: "kundenbindung", label: "🤝 Kundenbindungskosten (€)" },
    { key: "fixkosten", label: "🏭 Fixkosten (€)" },
    { key: "variableKosten", label: "⚙️ Variable Produktionskosten (€)" },
  ];

  const handleSimulate = () => {
    const monate = 6;
    const version = `Sim ${counter}`;
    const zollFaktor = 1 + inputs.zoll / 100;
    const ergebnisse = [];
    let lagerbestand = 300;
    let verschoben = false;

    for (let monat = 1; monat <= monate; monat++) {
      const strom = inputs.strompreis + monat * 15;
      const co2 = inputs.co2;
      let kommentar = "-";

      if (strom > 250) kommentar = "⚠️ Strompreis > 250 € → Zusatzkosten";
      if (lagerbestand < 200 && !verschoben) {
        kommentar = "🚫 Lager niedrig – Produktion verzögert";
        verschoben = true;
        lagerbestand += 50;
        ergebnisse.push({
          monat,
          strom,
          co2,
          lagerbestand,
          kommentar,
          kosten: "–",
        });
        continue;
      }

      const kosten =
        inputs.fixkosten +
        inputs.variableKosten +
        inputs.lieferkosten +
        inputs.kundenbindung +
        inputs.nachhaltigkeit +
        strom * 100 +
        co2 * 10 +
        inputs.zoll * 20;

      lagerbestand -= 50;

      ergebnisse.push({
        monat,
        strom,
        co2,
        lagerbestand,
        kommentar,
        kosten: kosten.toFixed(2),
      });
    }

    setSimulations([...simulations, { version, daten: ergebnisse }]);
    setCounter(counter + 1);
  };

  return (
    <div style={{
      padding: "2rem",
      fontFamily: "sans-serif",
      maxWidth: 900,
      margin: "auto"
    }}>
      {/* Titel & Intro */}
      <h1 style={{ marginBottom: 8 }}>🧠 STK Digital Twin</h1>
      <h2 style={{
        fontWeight: 400,
        fontSize: 22,
        marginTop: 0,
        marginBottom: 20,
        color: "#37506b"
      }}>
        VW Standort-Entscheidungssimulation
      </h2>
      <div style={{
        background: "#f1f6fa",
        padding: 24,
        borderRadius: 15,
        marginBottom: 32,
        boxShadow: "0 2px 6px rgba(0,0,0,0.05)"
      }}>
        <h3 style={{
          margin: 0,
          marginBottom: 14,
          fontWeight: 500,
          color: "#236597"
        }}>Kosten- und Einflussfaktoren</h3>
        <div style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(230px,1fr))",
          gap: 18
        }}>
          {inputFields.map(f => (
            <label key={f.key} style={{ fontSize: 16 }}>
              {f.label}
              <input
                type="number"
                value={inputs[f.key]}
                onChange={e => setInputs({ ...inputs, [f.key]: Number(e.target.value) })}
                style={{
                  padding: 8,
                  borderRadius: 5,
                  border: "1px solid #dde5ed",
                  marginTop: 6,
                  width: "100%",
                  fontSize: 16,
                  background: "#fff"
                }}
              />
            </label>
          ))}
        </div>
      </div>

      <button onClick={handleSimulate} style={{
        padding: "10px 32px",
        borderRadius: 8,
        background: "#0077b6",
        color: "#fff",
        fontWeight: 600,
        border: "none",
        fontSize: 18,
        marginBottom: 30,
        boxShadow: "0 2px 6px rgba(0,0,0,0.06)"
      }}>
        🔁 Simulation starten
      </button>

      {simulations.map((sim, idx) => (
        <div key={idx} style={{
          marginBottom: "3rem",
          background: "#fff",
          borderRadius: 10,
          boxShadow: "0 2px 6px rgba(0,0,0,0.03)",
          padding: 16
        }}>
          <h3>📁 {sim.version}</h3>
          <table border="1" cellPadding="4" style={{ width: "100%", marginBottom: "1rem", borderCollapse: "collapse" }}>
            <thead>
              <tr style={{ background: "#e3e7ea" }}>
                <th>Monat</th>
                <th>Strompreis</th>
                <th>CO₂</th>
                <th>Lager</th>
                <th>Kosten (€)</th>
                <th>Kommentar</th>
              </tr>
            </thead>
            <tbody>
              {sim.daten.map((eintrag, i) => (
                <tr key={i}>
                  <td>{eintrag.monat}</td>
                  <td>{eintrag.strom}</td>
                  <td>{eintrag.co2}</td>
                  <td>{eintrag.lagerbestand}</td>
                  <td>{eintrag.kosten}</td>
                  <td>{eintrag.kommentar}</td>
                </tr>
              ))}
            </tbody>
          </table>
          {/* Diagramm */}
          <LineChart width={700} height={300} data={sim.daten}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="monat" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="strom" stroke="#8884d8" name="Strompreis" />
            <Line type="monotone" dataKey="kosten" stroke="#82ca9d" name="Kosten (€)" />
            <Line type="monotone" dataKey="lagerbestand" stroke="#ffc658" name="Lagerbestand" />
          </LineChart>
        </div>
      ))}
    </div>
  );
}

export default App;

