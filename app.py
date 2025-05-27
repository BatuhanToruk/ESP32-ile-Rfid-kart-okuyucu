import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import io
import time

# --- Google Sheets Yetkilendirme ---
scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    'rfid-attendance-project-460911-4d53ab0ee056.json', scope
)
client = gspread.authorize(creds)
sheet = client.open("RFID Based Attendance System").sheet1
records = sheet.get_all_records()
df = pd.DataFrame(records)

# --- Veri Ön İşleme ---
df["Date"] = pd.to_datetime(df["Date"], format="%d.%m.%Y")
df["Hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
df["Weekday"] = df["Date"].dt.day_name()

# --- Streamlit Arayüzü ---

st.title("📋 RFID Katılım Paneli - Gelişmiş Görselleştirme")

# Genel İstatistikler
st.subheader("📦 Genel İstatistikler")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Toplam Giriş", len(df))
with col2:
    st.metric("Farklı Kişi Sayısı", df["Name"].nunique())
with col3:
    peak_hour = df["Hour"].mode()[0]
    st.metric("En Yoğun Saat", f"{peak_hour}:00")

# Ham Veri
st.subheader("🔍 Ham Veri")
st.dataframe(df)

# Tarih Aralığı Filtreleme
st.subheader("📅 Tarih Aralığı Filtrele")
min_date = df["Date"].min().date()
max_date = df["Date"].max().date()
start_date, end_date = st.date_input("Tarih Seç", [min_date, max_date], min_value=min_date, max_value=max_date)
mask = (df["Date"] >= pd.to_datetime(start_date)) & (df["Date"] <= pd.to_datetime(end_date))
filtered_by_date = df[mask]
st.write(f"{len(filtered_by_date)} kayıt bulundu.")

# Kişi Seçimi (Filtreli Veri Üzerinden)
st.subheader("👤 Kişi Seç ve Detayları Gör")
names_filtered = filtered_by_date["Name"].unique()
selected_name = st.selectbox("Kişi Seç", options=names_filtered)
filtered_df = filtered_by_date[filtered_by_date["Name"] == selected_name]
st.dataframe(filtered_df.sort_values(["Date", "Time"], ascending=False))

# Kişiye Göre Giriş Sayısı (Filtreli Veri)
st.subheader("👥 Kişiye Göre Giriş Sayısı")
name_counts = filtered_by_date["Name"].value_counts()
st.bar_chart(name_counts)

# Günlük Giriş Sayısı (Filtreli Veri)
st.subheader("📈 Günlük Giriş Sayısı")
daily_counts = filtered_by_date.groupby("Date").size()
st.line_chart(daily_counts)

# Saatlik Giriş Yoğunluğu (Filtreli Veri)
st.subheader("⏰ Saatlik Giriş Yoğunluğu")
hourly = filtered_by_date.groupby("Hour").size()
st.bar_chart(hourly)

# Heatmap - Gün & Saat Yoğunluğu (Filtreli Veri)
st.subheader("🔥 Saat & Gün Yoğunluğu (Isı Haritası)")
heatmap_data = filtered_by_date.groupby(["Weekday", "Hour"]).size().unstack(fill_value=0)
order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
heatmap_data = heatmap_data.reindex(order)
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(heatmap_data, cmap="YlOrRd", ax=ax)
st.pyplot(fig)

# Plotly ile Etkileşimli Günlük Giriş Grafiği (Filtreli Veri)
st.subheader("📊 Etkileşimli Günlük Giriş Grafiği (Plotly)")
daily_counts_df = daily_counts.reset_index(name="Giriş Sayısı")
fig2 = px.line(daily_counts_df, x="Date", y="Giriş Sayısı", markers=True, title="Günlük Giriş Sayısı")
st.plotly_chart(fig2)

# Haftalık Kişi Analizi
st.subheader("📅 Haftalık Kişi Analizi")
weekly_counts = filtered_by_date.groupby(["Weekday", "Name"]).size().unstack(fill_value=0)
weekly_counts = weekly_counts.reindex(order)
fig3 = px.bar(
    weekly_counts,
    barmode='group',
    title="Haftalık Günlere Göre Kişi Bazlı Girişler",
    labels={"value": "Giriş Sayısı", "Weekday": "Haftanın Günü"}
)
st.plotly_chart(fig3)

# Son 10 Giriş (Filtreli Veri)
st.subheader("🧍‍♂️ Son 10 Giriş")
st.dataframe(filtered_by_date.sort_values(["Date", "Time"], ascending=False).head(10))

# Excel ve CSV İndirme Butonları
st.subheader("💾 Veriyi Excel veya CSV olarak indir")

csv = filtered_by_date.to_csv(index=False).encode('utf-8')
st.download_button(
    label="CSV İndir",
    data=csv,
    file_name='rfid_data.csv',
    mime='text/csv'
)

output = io.BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    filtered_by_date.to_excel(writer, index=False, sheet_name='RFID_Data')

processed_data = output.getvalue()

st.download_button(
    label="Excel İndir",
    data=processed_data,
    file_name="rfid_data.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# Basit Uyarılar
st.subheader("⚠️ Uyarılar")
threshold = st.number_input("Uyarı için giriş sayısı eşik değeri", min_value=1, value=10)
name_entry_counts = filtered_by_date["Name"].value_counts()
alert_names = name_entry_counts[name_entry_counts > threshold]

if not alert_names.empty:
    st.warning(f"Aşağıdaki kişiler {threshold} girişten fazla yapmış:")
    for name, count in alert_names.items():
        st.write(f"- {name}: {count} giriş")
else:
    st.success("Uyarı: Şu anda anormal giriş yok.")

# Manuel Veriyi Yenile Butonu
if st.button("🔄 Verileri Yenile"):
    st.experimental_rerun()

# Otomatik Yenileme (Sidebar'dan ayarlanabilir)
refresh_interval = st.sidebar.number_input("Otomatik yenileme süresi (saniye)", min_value=10, max_value=3600, value=60)
st.sidebar.write(f"Sayfa her {refresh_interval} saniyede bir otomatik yenilenecek.")
time.sleep(refresh_interval)
st.experimental_rerun()
