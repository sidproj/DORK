import { ChatInput, ChatWindow } from "./components/chat";
import { useChat } from "./hooks/userChat";
function App() {
  const { messages, loading, error, send } = useChat();

  return (
    <div className="flex flex-row h-screen w-full">
      <header className="border-b border-gray-700 p-2">
        <h1 className="text-2xl font-bold">DORK</h1>

        <p className="text-sm text-gray-400">
          Data Organizer & Resource Knowledge
        </p>
      </header>
      <div className="w-full border border-gray-700">
        <ChatWindow messages={messages} />

        {error && <div className="px-4 py-2 text-red-400">{error}</div>}

        <ChatInput onSend={send} loading={loading} />
      </div>
    </div>
  );
}

export default App;
