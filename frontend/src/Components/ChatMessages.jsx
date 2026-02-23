import { useEffect, useRef } from "react";

function ChatMessages({ messages = [], loading = false, scrollContainerRef }) {
  const lastUserRef = useRef(null);
  const lastUserIndex = messages.map(m => m.role).lastIndexOf("user");

  useEffect(() => {
    const lastMsg = messages[messages.length - 1];
    if (!lastMsg || lastMsg.role !== "user") return;

    if (lastUserRef.current && scrollContainerRef?.current) {
      const container = scrollContainerRef.current;
      const el = lastUserRef.current;

      const containerRect = container.getBoundingClientRect();
      const elRect = el.getBoundingClientRect();

      const scrollAmount =
        container.scrollTop +
        (elRect.top - containerRect.top) -
        24;

      container.scrollTo({
        top: scrollAmount,
        behavior: "smooth",
      });
    }
  }, [messages.length]);

  return (
    <div className="space-y-5 pt-10">
      {messages.map((msg, index) => {
        const isUser = msg.role === "user";
        const isLastUser = index === lastUserIndex;

        return (
          <div
            key={index}
            ref={isLastUser ? lastUserRef : null}
            id={msg.id || undefined}
            data-role={msg.role}
            className={`flex ${!isUser ? "mb-16" : ""}`}
            style={{
              justifyContent: isUser ? "flex-end" : "flex-start",
              transform: isUser
                ? "translateX(10px)"
                : "translateX(-30px)",
            }}
          >
            <div
              className={`max-w-[65%] text-base whitespace-pre-wrap break-words ${
                isUser
                  ? `bg-[#2f2f2f] text-white px-4 py-2 ${
                      msg.isMultiline
                        ? "rounded-xl"
                        : "rounded-full"
                    }`
                  : "text-[#f3f3f3]"
              }`}
            >
              {msg.content}
            </div>
          </div>
        );
      })}

      {loading && (
        <div
          className="flex mb-16"
          style={{
            justifyContent: "flex-start",
            transform: "translateX(-30px)",
          }}
        >
          <div className="text-base whitespace-pre-wrap break-words text-[#f3f3f3]">
            Temporary assistant answer
          </div>
        </div>
      )}

      <div
        style={{
          height: scrollContainerRef?.current
            ? scrollContainerRef.current.clientHeight * 0.85
            : "80vh",
        }}
      />
    </div>
  );
}

export default ChatMessages;