import { ChatInput, ChatWindow } from "./components/chat";
import Sidebar from "./components/common/Sidebar";

function App() {
  return (
    <div className="flex flex-row h-screen w-full">
      <Sidebar/>
      <div className="w-full border border-gray-700">
        <ChatWindow/>
        <ChatInput/>
      </div>
    </div>
  );
}

export default App;
