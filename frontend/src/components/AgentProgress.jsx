const AGENTS = [
  {
    name: "EligibilityAnalyst",
    role: "Clinical Trial Eligibility Expert",
    task: "Checking inclusion & exclusion criteria per trial",
    icon: "🔬",
  },
  {
    name: "TrialMatcher",
    role: "Trial Matching Specialist",
    task: "Ranking top 3 trials with match scores",
    icon: "🎯",
  },
  {
    name: "ReportWriter",
    role: "Medical Report Writer",
    task: "Generating physician-ready report",
    icon: "📋",
  },
];

export default function AgentProgress({ currentStep = 0, completed = false }) {
  return (
    <div className="agent-progress">
      {AGENTS.map((agent, i) => {
        const isDone = completed || i < currentStep;
        const isActive = !completed && i === currentStep;
        const isPending = !completed && i > currentStep;

        return (
          <div key={agent.name}
            className={`agent-card ${isDone ? "done" : ""} ${isActive ? "active" : ""} ${isPending ? "pending" : ""}`}>
            <div className="agent-icon">{agent.icon}</div>
            <div className="agent-info">
              <div className="agent-name">{agent.name}</div>
              <div className="agent-role">{agent.role}</div>
              <div className="agent-task">{agent.task}</div>
            </div>
            <div className="agent-status">
              {isDone && <span className="status-done">✓</span>}
              {isActive && <span className="status-active">●</span>}
              {isPending && <span className="status-pending">○</span>}
            </div>
            {i < AGENTS.length - 1 && <div className="connector" />}
          </div>
        );
      })}
    </div>
  );
}