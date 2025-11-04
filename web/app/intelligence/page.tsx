import { Card } from '@/components/Card';

const cards = [
  {
    title: 'Clinical Evidence Graph',
    description:
      'Surface curated oncology literature, practice-changing trials, and biomarker insights to support every care decision.'
  },
  {
    title: 'Tumor Board Navigator',
    description:
      'Coordinate multidisciplinary workflows with shared agendas, structured case summaries, and role-based collaboration.'
  },
  {
    title: 'Patient Journey Signals',
    description:
      'Monitor adherence, toxicity, and quality-of-life trends across cohorts to unlock proactive interventions.'
  }
];

export default function IntelligencePage() {
  return (
    <main className="mx-auto max-w-6xl px-6 py-26 lg:px-12">
      <header className="space-y-6 pb-18">
        <p className="text-sm font-semibold uppercase tracking-[0.2em] text-primary-600">Intelligence</p>
        <h1 className="text-4xl font-bold tracking-tight text-slate-900 sm:text-5xl">
          Operate with clarity across every patient journey.
        </h1>
        <p className="max-w-3xl text-lg text-slate-600">
          Karkinos Intelligence harmonizes guidelines, research, and real-world evidence to ensure each patient
          receives timely and precise interventions.
        </p>
      </header>
      <section className="grid gap-10 md:grid-cols-2">
        {cards.map(({ title, description }) => (
          <Card key={title} title={title} description={description} emptyState="Connect or upload guidelines" />
        ))}
      </section>
    </main>
  );
}
