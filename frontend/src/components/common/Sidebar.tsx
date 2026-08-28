import { useConversation } from "../../hooks/useConversations";

export default function Sidebar() {
  const {
    conversations,
    selectedConversation,
    selectConversation,
    createConversation,
    loading,
  } = useConversation();

  if (loading) {
    return (
      <aside className="flex h-full w-[25%] items-center justify-center border-r border-(--border) bg-(--surface-muted)">
        <span className="text-sm text-(--text-muted)">Loading...</span>
      </aside>
    );
  }

  return (
    <aside className="flex h-full w-[25%] min-w-60 flex-col border-r border-(--border) bg-(--surface-muted)">
      {/* Header */}
      <header className="border-b border-(--border) px-5 py-5 text-left">
        <h1 className="font-mono text-2xl font-semibold tracking-tight text-(--text)">
          DORK
        </h1>
        <p className="mt-1 text-xs leading-relaxed text-(--text-muted)">
          Data Organizer & Resource Knowledge
        </p>
      </header>
      {/* New Chat */}
      <div className="border-b border-(--border) p-3">
        <button
          onClick={createConversation}
          className="
        flex
        w-full
        items-center
        justify-center
        gap-2
        rounded-md
        border
        border-(--border-strong)
        bg-(--surface)
        px-3
        py-2
        text-sm
        font-medium
        text-(--text)
        transition-colors
        duration-150
        hover:border-(--blue)
        hover:bg-(--blue-muted)
        focus:outline-none
        focus-visible:ring-2
        focus-visible:ring-(--blue)
        focus-visible:ring-offset-2
        focus-visible:ring-offset-(--surface-muted)
      "
        >
          <span className="text-base leading-none">+</span>
          New Chat
        </button>
      </div>
      {/* Conversation list */}
      <div className="flex-1 overflow-y-auto px-2 py-3">
        <p className="mb-2 px-3 text-[10px] font-semibold uppercase tracking-[0.14em] text-(--text-faint)">
          Conversations
        </p>

        <div className="space-y-1">
          {conversations.map((conversation) => {
            const isSelected = selectedConversation?.id === conversation.id;

            return (
              <button
                key={conversation.id}
                onClick={() => selectConversation(conversation)}
                className={`
              group
              w-full
              rounded-md
              px-3
              py-2.5
              text-left
              text-sm
              transition-colors
              duration-150
              ${
                isSelected
                  ? `
                    border
                    border-(--border)
                    bg-(--surface)
                    text-(--text)
                    shadow-(--shadow-sm)
                  `
                  : `
                    border
                    border-transparent
                    text-(--text-muted)
                    hover:bg-(--surface)
                    hover:text-(--text)
                  `
              }
            `}
              >
                <span className="block truncate">{conversation.title}</span>
              </button>
            );
          })}
        </div>

        {conversations.length === 0 && (
          <div className="px-3 py-8 text-center">
            <p className="text-sm text-(--text-faint)">No conversations yet.</p>
          </div>
        )}
      </div>
      {/* Footer */}
      <footer className="border-t border-(--border) px-4 py-3">
        <div className="flex items-center gap-2 text-xs text-(--text-faint)">
          <span className="h-2 w-2 rounded-full bg-(--green)" />

          <span>DORK Local</span>
        </div>
      </footer>
    </aside>
  );
}
