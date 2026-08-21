import { useRef, useState } from 'react'
import {
  AlertTriangle,
  CheckCircle2,
  ChevronRight,
  FileWarning,
  History,
  X,
} from 'lucide-react'

import { getScanDetail } from '../services/api'
import type {
  ScanDetailResponse,
  ScanHistoryItem,
} from '../types/scan'

interface ScanHistoryProps {
  scans: ScanHistoryItem[]
  loading: boolean
}

function formatDate(value: string): string {
  const date = new Date(value)

  if (Number.isNaN(date.getTime())) {
    return 'Unknown'
  }

  return new Intl.DateTimeFormat('en-IN', {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(date)
}

function formatSeverity(value: string): string {
  if (!value) {
    return 'Unknown'
  }

  return value.charAt(0).toUpperCase() + value.slice(1)
}

export function ScanHistory({
  scans,
  loading,
}: ScanHistoryProps) {
  const [selectedScan, setSelectedScan] =
    useState<ScanDetailResponse | null>(null)
  const [selectedScanId, setSelectedScanId] =
    useState<number | null>(null)
  const [detailLoading, setDetailLoading] = useState(false)
  const [detailError, setDetailError] =
    useState<string | null>(null)

  const requestIdRef = useRef(0)

  async function handleSelectScan(scanId: number) {
    if (selectedScanId === scanId && selectedScan) {
      setSelectedScan(null)
      setSelectedScanId(null)
      setDetailError(null)
      return
    }

    const requestId = requestIdRef.current + 1
    requestIdRef.current = requestId

    setSelectedScanId(scanId)
    setSelectedScan(null)
    setDetailError(null)
    setDetailLoading(true)

    try {
      const detail = await getScanDetail(scanId)

      if (requestId === requestIdRef.current) {
        setSelectedScan(detail)
      }
    } catch (error) {
      if (requestId === requestIdRef.current) {
        setDetailError(
          error instanceof Error
            ? error.message
            : 'Unable to load scan details',
        )
      }
    } finally {
      if (requestId === requestIdRef.current) {
        setDetailLoading(false)
      }
    }
  }

  function handleCloseDetails() {
    requestIdRef.current += 1
    setSelectedScan(null)
    setSelectedScanId(null)
    setDetailError(null)
    setDetailLoading(false)
  }

  return (
    <section className="panel scan-history">
      <div className="panel__header">
        <div>
          <p className="eyebrow">Audit trail</p>
          <h2>Scan history</h2>
        </div>

        <History size={22} aria-hidden="true" />
      </div>

      {loading ? (
        <div className="empty-state">
          <div className="spinner" aria-hidden="true" />
          <p>Loading scan history…</p>
        </div>
      ) : scans.length === 0 ? (
        <div className="empty-state">
          <History size={32} aria-hidden="true" />
          <p>No scans have been recorded yet.</p>
        </div>
      ) : (
        <>
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>Scan</th>
                  <th>Generated</th>
                  <th>Services</th>
                  <th>Files</th>
                  <th>Dependencies</th>
                  <th>Violations</th>
                  <th>Status</th>
                  <th aria-label="View details" />
                </tr>
              </thead>

              <tbody>
                {scans.map((scan) => {
                  const isSelected =
                    selectedScanId === scan.scan_id

                  return (
                    <tr
                      key={scan.scan_id}
                      className={
                        isSelected
                          ? 'scan-history__row scan-history__row--selected'
                          : 'scan-history__row'
                      }
                    >
                      <td>
                        <button
                          className="scan-link"
                          type="button"
                          aria-expanded={isSelected}
                          aria-controls="scan-detail-panel"
                          onClick={() =>
                            void handleSelectScan(scan.scan_id)
                          }
                        >
                          #{scan.scan_id}
                        </button>
                      </td>

                      <td>{formatDate(scan.generated_at)}</td>
                      <td>{scan.services_scanned}</td>
                      <td>{scan.files_scanned}</td>
                      <td>{scan.dependencies_found}</td>
                      <td>{scan.violations_found}</td>

                      <td>
                        <span
                          className={
                            scan.blocking
                              ? 'status-badge status-badge--danger'
                              : 'status-badge status-badge--success'
                          }
                        >
                          {scan.blocking ? (
                            <AlertTriangle size={15} />
                          ) : (
                            <CheckCircle2 size={15} />
                          )}

                          {scan.blocking
                            ? 'Blocked'
                            : 'Conformant'}
                        </span>
                      </td>

                      <td>
                        <button
                          className="row-action"
                          type="button"
                          aria-label={`View details for scan ${scan.scan_id}`}
                          aria-expanded={isSelected}
                          aria-controls="scan-detail-panel"
                          onClick={() =>
                            void handleSelectScan(scan.scan_id)
                          }
                        >
                          <ChevronRight
                            size={18}
                            className={
                              isSelected
                                ? 'row-action__icon row-action__icon--open'
                                : 'row-action__icon'
                            }
                          />
                        </button>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>

          {(selectedScanId !== null ||
            selectedScan ||
            detailError) && (
            <div
              id="scan-detail-panel"
              className="scan-detail"
              aria-live="polite"
            >
              <div className="scan-detail__header">
                <div>
                  <span className="scan-detail__label">
                    Scan evidence
                  </span>

                  <h3>
                    {selectedScan
                      ? `Scan #${selectedScan.scan_id}`
                      : `Scan #${selectedScanId}`}
                  </h3>
                </div>

                <button
                  className="scan-detail__close"
                  type="button"
                  aria-label="Close scan details"
                  onClick={handleCloseDetails}
                >
                  <X size={18} />
                </button>
              </div>

              {detailLoading ? (
                <div className="scan-detail__state">
                  <div
                    className="spinner"
                    aria-hidden="true"
                  />
                  <p>Loading stored scan evidence…</p>
                </div>
              ) : detailError ? (
                <div
                  className="scan-detail__error"
                  role="alert"
                >
                  <AlertTriangle
                    size={20}
                    aria-hidden="true"
                  />

                  <div>
                    <strong>Unable to load scan</strong>
                    <p>{detailError}</p>
                  </div>
                </div>
              ) : selectedScan ? (
                <>
                  <div className="scan-detail__summary">
                    <div>
                      <span>Generated</span>
                      <strong>
                        {formatDate(selectedScan.generated_at)}
                      </strong>
                    </div>

                    <div>
                      <span>Application</span>
                      <strong>{selectedScan.application}</strong>
                    </div>

                    <div>
                      <span>Rule set</span>
                      <strong>{selectedScan.rules_version}</strong>
                    </div>

                    <div>
                      <span>Status</span>
                      <strong
                        className={
                          selectedScan.blocking
                            ? 'detail-status detail-status--danger'
                            : 'detail-status detail-status--success'
                        }
                      >
                        {selectedScan.blocking
                          ? 'Blocked'
                          : 'Conformant'}
                      </strong>
                    </div>
                  </div>

                  {selectedScan.violations.length === 0 ? (
                    <div className="scan-detail__clean">
                      <CheckCircle2
                        size={24}
                        aria-hidden="true"
                      />

                      <div>
                        <strong>No violations recorded</strong>
                        <p>
                          This scan passed all configured
                          architecture rules.
                        </p>
                      </div>
                    </div>
                  ) : (
                    <div className="violation-list">
                      {selectedScan.violations.map(
                        (violation) => (
                          <article
                            className="violation-card"
                            key={violation.violation_id}
                          >
                            <div className="violation-card__heading">
                              <div className="violation-card__icon">
                                <FileWarning
                                  size={20}
                                  aria-hidden="true"
                                />
                              </div>

                              <div>
                                <div className="violation-card__badges">
                                  <span className="violation-type">
                                    {violation.violation_type}
                                  </span>

                                  <span
                                    className={`severity-badge severity-badge--${violation.severity.toLowerCase()}`}
                                  >
                                    {formatSeverity(
                                      violation.severity,
                                    )}
                                  </span>
                                </div>

                                <h4>{violation.message}</h4>
                              </div>
                            </div>

                            <dl className="violation-card__evidence">
                              <div>
                                <dt>Service</dt>
                                <dd>
                                  {violation.service_name}
                                </dd>
                              </div>

                              <div>
                                <dt>Source</dt>
                                <dd>
                                  {violation.source_file}
                                  {violation.line > 0
                                    ? `:${violation.line}`
                                    : ''}
                                </dd>
                              </div>

                              <div>
                                <dt>Dependency</dt>
                                <dd>
                                  {violation.source_layer}
                                  {' → '}
                                  {violation.target_layer}
                                </dd>
                              </div>

                              <div>
                                <dt>Target module</dt>
                                <dd>
                                  {violation.target_module}
                                </dd>
                              </div>

                              <div>
                                <dt>Evidence</dt>
                                <dd>
                                  {violation.evidence_type}
                                </dd>
                              </div>

                              <div>
                                <dt>Violation ID</dt>
                                <dd>
                                  {violation.violation_id}
                                </dd>
                              </div>
                            </dl>
                          </article>
                        ),
                      )}
                    </div>
                  )}
                </>
              ) : null}
            </div>
          )}
        </>
      )}
    </section>
  )
}