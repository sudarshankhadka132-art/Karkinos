import type { ReactNode } from 'react';
import clsx from 'clsx';

type CardProps = {
  title: string;
  description?: string;
  emptyState?: ReactNode;
  className?: string;
  children?: ReactNode;
};

export function Card({ title, description, emptyState, className, children }: CardProps) {
  return (
    <section
      className={clsx(
        'flex flex-col gap-6 rounded-3xl border border-primary-100 bg-white px-8 py-12 shadow-soft transition hover:-translate-y-1 hover:shadow-lg',
        className
      )}
    >
      <div className="space-y-4">
        <h2 className="text-2xl font-semibold text-slate-900">{title}</h2>
        {description && <p className="text-base text-slate-600">{description}</p>}
      </div>
      {children}
      {emptyState && (
        <p className="text-sm font-medium text-slate-400">{emptyState}</p>
      )}
    </section>
  );
}
