/**
 * React hooks for Temple API integration.
 */

import { useState, useCallback } from 'react';
import { templeApi } from '../services/templeApi';
import type {
  PatternDefinition,
  PatternMatchResponse,
  ScanResponse,
  UniverseListResponse,
} from '../types/api';

interface UseApiState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
}

/**
 * Hook for pattern matching.
 */
export function usePatternMatch() {
  const [state, setState] = useState<UseApiState<PatternMatchResponse>>({
    data: null,
    loading: false,
    error: null,
  });

  const matchPattern = useCallback(
    async (symbol: string, pattern: PatternDefinition, lookbackDays: number = 365) => {
      setState({ data: null, loading: true, error: null });

      try {
        const result = await templeApi.matchPattern({
          symbol,
          pattern,
          lookback_days: lookbackDays,
        });
        setState({ data: result, loading: false, error: null });
        return result;
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Unknown error';
        setState({ data: null, loading: false, error: errorMessage });
        throw error;
      }
    },
    []
  );

  return { ...state, matchPattern };
}

/**
 * Hook for stock scanning.
 */
export function useScanStocks() {
  const [state, setState] = useState<UseApiState<ScanResponse>>({
    data: null,
    loading: false,
    error: null,
  });

  const scanStocks = useCallback(
    async (
      symbolsOrUniverse: { symbols?: string[]; universe?: string },
      pattern: PatternDefinition,
      minConfidence: number = 0.7,
      parallel: boolean = true,
      lookbackDays: number = 365
    ) => {
      setState({ data: null, loading: true, error: null });

      try {
        const result = await templeApi.scanStocks({
          ...symbolsOrUniverse,
          pattern,
          min_confidence: minConfidence,
          parallel,
          lookback_days: lookbackDays,
        });
        setState({ data: result, loading: false, error: null });
        return result;
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Unknown error';
        setState({ data: null, loading: false, error: errorMessage });
        throw error;
      }
    },
    []
  );

  return { ...state, scanStocks };
}

/**
 * Hook for listing universes.
 */
export function useUniverses() {
  const [state, setState] = useState<UseApiState<UniverseListResponse>>({
    data: null,
    loading: false,
    error: null,
  });

  const fetchUniverses = useCallback(async () => {
    setState({ data: null, loading: true, error: null });

    try {
      const result = await templeApi.listUniverses();
      setState({ data: result, loading: false, error: null });
      return result;
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      setState({ data: null, loading: false, error: errorMessage });
      throw error;
    }
  }, []);

  return { ...state, fetchUniverses };
}

/**
 * Hook for getting example patterns.
 */
export function useExamplePatterns() {
  const [state, setState] = useState<UseApiState<PatternDefinition[]>>({
    data: null,
    loading: false,
    error: null,
  });

  const fetchExamples = useCallback(async () => {
    setState({ data: null, loading: true, error: null });

    try {
      const result = await templeApi.getExamplePatterns();
      setState({ data: result, loading: false, error: null });
      return result;
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      setState({ data: null, loading: false, error: errorMessage });
      throw error;
    }
  }, []);

  return { ...state, fetchExamples };
}

/**
 * Hook for health check.
 */
export function useHealthCheck() {
  const [state, setState] = useState({
    healthy: false,
    loading: false,
    error: null as string | null,
    mode: 'unknown' as string,
  });

  const checkHealth = useCallback(async () => {
    setState(prev => ({ ...prev, loading: true, error: null }));

    try {
      const result = await templeApi.scannerHealth();
      setState({
        healthy: result.status === 'healthy',
        loading: false,
        error: null,
        mode: result.mode,
      });
      return result;
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      setState({
        healthy: false,
        loading: false,
        error: errorMessage,
        mode: 'unknown',
      });
      throw error;
    }
  }, []);

  return { ...state, checkHealth };
}
