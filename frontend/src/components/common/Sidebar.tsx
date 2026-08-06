import { useConversation } from "../../hooks/useConversations";

export default function Sidebar() {
  const {
    conversations,
    selectedConversation,
    selectConversation,
    createConversation,
    loading,
  } = useConversation();

  if (loading) return <div className="w-[25%]">Loading...</div>;

  return (
    <div className="w-[25%] border-r">
      <header className="border-b border-gray-700 p-2">
        <h1 className="text-2xl font-bold">DORK</h1>

        <p className="text-sm text-gray-400">
          Data Organizer & Resource Knowledge
        </p>
      </header>

      <button
        onClick={createConversation}
        className="
                    m-3
                    flex
                    items-center
                    justify-center
                    gap-2
                    rounded-lg
                    border
                    border-zinc-700
                    py-1 px-3
                    hover:bg-zinc-800
                "
      >
        New Chat
      </button>
      {conversations.map((conversation) => (
        <button
          key={conversation.id}
          className={`w-full text-left p-3 ${selectedConversation?.id === conversation.id ? "bg-gray-800" : "hover:bg-gray-600"}`}
          onClick={() => selectConversation(conversation)}
        >
          {conversation.title}
        </button>
      ))}
    </div>
  );
}
