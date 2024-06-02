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