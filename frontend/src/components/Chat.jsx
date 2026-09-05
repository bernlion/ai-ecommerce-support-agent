import { useMemo, useRef, useState } from 'react';
import { BadgeIndianRupee, Heart, List, RotateCcw, Search, SendHorizontal, Truck } from 'lucide-react';
import { sendChat } from '../api.js';
import Message from './Message.jsx';

const prompts = [
  { text: 'Show catalog', icon: List },
  { text: 'Find laptops under ₹60000', icon: Search },
  { text: 'Where is my order ORD1001?', icon: Truck },
  { text: 'Can I cancel ORD1002?', icon: BadgeIndianRupee },
  { text: 'I want to return ORD1003 because it is damaged', icon: RotateCcw },
  { text: 'I prefer Samsung phones', icon: Heart },
  { text: 'Recommend a phone for me', icon: Heart },
];

function now() {
  return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

export default function Chat() {
  const [customerId, setCustomerId] = useState('C1001');
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([
    { role: 'agent', text: 'Hi! I can help with products, orders, cancellations, returns, and recommendations.', time: now() },
  ]);
  const [loading, setLoading] = useState(false);
  const listRef = useRef(null);

  const canSend = useMemo(() => input.trim().length > 0 && !loading, [input, loading]);

  async function submit(text = input) {
    const clean = text.trim();
    if (!clean || loading) return;
    setInput('');
    setMessages((items) => [...items, { role: 'user', text: clean, time: now() }]);
    setLoading(true);
    try {
      const result = await sendChat(customerId, clean);
      setMessages((items) => [
        ...items,
        { role: 'agent', text: result.response, time: now(), tool: result.tool_used, products: result.products || [] },
      ]);
      setTimeout(() => listRef.current?.scrollTo({ top: listRef.current.scrollHeight, behavior: 'smooth' }), 50);
    } catch (error) {
      setMessages((items) => [...items, { role: 'agent', text: error.message, time: now(), error: true }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="chat-layout">
      <div className="prompt-strip">
        <label>
          Customer
          <input value={customerId} onChange={(event) => setCustomerId(event.target.value)} />
        </label>
        {prompts.map(({ text, icon: Icon }) => (
          <button key={text} onClick={() => submit(text)} disabled={loading}>
            <Icon size={15} />
            {text}
          </button>
        ))}
      </div>
      <div className="messages" ref={listRef}>
        {messages.map((message, index) => <Message key={`${message.time}-${index}`} message={message} />)}
        {loading && <div className="typing">Agent is checking the store data...</div>}
      </div>
      <form className="composer" onSubmit={(event) => { event.preventDefault(); submit(); }}>
        <input
          value={input}
          onChange={(event) => setInput(event.target.value)}
          placeholder="Ask about an order, product, return, or recommendation"
          aria-label="Chat message"
        />
        <button disabled={!canSend} title="Send message" aria-label="Send message">
          <SendHorizontal size={20} />
        </button>
      </form>
    </section>
  );
}
