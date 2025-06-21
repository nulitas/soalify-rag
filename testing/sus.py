import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def hitung_skor_sus(df):
    """
    Menghitung skor SUS (System Usability Scale) dari DataFrame.
    
    Parameter:
    df (pandas.DataFrame): DataFrame dengan respons kuesioner SUS
                          Kolom pertama berisi nama/ID responden
                          Kolom 2-11 berisi respons SUS (skala 1-5)
    
    Mengembalikan:
    dict: Dictionary berisi berbagai statistik SUS
    """
    
    # Ekstrak hanya kolom SUS (tidak termasuk nama responden)
    data_sus = df.iloc[:, 1:11]  # Asumsi 10 pertanyaan SUS
    
    # Bersihkan nama kolom (hapus spasi ekstra)
    data_sus.columns = [col.strip() for col in data_sus.columns]
    
    # Konversi semua data ke numerik (tangani nilai string)
    data_sus = data_sus.apply(pd.to_numeric, errors='coerce')
    
    # Periksa nilai yang hilang
    if data_sus.isnull().any().any():
        print("Peringatan: Terdeteksi nilai yang hilang. Akan diisi dengan nilai netral (3).")
        data_sus = data_sus.fillna(3)
    
    # Dapatkan total responden
    total_responden = len(data_sus)
    
    def hitung_skor_sus_individu(baris):
        """Hitung skor SUS untuk satu responden"""
        # Pertanyaan ganjil (1,3,5,7,9): skor - 1
        skor_ganjil = baris.iloc[::2] - 1  # Pertanyaan 1,3,5,7,9
        
        # Pertanyaan genap (2,4,6,8,10): 5 - skor
        skor_genap = 5 - baris.iloc[1::2]  # Pertanyaan 2,4,6,8,10
        
        # Jumlahkan semua skor dan kalikan dengan 2.5
        total_skor = (skor_ganjil.sum() + skor_genap.sum()) * 2.5
        return total_skor
    
    # Hitung skor SUS untuk setiap responden
    skor_sus = data_sus.apply(hitung_skor_sus_individu, axis=1)
    
    # Hitung statistik
    rata_rata_skor_sus = skor_sus.mean()
    median_skor_sus = skor_sus.median()
    std_skor_sus = skor_sus.std()
    min_skor_sus = skor_sus.min()
    max_skor_sus = skor_sus.max()
    
    # Hitung persentil
    persentil_25 = skor_sus.quantile(0.25)
    persentil_75 = skor_sus.quantile(0.75)
    
    # Interpretasi SUS
    if rata_rata_skor_sus >= 80:
        interpretasi = "Sangat Baik"
    elif rata_rata_skor_sus >= 70:
        interpretasi = "Baik"
    elif rata_rata_skor_sus >= 50:
        interpretasi = "Cukup/Marginal"
    else:
        interpretasi = "Buruk"
    
    # Buat dictionary hasil
    hasil = {
        'total_responden': total_responden,
        'skor_individu': skor_sus.tolist(),
        'skor_rata_rata': round(rata_rata_skor_sus, 2),
        'skor_median': round(median_skor_sus, 2),
        'standar_deviasi': round(std_skor_sus, 2),
        'skor_minimum': round(min_skor_sus, 2),
        'skor_maksimum': round(max_skor_sus, 2),
        'persentil_25': round(persentil_25, 2),
        'persentil_75': round(persentil_75, 2),
        'interpretasi': interpretasi
    }
    
    return hasil, skor_sus

def cetak_hasil_sus(hasil):
    """Cetak hasil SUS yang diformat"""
    print("=" * 50)
    print("HASIL SUS (System Usability Scale)")
    print("=" * 50)
    print(f"Total Responden: {hasil['total_responden']}")
    print(f"Skor SUS Rata-rata: {hasil['skor_rata_rata']}")
    print(f"Skor SUS Median: {hasil['skor_median']}")
    print(f"Standar Deviasi: {hasil['standar_deviasi']}")
    print(f"Skor Minimum: {hasil['skor_minimum']}")
    print(f"Skor Maksimum: {hasil['skor_maksimum']}")
    print(f"Persentil ke-25: {hasil['persentil_25']}")
    print(f"Persentil ke-75: {hasil['persentil_75']}")
    print(f"Interpretasi: {hasil['interpretasi']}")
    print("=" * 50)

