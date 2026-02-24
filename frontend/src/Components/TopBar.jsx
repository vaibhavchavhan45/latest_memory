import logo from "../assets/logo.jpeg";

function TopBar({ onNewChat }) {
  return (
    <div className="
      w-full h-16 flex items-center justify-between px-6
      bg-[#1e1e1e]
      backdrop-blur-xl
      border-b border-white/5
      sticky top-0 z-50
    ">
      
      {/* LEFT: Brand */}
      <div className="flex items-center gap-3">
        <img
          src={logo}
          alt="FluxIntelAI Logo"
          className="h-11 w-11 rounded-xl object-contain"
        />

        <div className="flex flex-col leading-tight">
  <span className="tracking-wide" style={{ fontFamily: "'Playfair Display', serif" }}>
    <span className="text-[22px] font-black text-white" style={{ fontFamily: "'Playfair Display', serif" }}>F</span>
    <span className="text-[22px] font-black text-white" style={{ fontFamily: "'Playfair Display', serif" }}>lux</span>
    <span className="text-[22px] font-black text-white mx-0.5" style={{ fontFamily: "'Playfair Display', serif" }}>I</span>
    <span className="text-[22px] font-black text-white" style={{ fontFamily: "'Playfair Display', serif" }}>ntel</span>
    <span className="text-[22px] font-black text-white ml-0.5" style={{ fontFamily: "'Playfair Display', serif" }}>AI</span>
  </span>
  <span className="text-[12px] text-white/30 tracking-[0.1em]" style={{ fontFamily: "'Dancing Script', cursive", fontWeight: 300 }}>
  The Rizz RAG
</span>
</div>
      </div>

      {/* RIGHT */}
      <button
        type="button"
        onClick={onNewChat}
        className="
          px-5 py-2
          rounded-full
          bg-white/10 hover:bg-white/20
          text-white font-semibold text-sm
          flex items-center gap-2
          transition
        "
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="currentColor"
          className="size-4"
        >
          <path
            fillRule="evenodd"
            d="M15.75 2.25H21a.75.75 0 0 1 .75.75v5.25a.75.75 0 0 1-1.5 0V4.81L8.03 17.03a.75.75 0 0 1-1.06-1.06L19.19 3.75h-3.44a.75.75 0 0 1 0-1.5Zm-10.5 4.5a1.5 1.5 0 0 0-1.5 1.5v10.5a1.5 1.5 0 0 0 1.5 1.5h10.5a1.5 1.5 0 0 0 1.5-1.5V10.5a.75.75 0 0 1 1.5 0v8.25a3 3 0 0 1-3 3H5.25a3 3 0 0 1-3-3V8.25a3 3 0 0 1 3-3h8.25a.75.75 0 0 1 0 1.5H5.25Z"
            clipRule="evenodd"
          />
        </svg>
        <span>New Chat</span>
      </button>

    </div>
  );
}

export default TopBar;