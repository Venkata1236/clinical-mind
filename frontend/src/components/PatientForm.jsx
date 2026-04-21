import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { checkEligibility } from "../services/api";

const INITIAL = {
  patient_id: "",
  name: "",
  age: "",
  diagnosis: "",
  comorbidities: [],
  current_medications: [],
  prior_treatments: [],
  lab_values: { HbA1c: "", eGFR: "", ECOG_score: "" },
  trial_phase_preference: "any",
};

function TagInput({ label, value, onChange, placeholder }) {
  const [input, setInput] = useState("");

  const add = () => {
    const trimmed = input.trim();
    if (trimmed && !value.includes(trimmed)) {
      onChange([...value, trimmed]);
    }
    setInput("");
  };

  const remove = (tag) => onChange(value.filter((t) => t !== tag));

  return (
    <div className="field">
      <label>{label}</label>
      <div className="tag-input-wrapper">
        {value.map((tag) => (
          <span key={tag} className="tag">
            {tag}
            <button type="button" onClick={() => remove(tag)}>×</button>
          </span>
        ))}
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && (e.preventDefault(), add())}
          placeholder={placeholder}
        />
      </div>
      <span className="hint">Press Enter to add</span>
    </div>
  );
}

export default function PatientForm() {
  const [form, setForm] = useState(INITIAL);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const set = (key, val) => setForm((f) => ({ ...f, [key]: val }));
  const setLab = (key, val) =>
    setForm((f) => ({ ...f, lab_values: { ...f.lab_values, [key]: val } }));

  const submit = async () => {
    setLoading(true);
    setError(null);
    try {
      const payload = {
        ...form,
        age: parseInt(form.age),
        lab_values: {
          HbA1c: form.lab_values.HbA1c ? parseFloat(form.lab_values.HbA1c) : null,
          eGFR: form.lab_values.eGFR ? parseFloat(form.lab_values.eGFR) : null,
          ECOG_score: form.lab_values.ECOG_score
            ? parseInt(form.lab_values.ECOG_score)
            : null,
        },
      };
      const res = await checkEligibility(payload);
      navigate("/results", { state: { result: res.data } });
    } catch (err) {
      setError(err.response?.data?.detail || "Something went wrong. Try again.");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="pulse-ring" />
        <h2>Analyzing eligibility...</h2>
        <p>Our AI crew is reviewing clinical trial criteria</p>
        <div className="crew-steps">
          {["EligibilityAnalyst", "TrialMatcher", "ReportWriter"].map((agent, i) => (
            <div key={agent} className="crew-step" style={{ animationDelay: `${i * 0.8}s` }}>
              <span className="dot" />
              <span>{agent}</span>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="form-page">
      <header className="form-header">
        <div className="logo-mark">CM</div>
        <div>
          <h1>ClinicalMind</h1>
          <p>Clinical Trial Eligibility System</p>
        </div>
      </header>

      <div className="form-card">
        {/* Section 1 — Demographics */}
        <div className="form-section">
          <div className="section-label">01 — Patient Demographics</div>
          <div className="grid-2">
            <div className="field">
              <label>Patient ID</label>
              <input value={form.patient_id} onChange={(e) => set("patient_id", e.target.value)}
                placeholder="P001" />
            </div>
            <div className="field">
              <label>Full Name</label>
              <input value={form.name} onChange={(e) => set("name", e.target.value)}
                placeholder="Ravi Kumar" />
            </div>
            <div className="field">
              <label>Age</label>
              <input type="number" value={form.age} onChange={(e) => set("age", e.target.value)}
                placeholder="52" min={0} max={120} />
            </div>
            <div className="field">
              <label>Primary Diagnosis</label>
              <input value={form.diagnosis} onChange={(e) => set("diagnosis", e.target.value)}
                placeholder="Type 2 Diabetes" />
            </div>
          </div>
        </div>

        {/* Section 2 — Clinical History */}
        <div className="form-section">
          <div className="section-label">02 — Clinical History</div>
          <TagInput label="Comorbidities" value={form.comorbidities}
            onChange={(v) => set("comorbidities", v)} placeholder="Hypertension" />
          <TagInput label="Current Medications" value={form.current_medications}
            onChange={(v) => set("current_medications", v)} placeholder="Metformin 500mg" />
          <TagInput label="Prior Treatments" value={form.prior_treatments}
            onChange={(v) => set("prior_treatments", v)} placeholder="Insulin therapy" />
        </div>

        {/* Section 3 — Lab Values */}
        <div className="form-section">
          <div className="section-label">03 — Lab Values</div>
          <div className="grid-3">
            <div className="field">
              <label>HbA1c (%)</label>
              <input type="number" step="0.1" value={form.lab_values.HbA1c}
                onChange={(e) => setLab("HbA1c", e.target.value)} placeholder="8.5" />
              <span className="hint">Normal: &lt; 5.7%</span>
            </div>
            <div className="field">
              <label>eGFR (mL/min)</label>
              <input type="number" value={form.lab_values.eGFR}
                onChange={(e) => setLab("eGFR", e.target.value)} placeholder="72" />
              <span className="hint">Normal: ≥ 60</span>
            </div>
            <div className="field">
              <label>ECOG Score</label>
              <select value={form.lab_values.ECOG_score}
                onChange={(e) => setLab("ECOG_score", e.target.value)}>
                <option value="">Select</option>
                <option value="0">0 — Fully active</option>
                <option value="1">1 — Restricted activity</option>
                <option value="2">2 — Ambulatory</option>
                <option value="3">3 — Limited self-care</option>
                <option value="4">4 — Disabled</option>
              </select>
              <span className="hint">Performance status</span>
            </div>
          </div>
        </div>

        {/* Section 4 — Trial Preference */}
        <div className="form-section">
          <div className="section-label">04 — Trial Preference</div>
          <div className="phase-group">
            {["any", "I", "II", "III", "IV"].map((phase) => (
              <label key={phase} className={`phase-pill ${form.trial_phase_preference === phase ? "active" : ""}`}>
                <input type="radio" name="phase" value={phase}
                  checked={form.trial_phase_preference === phase}
                  onChange={() => set("trial_phase_preference", phase)} />
                {phase === "any" ? "Any Phase" : `Phase ${phase}`}
              </label>
            ))}
          </div>
        </div>

        {error && <div className="error-banner">{error}</div>}

        <button className="submit-btn" onClick={submit}
          disabled={!form.patient_id || !form.name || !form.age || !form.diagnosis}>
          <span>Check Eligibility</span>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" strokeWidth="2">
            <path d="M5 12h14M12 5l7 7-7 7" />
          </svg>
        </button>

        <p className="disclaimer">
          For physician review only. AI output must be confirmed by a qualified
          clinical research coordinator. Not medical advice.
        </p>
      </div>
    </div>
  );
}