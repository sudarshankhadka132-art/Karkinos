export type EvidenceSource = {
  id: string;
  name: string;
  description: string;
  accent: string;
  cancers: CancerType[];
};

export type CancerType = {
  id: string;
  name: string;
  summary: string;
  supportApi: boolean;
};

export const knowledgeSources: EvidenceSource[] = [
  {
    id: 'nccn',
    name: 'NCCN',
    description: 'Continuously updated standards of care from the National Comprehensive Cancer Network.',
    accent: '#ff6b2c',
    cancers: [
      { id: 'breast', name: 'Breast Cancer', summary: 'Latest algorithms covering screening to adjuvant therapy.', supportApi: false },
      { id: 'lung', name: 'Non-Small Cell Lung Cancer', summary: 'Staging-driven care pathways and biomarker directed regimens.', supportApi: false },
      { id: 'prostate', name: 'Prostate Cancer', summary: 'Localized and metastatic treatment recommendations.', supportApi: false }
    ]
  },
  {
    id: 'asco',
    name: 'ASCO',
    description: 'Clinical practice guidelines and living updates curated by ASCO expert panels.',
    accent: '#ff8b55',
    cancers: [
      { id: 'breast', name: 'Breast Cancer', summary: 'Patient stratification and systemic therapy updates.', supportApi: false },
      { id: 'colorectal', name: 'Colorectal Cancer', summary: 'Adjuvant, metastatic, and MSI-H targeted care recommendations.', supportApi: false },
      { id: 'pancreatic', name: 'Pancreatic Cancer', summary: 'Systemic regimens and supportive care guidance.', supportApi: false }
    ]
  },
  {
    id: 'esmo',
    name: 'ESMO',
    description: 'European Society for Medical Oncology evidence-based clinical practice guidelines.',
    accent: '#ff9d6d',
    cancers: [
      { id: 'ovarian', name: 'Ovarian Cancer', summary: 'First-line, maintenance, and recurrence management pathways.', supportApi: false },
      { id: 'melanoma', name: 'Melanoma', summary: 'Targeted and immunotherapy guidance across stages.', supportApi: false },
      { id: 'gastric', name: 'Gastric Cancer', summary: 'Precision medicine informed systemic therapy options.', supportApi: false }
    ]
  },
  {
    id: 'pmc',
    name: 'PubMed Central',
    description: 'Open-access biomedical literature from the US National Library of Medicine.',
    accent: '#ff7d3d',
    cancers: [
      { id: 'hematologic', name: 'Hematologic Malignancies', summary: 'Rapidly evolving evidence base for leukemias and lymphomas.', supportApi: true },
      { id: 'sarcoma', name: 'Sarcoma', summary: 'Rare tumor insights consolidated from multi-center studies.', supportApi: true },
      { id: 'neuro-oncology', name: 'Neuro-Oncology', summary: 'Glioma and CNS tumor research with molecular profiling.', supportApi: true }
    ]
  }
];
