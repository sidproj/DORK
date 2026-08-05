import { useConversation } from "../../hooks/useConversations";

export default function Sidebar() {
  const { conversations, selectedConversation, selectConversation, loading } =
    useConversation();

  if (loading) return <div className="w-[25%]">Loading...</div>;

  return (
    <div className="w-[25%] border-r">
      <header className="border-b border-gray-700 p-2">
        <h1 className="text-2xl font-bold">DORK</h1>

        <p className="text-sm text-gray-400">
          Data Organizer & Resource Knowledge
        </p>
      </header>

      {conversations.map((conversation) => (
        <button
          key={conversation.id}
          className={`w-full text-left p-3 ${selectedConversation?.id === conversation.id ? "bg-gray-100" : "hover:bg-gray-100"}`}
          onClick={() => selectConversation(conversation)}
        >
          {conversation.title}
        </button>
      ))}
    </div>
  );
}
