import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import matplotlib.pyplot as plt

# Yetkilendirme
scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    'indirilen .json dosyası', scope
)
client = gspread.authorize(creds)
sheet = client.open("RFID Based Attendance System").sheet1
records = sheet.get_all_records()
df = pd.DataFrame(records)

# 🔍 Tüm verileri göster
print(df)

# 🗓️ Tarih sütununu tarih nesnesine çevir
df["Date"] = pd.to_datetime(df["Date"], format="%d.%m.%Y")

# 👤 Kişi başına giriş sayısı (bar chart)
name_counts = df["Name"].value_counts()
name_counts.plot(kind="bar", title="Kişiye Göre Giriş Sayısı", ylabel="Giriş Sayısı")
plt.tight_layout()
plt.show()

# 📈 Günlük giriş sayısı (line chart)
daily_counts = df.groupby("Date").size()
daily_counts.plot(kind="line", marker='o', title="Günlük Giriş Sayısı", ylabel="Giriş")
plt.tight_layout()
plt.show()
