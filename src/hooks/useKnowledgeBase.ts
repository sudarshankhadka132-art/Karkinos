import { useEffect, useMemo, useReducer } from 'react';
import type { EvidenceSource, CancerType } from '../data/knowledgeSources';

type StorageKey = `${string}:${string}`;

type GuidelineOrigin = 'upload' | 'api';

export type GuidelineDocument = {
  id: string;
  name: string;
  uploadedAt: string;
  size?: number;
  origin: GuidelineOrigin;
  notes?: string;
};

type KnowledgeAction =
  | { type: 'load'; payload: Record<StorageKey, GuidelineDocument[]> }
  | { type: 'add'; source: EvidenceSource; cancer: CancerType; document: GuidelineDocument }
  | { type: 'remove'; source: EvidenceSource; cancer: CancerType; documentId: string };

type KnowledgeState = Record<StorageKey, GuidelineDocument[]>;

const STORAGE_PREFIX = 'karkinos-guidelines';

const storageKeyFor = (sourceId: string, cancerId: string): StorageKey => `${sourceId}:${cancerId}`;

const reducer = (state: KnowledgeState, action: KnowledgeAction): KnowledgeState => {
  switch (action.type) {
    case 'load':
      return { ...state, ...action.payload };
    case 'add': {
      const key = storageKeyFor(action.source.id, action.cancer.id);
      const existing = state[key] ?? [];
      return {
        ...state,
        [key]: [...existing, action.document]
      };
    }
    case 'remove': {
      const key = storageKeyFor(action.source.id, action.cancer.id);
      const existing = state[key] ?? [];
      return {
        ...state,
        [key]: existing.filter((item) => item.id !== action.documentId)
      };
    }
    default:
      return state;
  }
};

export const useKnowledgeBase = () => {
  const [state, dispatch] = useReducer(reducer, {});

  useEffect(() => {
    const saved = window.localStorage.getItem(STORAGE_PREFIX);
    if (saved) {
      try {
        const parsed = JSON.parse(saved) as KnowledgeState;
        dispatch({ type: 'load', payload: parsed });
      } catch (error) {
        console.warn('Unable to parse stored guidelines', error);
      }
    }
  }, []);

  useEffect(() => {
    window.localStorage.setItem(STORAGE_PREFIX, JSON.stringify(state));
  }, [state]);

  const getDocuments = useMemo(() => {
    return (sourceId: string, cancerId: string) => {
      const key = storageKeyFor(sourceId, cancerId);
      return state[key] ?? [];
    };
  }, [state]);

  const addDocument = (source: EvidenceSource, cancer: CancerType, document: GuidelineDocument) => {
    dispatch({ type: 'add', source, cancer, document });
  };

  const removeDocument = (source: EvidenceSource, cancer: CancerType, documentId: string) => {
    dispatch({ type: 'remove', source, cancer, documentId });
  };

  return { getDocuments, addDocument, removeDocument };
};
