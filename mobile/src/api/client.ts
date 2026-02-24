/**
 * API Client for Object Measurer Backend
 */

import { API_BASE_URL, API_ENDPOINTS } from '../config/api';

// ─── Types ───────────────────────────────────────────────────────────

export interface MeasurementPoint {
  x: number;
  y: number;
}

export interface MeasurementLine {
  start: MeasurementPoint;
  end: MeasurementPoint;
  distance: number;
  unit: string;
}

export interface MeasurementResult {
  id: number;
  title: string;
  original_image_url: string;
  result_image_url: string | null;
  reference_height: number;
  unit: string;
  pixel_ratio: number | null;
  horizontal_lines: MeasurementLine[];
  vertical_lines: MeasurementLine[];
  notes: string | null;
  created_at: string;
  updated_at: string;
}

export interface MeasurementSummary {
  id: number;
  title: string;
  result_image_url: string | null;
  reference_height: number;
  unit: string;
  created_at: string;
}

// ─── Helper ──────────────────────────────────────────────────────────

function getFullUrl(path: string): string {
  return `${API_BASE_URL}${path}`;
}

function getImageUrl(relativePath: string | null): string | null {
  if (!relativePath) return null;
  return `${API_BASE_URL}${relativePath}`;
}

// ─── API Functions ───────────────────────────────────────────────────

export async function checkHealth(): Promise<boolean> {
  try {
    const res = await fetch(getFullUrl(API_ENDPOINTS.health));
    return res.ok;
  } catch {
    return false;
  }
}

export async function createMeasurement(params: {
  imageUri: string;
  title?: string;
  referenceHeight: number;
  unit?: string;
  interval?: number;
  notes?: string;
}): Promise<MeasurementResult> {
  const formData = new FormData();

  // Expo provides file URIs - we need to create a proper file object
  const filename = params.imageUri.split('/').pop() || 'photo.jpg';
  const match = /\.(\w+)$/.exec(filename);
  const type = match ? `image/${match[1]}` : 'image/jpeg';

  formData.append('image', {
    uri: params.imageUri,
    name: filename,
    type,
  } as any);

  formData.append('reference_height', params.referenceHeight.toString());
  if (params.title) formData.append('title', params.title);
  if (params.unit) formData.append('unit', params.unit);
  if (params.interval) formData.append('interval', params.interval.toString());
  if (params.notes) formData.append('notes', params.notes);

  const res = await fetch(getFullUrl(API_ENDPOINTS.measure), {
    method: 'POST',
    body: formData,
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `Request failed: ${res.status}`);
  }

  const data: MeasurementResult = await res.json();

  // Convert relative URLs to full URLs
  data.original_image_url = getImageUrl(data.original_image_url) || '';
  data.result_image_url = getImageUrl(data.result_image_url);

  return data;
}

export async function getMeasurements(
  skip = 0,
  limit = 20
): Promise<MeasurementSummary[]> {
  const res = await fetch(
    getFullUrl(`${API_ENDPOINTS.history}?skip=${skip}&limit=${limit}`)
  );

  if (!res.ok) throw new Error(`Failed to fetch history: ${res.status}`);

  const data: MeasurementSummary[] = await res.json();

  return data.map((m) => ({
    ...m,
    result_image_url: getImageUrl(m.result_image_url),
  }));
}

export async function getMeasurement(id: number): Promise<MeasurementResult> {
  const res = await fetch(getFullUrl(`${API_ENDPOINTS.history}${id}`));

  if (!res.ok) throw new Error(`Failed to fetch measurement: ${res.status}`);

  const data: MeasurementResult = await res.json();
  data.original_image_url = getImageUrl(data.original_image_url) || '';
  data.result_image_url = getImageUrl(data.result_image_url);

  return data;
}

export async function updateMeasurement(
  id: number,
  update: { title?: string; notes?: string }
): Promise<MeasurementSummary> {
  const res = await fetch(getFullUrl(`${API_ENDPOINTS.history}${id}`), {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(update),
  });

  if (!res.ok) throw new Error(`Failed to update: ${res.status}`);

  const data: MeasurementSummary = await res.json();
  data.result_image_url = getImageUrl(data.result_image_url);
  return data;
}

export async function deleteMeasurement(id: number): Promise<void> {
  const res = await fetch(getFullUrl(`${API_ENDPOINTS.history}${id}`), {
    method: 'DELETE',
  });

  if (!res.ok) throw new Error(`Failed to delete: ${res.status}`);
}

export function getExportPdfUrl(id: number): string {
  return getFullUrl(`${API_ENDPOINTS.export}${id}/pdf`);
}
