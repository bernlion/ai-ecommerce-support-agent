import { PackageCheck, Star } from 'lucide-react';

export default function ProductCard({ product }) {
  return (
    <article className="product-card">
      <div>
        <p className="product-category">{product.category} · {product.brand}</p>
        <h3>{product.name}</h3>
      </div>
      <p className="product-desc">{product.description}</p>
      <div className="product-facts">
        <span>₹{Number(product.price).toLocaleString('en-IN')}</span>
        <span><Star size={14} /> {product.rating}</span>
        <span><PackageCheck size={14} /> {product.stock > 0 ? `${product.stock} in stock` : 'Out of stock'}</span>
      </div>
    </article>
  );
}
