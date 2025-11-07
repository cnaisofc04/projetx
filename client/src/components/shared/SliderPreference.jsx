export default function SliderPreference({ label, value, onChange, leftLabel, rightLabel, description }) {
  const getLabel = (val) => {
    if (val < 25) return `Pas ${leftLabel?.toLowerCase() || 'intéressé'}`;
    if (val < 45) return `Plutôt ${leftLabel?.toLowerCase() || 'non'}`;
    if (val >= 45 && val <= 55) return 'Neutre';
    if (val > 75) return `Très ${rightLabel?.toLowerCase() || 'intéressé'}`;
    return `Plutôt ${rightLabel?.toLowerCase() || 'oui'}`;
  };

  return (
    <div className="preference-item">
      <div className="preference-header">
        <label>{label}</label>
        <span className="preference-value">{value}%</span>
      </div>
      
      <div className="slider-labels">
        <span>{leftLabel}</span>
        <span>{rightLabel}</span>
      </div>

      <input
        type="range"
        min="0"
        max="100"
        value={value}
        onChange={(e) => onChange(parseInt(e.target.value))}
        className="preference-slider"
      />

      <div className="preference-description">
        {description || getLabel(value)}
      </div>
    </div>
  );
}
