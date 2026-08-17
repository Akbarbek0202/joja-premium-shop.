import axios from 'axios'
import React, { useEffect, useState } from 'react'
import { Plus, Minus, ShoppingBag } from 'lucide-react'
import { translations } from './components/language';

const tg = window.Telegram?.WebApp;

const App = () => {
  const apiURL = import.meta.env.VITE_API_URL
  const [products, setProducts] = useState([])
  const [cart, setCart] = useState({})
  const [loading, setLoading] = useState(true)
  const [activeCategory, setActiveCategory] = useState('all')
  const [lang, setLang] = useState('uz')

  async function fetchChicken() {
    try {
      const res = await axios.get(apiURL)
      setProducts(res.data)
    } catch (err) {
      console.log("Xatolik:", err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchChicken()
    if (tg) {
      tg.ready();
      tg.expand();
    }
  }, [])

  const toggleCart = (id, action) => {
    setCart(prev => {
      const newCart = { ...prev }
      if (action === 'plus') newCart[id] = (newCart[id] || 0) + 1
      else if (action === 'minus' && newCart[id] > 1) newCart[id] -= 1
      else delete newCart[id]
      return newCart
    })
  }

  const totalItems = Object.values(cart).reduce((a, b) => a + b, 0)

  const totalPrice = products
    .filter(item => cart[item.id])
    .reduce((sum, item) => sum + (item.price * cart[item.id]), 0);

  const filteredProducts = activeCategory === 'all'
    ? products
    : products.filter(item => item.category === activeCategory)

  const t = translations[lang] || translations.uz;

  const getProductName = (name) => {
    if (!name) return '';
    const cleanName = name.trim();
    return t.products[cleanName] || t.products[name] || name;
  };

  const getProductDesc = (desc) => {
    if (!desc) return '';
    const cleanDesc = desc.trim();
    return t.descriptions[cleanDesc] || t.descriptions[desc] || desc;
  };

  const handleSendOrder = () => {
    const orderItems = products
      .filter(item => cart[item.id])
      .map(item => ({
        id: item.id,
        name: getProductName(item.name),
        price: item.price,
        quantity: cart[item.id],
        total: item.price * cart[item.id]
      }));

    const orderData = {
      lang: lang,
      items: orderItems,
      totalPrice: totalPrice
    };

    if (tg) {
      tg.sendData(JSON.stringify(orderData));
      tg.close();
    } else {
      console.log("Telegram topilmadi. Buyurtma:", orderData);
    }
  };

  return (
    <div className="min-h-screen bg-[#0b0c10] text-[#1e2022] pb-32 font-sans">

      <nav className="sticky top-0 z-50 bg-[#0b0c10]/90 backdrop-blur-md border-b border-zinc-900 px-6 py-5">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="flex flex-col">
            <h1 className="text-xl font-bold text-zinc-100 tracking-tight">
              {t.title} <span className="text-xs font-serif italic text-rose-600 ml-1">{t.subTitle}</span>
            </h1>
          </div>

          <div className="flex bg-zinc-900 rounded-lg p-1 border border-zinc-800 text-[11px] font-bold">
            <button onClick={() => setLang('uz')} className={`px-2.5 py-1 rounded-md transition-all duration-200 ${lang === 'uz' ? 'bg-rose-700 text-white' : 'text-zinc-500 hover:text-zinc-300'}`}>UZ</button>
            <button onClick={() => setLang('ru')} className={`px-2.5 py-1 rounded-md transition-all duration-200 ${lang === 'ru' ? 'bg-rose-700 text-white' : 'text-zinc-500 hover:text-zinc-300'}`}>RU</button>
          </div>

          <div className="relative p-3 bg-zinc-900 text-zinc-400 rounded-xl border border-zinc-800">
            <ShoppingBag className="w-5 h-5 text-rose-500" />
            {totalItems > 0 && (
              <span className="absolute -top-1 -right-1 bg-rose-600 text-white text-[10px] font-bold w-5 h-5 flex items-center justify-center rounded-full shadow-lg">{totalItems}</span>
            )}
          </div>
        </div>
      </nav>

      <main className="max-w-6xl mx-auto px-4 mt-8">

        <div className="flex gap-2 overflow-x-auto pb-3 mb-6 scrollbar-none md:justify-center">
          {[
            { id: 'all', label: t.all },
            { id: 'parts', label: t.parts },
            { id: 'lotok', label: t.lotok },
            { id: 'naggets', label: t.naggets },
            { id: 'marinade', label: t.marinade }
          ].map(cat => (
            <button
              key={cat.id}
              onClick={() => setActiveCategory(cat.id)}
              className={`px-4 py-2 rounded-xl text-xs font-medium whitespace-nowrap transition-all duration-200 border ${activeCategory === cat.id
                ? 'bg-rose-700 text-white border-rose-600 shadow-md'
                : 'bg-zinc-900 text-zinc-400 border-zinc-800 hover:text-zinc-200'}`}>{cat.label}</button>))}
        </div>

        {loading ? (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="bg-zinc-900 h-64 rounded-2xl animate-pulse border border-zinc-800"></div>
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {filteredProducts.map((item) => (
              <div key={item.id} className="bg-[#f9f9f7] rounded-2xl p-4 flex flex-col justify-between border border-stone-200/60 shadow-[0_10px_25px_-5px_rgba(0,0,0,0.2)] transition-all duration-300 hover:shadow-[0_20px_35px_-5px_rgba(0,0,0,0.35)] hover:-translate-y-0.5">
                <div>
                  <div className="w-full bg-[#eeede9] rounded-xl overflow-hidden shadow-inner border border-stone-300/40 flex items-center justify-center text-stone-400" style={{ height: '128px', minHeight: '128px', maxHeight: '128px' }}>
                    {item.image ? (
                      <img
                        src={item.image}
                        alt={item.name}
                        style={{
                          width: '100%',
                          height: '100%',
                          objectFit: 'cover',
                          objectPosition: 'center'
                        }} className="scale-105 transition-transform duration-300" />
                    ) : (
                      <span className="text-xs text-stone-400">{t.noImage}</span>
                    )}
                  </div>

                  <h3 className="font-serif italic text-sm md:text-base text-zinc-900 mt-3 font-bold tracking-tight min-h-[44px] flex items-center">
                    {getProductName(item.name)}
                  </h3>
                  <p className="text-[11px] text-stone-500 mt-1 leading-snug line-clamp-2 min-h-[32px]">
                    {getProductDesc(item.description)}
                  </p>
                </div>

                <div className="mt-4 pt-3 border-t border-stone-200/80 flex items-center justify-between">
                  <span className="text-xs font-bold tracking-tight text-zinc-900 whitespace-nowrap">{Number(item.price).toLocaleString('ru-RU')} {t.currency}</span>

                  {cart[item.id] ? (
                    <div className="flex items-center gap-2 bg-stone-200/60 rounded-lg p-1 border border-stone-300/30">
                      <button onClick={() => toggleCart(item.id, 'minus')} className="p-1 bg-stone-100 hover:bg-white text-zinc-800 rounded shadow-sm" >
                        <Minus className="w-3 h-3" /></button>
                      <span className="text-xs font-bold w-4 text-center text-zinc-900">{cart[item.id]}</span>
                      <button onClick={() => toggleCart(item.id, 'plus')} className="p-1 bg-zinc-900 hover:bg-zinc-800 text-white rounded shadow-sm"><Plus className="w-3 h-3" /></button>
                    </div>
                  ) : (
                    <button onClick={() => toggleCart(item.id, 'plus')} className="p-2 bg-zinc-900 hover:bg-rose-700 text-white rounded-xl transition-all duration-200 active:scale-95"><Plus className="w-4 h-4" /></button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </main>

      {totalItems > 0 && (
        <div className="fixed bottom-6 left-4 right-4 z-50 max-w-sm mx-auto">
          <button
            onClick={handleSendOrder}
            className="w-full py-4 bg-zinc-950 text-stone-100 font-medium rounded-2xl text-center text-sm tracking-wider uppercase transition-all duration-300 active:scale-98 border border-zinc-800 shadow-[0_20px_40px_rgba(0,0,0,0.7)] hover:bg-rose-800 flex items-center justify-between px-6 cursor-pointer"
          >
            <div className="flex items-center gap-2">
              <ShoppingBag className="w-4 h-4 text-rose-500" />
              <span>{t.buyurtma} ({totalItems})</span>
            </div>

            <span className="font-bold text-rose-400 font-mono">
              {totalPrice.toLocaleString('ru-RU')} {t.currency}
            </span>
          </button>
        </div>
      )}

    </div>
  )
}

export default App