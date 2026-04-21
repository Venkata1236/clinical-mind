import { useLocation, useNavigate } from "react-router-dom";
import EligibilityResults from "../components/EligibilityResults";

export default function ResultsPage() {
  const { state } = useLocation();
  const navigate = useNavigate();

  if (!state?.result) {
    navigate("/");
    return null;
  }

  return (
    <div>
      <button className="back-btn" onClick={() => navigate("/")}>
        ← New Patient
      </button>
      <EligibilityResults result={state.result} />
    </div>
  );
}