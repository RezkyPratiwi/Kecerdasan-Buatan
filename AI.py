# 


import pandas as pd

# Fungsi Membership Servis
def servis_low(x):
    if x <= 1:
        return 1
    elif 1 < x < 50:
        return (50 - x) / (50 - 1)
    else:
        return 0

def servis_medium(x):
    if 30 < x < 50:
        return (x - 30) / (50 - 30)
    elif 50 <= x <= 70:
        return (70 - x) / (70 - 50)
    else:
        return 0

def servis_high(x):
    if x >= 100:
        return 1
    elif 50 < x < 100:
        return (x - 50) / (100 - 50)
    else:
        return 0

# Fungsi Membership Harga
def harga_cheap(x):
    if x <= 25000:
        return 1
    elif 25000 < x < 40000:
        return (40000 - x) / (40000 - 25000)
    else:
        return 0

def harga_medium(x):
    if 30000 < x < 40000:
        return (x - 30000) / (40000 - 30000)
    elif 40000 <= x <= 50000:
        return (50000 - x) / (50000 - 40000)
    else:
        return 0

def harga_expensive(x):
    if x >= 55000:
        return 1
    elif 40000 < x < 55000:
        return (x - 40000) / (55000 - 40000)
    else:
        return 0

# Fungsi Inferensi
def inferensi(servis_deg, harga_deg):
    rules = []
    for servis_label, s_val in servis_deg.items():
        for harga_label, h_val in harga_deg.items():
            activation = min(s_val, h_val)
            if activation > 0:
                if servis_label == 'Low' and harga_label == 'Expensive':
                    rules.append(('Low', activation))
                elif servis_label == 'Low' and harga_label == 'Medium':
                    rules.append(('Low', activation))
                elif servis_label == 'Low' and harga_label == 'Cheap':
                    rules.append(('Medium', activation))
                elif servis_label == 'Medium' and harga_label == 'Expensive':
                    rules.append(('Low', activation))
                elif servis_label == 'Medium' and harga_label == 'Medium':
                    rules.append(('Medium', activation))
                elif servis_label == 'Medium' and harga_label == 'Cheap':
                    rules.append(('High', activation))
                elif servis_label == 'High' and harga_label == 'Expensive':
                    rules.append(('Medium', activation))
                elif servis_label == 'High' and harga_label == 'Medium':
                    rules.append(('High', activation))
                elif servis_label == 'High' and harga_label == 'Cheap':
                    rules.append(('Very High', activation))
    return rules

# Defuzzification
def defuzzification(rules):
    output_values = {
        'Low': 25,
        'Medium': 50,
        'High': 75,
        'Very High': 90
    }
    numerator = 0
    denominator = 0
    for label, activation in rules:
        numerator += activation * output_values[label]
        denominator += activation
    if denominator == 0:
        return 0
    else:
        return numerator / denominator

# --- MAIN PROGRAM ---

# Membaca file restoran.xlsx
data = pd.read_excel('restoran.xlsx')

# Pastikan nama kolomnya benar: ID, Pelayanan, harga
data.columns = ['ID', 'Pelayanan', 'Harga']

# Proses fuzzy
scores = []
for idx, row in data.iterrows():
    pelayanan = row['Pelayanan']
    harga = row['Harga']
    
    # Gunakan kolom 'Pelayanan' untuk menggantikan 'Servis'
    servis_deg = {
        'Low': servis_low(pelayanan),
        'Medium': servis_medium(pelayanan),
        'High': servis_high(pelayanan)
    }
    harga_deg = {
        'Cheap': harga_cheap(harga),
        'Medium': harga_medium(harga),
        'Expensive': harga_expensive(harga)
    }
    
    rules = inferensi(servis_deg, harga_deg)
    skor = defuzzification(rules)
    scores.append(skor)

# Tambahkan skor ke DataFrame
data['Skor'] = scores

# Urutkan berdasarkan skor tertinggi
top5 = data.sort_values(by='Skor', ascending=False).head(5)

# Simpan hasil ke peringkat.xlsx
top5[['ID', 'Pelayanan', 'Harga', 'Skor']].to_excel('peringkat.xlsx', index=False)

# Tampilkan hasil
print("5 Restoran Terbaik:")
print(top5[['ID', 'Pelayanan', 'Harga', 'Skor']])
