import Link from 'next/link';

const highlights = [
  {
    title: 'Clinical Intelligence',
    description:
      'Unify evidence-based guidance from NCCN, ASCO, and ESMO with literature from PubMed Central.',
    href: '/intelligence'
  },
  {
    title: 'Source Transparency',
    description: 'Track provenance for every document and chunk to accelerate tumor board reviews.',
    href: '/intelligence/nccn'
  },
  {
    title: 'Semantic Search',
    description: 'Retrieve nuanced oncology context using pgvector embeddings tuned for clinical text.',
    href: '/intelligence'
  }
];

export default function HomePage() {
  return (
    <section className="space-y-12">
      <div className="space-y-6">
        <h1 className="text-4xl font-semibold tracking-tight text-slate-900 sm:text-5xl">
          Oncology knowledge, curated.
        </h1>
        <p className="max-w-2xl text-lg text-slate-500">
          Karkinos delivers a minimalist interface for reviewing the latest clinical guidelines,
          research updates, and evidence summaries tailored to oncology teams.
        </p>
      </div>
      <div className="card-grid">
        {highlights.map((highlight) => (
          <Link key={highlight.title} href={highlight.href} className="card">
            <h2 className="card-title">{highlight.title}</h2>
            <p className="card-description">{highlight.description}</p>
            <span className="mt-6 inline-flex items-center text-sm font-semibold text-primary-600">
              Explore
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.5"
                className="ml-2 h-4 w-4"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M13.5 4.5L21 12l-7.5 7.5M21 12H3"
                />
              </svg>
            </span>
          </Link>
        ))}
      </div>
    </section>
  );
}
