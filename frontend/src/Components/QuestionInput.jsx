import { useRef, useState, useEffect } from "react";

function QuestionInput({ value, onChange, onAsk, mode, youtubeUrl, loading, inputRef }) {
  const textareaRef = useRef(null);
  const [isMultilineInput, setIsMultilineInput] = useState(false);

  const isInitialDisabled =
    mode === "initial" && (!youtubeUrl?.trim() || !value.trim() || loading);

  const isChatDisabled =
    mode === "chat" && (!value.trim() || loading);

  const handleChange = (e) => {
    const el = e.target;
    onChange(el.value);

    el.style.height = "48px";
    el.style.height = Math.min(el.scrollHeight, 200) + "px";

    const meaningfulLines = el.value
      .split("\n")
      .filter((l) => l.trim() !== "");

    const hasMeaningfulNewLine = meaningfulLines.length > 1;
    const hasWrappedLine =
      el.scrollHeight > 48 && meaningfulLines.length === 1;

    setIsMultilineInput(hasMeaningfulNewLine || hasWrappedLine);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (!isInitialDisabled && !isChatDisabled) {
        onAsk();
      }
    }
  };

  useEffect(() => {
    if (!value && textareaRef.current) {
      textareaRef.current.style.height = "48px";
      setIsMultilineInput(false);
    }
  }, [value]);

  useEffect(() => {
    if (mode === "chat" && !loading && textareaRef.current) {
      textareaRef.current.focus();
    }
  }, [loading]);

  if (mode === "initial") {
    return (
      <div className="flex flex-col items-center">
        <textarea
          ref={textareaRef}
          rows={1}
          value={value}
          placeholder="Ask a question"
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          disabled={loading}
          className="w-full resize-none overflow-hidden px-4 py-3 min-h-[48px] leading-[24px] rounded-xl bg-[#2f2f2f] border border-white/10 text-white placeholder-gray-400 focus:placeholder-gray-200 outline-none"
        />

        <button
          type="button"
          onClick={onAsk}
          disabled={isInitialDisabled}
          className="mt-6 w-1/4 py-2 rounded-full bg-white text-black disabled:bg-white/40"
        >
          Ask
        </button>
      </div>
    );
  }

  return (
    <div className="relative w-full">
      <textarea
        ref={(el) => {
          textareaRef.current = el;
          if (inputRef) inputRef.current = el;
        }}
        rows={1}
        value={value}
        placeholder="Ask a question"
        onChange={handleChange}
        onKeyDown={handleKeyDown}
        disabled={loading}
        className={`w-full resize-none overflow-hidden min-h-[48px] leading-[24px] bg-[#2f2f2f] border border-white/10 text-white placeholder-gray-400 focus:placeholder-gray-200 outline-none px-4 py-3 pr-16 ${
          isMultilineInput ? "rounded-xl" : "rounded-full"
        }`}
      />

      <div
        className={`absolute right-3 ${
          isMultilineInput ? "bottom-3" : "top-0 min-h-[48px]"
        } flex items-center`}
      >
        <button
          type="button"
          onClick={onAsk}
          disabled={isChatDisabled}
          className="w-9 h-9 rounded-full bg-white text-black disabled:bg-white/40 flex items-center justify-center"
        >
          ↑
        </button>
      </div>
    </div>
  );
}

export default QuestionInput;