import { useEffect, useState } from "react";
import Sidebar from "./components/Sidebar";
import "./App.css";

const API_URL = "/api";

const PIPELINE = [
  {
    id: "detect",
    number: "01",
    title: "Detect",
    description: "Identify abnormal payment behavior",
  },
  {
    id: "diagnose",
    number: "02",
    title: "Diagnose",
    description: "Find the source of degradation",
  },
  {
    id: "decide",
    number: "03",
    title: "Decide",
    description: "AI evaluates recovery options",
  },
  {
    id: "guardrail",
    number: "04",
    title: "Guardrail",
    description: "Policy validates the action",
  },
  {
    id: "recover",
    number: "05",
    title: "Recover",
    description: "Execute a bounded recovery",
  },
  {
    id: "verify",
    number: "06",
    title: "Verify",
    description: "Measure money recovered",
  },
];

function formatCurrency(value) {
  if (value === undefined || value === null) return "₹0";

  return `₹${Number(value).toLocaleString("en-IN")}`;
}

function formatNumber(value) {
  if (value === undefined || value === null) return "0";

  return Number(value).toLocaleString("en-IN");
}

function formatPercent(value) {
  if (value === undefined || value === null) return "0%";

  return `${Number(value).toFixed(1)}%`;
}

function titleCase(value) {
  if (!value) return "";

  return value
    .replaceAll("_", " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function App() {
  const [scenario, setScenario] = useState("provider_degradation");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [activeStage, setActiveStage] = useState("diagnose");
  const [selectedProvider, setSelectedProvider] = useState(null);
  const [isReplaying, setIsReplaying] = useState(false);
  const [replayStage, setReplayStage] = useState(-1);
  const [replayRecoveryAmount, setReplayRecoveryAmount] = useState(null);

  async function runAnalysis() {
    setLoading(true);
    setError("");

    try {
      const response = await fetch(
        `${API_URL}/analyze?scenario=${scenario}`,
        {
          method: "POST",
        }
      );

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status}`);
      }

      const result = await response.json();

      setData(result);

      if (result.diagnosis) {
        setActiveStage("diagnose");
      }
    } catch (err) {
      setError(
        "The recovery engine returned an error. The API is reachable, but AI reasoning may be temporarily unavailable."
      );
    } finally {
      setLoading(false);
    }
  }

  const diagnosis = data?.diagnosis;
  const impact = data?.impact;
  const recommendation = data?.ai_recommendation;
  const recovery = data?.recovery;
  const verification = data?.verification;
  const policy = data?.policy;
  const audit = data?.audit;

  function startReplay() {
    if (!data || isReplaying) return;

    setIsReplaying(true);
    setReplayStage(0);
    setReplayRecoveryAmount(0);
    setSelectedProvider(null);
  }

  useEffect(() => {
    if (!isReplaying || replayStage < 0) return;

    if (replayStage >= PIPELINE.length - 1) return;

    const timer = setTimeout(() => {
      setReplayStage((current) => current + 1);
    }, 850);

    return () => clearTimeout(timer);
  }, [isReplaying, replayStage]);

  useEffect(() => {
    if (!isReplaying || replayStage !== PIPELINE.length - 1) return;

    if (!verification?.recovered_amount) {
      setIsReplaying(false);
      return;
    }

    const target = verification.recovered_amount;
    const duration = 1200;
    const interval = 30;
    const steps = duration / interval;
    const increment = target / steps;
    let current = 0;

    const timer = setInterval(() => {
      current += increment;

      if (current >= target) {
        current = target;
        clearInterval(timer);
        setTimeout(() => setIsReplaying(false), 250);
      }

      setReplayRecoveryAmount(Math.round(current));
    }, interval);

    return () => clearInterval(timer);
  }, [isReplaying, replayStage, verification]);

  useEffect(() => {
    if (!isReplaying || replayStage < 0) return;

    const currentStage = PIPELINE[replayStage];

    if (currentStage) {
      setActiveStage(currentStage.id);
    }

    if (replayStage >= 2 && recommendation?.recommended_provider) {
      setSelectedProvider(recommendation.recommended_provider);
    }
  }, [isReplaying, replayStage, recommendation]);

  const providers = data?.provider_health || {};

  return (
    <div className="app-shell">
      <Sidebar />

      <main className="main-content">
        <header className="topbar">
          <div className="title-block">
            <div className="live-label">
              <span className="live-pulse"></span>
              PAYMENT OPERATIONS · LIVE
            </div>

            <h1>Recovery command center</h1>

            <p>
              Detect revenue leakage. Understand the cause. Recover what can
              still be recovered.
            </p>
          </div>

          <div className="topbar-controls">
            <select
              value={scenario}
              onChange={(event) => setScenario(event.target.value)}
            >
              <option value="provider_degradation">
                Provider degradation
              </option>
              <option value="bank_degradation">
                Bank degradation
              </option>
              <option value="timeout_spike">
                Timeout spike
              </option>
            </select>

            <button
              className="run-button"
              onClick={runAnalysis}
              disabled={loading}
            >
              <span>{loading ? "Running..." : "Run recovery analysis"}</span>
              {!loading && <span className="button-arrow">↗</span>}
            </button>
          </div>
        </header>

        {error && <div className="error-banner">{error}</div>}

        {!data && !loading && (
          <section className="launch-screen">
            <div className="launch-orbit">
              <div className="orbit-dot"></div>
              <div className="orbit-ring"></div>
              <div className="launch-symbol">↗</div>
            </div>

            <div>
              <span className="section-kicker">RECOVERY ENGINE</span>
              <h2>Find the money before it is lost.</h2>
              <p>
                Run an analysis against the payment stream and watch the
                recovery engine move from detection to verified recovery.
              </p>
            </div>

            <button className="launch-button" onClick={runAnalysis}>
              Analyze payment stream
              <span>→</span>
            </button>
          </section>
        )}

        {loading && (
          <section className="launch-screen loading-screen">
            <div className="loading-visual">
              <div className="loading-core"></div>
            </div>

            <span className="section-kicker">RECOVERY ENGINE ACTIVE</span>

            <h2>Tracing payment degradation...</h2>

            <p>
              Comparing payment behavior, evaluating cohorts and preparing a
              bounded recovery decision.
            </p>

            <div className="loading-steps">
              <span>DETECT</span>
              <span>DIAGNOSE</span>
              <span>REASON</span>
              <span>RECOVER</span>
            </div>
          </section>
        )}

        {data && !loading && (
          <div className="dashboard">
            <section className="hero-strip">
              <div className="hero-copy">
                <div className="incident-tag">
                  <span></span>
                  INCIDENT DETECTED
                </div>

                <h2>
                  {titleCase(diagnosis?.type)}
                  <span className="hero-muted">
                    {" "}
                    · {diagnosis?.value}
                  </span>
                </h2>

                <p>
                  Payment degradation detected between{" "}
                  <strong>
                    {diagnosis?.start?.replace("T", " ")}
                  </strong>{" "}
                  and{" "}
                  <strong>
                    {diagnosis?.end?.replace("T", " ")}
                  </strong>
                  .
                </p>
              </div>

              <div className="hero-risk">
                <span>INCIDENT VALUE</span>
                <strong>{formatCurrency(impact?.failed_amount)}</strong>
                <small>
                  {formatNumber(impact?.failed_transactions)} failed payments
                </small>
              </div>
            </section>

            <section className="pipeline-panel">
              <div className="panel-topline">
                <div>
                  <span className="section-kicker">AUTONOMOUS RECOVERY LOOP</span>
                  <h3>From signal to recovered revenue</h3>
                </div>

                <div className="pipeline-actions">
                  <button
                    className={`replay-button ${isReplaying ? "replaying" : ""}`}
                    onClick={startReplay}
                    disabled={isReplaying}
                  >
                    <span>{isReplaying ? "●" : "↻"}</span>
                    {isReplaying ? "Replaying path..." : "Replay recovery"}
                  </button>

                  <span className="pipeline-status">
                    {isReplaying
                      ? "DECISION PATH ACTIVE"
                      : policy?.approved
                      ? "RECOVERY APPROVED"
                      : "ACTION BLOCKED"}
                  </span>
                </div>
              </div>

              <div className="pipeline">
                {PIPELINE.map((stage, index) => (
                  <div className="pipeline-wrapper" key={stage.id}>
                    <button
                      className={`pipeline-stage ${
                        activeStage === stage.id ? "active" : ""
                      } ${
                        PIPELINE.findIndex(
                          (item) => item.id === activeStage
                        ) > index
                          ? "completed"
                          : ""
                      }`}
                      onClick={() => setActiveStage(stage.id)}
                    >
                      <span className="stage-number">{stage.number}</span>

                      <span className="stage-title">{stage.title}</span>

                      <span className="stage-description">
                        {stage.description}
                      </span>
                    </button>

                    {index < PIPELINE.length - 1 && (
                      <span className="pipeline-arrow">→</span>
                    )}
                  </div>
                ))}
              </div>

              <div className="stage-detail">
                <div className="stage-detail-number">
                  {PIPELINE.find((item) => item.id === activeStage)?.number}
                </div>

                <div>
                  <span className="section-kicker">
                    CURRENT STAGE
                  </span>

                  <h4>
                    {PIPELINE.find((item) => item.id === activeStage)?.title}
                  </h4>

                  <p>
                    {getStageDescription(
                      activeStage,
                      diagnosis,
                      recommendation,
                      policy,
                      verification
                    )}
                  </p>
                </div>
              </div>
            </section>

            <section className="metric-row">
              <Metric
                label="Affected value"
                value={formatCurrency(impact?.failed_amount)}
                detail="diagnosed incident"
                type="risk"
              />

              <Metric
                label="Failure spike"
                value={`${diagnosis?.relative_increase?.toFixed(2)}×`}
                detail={`${formatPercent(diagnosis?.failure_rate)} current`}
              />

              <Metric
                label="AI confidence"
                value={`${Math.round(
                  (recommendation?.confidence || 0) * 100
                )}%`}
                detail={`${recommendation?.risk || "unknown"} operational risk`}
              />

              <Metric
                label="Recovered"
                value={formatCurrency(verification?.recovered_amount)}
                detail={`${formatPercent(verification?.recovery_rate)} recovery`}
                type="success"
              />
            </section>

            <section className="main-grid">
              <div className="decision-card">
                <div className="card-header">
                  <div>
                    <span className="section-kicker">AI REASONER</span>
                    <h3>Recovery decision</h3>
                  </div>

                  <div className="ai-orb">✦</div>
                </div>

                <div className="decision-main">
                  <div>
                    <span className="decision-label">RECOMMENDED ACTION</span>

                    <h2>
                      {titleCase(
                        recommendation?.recommended_strategy
                      )}
                    </h2>
                  </div>

                  {recommendation?.recommended_provider && (
                    <div className="destination">
                      <span>ROUTE TO</span>
                      <strong>
                        {recommendation.recommended_provider}
                      </strong>
                      <span className="destination-arrow">↗</span>
                    </div>
                  )}
                </div>

                <div className="reasoning-box">
                  <span>WHY THIS ACTION</span>
                  <p>{recommendation?.reasoning}</p>
                </div>

                <div className="decision-footer">
                  <div>
                    <span>CONFIDENCE</span>
                    <strong>
                      {Math.round(
                        (recommendation?.confidence || 0) * 100
                      )}
                      %
                    </strong>
                  </div>

                  <div>
                    <span>RISK</span>
                    <strong className="low-risk">
                      {recommendation?.risk?.toUpperCase()}
                    </strong>
                  </div>

                  <div>
                    <span>POLICY</span>
                    <strong className="approved">
                      {policy?.approved ? "APPROVED" : "BLOCKED"}
                    </strong>
                  </div>
                </div>
              </div>

              <div className="impact-card">
                <div className="card-header">
                  <div>
                    <span className="section-kicker">INCIDENT SCOPE</span>
                    <h3>What was affected?</h3>
                  </div>

                  <span className="scope-count">
                    {formatNumber(impact?.affected_transactions)}
                  </span>
                </div>

                <div className="scope-main">
                  <div className="scope-circle">
                    <strong>
                      {formatPercent(
                        diagnosis?.failure_rate
                      )}
                    </strong>
                    <span>failure</span>
                  </div>

                  <div className="scope-details">
                    <div>
                      <span>COHORT</span>
                      <strong>
                        {diagnosis?.dimension} = {diagnosis?.value}
                      </strong>
                    </div>

                    <div>
                      <span>BASELINE</span>
                      <strong>
                        {formatPercent(
                          diagnosis?.baseline_failure_rate
                        )}
                      </strong>
                    </div>

                    <div>
                      <span>DELTA</span>
                      <strong className="danger-text">
                        +
                        {diagnosis?.absolute_increase?.toFixed(
                          1
                        )} pp
                      </strong>
                    </div>
                  </div>
                </div>

                <div className="scope-footer">
                  <span>
                    {formatNumber(impact?.failed_transactions)} failed
                  </span>

                  <span>
                    {formatCurrency(impact?.failed_amount)} at risk
                  </span>
                </div>
              </div>
            </section>

            <section className="bottom-grid">
              <div className="provider-card">
                <div className="card-header">
                  <div>
                    <span className="section-kicker">PROVIDER HEALTH</span>
                    <h3>Payment routing landscape</h3>
                  </div>

                  <span className="card-hint">CLICK A PROVIDER</span>
                </div>

                <div className="provider-list">
                  {Object.entries(providers).map(
                    ([provider, stats]) => (
                      <button
                        className={`provider-row ${
                          selectedProvider === provider
                            ? "selected"
                            : ""
                        }`}
                        key={provider}
                        onClick={() =>
                          setSelectedProvider(
                            selectedProvider === provider
                              ? null
                              : provider
                          )
                        }
                      >
                        <span className="provider-status"></span>

                        <div className="provider-name">
                          <strong>{provider}</strong>
                          <span>
                            {formatNumber(
                              stats.total_transactions
                            )}{" "}
                            transactions
                          </span>
                        </div>

                        <div className="provider-bar">
                          <div
                            style={{
                              width: `${Math.min(
                                stats.failure_rate * 8,
                                100
                              )}%`,
                            }}
                          ></div>
                        </div>

                        <div className="provider-rate">
                          <strong>
                            {formatPercent(stats.failure_rate)}
                          </strong>
                          <span>failure</span>
                        </div>

                        <span className="provider-chevron">
                          {selectedProvider === provider
                            ? "−"
                            : "+"}
                        </span>
                      </button>
                    )
                  )}
                </div>

                {selectedProvider && providers[selectedProvider] && (
                  <div className="provider-detail">
                    <div>
                      <span>SELECTED ROUTE</span>
                      <strong>{selectedProvider}</strong>
                    </div>

                    <div>
                      <span>TRANSACTIONS</span>
                      <strong>
                        {formatNumber(
                          providers[selectedProvider]
                            .total_transactions
                        )}
                      </strong>
                    </div>

                    <div>
                      <span>FAILED</span>
                      <strong>
                        {formatNumber(
                          providers[selectedProvider]
                            .failed_transactions
                        )}
                      </strong>
                    </div>
                  </div>
                )}
              </div>

              <div className="recovery-card">
                <div className="card-header">
                  <div>
                    <span className="section-kicker">VERIFICATION</span>
                    <h3>Money recovered</h3>
                  </div>

                  <span className="verified-badge">VERIFIED</span>
                </div>

                <div className="recovery-amount">
                  <strong>
                    {formatCurrency(
                      isReplaying && replayRecoveryAmount !== null
                        ? replayRecoveryAmount
                        : verification?.recovered_amount
                    )}
                  </strong>

                  <span>
                    recovered from{" "}
                    {formatNumber(verification?.attempted)}{" "}
                    bounded attempts
                  </span>
                </div>

                <div className="recovery-visual">
                  <div
                    className="recovery-fill"
                    style={{
                      width:
                        isReplaying && replayStage < 5
                          ? "0%"
                          : `${verification?.recovery_rate || 0}%`,
                    }}
                  ></div>

                  <div className="recovery-marker">
                    <span>
                      {verification?.recovery_rate?.toFixed(0)}%
                    </span>
                  </div>
                </div>

                <div className="recovery-stats">
                  <div>
                    <span>ATTEMPTED</span>
                    <strong>
                      {formatNumber(verification?.attempted)}
                    </strong>
                  </div>

                  <div>
                    <span>RECOVERED</span>
                    <strong>
                      {formatNumber(verification?.recovered)}
                    </strong>
                  </div>

                  <div>
                    <span>REMAINING</span>
                    <strong>
                      {formatNumber(
                        (verification?.attempted || 0) -
                          (verification?.recovered || 0)
                      )}
                    </strong>
                  </div>
                </div>
              </div>
            </section>

            <section className="audit-strip">
              <div className="audit-title">
                <span className="section-kicker">AUDIT TRAIL</span>
                <strong>Every automated decision is traceable.</strong>
              </div>

              <AuditStep
                number="01"
                title="Incident"
                value={`${audit?.affected_dimension} = ${audit?.affected_value}`}
              />

              <AuditStep
                number="02"
                title="AI decision"
                value={titleCase(
                  recommendation?.recommended_strategy
                )}
              />

              <AuditStep
                number="03"
                title="Policy"
                value={policy?.approved ? "Approved" : "Blocked"}
              />

              <AuditStep
                number="04"
                title="Outcome"
                value={`${formatCurrency(
                  audit?.recovered_amount
                )} recovered`}
              />
            </section>

            <footer className="dashboard-footer">
              <span>PAYMENT RECOVERY INTELLIGENCE</span>
              <span>BOUNDED AUTONOMY · AUDITABLE RECOVERY · V1.0</span>
            </footer>
          </div>
        )}
      </main>
    </div>
  );
}

function getStageDescription(
  stage,
  diagnosis,
  recommendation,
  policy,
  verification
) {
  if (stage === "detect") {
    return "The engine scans payment behavior for statistically significant changes in failure patterns.";
  }

  if (stage === "diagnose") {
    return diagnosis
      ? `${diagnosis.dimension} ${diagnosis.value} is failing at ${diagnosis.failure_rate.toFixed(
          2
        )}% versus a ${diagnosis.baseline_failure_rate.toFixed(
          2
        )}% baseline.`
      : "The system is identifying the strongest incident signal.";
  }

  if (stage === "decide") {
    return recommendation
      ? `The AI reasoner recommends ${titleCase(
          recommendation.recommended_strategy
        )}.`
      : "The AI reasoner evaluates the available recovery actions.";
  }

  if (stage === "guardrail") {
    return policy?.approved
      ? "The recommendation passed deterministic recovery policy checks and is eligible for bounded execution."
      : "The recovery recommendation was blocked by deterministic policy.";
  }

  if (stage === "recover") {
    return "Only a bounded recovery batch is executed, preventing uncontrolled retries.";
  }

  return verification
    ? `${verification.recovered} payments were recovered, returning ${formatCurrency(
        verification.recovered_amount
      )} in payment value.`
    : "The recovery outcome is verified after execution.";
}

function Metric({ label, value, detail, type = "" }) {
  return (
    <div className={`metric ${type}`}>
      <span>{label}</span>
      <strong>{value}</strong>
      <small>{detail}</small>
    </div>
  );
}

function AuditStep({ number, title, value }) {
  return (
    <div className="audit-step">
      <span>{number}</span>

      <div>
        <small>{title}</small>
        <strong>{value}</strong>
      </div>
    </div>
  );
}

export default App;