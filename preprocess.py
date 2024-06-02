from datetime import datetime
import pandas as pd
import re

file_path = 'company_data.csv'
data = pd.read_csv(file_path)

data_cleaned = data.replace('-', pd.NA).dropna(axis=1, how='all')
# Tamamen boş olan satırları silme
data_cleaned_rows = data_cleaned.dropna(how='all').reset_index(drop=True)

cleaned_file_path = 'cleaned_company_data.csv'
data_cleaned_rows.to_csv(cleaned_file_path, index=False)

print(f'Temizlenmiş veri seti {cleaned_file_path} dosyasına kaydedildi.')

core_data = data_cleaned_rows[
    (data_cleaned_rows['Arz Tarihi'] != 'Hazırlanıyor...') &
    (data_cleaned_rows['Arz Tarihi'] != 'Ertelendi') &
    data_cleaned_rows['Arz Tarihi'].notna()
]

core_data_file_path = 'core_data.csv'
core_data.to_csv(core_data_file_path, index=False)

print(f'Filtrelenmiş veri seti {core_data_file_path} dosyasına kaydedildi.')

def extract_percentages(text):
    sermaye_artirimi = ortak_satisi = 0

    if isinstance(text, str):
        sermaye_artirimi_match = re.search(r'Sermaye Artırımı : ([\d,\.]+) Lot', text)
        ortak_satisi_matches = re.findall(r'Ortak Satışı : ([\d,\.]+) Lot', text)

        if sermaye_artirimi_match:
            sermaye_artirimi = float(sermaye_artirimi_match.group(1).replace('.', '').replace(',', '.'))

        if ortak_satisi_matches:
            ortak_satisi = sum(float(s.replace('.', '').replace(',', '.')) for s in ortak_satisi_matches)

    toplam = sermaye_artirimi + ortak_satisi
    sermaye_artirimi_orani = round(sermaye_artirimi / toplam, 2) if toplam > 0 else 0
    ortak_satisi_orani = round(ortak_satisi / toplam, 2) if toplam > 0 else 0

    return sermaye_artirimi_orani, ortak_satisi_orani

core_data[['sermaye_artirimi_orani', 'ortak_satisi_orani']] = core_data['Arz Şekli'].apply(
    lambda x: pd.Series(extract_percentages(x)))
core_data.drop(columns=['Arz Şekli'], inplace=True)
ml_data_file_path = 'ml_ready_data.csv'
core_data.to_csv(ml_data_file_path, index=False)
print(f'Temizlenmiş ve makine öğrenimi için hazır veri seti {ml_data_file_path} dosyasına kaydedildi.')

def extract_fund_distribution(text):
    borc = yatirim = isletme = 0
    if isinstance(text, str):
        matches = re.findall(r'%(\d+-?\d*)\s+([^\.\n]+)', text)
        for match in matches:
            if '-' in match[0]:
                lower, upper = map(int, match[0].split('-'))
                percentage = (lower + upper) / 2
            else:
                percentage = int(match[0])
            usage = match[1].lower()
            if 'borç' in usage:
                borc += percentage
            elif 'yatırım' in usage:
                yatirim += percentage
            else:
                isletme += percentage
    return borc, yatirim, isletme

core_data[['borc_odeme', 'yatirim_sermayesi', 'isletme_sermayesi']] = core_data['Fonun Kullanım Yeri'].apply(
    lambda x: pd.Series(extract_fund_distribution(x)))

core_data.drop(columns=['Fonun Kullanım Yeri'], inplace=True)

ml_data_file_path = 'ml_ready_data.csv'
core_data.to_csv(ml_data_file_path, index=False)
print(f'Temizlenmiş ve makine öğrenimi için hazır veri seti {ml_data_file_path} dosyasına kaydedildi.')

def extract_days(text):
    if isinstance(text, str):
        days_match = re.search(r'(\d+)\s+gün', text)
        if days_match:
            return int(days_match.group(1))
        else:
            return 0
    return None

core_data['fiyat_istikrari_gun'] = core_data['Fiyat İstikrarı'].apply(extract_days)
core_data.drop(columns=['Fiyat İstikrarı'], inplace=True)

core_data.drop(columns=['Satmama Taahhüdü'], inplace=True)
ml_data_file_path = 'ml_ready_data.csv'
core_data.to_csv(ml_data_file_path, index=False)
print(f'Temizlenmiş ve makine öğrenimi için hazır veri seti {ml_data_file_path} dosyasına kaydedildi.')
def extract_halka_aciklik_orani(text):
    if isinstance(text, str):
        percentage_match = re.search(r'%(\d+)', text)
        if percentage_match:
            return int(percentage_match.group(1))
    return 20

