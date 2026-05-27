import requests, flask, xml.etree.ElementTree as ET
app = flask.Flask(__name__)
@app.route('/')
def ana_sayfa():
    try:
        res = requests.get("https://www.trthaber.com/gundem_articles.rss", headers={'User-Agent': 'Mozilla'}, timeout=10)
        root = ET.fromstring(res.content)
        h_list = []
        for item in root.findall('.//item')[:12]:
            title = item.find('title').text if item.find('title') is not None else ""
            desc = item.find('description').text if item.find('description') is not None else ""
            img = ""
            enclosure = item.find('enclosure')
            if enclosure is not None and 'url' in enclosure.attrib:
                img = enclosure.attrib['url']
            if not img:
                for child in item:
                    if 'content' in child.tag and 'url' in child.attrib:
                        img = child.attrib['url']
            if title:
                h_list.append({'title': title, 'desc': desc, 'img': img})
    except Exception as e:
        h_list = [{'title': 'Hata Oluştu', 'desc': str(e), 'img': ''}]
    
    html_template = """<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Arda Gündem | Canlı Haber</title><script src="https://cdn.tailwindcss.com"></script></head><body class="bg-slate-950 text-slate-100 min-h-screen font-sans"><header class="bg-slate-900 border-b border-red-600/30 sticky top-0 z-50 backdrop-blur-md bg-opacity-80"><div class="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between"><h1 class="text-2xl font-black text-red-500 tracking-wider flex items-center gap-2">🔴 ARDA GÜNDEM</h1><span class="text-xs bg-red-500/10 text-red-400 border border-red-500/20 px-2.5 py-1 rounded-full font-medium animate-pulse">ANLIK GÜNCEL</span></div></header><main class="max-w-6xl mx-auto px-4 py-8"><div class="grid grid-cols-1 lg:grid-cols-3 gap-8">{% if haberler %}<div class="lg:col-span-2 space-y-6">{% set ana = haberler[0] %}<div class="bg-slate-900 rounded-2xl overflow-hidden border border-slate-800 shadow-2xl"><img src="{% if ana.img %}{{ ana.img }}{% else %}https://images.unsplash.com/photo-1504711434969-e33886168f5c?q=80&w=800{% endif %}" class="w-full h-72 md:h-96 object-cover" alt="Ana Haber"><div class="p-6 md:p-8"><span class="text-xs font-bold text-red-500 tracking-widest uppercase block mb-2">MANŞET HABER</span><h2 class="text-xl md:text-3xl font-extrabold text-white mb-4 leading-tight">{{ ana.title }}</h2><p class="text-slate-400 text-sm md:text-base leading-relaxed">{{ ana.desc }}</p></div></div></div><div class="space-y-4 h-[calc(100vh-12rem)] overflow-y-auto pr-2 custom-scrollbar"><h3 class="text-sm font-black text-slate-400 tracking-wider uppercase mb-2">Öne Çıkan Gelişmeler</h3>{% for h in haberler[1:] %}<div class="bg-slate-900 p-4 rounded-xl border border-slate-800 shadow-md hover:border-slate-700 transition flex gap-4">{% if h.img % train %}<img src="{{ h.img }}" class="w-20 h-20 object-cover rounded-lg flex-shrink-0 bg-slate-800">{% endif %}<div class="space-y-1"><h4 class="text-sm font-bold text-slate-200 leading-snug line-clamp-2">{{ h.title }}</h4><p class="text-xs text-slate-400 line-clamp-2 leading-relaxed">{{ h.desc }}</p></div></div>{% endfor %}</div>{% else %"><div class="col-span-full text-center py-12 text-slate-500">Haberler şu an yüklenemiyor.</div>{% endif %}</div></main><footer class="border-t border-slate-900 mt-12 py-6 text-center text-xs text-slate-600"><p>Veri Sağlayıcı: TRT Haber RSS Servisi</p></footer></body></html>"""
    return flask.render_template_string(html_template, haberler=h_list)
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=10000)
