import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def plot_hourly_seasonal_rental(hour_df):
    # Definisikan warna untuk setiap musim
    season_colors = {"Spring": "#59D5E0", "Summer": "#87A922", "Fall": "#ECB159",  "Winter": "#333A73"}

    # Buat plot menggunakan seaborn
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.pointplot(data=hour_df.groupby(by=[hour_df["hour"], hour_df['season']]).agg({
                    "total": "sum"
                    }).reset_index(),
                  x='hour',
                  y='total',
                  hue='season',
                  palette=season_colors,
                  ax=ax)

    # Atur judul plot
    ax.set_title('Total Sewa Tiap Jam Berdasarkan Musim', fontsize=20)

    # Atur label sumbu x dan sumbu y
    ax.set_xlabel('Jam', fontsize=13)
    ax.set_ylabel('Total', fontsize=13)

    # Aktifkan grid
    ax.grid(True)

    return fig

def plot_weather_rental(hour_df):
    # Hitung total penyewaan sepeda berdasarkan cuaca
    byweather = hour_df.groupby('weather')['total'].sum()
    max_count = byweather.max()

    # Ubah warna
    colors = ['lightgray'] * len(byweather)
    max_index = byweather[byweather == max_count].index[0]
    colors[byweather.index.get_loc(max_index)] = 'skyblue'

    # Bar Chart
    fig, ax = plt.subplots()
    ax.bar(range(len(byweather)), byweather, color=colors)
    ax.set_xlabel('Cuaca')
    ax.set_ylabel('Total')
    ax.set_title('Total Sewa Berdasarkan Cuaca')

    # Tambahkan nilai di atas setiap batang
    for i, value in enumerate(byweather):
        ax.text(i, value, str(int(value)), ha='center', va='bottom', fontsize=10)

    # Mengganti label sumbu x
    ax.set_xticks(range(len(byweather)))
    ax.set_xticklabels(['Cerah\nSedikit Berawan', 'Kabut\nBerawan', 'Hujan\nHujan Salju', 'Hujan Lebat\nBadai Salju'], fontsize=13)

    # Mengubah format sumbu y
    ax.ticklabel_format(style='plain', axis='y')

    return fig

# Load Cleaned Data
hour_data = pd.read_csv("hour_data.csv")

datetime_columns = ["datetime"]
hour_data.sort_values(by="datetime", inplace=True)
hour_data.reset_index(inplace=True)

for column in datetime_columns:
    hour_data[column] = pd.to_datetime(hour_data[column])

min_date = hour_data["datetime"].min()
max_date = hour_data["datetime"].max()

with st.sidebar:
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = hour_data[(hour_data['datetime'] >= str(start_date)) &
                    (hour_data['datetime'] <= str(end_date))]

# mainpage
st.title("Bike-Sharing :bike:")

# membuat subheader daily rental
st.subheader('Daily Bike Rental')

col1, col2, col3 = st.columns(3)
 
with col1:
    total_transaction = hour_data['total'].sum()
    st.metric("Total Rental", total_transaction)
 
with col2:
    total_registered = hour_data['registered'].sum()
    st.metric("Total Registered", total_registered)
 
with col3:
    total_casual = hour_data['casual'].sum()
    st.metric("Total Casual", total_casual)

st.subheader('Rent by Hour and Season')

# Gunakan fungsi plot_hourly_seasonal_rental untuk membuat plot
fig_hourly_seasonal = plot_hourly_seasonal_rental(hour_data)

# Tampilkan plot dalam aplikasi Streamlit
st.pyplot(fig_hourly_seasonal)

st.subheader('Rent by Weather')

# Gunakan fungsi plot_weather_rental untuk membuat plot
fig_weather = plot_weather_rental(hour_data)

# Tampilkan plot dalam aplikasi Streamlit
st.pyplot(fig_weather)