import type {
  ScanDetailResponse,
  ScanHistoryItem,
  ScanResponse,
} from '../types/scan'

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

interface ApiErrorResponse {
  detail?: string
}

async function request<T>(
  path: string,
  options?: RequestInit,
): Promise<T> {
  let response: Response

  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      ...options,
      headers: {
        Accept: 'application/json',
        ...options?.headers,
      },
    })
  } catch {
    throw new Error(
      'Unable to connect to the Architecture Guard API',
    )
  }

  if (!response.ok) {
    let message = `Request failed with status ${response.status}`

    try {
      const errorBody =
        (await response.json()) as ApiErrorResponse

      if (errorBody.detail) {
        message = errorBody.detail
      }
    } catch {
      // Keep the status-based fallback when no JSON body exists.
    }

    throw new Error(message)
  }

  if (response.status === 204) {
    return undefined as T
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

export function getScanDetail(
  scanId: number,
): Promise<ScanDetailResponse> {
  if (!Number.isInteger(scanId) || scanId <= 0) {
    return Promise.reject(
      new Error('A valid scan ID is required'),
    )
  }

  return request<ScanDetailResponse>(
    `/api/v1/scans/${scanId}`,
  )
}