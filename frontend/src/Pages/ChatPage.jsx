import { useState, useRef } from "react";
import YoutubeInput from "../Components/YoutubeInput";
import QuestionInput from "../Components/QuestionInput";
import TopBar from "../Components/TopBar";
import ChatMessages from "../Components/ChatMessages";

function ChatPage() {
  const [youtubeUrl, setYoutubeUrl] = useState("");
  const [question, setQuestion] = useState("");
  const [hasAskedOnce, setHasAskedOnce] = useState(false);
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([]);

  const chatInputRef = useRef(null);
  const scrollRef = useRef(null);

  const isRenderedMultiline = (text) => {
    const el = document.createElement("div");
    el.style.position = "absolute";
    el.style.visibility = "hidden";
    el.style.whiteSpace = "pre-wrap";
    el.style.wordBreak = "break-word";
    el.style.width = "520px";
    el.style.fontSize = "16px";
    el.style.lineHeight = "24px";
    el.textContent = text;

    document.body.appendChild(el);
    const height = el.scrollHeight;
    document.body.removeChild(el);

    return height > 24;
  };

  const handleAsk = async () => {
    const trimmed = question.trim();
    if (!trimmed) return;

    if (!hasAskedOnce) setHasAskedOnce(true);

    const lines = trimmed
      .split("\n")
      .filter((l) => l.trim() !== "");

    const isMultiline =
      lines.length > 1 || isRenderedMultiline(trimmed);

    const msgId = `user-msg-${Date.now()}`;

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: trimmed,
        isMultiline,
        id: msgId,
      },
    ]);

    setQuestion("");
    setLoading(true);

    await new Promise((r) => setTimeout(r, 800));

    setMessages((prev) => [
      ...prev,
      {
        role: "assistant",
        content: "Temporary assistant answer",
      },
    ]);

    setLoading(false);

    setTimeout(() => {
      chatInputRef.current?.focus();
    }, 0);
  };

  const handleNewChat = () => {
    setYoutubeUrl("");
    setQuestion("");
    setHasAskedOnce(false);
    setLoading(false);
    setMessages([]);
  };

  return (
    <div className="h-screen bg-[#1e1e1e] flex flex-col">
      <TopBar onNewChat={handleNewChat} />

      {!hasAskedOnce && (
        <div className="flex flex-1 items-center justify-center px-4">
          <div className="w-full max-w-[600px] space-y-5">
            <YoutubeInput
              value={youtubeUrl}
              onChange={setYoutubeUrl}
            />
            <QuestionInput
              value={question}
              onChange={setQuestion}
              onAsk={handleAsk}
              mode="initial"
              youtubeUrl={youtubeUrl}
              loading={loading}
            />
          </div>
        </div>
      )}

      {hasAskedOnce && (
        <>
          <div
            ref={scrollRef}
            className="flex-1 overflow-y-auto px-4 pt-4 min-h-0"
          >
            <div className="max-w-[700px] mx-auto">
              <ChatMessages
                messages={messages}
                loading={loading}
                scrollContainerRef={scrollRef}
              />
            </div>
          </div>

          <div className="px-4 pb-7 shrink-0">
            <div className="max-w-[850px] mx-auto mt-4">
              <QuestionInput
                value={question}
                onChange={setQuestion}
                onAsk={handleAsk}
                mode="chat"
                loading={loading}
                inputRef={chatInputRef}
              />
            </div>
          </div>
        </>
      )}
    </div>
  );
}

export default ChatPage;