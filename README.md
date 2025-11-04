# Karkinos

Karkinos is an intelligence workspace designed to help oncologists stay aligned with the latest evidence, collaborate across multidisciplinary teams, and match patients to the most relevant clinical trials. This first iteration focuses on the **Knowledge Base** feature, enabling clinicians to curate and organize guidelines and research assets from trusted sources.

## Getting started

This repository contains a Vite + React single-page application built with TypeScript.

```bash
npm install
npm run dev
```

The development server runs on [http://localhost:5173](http://localhost:5173).

> **Note:** Package installation requires access to the npm registry. In restricted environments you can still explore the codebase even if dependencies cannot be downloaded.

## Feature overview

### Knowledge Base (v0.1)

- **Evidence sources**: Browse NCCN, ASCO, ESMO, and PubMed Central collections presented as minimal, orange-accented cards.
- **Cancer libraries**: Drill down into cancer types within each source to view summaries and supported ingestion methods.
- **Document workspace**: Upload internal PDFs or simulate API captures to build a tailored guideline repository. Documents persist locally in the browser via `localStorage` for quick iteration.
- **API sync indicator**: Cancer libraries with future API integrations are highlighted, establishing the path toward automated ingestion.

### Design foundations

- Minimalist, white-heavy layout with soft gradients and orange accenting inspired by Apple-esque clarity.
- Placeholder Karkinos logomark for initial branding alignment.
- Responsive adjustments for smaller viewports while preserving focus on evidence curation workflows.

## Next steps

- Wire the upload workspace to backend storage and document processing pipelines.
- Expand beyond knowledge base: tumor board collaboration tools and clinical trial matching.
- Integrate real NCCN / ASCO / ESMO / PMC APIs and scheduling for continuous updates.
