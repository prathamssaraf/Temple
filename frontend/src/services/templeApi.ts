/**
 * Temple API service for frontend integration.
 */

import type {
  PatternDefinition,
  PatternMatchRequest,
  PatternMatchResponse,
  ScanRequest,
  ScanResponse,
  UniverseListResponse,
  HealthCheckResponse
} from '../types/api';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const API_PREFIX = '/api/v1';

class TempleApiService {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  /**
   * Make a fetch request with error handling.
   */
  private async request<T>(
    endpoint: string,
    options?: RequestInit
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;

    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options?.headers,
        },
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || `HTTP ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      if (error instanceof Error) {
        throw error;
      }
      throw new Error('Unknown error occurred');
    }
  }

  // Health Check
  async healthCheck(): Promise<{ status: string; service: string }> {
    return this.request('/health');
  }

  async scannerHealth(): Promise<HealthCheckResponse> {
    return this.request(`${API_PREFIX}/scanner/health`);
  }

  // Pattern Endpoints
  async matchPattern(request: PatternMatchRequest): Promise<PatternMatchResponse> {
    return this.request(`${API_PREFIX}/patterns/match`, {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async getExamplePatterns(): Promise<PatternDefinition[]> {
    return this.request(`${API_PREFIX}/patterns/examples`);
  }

  // Scanner Endpoints
  async scanStocks(request: ScanRequest): Promise<ScanResponse> {
    return this.request(`${API_PREFIX}/scanner/scan`, {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async listUniverses(): Promise<UniverseListResponse> {
    return this.request(`${API_PREFIX}/scanner/universes`);
  }

  // Convenience Methods
  async scanSymbols(
    symbols: string[],
    pattern: PatternDefinition,
    minConfidence: number = 0.7,
    parallel: boolean = true
  ): Promise<ScanResponse> {
    return this.scanStocks({
      symbols,
      pattern,
      min_confidence: minConfidence,
      parallel,
    });
  }

  async scanUniverse(
    universe: string,
    pattern: PatternDefinition,
    minConfidence: number = 0.7,
    parallel: boolean = true
  ): Promise<ScanResponse> {
    return this.scanStocks({
      universe,
      pattern,
      min_confidence: minConfidence,
      parallel,
    });
  }
}

// Export singleton instance
export const templeApi = new TempleApiService();

// Also export the class for custom instances
export default TempleApiService;
