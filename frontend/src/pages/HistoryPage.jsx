import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getHistory } from "../services/api";

export default function HistoryPage() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    getHistory()
      .then((res) => setHistory(res.data))
      .catch(() => setHistory([]))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="history-page">
      <div className="results-header">
        <div className="logo-mark">CM</div>
        <div>
          <h1>History</h1>
          <p>All past eligibility checks</p>
        </div>
      </div>
      <button className="back-btn" onClick={() => navigate("/")}>
        ← New Patient
      </button>

      {loading ? (
        <p style={{ padding: "2rem" }}>Loading...</p>
      ) : history.length === 0 ? (
        <p style={{ padding: "2rem", color: "#888" }}>No checks yet.</p>
      ) : (
        <table className="history-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Patient ID</th>
              <th>Diagnosis</th>
              <th>Top Trial</th>
              <th>Score</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {history.map((row) => (
              <tr key={row.session_id}>
                <td>{new Date(row.created_at).toLocaleDateString()}</td>
                <td>{row.patient_id}</td>
                <td>{row.diagnosis}</td>
                <td>{row.top_trial_id || "—"}</td>
                <td>{row.top_trial_score ? `${row.top_trial_score}%` : "—"}</td>
                <td><span className="status-pill">{row.eligibility_status || "—"}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}