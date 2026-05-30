import requests, flask, xml.etree.ElementTree as ET
from datetime import datetime
import email.utils

app = flask.Flask(__name__)

def rss_veri_cek(url, kaynak_adi):
    liste = []
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        res = requests.get(url, headers=headers, timeout=10)
        root = ET.fromstring(res.content)
        
        # Her siteden en az 15 haber çekerek havuzu büyütüyoruz
        for item in root.findall('.//item')[:15]:
            title = item.find('title').text if item.find('title') is not None else ""
            desc = item.find('description').text if item.find('description') is not None else ""
            pub_date_str = item.find('pubDate').text if item.find('pubDate') is not None else ""
            
            try:
                parsed_date = email.utils.parsedate_to_datetime(pub_date_str)
            except:
                parsed_date = datetime.now()

            if title:
                clean_desc = desc if desc else "Haber detayı için orijinal kaynağı ziyaret ediniz."
                liste.append({
                    'title': title, 
                    'desc': clean_desc, 
                    'kaynak': kaynak_adi,
                    'tarih': parsed_date
                })
    except Exception as e:
        print(f"{kaynak_adi} verisi çekilirken bir sorun yaşandı, atlanıyor...")
    return list

@app.route('/')
def ana_sayfa():
    tum_haberler = []
    
    # 5 farklı kaynaktan bolca haber topluyoruz
    tum_haberler.extend(rss_veri_cek("https://www.trthaber.com/main_articles.rss", "TRT Haber"))
    tum_haberler.extend(rss_veri_cek("https://feeds.bbci.co.uk/turkce/rss.xml", "BBC Türkçe"))
    tum_haberler.extend(rss_veri_cek("https://www.ntv.com.tr/gundem.rss", "NTV"))
    tum_haberler.extend(rss_veri_cek("https://www.aa.com.tr/tr/rss/default?cat=guncel", "Anadolu Ajansı"))
    tum_haberler.extend(rss_veri_cek("https://www.hurriyet.com.tr/rss/gundem", "Hürriyet"))
    
    # Hepsini zamana göre kronolojik sıralıyoruz
    tum_haberler.sort(key=lambda x: x['tarih'], reverse=True)
    
    html_template = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arda Gündem | Büyük Haber Havuzu</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen font-sans">
    <header class="bg-slate-900 border-b border-red-600/30 sticky top-0 z-50">
        <div class="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
            <h1 class="text-2xl font-black text-red-500 tracking-wider">🔴 ARDA GÜNDEM</h1>
            <span class="text-xs bg-red-500/10 text-red-400 border border-red-500/20 px-2.5 py-1 rounded-full font-medium">BÜYÜK HAVUZ</span>
        </div>
    </header>
    <main class="max-w-4xl mx-auto px-4 py-8">
        <div class="space-y-6">
            {% for h in haberler %}
            <div class="bg-slate-900 p-6 rounded-2xl border border-slate-800 shadow-xl relative overflow-hidden">
                <span class="absolute top-4 right-4 text-xs font-bold px-2.5 py-1 rounded-md bg-red-500/10 text-red-400 border border-red-500/20">
                    {{ h.kaynak }}
                </span>
                
                <h2 class="text-lg md:text-xl font-bold text-white mb-4 leading-tight pr-28">{{ h.title }}</h2>
                <div class="text-slate-400 text-sm md:text-base leading-relaxed space-y-4">
                    {{ h.desc | safe }}
                </div>
            </div>
            {% endfor %}
        </div>
    </main>
</body>
</html>"""
    # Ziyaretçiye en güncel 60 haberi birden sunuyoruz
    return flask.render_template_string(html_template, haberler=tum_haberler[:60])

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=10000)
