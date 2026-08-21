import type {
  ScanHistoryItem,
  ScanResponse,
} from '../types/scan'

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

async function request<T>(
  path: string,
  options?: RequestInit,
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      Accept: 'application/json',
      ...options?.headers,
    },
  })

  if (!response.ok) {
    let message = `Request failed with status ${response.status}`

    try {
      const errorBody = (await response.json()) as {
        detail?: string
      }

      if (errorBody.detail) {
        message = errorBody.detail
      }
    } catch {
      // The server did not return a JSON error response.
    }

    throw new Error(message)
  }

  return (await response.json()) as T
}

export function createScan(): Promise<ScanResponse> {
  return request<ScanResponse>('/api/v1/scans', {
    method: 'POST',
  })
}

export function getLatestScan(): Promise<ScanResponse> {
  return request<ScanResponse>('/api/v1/scans/latest')
}

export function getScanHistory(): Promise<ScanHistoryItem[]> {
  return request<ScanHistoryItem[]>('/api/v1/scans/history')
}