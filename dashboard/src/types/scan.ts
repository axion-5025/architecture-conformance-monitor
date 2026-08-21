export interface ScanSummary {
  services_scanned: number
  files_scanned: number
  dependencies_found: number
  violations_found: number
}

export interface DependencyEvidence {
  source_file: string
  source_layer: string
  target_layer: string
  imported_module: string
}

export interface ServiceScanResult {
  service_name: string
  source_path: string
  files_scanned: number
  dependencies: DependencyEvidence[]
}

export interface Violation {
  violation_id: string
  rule_id: string
  severity: string
  message: string
  service_name: string
  source_file?: string
  source_layer?: string
  target_layer?: string
}

export interface ConformanceReport {
  generated_at: string
  application: string
  rules_version: string
  summary: ScanSummary
  services: ServiceScanResult[]
  violations: Violation[]
}

export interface ScanResponse {
  scan_id: number
  blocking: boolean
  report: ConformanceReport
}

export interface ScanHistoryItem {
  scan_id: number
  generated_at: string
  application: string
  rules_version: string
  services_scanned: number
  files_scanned: number
  dependencies_found: number
  violations_found: number
  blocking: boolean
}