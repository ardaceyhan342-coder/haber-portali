import requests, flask, xml.etree.ElementTree as ET, email.utils, datetime
app = flask.Flask(__name__)
def rss_veri_cek(url, kaynak_adi):
    liste = []
    try:
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        root = ET.fromstring(res.content)
        for item in root.findall('.//item')[:12]:
            title = item.find('title').text if item.find('title') is not None else ""
            desc = item.find('description').text if item.find('description') is not None else ""
            pub_date_str = item.find('pubDate').text if item.find('pubDate') is not None else ""
            img_url = ""
            enclosure = item.find('enclosure')
            if enclosure is not None and 'url' in enclosure.attrib: img_url = enclosure.attrib['url']
            else:
                media_content = item.find('.//{http://search.yahoo.com/mrss/}content')
                if media_content is not None and 'url' in media_content.attrib: img_url = media_content.attrib['url']
                else:
                    media_thumbnail = item.find('.//{http://search.yahoo.com/mrss/}thumbnail')
                    if media_thumbnail is not None and 'url' in media_thumbnail.attrib: img_url = media_thumbnail.attrib['url']
            try: parsed_date = email.utils.parsedate_to_datetime(pub_date_str)
            except: parsed_date = datetime.datetime.now()
            if title: liste.append({'title': title, 'desc': desc if desc else "Detaylar orijinal kaynakta.", 'kaynak': kaynak_adi, 'tarih': parsed_date, 'img': img_url})
    except: pass
    return liste
@app.route('/')
def ana_sayfa():
    havuz = []
    havuz.extend(rss_veri_cek("https://www.trthaber.com/main_articles.rss", "TRT Haber"))
    havuz.extend(rss_veri_cek("https://feeds.bbci.co.uk/turkce/rss.xml", "BBC Türkçe"))
    havuz.extend(rss_veri_cek("https://www.ntv.com.tr/gundem.rss", "NTV"))
    havuz.extend(rss_veri_cek("https://www.aa.com.tr/tr/rss/default?cat=guncel", "Anadolu Ajansı"))
    havuz.extend(rss_veri_cek("https://www.hurriyet.com.tr/rss/gundem", "Hürriyet"))
    havuz.sort(key=lambda x: x['tarih'], reverse=True)
    html = """<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Arda Gündem</title><script src="https://cdn.tailwindcss.com"></script></head><body class="bg-slate-950 text-slate-100 min-h-screen font-sans"><header class="bg-slate-900 border-b border-red-600/30 sticky top-0 z-50"><div class="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between"><h1 class="text-2xl font-black text-red-500 tracking-wider">🔴 ARDA GÜNDEM</h1><span class="text-xs bg-red-500/10 text-red-400 border border-red-500/20 px-2.5 py-1 rounded-full font-medium">FOTOĞRAFLI AKIŞ</span></div></header><main class="max-w-4xl mx-auto px-4 py-8"><div class="space-y-6">{% for h in haberler %}<div class="bg-slate-900 rounded-2xl border border-slate-800 shadow-xl overflow-hidden flex flex-col md:flex-row relative">{% if h.img %}<div class="md:w-1/3 h-48 md:h-auto relative min-h-[12rem] bg-slate-800"><img src="{{ h.img }}" class="w-full h-full object-cover" alt="Haber"></div>{% endif %}<div class="p-6 flex-1 flex flex-col justify-between"><span class="absolute top-4 right-4 text-xs font-bold px-2.5 py-1 rounded-md bg-red-500/10 text-red-400 border border-red-500/20 z-10">{{ h.kaynak }}</span><div class="pr-24"><h2 class="text-lg font-bold text-white mb-3 leading-tight">{{ h.title }}</h2><div class="text-slate-400 text-sm leading-relaxed">{{ h.desc | safe }}</div></div></div></div>{% endfor %}</div></main></body></html>"""
    return flask.render_template_string(html, haberler=havuz[:50])
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=10000)