def plot_distribusi_sus(skor_sus, hasil):
    """Buat visualisasi distribusi skor SUS"""
    
    # Set font untuk mendukung bahasa Indonesia
    plt.rcParams['font.family'] = 'DejaVu Sans'
    
    # Buat subplot
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    
    # Histogram
    ax1.hist(skor_sus, bins=10, edgecolor='black', alpha=0.7, color='skyblue')
    ax1.axvline(hasil['skor_rata_rata'], color='red', linestyle='--', 
                label=f'Rata-rata: {hasil["skor_rata_rata"]}')
    ax1.axvline(hasil['skor_median'], color='green', linestyle='--', 
                label=f'Median: {hasil["skor_median"]}')
    ax1.set_xlabel('Skor SUS')
    ax1.set_ylabel('Frekuensi')
    ax1.set_title('Distribusi Skor SUS')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Box plot
    ax2.boxplot(skor_sus, vert=True)
    ax2.set_ylabel('Skor SUS')
    ax2.set_title('Box Plot Skor SUS')
    ax2.grid(True, alpha=0.3)
    
    # Plot skor individu
    ax3.plot(range(1, len(skor_sus) + 1), skor_sus, 'o-', alpha=0.7)
    ax3.axhline(hasil['skor_rata_rata'], color='red', linestyle='--', 
                label=f'Rata-rata: {hasil["skor_rata_rata"]}')
    ax3.set_xlabel('Responden')
    ax3.set_ylabel('Skor SUS')
    ax3.set_title('Skor SUS Individual')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Grafik interpretasi skor
    rentang_skor = ['Buruk\n(0-49)', 'Marginal\n(50-69)', 'Baik\n(70-79)', 'Sangat Baik\n(80-100)']
    jumlah_rentang = [
        sum(1 for skor in skor_sus if skor < 50),
        sum(1 for skor in skor_sus if 50 <= skor < 70),
        sum(1 for skor in skor_sus if 70 <= skor < 80),
        sum(1 for skor in skor_sus if skor >= 80)
    ]
    
    warna = ['red', 'orange', 'lightgreen', 'green']
    ax4.bar(rentang_skor, jumlah_rentang, color=warna, alpha=0.7)
    ax4.set_ylabel('Jumlah Responden')
    ax4.set_title('Kategori Skor SUS')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def ekspor_hasil_ke_csv(df, skor_sus, hasil, nama_file='hasil_sus.csv'):
    """Ekspor hasil ke file CSV"""
    # Buat DataFrame baru dengan data asli plus skor SUS
    df_hasil = df.copy()
    df_hasil['Skor_SUS'] = skor_sus
    
    # Tambahkan interpretasi untuk setiap skor
    def dapatkan_interpretasi(skor):
        if skor >= 80:
            return "Sangat Baik"
        elif skor >= 70:
            return "Baik"
        elif skor >= 50:
            return "Cukup/Marginal"
        else:
            return "Buruk"
    
    df_hasil['Interpretasi_SUS'] = skor_sus.apply(dapatkan_interpretasi)
    
    # Simpan ke CSV
    df_hasil.to_csv(nama_file, index=False)
    print(f"Hasil diekspor ke {nama_file}")

# Contoh penggunaan dan fungsi utama
def main():
    """Fungsi utama untuk mendemonstrasikan perhitungan SUS"""
    
    # Contoh: Muat data dari file CSV
    # Ganti 'file_anda.csv' dengan path file yang sebenarnya
    try:
        # Coba muat dari file CSV
        df = pd.read_csv('data_sus.csv')  # Ganti dengan path file Anda
        print("Data berhasil dimuat dari file CSV.")
    except FileNotFoundError:
        # Buat data sampel jika file tidak ditemukan
        print("File CSV tidak ditemukan. Membuat data sampel...")
        
        # Data SUS sampel (10 pertanyaan, skala Likert 5 poin)
        np.random.seed(42)  # Untuk hasil yang dapat direproduksi
        data_sampel = {
            'Responden': [f'R{i+1:03d}' for i in range(20)],
        }
        
        # Generate respons sampel untuk 10 pertanyaan SUS
        for q in range(1, 11):
            if q % 2 == 1:  # Pertanyaan ganjil (pernyataan positif)
                data_sampel[f'P{q}'] = np.random.choice([3, 4, 5], size=20, p=[0.2, 0.5, 0.3])
            else:  # Pertanyaan genap (pernyataan negatif)
                data_sampel[f'P{q}'] = np.random.choice([1, 2, 3], size=20, p=[0.3, 0.5, 0.2])
        
        df = pd.DataFrame(data_sampel)
        print("Data sampel dibuat dengan 20 responden.")
    
    # Hitung skor SUS
    hasil, skor_sus = hitung_skor_sus(df)
    
    # Cetak hasil
    cetak_hasil_sus(hasil)
    
    # Buat visualisasi
    plot_distribusi_sus(skor_sus, hasil)
    
    # Ekspor hasil
    ekspor_hasil_ke_csv(df, skor_sus, hasil)
    
    return hasil, skor_sus

# Pertanyaan SUS standar untuk referensi
PERTANYAAN_SUS = [
    "P1: Saya pikir, saya akan sering menggunakan sistem ini.",
    "P2: Saya merasa sistem ini terlalu rumit untuk digunakan.",
    "P3: Saya rasa sistem ini mudah untuk digunakan.",
    "P4: Saya butuh bantuan dari orang teknis (ahli) untuk bisa menggunakan sistem ini.",
    "P5: Saya merasa berbagai fungsi dalam sistem ini terintegrasi dengan baik.",
    "P6: Saya rasa ada terlalu banyak hal yang tidak konsisten pada sistem ini.",
    "P7: Saya dapat membayangkan bahwa kebanyakan orang akan dapat mempelajari sistem ini dengan cepat.",
    "P8: Saya merasa sistem ini sangat berbelit-belit untuk digunakan.",
    "P9: Saya merasa tidak ada hambatan saat menggunakan sistem ini.",
    "P10: Saya perlu mempelajari banyak hal terlebih dahulu sebelum bisa menggunakan sistem ini."
]

if __name__ == "__main__":
    print("Kalkulator SUS (System Usability Scale)")
    print("Pertanyaan SUS Standar:")
    for pertanyaan in PERTANYAAN_SUS:
        print(f"  {pertanyaan}")
    print("\nCatatan: Respons menggunakan skala 5 poin (1=Sangat Tidak Setuju, 5=Sangat Setuju)")
    print("\n" + "="*80 + "\n")
    
    # Jalankan perhitungan utama
    hasil, skor_sus = main()