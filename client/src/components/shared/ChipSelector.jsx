export default function ChipSelector({ options, selected, onToggle, maxSelection }) {
  const isSelected = (optionId) => selected.includes(optionId);
  
  const handleClick = (optionId) => {
    if (isSelected(optionId)) {
      onToggle(selected.filter(id => id !== optionId));
    } else {
      if (!maxSelection || selected.length < maxSelection) {
        onToggle([...selected, optionId]);
      }
    }
  };

  return (
    <div className="chip-selector">
      {options.map(option => (
        <button
          key={option.id}
          type="button"
          className={isSelected(option.id) ? 'chip active' : 'chip'}
          onClick={() => handleClick(option.id)}
        >
          {option.icon && <span className="chip-icon">{option.icon}</span>}
          {option.label}
        </button>
      ))}
    </div>
  );
}
