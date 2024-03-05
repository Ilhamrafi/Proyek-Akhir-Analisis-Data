import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import hydralit_components as hc

# Fungsi untuk konfigurasi halaman
def setup_page_configuration():
    st.set_page_config(
        page_title='Dashboard',
        page_icon="🎮",
        layout='wide',
        initial_sidebar_state='auto',
    )

# Fungsi untuk menyiapkan navigasi
def setup_navigation_bar():
    menu_data = [
        {'icon': "📇", 'label': "Pengaruh Musim"},
        {'icon': "💾", 'label': "Hubungan Cuaca"},
        {'icon': "🚀", 'label': "Pola berdasarkan Waktu(bulan)"},
        {'icon': "🔮", 'label': "Pola Berdasarkan Musim"},
    ]

    over_theme = {
        'txc_inactive': '#FFFFFF', 
        'txc_active': '#000000',   
        'menu_background': '#2C3E50',  
        'option_active': '#E74C3C',  
        'font_family': 'Montserrat, sans-serif', 
    }

    menu_id = hc.nav_bar(
        menu_definition=menu_data,
        override_theme=over_theme,
        home_name='Home',
        hide_streamlit_markers=False,
        sticky_nav=True,
        sticky_mode='pinned',
    )

    return menu_id

# Membaca data dari file CSV
df_day = pd.read_csv('dashboard/day.csv')

def create_visualizations(df_day):
    # Mengubah nama kolom
    df_day.rename(columns={
        'dteday': 'dateday',
        'yr': 'year',
        'mnth': 'month',
        'cnt': 'cnt'
    }, inplace=True)

    # Mengubah angka menjadi teks
    df_day['month'] = df_day['month'].map({
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
        7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
    })

    df_day['season'] = df_day['season'].map({
        1: 'Spring',
        2: 'Summer',
        3: 'Fall',
        4: 'Winter'
    })

    df_day['weekday'] = df_day['weekday'].map({
        0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'
    })

    df_day['weathersit'] = df_day['weathersit'].map({
        1: 'Clear/Partly Cloudy',
        2: 'Mist/Cloudy',
        3: 'Light Snow/Rain',
        4: 'Severe Weather'
    })

    # Mengubah tipe data ke datetime dan categorical
    df_day['dateday'] = pd.to_datetime(df_day.dateday)
    for col in ['season', 'year', 'month', 'holiday', 'weekday', 'workingday', 'weathersit']:
        df_day[col] = df_day[col].astype('category')

# Fungsi untuk menangani menu beranda
def handle_home_menu():
    st.markdown(
        """
        <h1 style="text-align: center; color: #007BFF;">Selamat Datang di Proyek Akhir: Belajar Analisis Data dengan Python</h1>
        """,
        unsafe_allow_html=True
    )    

    st.info("""
        Selamat datang di Proyek Analisis Data: Bike Sharing Dataset! 

        Dalam proyek ini, saya akan menjelajahi dataset penyewaan sepeda dan mencoba menjawab beberapa pertanyaan penting:

        1. Bagaimana hubungan antara musim dan jumlah sewa sepeda harian?
        2. Bagaimana hubungan antara cuaca (weathersit) dan jumlah sewa sepeda harian?
        3. Apakah terdapat perbedaan dalam jumlah sewa sepeda harian antara hari kerja (working day), hari libur (holiday), dan akhir pekan (weekend)?
        4. Bagaimana pola penyewaan sepeda berdasarkan waktu (bulan)?
        5. Bagaimana pola penyewaan sepeda berdasarkan musim (spring, summer, fall, winter)?

        Dengan menganalisis pertanyaan-pertanyaan ini, saya berharap dapat memperoleh pemahaman yang lebih baik tentang tren dan pola dalam penyewaan sepeda, yang dapat bermanfaat untuk pengambilan keputusan dan perencanaan strategis di masa depan.
    """)

def handle_musim_menu():
        # Menghitung total sewa per musim
        df_season = df_day.groupby('season').sum(numeric_only=True).reset_index()

        # Menampilkan bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        plt.bar(
            df_season['season'],
            df_season['registered'],
            label='Registered',
            color='blue'
        )

        plt.bar(
            df_season['season'],
            df_season['casual'],
            label='Casual',
            color='orange'
        )

        plt.title('Total Sewa Sepeda per Musim')

        # Mengubah label sumbu x
        plt.xticks(df_season['season'], ['Spring', 'Summer', 'Fall', 'Winter'])

        plt.legend()
        st.pyplot(fig)

def handle_cuaca_menu():
    colors = sns.color_palette('husl', len(df_day['weathersit'].unique()))

    plt.figure(figsize=(10, 6))
    sns.barplot(
        x='weathersit',
        y='cnt',
        data=df_day,
        palette=colors,
        hue='weathersit', 
        legend=False 
    )
    plt.title('Jumlah Sewa Sepeda Berdasarkan Kondisi Cuaca (weathersit)')
    plt.xlabel('Kondisi Cuaca')
    plt.ylabel('Jumlah Sewa Sepeda')
    st.pyplot(plt)

def handle_waktu_menu():
    sns.set_style("whitegrid")
    plt.figure(figsize=(12, 6))
    sns.lineplot(x="mnth", y="cnt", data=df_day, errorbar=None)
    plt.title("Pola Jumlah Sewa Sepeda Harian Berdasarkan Bulan")
    plt.xlabel("Bulan")
    plt.ylabel("Jumlah Sewa Sepeda Harian")
    st.pyplot(plt)

def handle_pola_menu():
    sns.set_style("whitegrid")
    plt.figure(figsize=(12, 6))
    sns.lineplot(x="season", y="cnt", data=df_day, errorbar=None)
    plt.title("Pola Jumlah Sewa Sepeda Harian Berdasarkan Musim")
    plt.xlabel("Musim")
    plt.ylabel("Jumlah Sewa Sepeda Harian")
    st.pyplot(plt)

def handle_menu_selection(menu_id):
    if menu_id == "Home":
        handle_home_menu()
    elif menu_id == "Pengaruh Musim":
        handle_musim_menu()
    elif menu_id == "Hubungan Cuaca":
        handle_cuaca_menu()
    elif menu_id == "Pola berdasarkan Waktu(bulan)":
        handle_waktu_menu()
    elif menu_id == "Pola Berdasarkan Musim":
        handle_pola_menu()

def main():
    setup_page_configuration()
    menu_id = setup_navigation_bar()
    handle_menu_selection(menu_id)

if __name__ == "__main__":
    main()
