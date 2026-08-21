import type { LucideIcon } from 'lucide-react'

interface MetricCardProps {
  label: string
  value: number
  description: string
  icon: LucideIcon
  tone?: 'blue' | 'green' | 'amber' | 'red'
}

export function MetricCard({
  label,
  value,
  description,
  icon: Icon,
  tone = 'blue',
}: MetricCardProps) {
  return (
    <article className={`metric-card metric-card--${tone}`}>
      <div className="metric-card__header">
        <span className="metric-card__label">{label}</span>

        <span className="metric-card__icon" aria-hidden="true">
          <Icon size={20} strokeWidth={2} />
        </span>
      </div>

      <strong className="metric-card__value">{value}</strong>
      <p className="metric-card__description">{description}</p>
    </article>
  )
}