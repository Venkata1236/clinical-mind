import { useState } from "react";
import AgentProgress from "./AgentProgress";

const STATUS_CONFIG = {
  ELIGIBLE: { label: "Eligible", color: "#0d9488", bg: "#f0fdfa" },
  POTENTIALLY_ELIGIBLE: { label: "Potentially Eligible", color: "#d97706", bg: "#fffbeb" },
  INELIGIBLE: { label: "Ineligible", color: "#dc2626", bg: "#fef2f2" },
};

function TrialCard({ trial, rank }) {
  const [expanded, setExpanded] = useState(false);
  const status = STATUS_CONFIG[trial.eligibility_status] || STATUS_CONFIG.POTENTIALLY_ELIGIBLE;

  return (
    <div className={`trial-card rank-${rank}`}>
      <div className="trial-header">
        <div className="trial-rank">#{rank}</div>
        <div className="trial-meta">
          <span className="trial-phase">Phase {trial.phase}</span>
          <span className="status-badge" style={{ color: status.color, background: status.bg }}>
            {status.label}
          </span>
        </div>
      </div>

      <h3 className="trial-title">{trial.title}</h3>
      <p className="trial-condition">{trial.condition}</p>

      {/* Match score bar */}
      <div className="score-section">
        <div className="score-label">
          <span>Match Score</span>
          <span className="score-value">{trial.match_score}%</span>
        </div>
        <div className="score-bar">
          <div className="score-fill"
            style={{
              width: `${trial.match_score}%`,
              background: trial.match_score >= 70 ? "#0d9488"
                : trial.match_score >= 40 ? "#d97706" : "#dc2626",
            }}
          />
        </div>
      </div>

      {/* Criteria */}
      <div className="criteria-grid">
        <div className="criteria-col">
          <div className="criteria-heading met">✓ Met Criteria</div>
          {trial.met_criteria.map((c, i) => (
            <div key={i} className="criterion met">{c}</div>
          ))}
        </div>
        {trial.unmet_criteria.length > 0 && (
          <div className="criteria-col">
            <div className="criteria-heading unmet">✗ Unmet Criteria</div>
            {trial.unmet_criteria.map((c, i) => (
              <div key={i} className="criterion unmet">{c}</div>
            ))}
          </div>
        )}
      </div>

      {/* Reasoning toggle */}
      <button className="expand-btn" onClick={() => setExpanded(!expanded)}>
        {expanded ? "Hide reasoning ↑" : "View reasoning ↓"}
      </button>
      {expanded && (
        <div className="reasoning-box">{trial.reasoning}</div>
      )}
    </div>
  );
}

export default function EligibilityResults({ result }) {
  if (!result) return null;

  return (
    <div className="results-page">
      <div className="results-header">
        <div className="logo-mark">CM</div>
        <div>
          <h1>Eligibility Report</h1>
          <p>Session {result.session_id?.slice(0, 8)}... · {result.processing_time_seconds}s</p>
        </div>
      </div>

      <AgentProgress completed={true} />

      <div className="trials-list">
        <h2>Top Matching Trials</h2>
        {result.top_trials.map((trial, i) => (
          <TrialCard key={trial.trial_id} trial={trial} rank={i + 1} />
        ))}
      </div>

      <div className="report-card">
        <h2>Clinical Recommendation</h2>
        <div className="report-section">
          <div className="report-label">Summary</div>
          <p>{result.report.summary}</p>
        </div>
        <div className="report-section">
          <div className="report-label">Recommendation</div>
          <p>{result.report.recommendation}</p>
        </div>
        <div className="disclaimer-box">
          <span>⚕</span>
          {result.report.disclaimer}
        </div>
      </div>
    </div>
  );
}

// Need to import AgentProgress — add this at the top:
// import AgentProgress from "./AgentProgress";