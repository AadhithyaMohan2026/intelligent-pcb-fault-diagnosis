import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [activeSection, setActiveSection] = useState("dashboard");

  // ==================================================
  // DIAGNOSIS MEASUREMENTS
  // ==================================================

  // Keep input values as STRINGS while typing.
  // Convert to numbers only when sending to backend.
  const [measurements, setMeasurements] = useState({
    supply_voltage: "12",
    input_current: "0.6",
    regulator_output: "5",
    mcu_voltage: "3.3",
    temperature: "35",
    ripple_voltage: "0.04",
    signal_frequency: "10",
    continuity: "1",
  });

  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [analytics, setAnalytics] = useState(null);

  // ==================================================
  // REPAIR MEASUREMENTS
  // ==================================================

  const [repairMeasurements, setRepairMeasurements] = useState({
    supply_voltage: "12",
    input_current: "0.6",
    regulator_output: "5",
    mcu_voltage: "3.3",
    temperature: "35",
    ripple_voltage: "0.04",
    signal_frequency: "10",
    continuity: "1",
  });

  const [repairResult, setRepairResult] = useState(null);

  const [loading, setLoading] = useState(false);
  const [repairLoading, setRepairLoading] = useState(false);

  // ==================================================
  // LOAD HISTORY
  // ==================================================

  const loadHistory = async () => {
    try {
      const response = await fetch(`${API_URL}/history`);

      if (!response.ok) {
        throw new Error("Failed to load history");
      }

      const data = await response.json();
      setHistory(data);
    } catch (error) {
      console.error("History error:", error);
    }
  };

  // ==================================================
  // LOAD ANALYTICS
  // ==================================================

  const loadAnalytics = async () => {
    try {
      const response = await fetch(`${API_URL}/analytics`);

      if (!response.ok) {
        throw new Error("Failed to load analytics");
      }

      const data = await response.json();
      setAnalytics(data);
    } catch (error) {
      console.error("Analytics error:", error);
    }
  };

  // ==================================================
  // INITIAL LOAD
  // ==================================================

  useEffect(() => {
    loadHistory();
    loadAnalytics();
  }, []);

  // ==================================================
  // HANDLE DIAGNOSIS INPUT
  // ==================================================

  const handleMeasurementChange = (e) => {
    const { name, value } = e.target;

    // IMPORTANT:
    // Do NOT use Number(value) here.
    // Keep exactly what the user types.
    setMeasurements((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  // ==================================================
  // HANDLE REPAIR INPUT
  // ==================================================

  const handleRepairChange = (e) => {
    const { name, value } = e.target;

    // IMPORTANT:
    // Keep repair input as STRING while typing.
    setRepairMeasurements((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  // ==================================================
  // DIAGNOSE PCB
  // ==================================================

  const diagnosePCB = async (e) => {
    e.preventDefault();

    setLoading(true);
    setResult(null);

    // Convert values ONLY when submitting
    const payload = {
      supply_voltage: Number(measurements.supply_voltage),
      input_current: Number(measurements.input_current),
      regulator_output: Number(measurements.regulator_output),
      mcu_voltage: Number(measurements.mcu_voltage),
      temperature: Number(measurements.temperature),
      ripple_voltage: Number(measurements.ripple_voltage),
      signal_frequency: Number(measurements.signal_frequency),
      continuity: Number(measurements.continuity),
    };

    console.log("=================================");
    console.log("SENDING PCB MEASUREMENTS");
    console.log(payload);
    console.log("CONTINUITY:", payload.continuity);
    console.log("CONTINUITY TYPE:", typeof payload.continuity);
    console.log("=================================");

    try {
      const response = await fetch(`${API_URL}/diagnose`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(errorText);
      }

      const data = await response.json();

      console.log("DIAGNOSIS RESULT:", data);

      setResult(data);

      await loadHistory();
      await loadAnalytics();
    } catch (error) {
      console.error("Diagnosis error:", error);

      setResult({
        error:
          "Unable to connect to backend. Make sure FastAPI is running on port 8000.",
      });
    }

    setLoading(false);
  };

  // ==================================================
  // VERIFY REPAIR
  // ==================================================

  const verifyRepair = async (e) => {
    e.preventDefault();

    setRepairLoading(true);
    setRepairResult(null);

    // Convert values ONLY when submitting
    const payload = {
      original_diagnosis: result?.diagnosis || "Not Provided",

      supply_voltage: Number(repairMeasurements.supply_voltage),

      input_current: Number(repairMeasurements.input_current),

      regulator_output: Number(repairMeasurements.regulator_output),

      mcu_voltage: Number(repairMeasurements.mcu_voltage),

      temperature: Number(repairMeasurements.temperature),

      ripple_voltage: Number(repairMeasurements.ripple_voltage),

      signal_frequency: Number(repairMeasurements.signal_frequency),

      continuity: Number(repairMeasurements.continuity),
    };

    console.log("=================================");
    console.log("SENDING REPAIR VERIFICATION");
    console.log(payload);
    console.log("CONTINUITY:", payload.continuity);
    console.log("CONTINUITY TYPE:", typeof payload.continuity);
    console.log("=================================");

    try {
      const response = await fetch(`${API_URL}/verify-repair`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(errorText);
      }

      const data = await response.json();

      console.log("REPAIR RESULT:", data);

      setRepairResult(data);
    } catch (error) {
      console.error("Repair verification error:", error);

      setRepairResult({
        error:
          "Unable to connect to backend. Make sure FastAPI is running on port 8000.",
      });
    }

    setRepairLoading(false);
  };

  // ==================================================
  // CONFIDENCE FORMAT
  // ==================================================

  const formatConfidence = (confidence) => {
    if (confidence === undefined || confidence === null) {
      return "-";
    }

    return `${(confidence * 100).toFixed(1)}%`;
  };

  // ==================================================
  // RENDER SECTIONS
  // ==================================================

  const renderSection = () => {
    // ==================================================
    // DASHBOARD
    // ==================================================

    if (activeSection === "dashboard") {
      return (
        <div>
          <div className="page-header">
            <h1>PCB Diagnostic Dashboard</h1>

            <p>
              Intelligent PCB fault diagnosis and maintenance
              decision-support platform.
            </p>
          </div>

          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-icon">🔧</div>

              <div>
                <h3>Total Diagnoses</h3>

                <strong>
                  {analytics?.total_diagnoses ?? 0}
                </strong>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon">✅</div>

              <div>
                <h3>Healthy Boards</h3>

                <strong>
                  {analytics?.healthy_boards ?? 0}
                </strong>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon">⚠️</div>

              <div>
                <h3>Faulty Boards</h3>

                <strong>
                  {analytics?.faulty_boards ?? 0}
                </strong>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon">🚨</div>

              <div>
                <h3>Critical Faults</h3>

                <strong>
                  {analytics?.critical_faults ?? 0}
                </strong>
              </div>
            </div>
          </div>

          <div className="dashboard-grid">
            <div className="card">
              <h2>System Overview</h2>

              <div className="overview-item">
                <span>Most Common Fault</span>

                <strong>
                  {analytics?.most_common_fault || "No data"}
                </strong>
              </div>

              <div className="overview-item">
                <span>Most Affected Area</span>

                <strong>
                  {analytics?.most_common_area || "No data"}
                </strong>
              </div>

              <div className="overview-item">
                <span>Database Records</span>

                <strong>{history.length}</strong>
              </div>
            </div>

            <div className="card quick-actions">
              <h2>Quick Actions</h2>

              <button
                onClick={() =>
                  setActiveSection("diagnose")
                }
              >
                🔧 Start New Diagnosis
              </button>

              <button
                onClick={() =>
                  setActiveSection("history")
                }
              >
                📋 View Diagnosis History
              </button>

              <button
                onClick={() =>
                  setActiveSection("analytics")
                }
              >
                📊 View Analytics
              </button>

              <button
                onClick={() =>
                  setActiveSection("repair")
                }
              >
                🔍 Verify Repair
              </button>
            </div>
          </div>
        </div>
      );
    }

    // ==================================================
    // DIAGNOSIS
    // ==================================================

    if (activeSection === "diagnose") {
      return (
        <div>
          <div className="page-header">
            <h1>PCB Diagnosis</h1>

            <p>
              Enter electrical measurements collected from
              the PCB under test.
            </p>
          </div>

          <div className="card">
            <form onSubmit={diagnosePCB}>
              <div className="form-grid">
                <div className="input-group">
                  <label>Supply Voltage (V)</label>

                  <input
                    type="number"
                    step="0.01"
                    name="supply_voltage"
                    value={measurements.supply_voltage}
                    onChange={handleMeasurementChange}
                    required
                  />
                </div>

                <div className="input-group">
                  <label>Input Current (A)</label>

                  <input
                    type="number"
                    step="0.01"
                    name="input_current"
                    value={measurements.input_current}
                    onChange={handleMeasurementChange}
                    required
                  />
                </div>

                <div className="input-group">
                  <label>Regulator Output (V)</label>

                  <input
                    type="number"
                    step="0.01"
                    name="regulator_output"
                    value={measurements.regulator_output}
                    onChange={handleMeasurementChange}
                    required
                  />
                </div>

                <div className="input-group">
                  <label>MCU Voltage (V)</label>

                  <input
                    type="number"
                    step="0.01"
                    name="mcu_voltage"
                    value={measurements.mcu_voltage}
                    onChange={handleMeasurementChange}
                    required
                  />
                </div>

                <div className="input-group">
                  <label>Temperature (°C)</label>

                  <input
                    type="number"
                    step="0.1"
                    name="temperature"
                    value={measurements.temperature}
                    onChange={handleMeasurementChange}
                    required
                  />
                </div>

                <div className="input-group">
                  <label>Ripple Voltage (V)</label>

                  <input
                    type="number"
                    step="0.001"
                    name="ripple_voltage"
                    value={measurements.ripple_voltage}
                    onChange={handleMeasurementChange}
                    required
                  />
                </div>

                <div className="input-group">
                  <label>Signal Frequency (MHz)</label>

                  <input
                    type="number"
                    step="0.1"
                    name="signal_frequency"
                    value={measurements.signal_frequency}
                    onChange={handleMeasurementChange}
                    required
                  />
                </div>

                <div className="input-group">
                  <label>Continuity</label>

                  <select
                    name="continuity"
                    value={String(measurements.continuity)}
                    onChange={handleMeasurementChange}
                  >
                    <option value="1">
                      Pass
                    </option>

                    <option value="0">
                      Fail
                    </option>
                  </select>
                </div>
              </div>

              <button
                className="primary-button"
                type="submit"
                disabled={loading}
              >
                {loading
                  ? "Analyzing PCB..."
                  : "🔍 Diagnose PCB"}
              </button>
            </form>
          </div>

          {/* DIAGNOSIS RESULT */}

          {result && !result.error && (
            <div className="result-card">
              <div className="result-header">
                <h2>Diagnosis Result</h2>

                <span
                  className={`severity ${String(
                    result.severity || ""
                  ).toLowerCase()}`}
                >
                  {result.severity || "Unknown"}
                </span>
              </div>

              <div className="diagnosis-main">
                <span>Detected Condition</span>

                <h1>{result.diagnosis}</h1>
              </div>

              <div className="result-grid">
                <div>
                  <span>ML Prediction</span>

                  <strong>
                    {result.ml_prediction}
                  </strong>
                </div>

                <div>
                  <span>Rule Prediction</span>

                  <strong>
                    {result.rule_prediction}
                  </strong>
                </div>

                <div>
                  <span>Model Confidence</span>

                  <strong>
                    {formatConfidence(
                      result.confidence
                    )}
                  </strong>
                </div>

                <div>
                  <span>Suspected Area</span>

                  <strong>
                    {result.suspected_area}
                  </strong>
                </div>
              </div>

              <div className="evidence-box">
                <h3>Evidence</h3>

                <p>{result.evidence}</p>
              </div>

              <div className="recommendation-box">
                <h3>Recommended Action</h3>

                <p>{result.recommendation}</p>
              </div>
            </div>
          )}

          {result?.error && (
            <div className="error-box">
              ❌ {result.error}
            </div>
          )}
        </div>
      );
    }

    // ==================================================
    // HISTORY
    // ==================================================

    if (activeSection === "history") {
      return (
        <div>
          <div className="page-header">
            <h1>Diagnosis History</h1>

            <p>
              Historical PCB diagnostic records stored in
              PostgreSQL.
            </p>
          </div>

          <div className="card">
            {history.length === 0 ? (
              <div className="empty-state">
                No diagnosis records found.
              </div>
            ) : (
              <div className="table-container">
                <table>
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Date</th>
                      <th>Diagnosis</th>
                      <th>ML Prediction</th>
                      <th>Confidence</th>
                      <th>Severity</th>
                      <th>Suspected Area</th>
                    </tr>
                  </thead>

                  <tbody>
                    {history.map((record) => (
                      <tr key={record.id}>
                        <td>{record.id}</td>

                        <td>
                          {record.created_at
                            ? new Date(
                                record.created_at
                              ).toLocaleString()
                            : "-"}
                        </td>

                        <td>
                          <span className="diagnosis-badge">
                            {record.diagnosis}
                          </span>
                        </td>

                        <td>
                          {record.ml_prediction}
                        </td>

                        <td>
                          {formatConfidence(
                            record.confidence
                          )}
                        </td>

                        <td>{record.severity}</td>

                        <td>
                          {record.suspected_area}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      );
    }

    // ==================================================
    // ANALYTICS
    // ==================================================

    if (activeSection === "analytics") {
      return (
        <div>
          <div className="page-header">
            <h1>Analytics</h1>

            <p>
              Diagnostic trends and PCB fault distribution.
            </p>
          </div>

          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-icon">
                📋
              </div>

              <div>
                <h3>Total Diagnoses</h3>

                <strong>
                  {analytics?.total_diagnoses ?? 0}
                </strong>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon">
                ✅
              </div>

              <div>
                <h3>Healthy</h3>

                <strong>
                  {analytics?.healthy_boards ?? 0}
                </strong>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon">
                ⚠️
              </div>

              <div>
                <h3>Faulty</h3>

                <strong>
                  {analytics?.faulty_boards ?? 0}
                </strong>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon">
                🚨
              </div>

              <div>
                <h3>Critical</h3>

                <strong>
                  {analytics?.critical_faults ?? 0}
                </strong>
              </div>
            </div>
          </div>

          <div className="analytics-grid">
            <div className="card">
              <h2>Diagnosis Distribution</h2>

              {analytics?.diagnosis_distribution ? (
                Object.entries(
                  analytics.diagnosis_distribution
                ).map(([name, count]) => {
                  const total =
                    analytics.total_diagnoses || 1;

                  const percentage =
                    (count / total) * 100;

                  return (
                    <div
                      className="bar-row"
                      key={name}
                    >
                      <div className="bar-label">
                        <span>{name}</span>

                        <strong>{count}</strong>
                      </div>

                      <div className="bar-background">
                        <div
                          className="bar-fill"
                          style={{
                            width:
                              `${percentage}%`,
                          }}
                        />
                      </div>
                    </div>
                  );
                })
              ) : (
                <p>No analytics available.</p>
              )}
            </div>

            <div className="card">
              <h2>Affected PCB Areas</h2>

              {analytics?.area_distribution &&
              Object.keys(
                analytics.area_distribution
              ).length > 0 ? (
                Object.entries(
                  analytics.area_distribution
                ).map(([area, count]) => (
                  <div
                    className="area-row"
                    key={area}
                  >
                    <span>{area}</span>

                    <strong>{count}</strong>
                  </div>
                ))
              ) : (
                <p>
                  No faulty-area data available.
                </p>
              )}
            </div>
          </div>

          <div className="card">
            <h2>Key Findings</h2>

            <div className="finding">
              <span>Most Common Fault</span>

              <strong>
                {analytics?.most_common_fault ||
                  "No data"}
              </strong>
            </div>

            <div className="finding">
              <span>Most Affected Area</span>

              <strong>
                {analytics?.most_common_area ||
                  "No data"}
              </strong>
            </div>
          </div>
        </div>
      );
    }

    // ==================================================
    // REPAIR VERIFICATION
    // ==================================================

    if (activeSection === "repair") {
      return (
        <div>
          <div className="page-header">
            <h1>Repair Verification</h1>

            <p>
              Re-enter measurements after component
              replacement to verify whether the PCB has
              returned to a healthy state.
            </p>
          </div>

          <div className="card">
            <form onSubmit={verifyRepair}>
              <div className="form-grid">
                <div className="input-group">
                  <label>
                    Supply Voltage (V)
                  </label>

                  <input
                    type="number"
                    step="0.01"
                    name="supply_voltage"
                    value={
                      repairMeasurements.supply_voltage
                    }
                    onChange={handleRepairChange}
                    required
                  />
                </div>

                <div className="input-group">
                  <label>
                    Input Current (A)
                  </label>

                  <input
                    type="number"
                    step="0.01"
                    name="input_current"
                    value={
                      repairMeasurements.input_current
                    }
                    onChange={handleRepairChange}
                    required
                  />
                </div>

                <div className="input-group">
                  <label>
                    Regulator Output (V)
                  </label>

                  <input
                    type="number"
                    step="0.01"
                    name="regulator_output"
                    value={
                      repairMeasurements.regulator_output
                    }
                    onChange={handleRepairChange}
                    required
                  />
                </div>

                <div className="input-group">
                  <label>
                    MCU Voltage (V)
                  </label>

                  <input
                    type="number"
                    step="0.01"
                    name="mcu_voltage"
                    value={
                      repairMeasurements.mcu_voltage
                    }
                    onChange={handleRepairChange}
                    required
                  />
                </div>

                <div className="input-group">
                  <label>
                    Temperature (°C)
                  </label>

                  <input
                    type="number"
                    step="0.1"
                    name="temperature"
                    value={
                      repairMeasurements.temperature
                    }
                    onChange={handleRepairChange}
                    required
                  />
                </div>

                <div className="input-group">
                  <label>
                    Ripple Voltage (V)
                  </label>

                  <input
                    type="number"
                    step="0.001"
                    name="ripple_voltage"
                    value={
                      repairMeasurements.ripple_voltage
                    }
                    onChange={handleRepairChange}
                    required
                  />
                </div>

                <div className="input-group">
                  <label>
                    Signal Frequency (MHz)
                  </label>

                  <input
                    type="number"
                    step="0.1"
                    name="signal_frequency"
                    value={
                      repairMeasurements.signal_frequency
                    }
                    onChange={handleRepairChange}
                    required
                  />
                </div>

                <div className="input-group">
                  <label>Continuity</label>

                  <select
                    name="continuity"
                    value={String(
                      repairMeasurements.continuity
                    )}
                    onChange={handleRepairChange}
                  >
                    <option value="1">
                      Pass
                    </option>

                    <option value="0">
                      Fail
                    </option>
                  </select>
                </div>
              </div>

              <button
                className="primary-button"
                type="submit"
                disabled={repairLoading}
              >
                {repairLoading
                  ? "Verifying..."
                  : "🔍 Verify Repair"}
              </button>
            </form>
          </div>

          {/* REPAIR RESULT */}

          {repairResult &&
            !repairResult.error && (
              <div className="result-card">
                <div className="result-header">
                  <h2>
                    Repair Verification Result
                  </h2>

                  <span className="severity">
                    {repairResult.repair_status ||
                      repairResult.status ||
                      "Completed"}
                  </span>
                </div>

                <div className="diagnosis-main">
                  <span>
                    Current PCB Status
                  </span>

                  <h1>
                    {repairResult.diagnosis ||
                      repairResult.repair_status ||
                      repairResult.status}
                  </h1>
                </div>

                <div className="recommendation-box">
                  <h3>
                    Verification Message
                  </h3>

                  <p>
                    {repairResult.recommendation ||
                      repairResult.message ||
                      "Repair verification completed."}
                  </p>
                </div>
              </div>
            )}

          {repairResult?.error && (
            <div className="error-box">
              ❌ {repairResult.error}
            </div>
          )}
        </div>
      );
    }

    return null;
  };

  // ==================================================
  // MAIN UI
  // ==================================================

  return (
    <div className="app">
      {/* SIDEBAR */}

      <aside className="sidebar">
        <div className="logo">
          <div className="logo-icon">
            ⚡
          </div>

          <div>
            <h2>PCB-Diag</h2>

            <span>
              Intelligent Diagnostics
            </span>
          </div>
        </div>

        <div className="nav-section">
          <p className="nav-title">
            MAIN
          </p>

          <button
            className={
              activeSection === "dashboard"
                ? "sidebar-button active"
                : "sidebar-button"
            }
            onClick={() =>
              setActiveSection("dashboard")
            }
          >
            🏠 Dashboard
          </button>

          <button
            className={
              activeSection === "diagnose"
                ? "sidebar-button active"
                : "sidebar-button"
            }
            onClick={() =>
              setActiveSection("diagnose")
            }
          >
            🔧 Diagnose PCB
          </button>

          <button
            className={
              activeSection === "history"
                ? "sidebar-button active"
                : "sidebar-button"
            }
            onClick={() =>
              setActiveSection("history")
            }
          >
            📋 History
          </button>

          <button
            className={
              activeSection === "analytics"
                ? "sidebar-button active"
                : "sidebar-button"
            }
            onClick={() =>
              setActiveSection("analytics")
            }
          >
            📊 Analytics
          </button>

          <p className="nav-title repair-title">
            MAINTENANCE
          </p>

          <button
            className={
              activeSection === "repair"
                ? "sidebar-button active"
                : "sidebar-button"
            }
            onClick={() =>
              setActiveSection("repair")
            }
          >
            🔍 Repair Verification
          </button>
        </div>

        <div className="sidebar-footer">
          <div className="status-dot"></div>

          <div>
            <strong>
              System Online
            </strong>

            <span>
              API Connected
            </span>
          </div>
        </div>
      </aside>

      {/* MAIN CONTENT */}

      <main className="main-content">
        <div className="topbar">
          <div>
            <span className="system-label">
              PCB DIAGNOSTIC SYSTEM
            </span>
          </div>

          <div className="api-status">
            <span className="online-dot"></span>
            Backend Online
          </div>
        </div>

        {renderSection()}
      </main>
    </div>
  );
}

export default App;