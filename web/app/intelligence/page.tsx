import Link from 'next/link';

const intelligenceCards = [
  {
    title: 'NCCN',
    description: 'National Comprehensive Cancer Network guidelines distilled into actionable insights.',
    href: '/intelligence/nccn'
  },
  {
    title: 'ASCO',
    description: 'American Society of Clinical Oncology recommendations summarized for rapid review.',
    href: '/intelligence/asco'
  },
  {
    title: 'ESMO',
    description: 'European Society for Medical Oncology perspectives on global standards of care.',
    href: '/intelligence/esmo'
  },
  {
    title: 'PubMed Central',
    description: 'Peer-reviewed literature, surfaced via embeddings-aware semantic search.',
    href: '/intelligence/pubmed-central'
  }
];

export default function IntelligencePage() {
  return (
    <section className="space-y-10">
      <div className="space-y-4">
        <h1 className="text-3xl font-semibold tracking-tight text-slate-900 sm:text-4xl">
          Intelligence Sources
        </h1>
        <p className="max-w-2xl text-base text-slate-500">
          Navigate our curated oncology sources. Each card will expand into focused workspaces as the
          platform evolves.
        </p>
      </div>
      <div className="card-grid">
        {intelligenceCards.map((card) => (
          <Link key={card.title} href={card.href} className="card">
            <h2 className="card-title">{card.title}</h2>
            <p className="card-description">{card.description}</p>
          </Link>
        ))}
      </div>
    </section>
  );
}
