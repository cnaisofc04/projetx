export default function Logo({ size = 60 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="50" cy="50" r="48" fill="white" stroke="#FF1493" strokeWidth="2"/>
      
      <path d="M50 50 Q30 30 20 50 T50 70 Z" fill="#FF1493"/>
      
      <path d="M50 50 Q70 30 80 50 T50 70 Z" fill="#000"/>
      
      <path d="M35 20 L40 10 L37 25" fill="white" stroke="white" strokeWidth="1.5"/>
      <path d="M45 15 L48 8 L46 22" fill="white" stroke="white" strokeWidth="1.5"/>
      
      <path d="M65 75 L60 85 L63 70" fill="#FF1493" stroke="#FF1493" strokeWidth="1.5"/>
      <path d="M55 80 L52 87 L54 73" fill="#FF1493" stroke="#FF1493" strokeWidth="1.5"/>
      
      <circle cx="50" cy="50" r="8" fill="white"/>
      <text x="50" y="55" textAnchor="middle" fontSize="10" fontWeight="bold" fill="#FF1493">12</text>
    </svg>
  );
}
