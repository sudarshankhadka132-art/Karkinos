import Link from 'next/link';

export default function HomePage() {
  return (
    <main className="mx-auto flex min-h-screen max-w-5xl flex-col justify-center px-6 py-26 lg:px-12">
      <section className="space-y-6">
        <p className="text-sm font-semibold uppercase tracking-wide text-primary-600">Karkinos</p>
        <h1 className="text-4xl font-bold tracking-tight text-slate-900 sm:text-5xl">
          Intelligent Platform for Oncologists
        </h1>
        <p className="max-w-2xl text-lg text-slate-600">
          Navigate evidence-based care pathways, coordinate multi-disciplinary teams, and stay ahead of
          evolving guidelines.
        </p>
        <div>
          <Link
            href="/intelligence"
            className="inline-flex items-center rounded-full bg-primary-600 px-5 py-2.5 text-sm font-semibold text-white shadow-soft transition hover:bg-primary-700"
          >
            Explore Intelligence
          </Link>
        </div>
      </section>
    </main>
  );
}