core_data['halka_aciklik_orani'] = core_data['Halka Açıklık Oranı'].apply(extract_halka_aciklik_orani)
core_data.drop(columns=['Halka Açıklık Oranı'], inplace=True)
ml_data_file_path = 'ml_ready_data.csv'
core_data.to_csv(ml_data_file_path, index=False)

print(f'Temizlenmiş ve makine öğrenimi için hazır veri seti {ml_data_file_path} dosyasına kaydedildi.')
def extract_city(text):
    if isinstance(text, str):
        city_match = re.search(r'Şehir\s*:\s*(.+)', text)
        if city_match:
            return city_match.group(1).strip()
    return None

core_data['Şehir'] = core_data['Şehir'].apply(extract_city)
ml_data_file_path = 'ml_ready_data.csv'
core_data.to_csv(ml_data_file_path, index=False)
print(f'Temizlenmiş ve makine öğrenimi için hazır veri seti {ml_data_file_path} dosyasına kaydedildi.')
def extract_company_age(text):
    if isinstance(text, str):
        year_match = re.search(r'Kuruluş Tarihi\s*:\s*(\d{2}\.\d{2}\.\d{4})', text)
        if year_match:
            kuruluş_tarihi = datetime.strptime(year_match.group(1), '%d.%m.%Y')
            current_year = datetime.now().year
            company_age = current_year - kuruluş_tarihi.year
            return company_age
    return None
core_data['sirket_yasi'] = core_data['Kuruluş Yılı'].apply(extract_company_age)
core_data.drop(columns=['Kuruluş Yılı'], inplace=True)
ml_data_file_path = 'ml_ready_data.csv'
core_data.to_csv(ml_data_file_path, index=False)
print(f'Temizlenmiş ve makine öğrenimi için hazır veri seti {ml_data_file_path} dosyasına kaydedildi.')

def extract_numbers(text):
    numbers = []
    if isinstance(text, str):
        matches = re.findall(r'([\d,.]+)\s*(Milyon|Milyar) TL', text)
        for match in matches:
            number_str, unit = match
            number = float(number_str.replace('.', '').replace(',', '.'))
            if unit == 'Milyon':
                number /= 1000  # Milyara çevir
            numbers.append(round(number, 2))
    while len(numbers) < 6:
        numbers.append(None)
    return numbers

columns = [
    'hasilat_1_yil_once (Milyar)', 'hasilat_2_yil_once (Milyar)', 'hasilat_3_yil_once (Milyar)',
    'brut_kar_1_yil_once (Milyar)', 'brut_kar_2_yil_once (Milyar)', 'brut_kar_3_yil_once (Milyar)'
]
core_data[columns] = pd.DataFrame(core_data['Gelir Tablosu Verileri'].apply(extract_numbers).tolist(), index=core_data.index)
print(f'Temizlenmiş ve makine öğrenimi için hazır veri seti {ml_data_file_path} dosyasına kaydedildi.')

halka_arz_buyuklukleri = [3.78, 1.88, 2.6, 2.6, 4.2, 0.5, 2.5, 0.9, 4.5, 0.9, 4.5, 1.7, 0.8, 0.8, 1.3, 1.9, 1, 3, 3.7, 1.3]
halka_arz_buyuklukleri_full = halka_arz_buyuklukleri + [None] * (len(core_data) - len(halka_arz_buyuklukleri))
core_data['halka_arz_buyuklugu (Milyar TL)'] = halka_arz_buyuklukleri_full
output_file_path = 'ml_ready_data.csv'
core_data.to_csv(output_file_path, index=False)
print(f'Halka arz büyüklükleri eklenmiş veri seti {output_file_path} dosyasına kaydedildi.')

performans_degerleri = [
    'average', 'good', 'bad', 'average', 'bad', 'good', 'good', 'good', 'bad', 'average',
    'bad', 'average', 'good', 'good', 'good', 'good', 'good', 'good', 'average', 'bad'
]
performans_degerleri_full = performans_degerleri + [None] * (len(core_data) - len(performans_degerleri))
core_data['performans'] = performans_degerleri_full
output_file_path = 'ml_ready_data.csv'
core_data.to_csv(output_file_path, index=False)
print(f'Performans değerleri eklenmiş veri seti {output_file_path} dosyasına kaydedildi.')

core_data.drop(columns=['Arz Tarihi'], inplace=True)
core_data.drop(columns=['Gelir Tablosu Verileri'], inplace=True)
ml_data_file_path = 'ml_ready_data.csv'
core_data.to_csv(ml_data_file_path, index=False)