import { useCallback, useEffect, useMemo, useState } from 'react'
import {
  Activity,
  AlertTriangle,
  Boxes,
  FileCode2,
  GitBranch,
  Play,
  RefreshCw,
  ScanSearch,
  ShieldCheck,
} from 'lucide-react'
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

import './App.css'
import { MetricCard } from './components/MetricCard'
import { ScanHistory } from './components/ScanHistory'
import {
  createScan,
  getLatestScan,
  getScanHistory,
} from './services/api'
import type {
  ScanHistoryItem,
  ScanResponse,
} from './types/scan'

function App() {
  const [latestScan, setLatestScan] =
    useState<ScanResponse | null>(null)
  const [history, setHistory] = useState<ScanHistoryItem[]>([])
  const [loading, setLoading] = useState(true)
  const [scanning, setScanning] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const loadDashboard = useCallback(async () => {
    setLoading(true)
    setError(null)

    const [latestResult, historyResult] = await Promise.allSettled([
      getLatestScan(),
      getScanHistory(),
    ])

    if (latestResult.status === 'fulfilled') {
      setLatestScan(latestResult.value)
    } else {
      setLatestScan(null)
    }

    if (historyResult.status === 'fulfilled') {
      setHistory(historyResult.value)
    } else {
      setHistory([])
      setError(
        historyResult.reason instanceof Error
          ? historyResult.reason.message
          : 'Unable to load scan history',
      )
    }

    setLoading(false)
  }, [])

  useEffect(() => {
    void loadDashboard()
  }, [loadDashboard])

  async function handleRunScan() {
    setScanning(true)
    setError(null)

    try {
      await createScan()
      await loadDashboard()
    } catch (scanError) {
      setError(
        scanError instanceof Error
          ? scanError.message
          : 'The architecture scan failed',
      )
    } finally {
      setScanning(false)
    }
  }

  const summary = latestScan?.report.summary

  const chartData = useMemo(
    () =>
      [...history]
        .slice(0, 8)
        .reverse()
        .map((scan) => ({
          scan: `#${scan.scan_id}`,
          dependencies: scan.dependencies_found,
          violations: scan.violations_found,
        })),
    [history],
  )

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand">
          <span className="brand__icon" aria-hidden="true">
            <GitBranch size={21} />
          </span>

          <strong>Architecture Guard</strong>
        </div>
      </header>

      <main className="dashboard">
        <section className="page-header">
          <div>
            <h1>Architecture overview</h1>
            <p>
              Monitor service boundaries, dependencies, and violations.
            </p>
          </div>

          <div className="page-header__actions">
            <button
              className="secondary-button"
              type="button"
              onClick={() => void loadDashboard()}
              disabled={loading || scanning}
              aria-label="Refresh dashboard"
            >
              <RefreshCw
                size={17}
                className={loading ? 'spin' : undefined}
              />
              Refresh
            </button>

            <button
              className="primary-button"
              type="button"
              onClick={() => void handleRunScan()}
              disabled={scanning}
            >
              {scanning ? (
                <RefreshCw size={17} className="spin" />
              ) : (
                <Play size={17} fill="currentColor" />
              )}

              {scanning ? 'Scanning…' : 'Run scan'}
            </button>
          </div>
        </section>

        {error && (
          <div className="error-banner" role="alert">
            <AlertTriangle size={19} aria-hidden="true" />

            <div>
              <strong>Backend unavailable</strong>
              <span>
                Start the backend services and refresh the dashboard.
              </span>
            </div>
          </div>
        )}

        <section
          className="metric-grid"
          aria-label="Latest scan summary"
        >
          <MetricCard
            label="Services"
            value={summary?.services_scanned ?? 0}
            description="Services included in the scan"
            icon={Boxes}
            tone="blue"
          />

          <MetricCard
            label="Files"
            value={summary?.files_scanned ?? 0}
            description="Python files inspected"
            icon={FileCode2}
            tone="green"
          />

          <MetricCard
            label="Dependencies"
            value={summary?.dependencies_found ?? 0}
            description="Internal dependencies detected"
            icon={GitBranch}
            tone="amber"
          />

          <MetricCard
            label="Violations"
            value={summary?.violations_found ?? 0}
            description="Architecture rules violated"
            icon={AlertTriangle}
            tone={
              summary?.violations_found
                ? 'red'
                : 'green'
            }
          />
        </section>

        <section className="dashboard-grid">
          <article className="panel overview-panel">
            <div className="panel__header">
              <div>
                <h2>Conformance status</h2>
              </div>

              {latestScan?.blocking ? (
                <AlertTriangle
                  className="danger-icon"
                  size={22}
                  aria-hidden="true"
                />
              ) : (
                <ShieldCheck
                  className="success-icon"
                  size={22}
                  aria-hidden="true"
                />
              )}
            </div>

            <div className="conformance-result">
              <div
                className={
                  latestScan?.blocking
                    ? 'score-ring score-ring--danger'
                    : 'score-ring score-ring--success'
                }
              >
                {!latestScan ? (
                  <ScanSearch size={30} aria-hidden="true" />
                ) : latestScan.blocking ? (
                  <AlertTriangle size={30} aria-hidden="true" />
                ) : (
                  <ShieldCheck size={30} aria-hidden="true" />
                )}
              </div>

              <div>
                <h3>
                  {!latestScan
                    ? 'No scan available'
                    : latestScan.blocking
                      ? 'Release blocked'
                      : 'Conformant'}
                </h3>

                <p>
                  {!latestScan
                    ? 'Run a scan to evaluate the current architecture.'
                    : latestScan.blocking
                      ? 'Resolve blocking violations before release.'
                      : 'No blocking violations were detected.'}
                </p>
              </div>
            </div>

            {latestScan && (
              <dl className="scan-metadata">
                <div>
                  <dt>Application</dt>
                  <dd>{latestScan.report.application}</dd>
                </div>

                <div>
                  <dt>Rule set</dt>
                  <dd>{latestScan.report.rules_version}</dd>
                </div>

                <div>
                  <dt>Scan</dt>
                  <dd>#{latestScan.scan_id}</dd>
                </div>
              </dl>
            )}
          </article>

          <article className="panel chart-panel">
            <div className="panel__header">
              <div>
                <h2>Findings trend</h2>
              </div>

              <Activity size={21} aria-hidden="true" />
            </div>

            {chartData.length === 0 ? (
              <div className="empty-state">
                <Activity size={30} aria-hidden="true" />
                <p>No trend data available.</p>
              </div>
            ) : (
              <div className="chart-container">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={chartData}
                    margin={{
                      top: 8,
                      right: 8,
                      left: -18,
                      bottom: 0,
                    }}
                  >
                    <CartesianGrid
                      stroke="#e5eaf1"
                      strokeDasharray="4 4"
                      vertical={false}
                    />

                    <XAxis
                      dataKey="scan"
                      axisLine={false}
                      tickLine={false}
                      tick={{ fill: '#64748b', fontSize: 11 }}
                    />

                    <YAxis
                      allowDecimals={false}
                      axisLine={false}
                      tickLine={false}
                      tick={{ fill: '#64748b', fontSize: 11 }}
                    />

                    <Tooltip
                      cursor={{ fill: '#f8fafc' }}
                      contentStyle={{
                        border: '1px solid #dfe6ef',
                        borderRadius: '9px',
                        boxShadow:
                          '0 8px 24px rgba(15, 23, 42, 0.08)',
                      }}
                    />

                    <Bar
                      dataKey="dependencies"
                      name="Dependencies"
                      fill="#3b82f6"
                      radius={[4, 4, 0, 0]}
                    />

                    <Bar
                      dataKey="violations"
                      name="Violations"
                      fill="#ef4444"
                      radius={[4, 4, 0, 0]}
                    />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            )}
          </article>
        </section>

        <ScanHistory scans={history} loading={loading} />
      </main>
    </div>
  )
}

export default App