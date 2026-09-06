import { demoOrders, demoProducts } from './demoData.js';

const API_BASE = import.meta.env?.VITE_API_BASE || 'http://localhost:8000';

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options,
  });
  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw new Error(data.detail || 'Request failed. Please try again.');
  }
  return response.json();
}

export function sendChat(customerId, message) {
  return request('/api/chat', {
    method: 'POST',
    body: JSON.stringify({ customer_id: customerId, message }),
  }).catch(() => demoChat(customerId, message));
}

export function getHealth() {
  return request('/api/health').catch(() => ({
    status: 'demo',
    mongodb: false,
    demo_mode: true,
    ollama: { running: false, model: 'gemma3:4b', model_available: false },
  }));
}

function demoChat(customerId, message) {
  const lower = message.toLowerCase();
  const conversationId = `demo-${Date.now()}`;
  if (isGreeting(lower)) {
    return Promise.resolve({
      response: 'Hello! I can help you browse the catalog, check sample orders, or recommend products. Demo mode is active because the local backend is not reachable from this page.',
      tool_used: null,
      conversation_id: conversationId,
      products: [],
    });
  }

  const orderId = lower.match(/ord\d+/i)?.[0]?.toUpperCase();
  if (orderId) {
    const order = demoOrders.find((item) => item.order_id === orderId);
    if (!order) {
      return Promise.resolve(baseResult(`I could not find order ${orderId} in the demo data.`, 'get_order_status', conversationId));
    }
    if (lower.includes('cancel')) {
      const canCancel = !['Delivered', 'Cancelled', 'Out for Delivery'].includes(order.status);
      return Promise.resolve(baseResult(
        canCancel ? `Order ${orderId} is eligible for cancellation. In local backend mode it can be cancelled in MongoDB.` : `Order ${orderId} cannot be cancelled because it is ${order.status}.`,
        'cancel_order',
        conversationId,
      ));
    }
    if (lower.includes('return')) {
      return Promise.resolve(baseResult(
        order.status === 'Delivered' ? `Return request can be created for ${orderId}. In local backend mode it will be saved in MongoDB.` : `Only delivered orders can be returned. ${orderId} is currently ${order.status}.`,
        'create_return_request',
        conversationId,
      ));
    }
    return Promise.resolve(baseResult(`Order ${orderId} is ${order.status}. Expected delivery: ${order.expected_delivery}.`, 'get_order_status', conversationId));
  }

  const products = findDemoProducts(lower);
  if (isCatalogRequest(lower)) {
    return Promise.resolve(productResult(`I found ${demoProducts.length} catalog items.`, demoProducts, 'search_products', conversationId));
  }
  if (lower.includes('recommend')) {
    return Promise.resolve(productResult(
      products.length ? `Here are ${products.length} recommended item${products.length === 1 ? '' : 's'} from the demo catalog.` : 'I could not find matching recommendations in the demo catalog.',
      products,
      'recommend_products',
      conversationId,
    ));
  }
  if (products.length) {
    return Promise.resolve(productResult(`I found ${products.length} matching item${products.length === 1 ? '' : 's'} in the demo catalog.`, products, 'search_products', conversationId));
  }
  return Promise.resolve(baseResult('I checked the demo catalog, but I could not find matching products. Try catalog, laptop, phone, headphones, tablet, watch, or accessories.', 'search_products', conversationId));
}

function baseResult(response, toolUsed, conversationId) {
  return { response, tool_used: toolUsed, conversation_id: conversationId, products: [] };
}

function productResult(response, products, toolUsed, conversationId) {
  return { response, tool_used: toolUsed, conversation_id: conversationId, products };
}

function isGreeting(lower) {
  return ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening'].includes(lower.trim());
}

function isCatalogRequest(lower) {
  return ['catalog', 'catalogue', 'list items', 'list products', 'show catalog', 'show products', 'all products', 'all items'].some((term) => lower.includes(term));
}

function findDemoProducts(lower) {
  const budget = Number(lower.match(/(?:under|below|budget|less than|upto|up to)\s*(?:rs\.?|₹|inr)?\s*(\d{3,7})/)?.[1] || 0);
  const categoryMap = {
    iphone: 'smartphones',
    mobile: 'smartphones',
    phone: 'smartphones',
    smartphone: 'smartphones',
    laptop: 'laptops',
    headphone: 'headphones',
    watch: 'smart watches',
    tablet: 'tablets',
    accessor: 'accessories',
  };
  const category = Object.entries(categoryMap).find(([key]) => lower.includes(key))?.[1];
  const cleanedQuery = lower.replace(/\b(order|buy|purchase|find|search|show|recommend|products?|items?|for|me)\b/g, ' ').replace(/\s+/g, ' ').trim();

  return demoProducts.filter((product) => {
    const haystack = `${product.name} ${product.description} ${product.brand} ${product.category}`.toLowerCase();
    const matchesCategory = !category || product.category.toLowerCase() === category;
    const matchesBudget = !budget || product.price <= budget;
    const matchesQuery = !cleanedQuery || cleanedQuery.split(' ').some((word) => haystack.includes(word));
    return matchesCategory && matchesBudget && matchesQuery && product.stock > 0;
  });
}
