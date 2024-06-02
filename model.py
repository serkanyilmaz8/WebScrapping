import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.utils.class_weight import compute_class_weight

file_path = 'ml_ready_data.csv'
data = pd.read_csv(file_path)

# Bağımsız değişkenler ve bağımlı değişken
X = data.drop(['performans', 'Şirket İsmi', 'Şehir'], axis=1)
y = data['performans']

# Performans değişkenini etiketleme
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Sınıf ağırlıklarını hesaplama
class_weights = compute_class_weight('balanced', classes=np.unique(y_encoded), y=y_encoded)
class_weights_dict = {i : class_weights[i] for i in range(len(class_weights))}

# Veriyi train ve test kısımlarına ayırma
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Random Forest modelini oluşturma ve eğitme (sınıf ağırlıkları ile)
model = RandomForestClassifier(random_state=42, class_weight=class_weights_dict)
model.fit(X_train, y_train)

# Çapraz doğrulama ile model değerlendirme
cv_scores = cross_val_score(model, X, y_encoded, cv=5)
print(f'Cross-validation scores: {cv_scores}')
print(f'Mean cross-validation score: {cv_scores.mean()}')

# Test verisi ile tahmin yapma
y_pred = model.predict(X_test)

# Performans metriklerini yazdırma
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, target_names=label_encoder.classes_, zero_division=0)

print(f'Accuracy: {accuracy}')
print('Classification Report:')
print(report)

# Verilen verilerden bir tanesini tahmin ettirme
sample_index = 0  # İlk veri örneğini kullanma
sample = X_test.iloc[sample_index]
sample_prediction = model.predict([sample])

# Tahmin edilen değeri ve orijinal değeri döndürme
original_value = y_test[sample_index]
predicted_value = sample_prediction[0]

# Orijinal ve tahmin edilen değerleri etiketlerden geri çevirme
original_label = label_encoder.inverse_transform([original_value])[0]
predicted_label = label_encoder.inverse_transform([predicted_value])[0]

print(f'Original Label: {original_label}')
print(f'Predicted Label: {predicted_label}')