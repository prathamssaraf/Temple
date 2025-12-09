/**
 * TypeScript types for Temple API.
 */

// Pattern Types
export interface EventDefinition {
  event_type: string;
  parameters: Record<string, any>;
}

export interface SequenceStep {
  event: EventDefinition;
  min_interval_days?: number;
  max_interval_days?: number;
}

export interface FrequencyConstraint {
  min_occurrences: number;
  timeframe_days: number;
}

export interface PatternDefinition {
  name: string;
  description: string;
  sequence: SequenceStep[];
  frequency: FrequencyConstraint;
}

// Pattern Match Types
export interface OccurrenceDetail {
  start_date: string;
  end_date: string;
  confidence: number;
}

export interface PatternMatchRequest {
  symbol: string;
  pattern: PatternDefinition;
  lookback_days: number;
}

export interface PatternMatchResponse {
  symbol: string;
  pattern_name: string;
  matched: boolean;
  confidence: number;
  occurrences: number;
  occurrence_details: OccurrenceDetail[];
  timeframe_start: string;
  timeframe_end: string;
}

// Scanner Types
export interface ScanRequest {
  symbols?: string[];
  universe?: string;
  pattern: PatternDefinition;
  min_confidence: number;
  parallel: boolean;
}

export interface ScanResultItem {
  symbol: string;
  pattern_name: string;
  matched: boolean;
  confidence: number;
  occurrences: number;
  timeframe_start: string;
  timeframe_end: string;
}

export interface ScanResponse {
  total_symbols: number;
  successful_scans: number;
  failed_scans: number;
  matches_found: number;
  average_confidence: number;
  duration_seconds: number;
  results: ScanResultItem[];
}

// Universe Types
export interface UniverseInfo {
  name: string;
  description: string;
  symbol_count: number;
}

export interface UniverseListResponse {
  universes: UniverseInfo[];
}

// Health Check Types
export interface ComponentHealth {
  data_layer: boolean;
  pattern_matcher: boolean;
  scanner: boolean;
}

export interface HealthCheckResponse {
  status: string;
  components: ComponentHealth;
  mode: string;
}
