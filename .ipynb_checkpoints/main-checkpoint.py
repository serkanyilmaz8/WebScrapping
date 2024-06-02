from bs4 import BeautifulSoup
import requests
import csv

session = requests.Session()  # requests kütüphanesinde bir session başlatır
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.google.com/'
}
response = session.get('https://halkarz.com/', headers=headers)
html_text = response.text

soup = BeautifulSoup(html_text, 'lxml')
isim = soup.find('h3')

ads = soup.find_all('h3', class_='il-halka-arz-sirket')

# Her şirketin detay sayfasına giden linkleri bulma
company_links = soup.find_all('a', href=True)  # href attribute'u olan tüm <a> etiketlerini bul
company_urls = set(link['href'] for link in company_links if '-' in link['href'])  # '-' işareti href içinde geçiyorsa ve benzersiz olanları al

# Her şirketin URL'i için
for url in company_urls:
    # Şirket detay sayfasına istek gönderme
    response = requests.get(url, headers=headers)
    detail_soup = BeautifulSoup(response.text, 'lxml')

    # şirket ismi çekiyor
    isim = detail_soup.find('h1', class_='il-halka-arz-sirket')

    # arz tarihini çekiyor
    arz_tarihi='-'
    time_tags = detail_soup.select("table.sp-table time")
    for time_tag in time_tags:
        datetime_value = time_tag.get('datetime')  # 'datetime' attribute değerini al
        arz_tarihi = time_tag.get('title', '')  # 'title' attribute değerini al

    # p lerin yer alığı li leri çekiyor
    lis = detail_soup.select("ul.aex-in li")

    if len(lis)>0:
        arz_sekli = lis[0].find('p').text
        print(arz_sekli)
    if len(lis) >= 1:
        fonun_kullanım_yeri = lis[1].find('p').text
        print(fonun_kullanım_yeri)
    if len(lis) >= 6:
        fiyat_istikrarı = lis[5].find('p').text
        print(fiyat_istikrarı)
    if len(lis) >= 7:
        satmama_taahhudu = lis[6].find('p').text
        print(satmama_taahhudu)
    if len(lis) >= 8:
        halka_aciklik_orani = lis[7].find('p').text
        print(halka_aciklik_orani)

    sehir = detail_soup.find('span', class_='shc-city')
    if sehir:
        print(sehir.text)
    kurulus_yili = detail_soup.find('span', class_='shc-founded')
    if kurulus_yili:
        print(kurulus_yili.text)

    # Gelir tablolarını çekiyor
    tables = detail_soup.find_all('table', class_='fs-extra rwd-table')
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            col_text = [ele.text.strip() for ele in cols]
            print(f"Data from {url}, {isim.text}, {arz_tarihi}, {col_text}")  # URL ve çekilen verileri yazdırma


# CSV dosyasını aç ve bir yazıcı nesnesi oluştur
with open('company_data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Kolon başlıkları
    writer.writerow(['Şirket İsmi', 'Arz Tarihi', 'Arz Şekli', 'Fonun Kullanım Yeri', 'Fiyat İstikrarı', 'Satmama Taahhüdü', 'Halka Açıklık Oranı', 'Şehir', 'Kuruluş Yılı', 'Gelir Tablosu Verileri'])

    for url in company_urls:
        response = requests.get(url, headers=headers)
        detail_soup = BeautifulSoup(response.text, 'lxml')

        # Şirket ismini çekiyor
        isim = detail_soup.find('h1', class_='il-halka-arz-sirket').text if detail_soup.find('h1', class_='il-halka-arz-sirket') else '-'

        # Arz tarihini çekiyor
        arz_tarihi = '-'
        time_tags = detail_soup.select("table.sp-table time")
        for time_tag in time_tags:
            arz_tarihi = time_tag.get('title', '') or time_tag.get('datetime', '-')

        # P'lerin yer aldığı li'leri çekiyor
        lis = detail_soup.select("ul.aex-in li")
        arz_sekli = lis[0].find('p').text if len(lis) > 0 else '-'
        fonun_kullanım_yeri = lis[1].find('p').text if len(lis) > 1 else '-'
        fiyat_istikrarı = lis[5].find('p').text if len(lis) > 5 else '-'
        satmama_taahhudu = lis[6].find('p').text if len(lis) > 6 else '-'
        halka_aciklik_orani = lis[7].find('p').text if len(lis) > 7 else '-'

        sehir = detail_soup.find('span', class_='shc-city').text if detail_soup.find('span', class_='shc-city') else '-'
        kurulus_yili = detail_soup.find('span', class_='shc-founded').text if detail_soup.find('span', class_='shc-founded') else '-'

        # Gelir tablosu verilerini çekiyor
        gelir_tablosu_verileri = []
        tables = detail_soup.find_all('table', class_='fs-extra rwd-table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                col_text = [ele.text.strip() for ele in cols]
                gelir_tablosu_verileri.append(', '.join(col_text))

        # Her şirket için bir satır yaz
        writer.writerow([isim, arz_tarihi, arz_sekli, fonun_kullanım_yeri, fiyat_istikrarı, satmama_taahhudu, halka_aciklik_orani, sehir, kurulus_yili, '; '.join(gelir_tablosu_verileri)])
