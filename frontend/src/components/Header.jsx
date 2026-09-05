import { PackageSearch, RotateCcw, ShieldCheck, Truck } from 'lucide-react';

export default function Header() {
  return (
    <header className="header">
      <div>
        <p className="eyebrow">Local customer support agent</p>
        <h2>Shop support that can search products, track orders, handle returns, and remember preferences.</h2>
      </div>
      <div className="header-actions">
        <div className="privacy-badge"><ShieldCheck size={18} /> Local LLM</div>
        <div className="capability-row">
          <span><PackageSearch size={15} /> Products</span>
          <span><Truck size={15} /> Orders</span>
          <span><RotateCcw size={15} /> Returns</span>
        </div>
      </div>
    </header>
  );
}
