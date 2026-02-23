function TopBar({ onNewChat }) {
  return (
    <div className="w-full h-14 flex items-center justify-between px-4 bg-[#1e1e1e] border-b border-white/10">
      
      {/* LEFT: App Name */}
      <div className="text-white font-semibold text-sm">
        YouTube RAG
      </div>

      {/* RIGHT: Actions */}
      <button
        type="button"
        onClick={onNewChat}
        className="text-sm text-white/70 hover:text-white transition"
      >
        New Chat
      </button>
    </div>
  );
}

export default TopBar;
