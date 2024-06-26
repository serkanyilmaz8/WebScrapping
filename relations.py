import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Veri setini yükleme
file_path = 'ml_ready_data.csv'
data = pd.read_csv(file_path)

# Grafiklerin genel stilini ayarlama
sns.set(style="whitegrid")

# 1. Sınıf dağılımı (performans)
plt.figure(figsize=(10, 6))
sns.countplot(x='performans', data=data)
plt.title('Performans Sınıf Dağılımı')
plt.xlabel('Performans')
plt.ylabel('Sayı')
plt.show()

# 2. Halka arz büyüklüğüne göre performans
plt.figure(figsize=(10, 6))
sns.boxplot(x='performans', y='halka_arz_buyuklugu (Milyar TL)', data=data)
plt.title('Performansa Göre Halka Arz Büyüklüğü')
plt.xlabel('Performans')
plt.ylabel('Halka Arz Büyüklüğü (Milyar TL)')
plt.show()

# 3. Şirket yaşı ve performans ilişkisi
plt.figure(figsize=(10, 6))
sns.boxplot(x='performans', y='sirket_yasi', data=data)
plt.title('Performansa Göre Şirket Yaşı')
plt.xlabel('Performans')
plt.ylabel('Şirket Yaşı')
plt.show()

# 4. Diğer bazı özelliklerin dağılımı ve ilişkisi
plt.figure(figsize=(14, 12))

plt.subplot(2, 2, 1)
sns.histplot(data['sermaye_artirimi_orani'], kde=True, bins=20)
plt.title('Sermaye Artırımı Oranı Dağılımı')

plt.subplot(2, 2, 2)
sns.histplot(data['ortak_satisi_orani'], kde=True, bins=20)
plt.title('Ortak Satışı Oranı Dağılımı')

plt.subplot(2, 2, 3)
sns.scatterplot(x='borc_odeme', y='yatirim_sermayesi', hue='performans', data=data)
plt.title('Borç Ödeme ve Yatırım Sermayesi İlişkisi')

plt.subplot(2, 2, 4)
sns.scatterplot(x='isletme_sermayesi', y='fiyat_istikrari_gun', hue='performans', data=data)
plt.title('İşletme Sermayesi ve Fiyat İstikrarı Gün Sayısı İlişkisi')

plt.tight_layout()
plt.show()

# 5. Halka Arz Büyüklüğüne Göre Hasılat Artışı
# Gerekli sütunları seçme
required_columns = ['hasilat_3_yil_once (Milyar)', 'hasilat_1_yil_once (Milyar)', 'halka_arz_buyuklugu (Milyar TL)']
data_temp = data[required_columns].copy()

# İki sütun arasındaki farkı hesaplama
data_temp.loc[:, 'hasilat_artisi'] = data_temp['hasilat_1_yil_once (Milyar)'] - data_temp['hasilat_3_yil_once (Milyar)']

# Scatter plot oluşturma
plt.figure(figsize=(12, 8))
sns.scatterplot(x='halka_arz_buyuklugu (Milyar TL)', y='hasilat_artisi', data=data_temp)
plt.title('Halka Arz Büyüklüğüne Göre Hasılat Artışı')
plt.xlabel('Halka Arz Büyüklüğü (Milyar TL)')
plt.ylabel('Hasılat Artışı (Milyar)')
plt.show()

# 6. Halka Arz Büyüklüğüne Göre Brüt Kar Farkı
# Gerekli sütunları seçme
required_columns = ['brut_kar_3_yil_once (Milyar)', 'brut_kar_1_yil_once (Milyar)', 'halka_arz_buyuklugu (Milyar TL)']
data_temp = data[required_columns].copy()

# İki sütun arasındaki farkı hesaplama
data_temp.loc[:, 'brut_kar_farki'] = data_temp['brut_kar_1_yil_once (Milyar)'] - data_temp['brut_kar_3_yil_once (Milyar)']

# Scatter plot oluşturma
plt.figure(figsize=(12, 8))
sns.scatterplot(x='halka_arz_buyuklugu (Milyar TL)', y='brut_kar_farki', data=data_temp)
plt.title('Halka Arz Büyüklüğüne Göre Brüt Kar Farkı')
plt.xlabel('Halka Arz Büyüklüğü (Milyar TL)')
plt.ylabel('Brüt Kar Artışı')
plt.show()