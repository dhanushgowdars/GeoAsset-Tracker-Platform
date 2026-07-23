function StatCard({ label, value, detail, tone = "default" }) {
  return (
    <article className={`stat-card stat-card-${tone}`}>
      <p>{label}</p>
      <strong>{value}</strong>
      <span>{detail}</span>
    </article>
  );
}

export default StatCard;
