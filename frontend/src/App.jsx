import { useEffect, useState } from 'react';
import { Bot, Database, Server, Sparkles, Zap } from 'lucide-react';
import { getHealth } from './api.js';
import Chat from './components/Chat.jsx';
import Header from './components/Header.jsx';

export default function App() {
  const [health, setHealth] = useState(null);

  useEffect(() => {
    getHealth().then(setHealth).catch(() => setHealth({ status: 'degraded', mongodb: false, ollama: { running: false } }));
  }, []);

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand-row">
          <div className="brand-mark"><Bot size={28} /></div>
          <div>
            <p className="eyebrow light">Support console</p>
            <h1>AI E-Commerce Support</h1>
          </div>
        </div>
        <div className="model-stack">
          <div className="model-pill"><Sparkles size={16} /> Gemma 3 4B</div>
          <div className="model-pill"><Server size={16} /> Ollama Local AI</div>
          <div className="model-pill"><Zap size={16} /> Tool Calling</div>
        </div>
        <div className="status-panel">
          <span className={health?.mongodb ? 'dot ok' : 'dot'} />
          MongoDB {health?.mongodb ? 'Connected' : 'Unavailable'}
          <span className={health?.ollama?.running ? 'dot ok' : 'dot'} />
          Ollama {health?.ollama?.running ? 'Running' : 'Offline'}
          <span className={health?.ollama?.model_available ? 'dot ok' : 'dot'} />
          Gemma {health?.ollama?.model_available ? 'Ready' : 'Missing'}
        </div>
        <div className="sidebar-card">
          <Database size={18} />
          <div>
            <strong>Live store data</strong>
            <span>Products, orders, returns, and customer memory stay in MongoDB.</span>
          </div>
        </div>
      </aside>
      <main className="main-panel">
        <Header />
        <Chat />
      </main>
    </div>
  );
}
