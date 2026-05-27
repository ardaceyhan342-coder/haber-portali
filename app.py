import requests, flask, xml.etree.ElementTree as ET
app = flask.Flask(__name__)
@app.route('/')
def ana_sayfa():
    h_list = []
    try:
        # Linki daha aktif olan ana manşet haberleri (main_articles) ile değiştirdik
        res = requests.get("https://www.trthaber.com/main_articles.rss", headers={'User-Agent': 'Mozilla'}, timeout=10)
        root = ET.fromstring(res.content)
        for item in root.findall('.//item')[:10]:
            title = item.find('title').text if item.find('title') is not None else ""
            desc = item.find('description').text if item.find('description') is not None else ""
            if title:
                h_list.append({'title': title, 'desc': desc})
    except Exception as e:
        h_list = [{'title': 'Hata Olustu', 'desc': str(e)}]
    
    html_template = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arda Gundem</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen font-sans">
    <header class="bg-slate-900 border-b border-red-600/30 sticky top-0 z-50">
        <div class="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
            <h1 class="text-2xl font-black text-red-500 tracking-wider">🔴 ARDA GÜNDEM</h1>
            <span class="text-xs bg-red-500/10 text-red-400 border border-red-500/20 px-2.5 py-1 rounded-full font-medium">CANLI</span>
        </div>
    </header>
    <main class="max-w-4xl mx-auto px-4 py-8">
        <div class="space-y-6">
            {% for h in haberler %}
            <div class="bg-slate-900 p-6 rounded-2xl border border-slate-800 shadow-xl">
                <h2 class="text-lg md:text-xl font-bold text-white mb-4 leading-tight">{{ h.title }}</h2>
                <div class="text-slate-400 text-sm md:text-base leading-relaxed space-y-4">
                    {{ h.desc | safe }}
                </div>
            </div>
            {% endfor %}
        </div>
    </main>
</body>
</html>"""
    return flask.render_template_string(html_template, haberler=h_list)
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=10000)
