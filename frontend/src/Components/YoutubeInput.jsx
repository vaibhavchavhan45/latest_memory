// src/Components/YoutubeInput.jsx

function YoutubeInput({ value, onChange }) {
  return (
    <input
      type="text"
      placeholder="Paste the YouTube URL"
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="
        w-full
        px-4 py-3
        rounded-xl
        bg-[#2f2f2f]
        border border-white/10
        text-blue-400
        caret-white
        placeholder-[#9aa0a6]
        outline-none
        transition-all duration-200
        focus:border-white/20
        focus:placeholder-[#cfd3d7]
      "
    />
  );
}

export default YoutubeInput;
