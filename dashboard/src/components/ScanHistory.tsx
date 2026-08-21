import {
  AlertTriangle,
  CheckCircle2,
  History,
} from 'lucide-react'

import type { ScanHistoryItem } from '../types/scan'

interface ScanHistoryProps {
  scans: ScanHistoryItem[]
  loading: boolean
}

function formatDate(value: string): string {
  return new Intl.DateTimeFormat('en-IN', {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(value))
}

export function ScanHistory({
  scans,
  loading,
}: ScanHistoryProps) {
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
              </tr>
            </thead>

            <tbody>
              {scans.map((scan) => (
                <tr key={scan.scan_id}>
                  <td>#{scan.scan_id}</td>
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

                      {scan.blocking ? 'Blocked' : 'Conformant'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  )
}