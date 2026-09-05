import ProductCard from './ProductCard.jsx';

export default function Message({ message }) {
  return (
    <div className={`message-row ${message.role}`}>
      <div className="message-bubble">
        <div className="message-meta">
          <span>{message.role === 'user' ? 'You' : 'Support Agent'}</span>
          <time>{message.time}</time>
        </div>
        <p>{message.text}</p>
        {message.tool && <span className="tool-chip">{message.tool}</span>}
        {message.error && <span className="error-chip">Needs attention</span>}
        {message.products?.length > 0 && (
          <div className="product-grid">
            {message.products.map((product) => <ProductCard key={product.product_id} product={product} />)}
          </div>
        )}
      </div>
    </div>
  );
}
