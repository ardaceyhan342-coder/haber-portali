import requests, flask, xml.etree.ElementTree as ET
app = flask.Flask(__name__)
@app.route('/')
def ana_sayfa():
    try:
        res = requests.get("https://www.trthaber.com/gundem_articles.rss", headers={'User-Agent': 'Mozilla'}, timeout=10)
        root = ET.fromstring(res.content)
        h_list = [t.text for item in root.findall('.//item')[:15] if (t := item.find('title')) is not None and t.text]
    except Exception as e:
        h_list = [f"Hata: {str(e)}"]
    html_template = """<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Haber Portalı</title><script src="https://cdn.tailwindcss.com"></script></head><body class="bg-slate-900 text-slate-100 min-h-screen p-4 flex flex-col items-center"><div class="max-w-md w-full"><h1 class="text-2xl font-black text-red-500 mb-6 border-b border-red-600 pb-2 tracking-wider">🔴 CANLI GÜNDEM</h1><div class="space-y-3">{% for h in haberler %}<div class="bg-slate-800 p-4 rounded-xl border border-slate-700 shadow-lg"><p class="text-sm font-bold leading-relaxed">{{ h }}</p></div>{% endfor %}</div><p class="text-center text-xs text-slate-500 mt-6">Veriler anlık olarak TRT Haber üzerinden çekilmektedir.</p></div></body></html>"""
    return flask.render_template_string(html_template, haberler=h_list)
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=10000)
