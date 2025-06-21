from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
import os

def buat_pdf_bahasa_indonesia():
    """BAHASA INDONESIA - untuk test RAG"""
    filename = "bahasa_indonesia.pdf"
    
    doc = SimpleDocTemplate(filename, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    # Judul
    title = Paragraph("PELAJARAN BAHASA INDONESIA", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 0.5*inch))
    
    # Konten
    content = [
        ("KELAS KATA", """
        Kelas kata adalah pengelompokan kata berdasarkan fungsi dan perannya dalam kalimat.
        
        Macam-macam kelas kata:
        
        1. KATA BENDA (NOMINA)
        Kata benda adalah kata yang menunjukkan nama orang, tempat, benda, atau hal.
        Contoh: meja, rumah, Jakarta, Budi, kebahagiaan, kecantikan
        
        2. KATA KERJA (VERBA)
        Kata kerja adalah kata yang menunjukkan perbuatan, tindakan, atau keadaan.
        Contoh: menulis, berlari, tidur, makan, berpikir
        
        3. KATA SIFAT (ADJEKTIVA)
        Kata sifat adalah kata yang menerangkan sifat atau keadaan orang, benda, atau hal.
        Contoh: cantik, besar, rajin, pintar, baik
        
        4. KATA KETERANGAN (ADVERBIA)
        Kata keterangan adalah kata yang memberikan keterangan pada kata kerja, kata sifat, atau kata keterangan lain.
        Contoh: sangat, agak, kemarin, di sana, dengan cepat
        """),
        
        ("KALIMAT", """
        Kalimat adalah satuan bahasa yang mengungkapkan pikiran yang utuh. Kalimat minimal terdiri dari subjek dan predikat.
        
        UNSUR-UNSUR KALIMAT:
        
        1. SUBJEK (S)
        Subjek adalah pelaku atau yang dibicarakan dalam kalimat.
        Contoh: "Ani membaca buku" - Ani adalah subjek
        
        2. PREDIKAT (P)
        Predikat adalah bagian kalimat yang menerangkan apa yang dilakukan atau dialami subjek.
        Contoh: "Ani membaca buku" - membaca adalah predikat
        
        3. OBJEK (O)
        Objek adalah bagian kalimat yang melengkapi predikat.
        Contoh: "Ani membaca buku" - buku adalah objek
        
        4. KETERANGAN (K)
        Keterangan adalah bagian kalimat yang memberikan informasi tambahan.
        Contoh: "Ani membaca buku di perpustakaan" - di perpustakaan adalah keterangan tempat
        """),
        
        ("PARAGRAF", """
        Paragraf adalah kumpulan kalimat yang saling berhubungan dan membahas satu pokok pikiran.
        
        STRUKTUR PARAGRAF:
        
        1. KALIMAT UTAMA
        Kalimat utama berisi ide pokok atau gagasan utama paragraf. Biasanya terletak di awal paragraf.
        
        2. KALIMAT PENJELAS
        Kalimat penjelas berisi penjelasan, rincian, atau contoh yang mendukung kalimat utama.
        
        JENIS-JENIS PARAGRAF:
        
        1. Paragraf Deduktif: kalimat utama di awal
        2. Paragraf Induktif: kalimat utama di akhir  
        3. Paragraf Campuran: kalimat utama di awal dan akhir
        
        CIRI-CIRI PARAGRAF YANG BAIK:
        • Kesatuan: semua kalimat membahas satu pokok pikiran
        • Kepaduan: ada hubungan logis antar kalimat
        • Kelengkapan: ide pokok dijelaskan dengan lengkap
        """),
        
        ("PUISI", """
        Puisi adalah karya sastra yang menggunakan bahasa yang padat, berima, dan berirama untuk mengungkapkan perasaan dan pikiran.
        
        UNSUR-UNSUR PUISI:
        
        1. TEMA
        Tema adalah pokok pikiran atau ide dasar puisi.
        Contoh tema: cinta, alam, kepahlawanan, persahabatan
        
        2. DIKSI
        Diksi adalah pilihan kata yang digunakan penyair.
        Kata-kata dipilih untuk menciptakan efek tertentu.
        
        3. RIMA
        Rima adalah persamaan bunyi pada akhir baris puisi.
        Contoh: 
        "Burung terbang tinggi di langit biru" (bunyi 'u')
        "Sayapnya mengepak rindu" (bunyi 'u')
        
        4. IRAMA
        Irama adalah pergantian tinggi rendah, panjang pendek, dan keras lembutnya bunyi.
        
        5. MAJAS
        Majas adalah gaya bahasa yang digunakan untuk memperindah puisi.
        Contoh: "Bulan adalah pelita malam" (majas metafora)
        """)
    ]
    
    for judul, isi in content:
        # Subjudul
        subtitle = Paragraph(judul, styles['Heading2'])
        story.append(subtitle)
        story.append(Spacer(1, 0.2*inch))
        
        # Isi
        paragraf = Paragraph(isi.replace("\n", "<br/>"), styles['Normal'])
        story.append(paragraf)
        story.append(Spacer(1, 0.3*inch))
    
    doc.build(story)
    print(f"✅ PDF '{filename}' berhasil dibuat!")
    return filename

def buat_pdf_matematika():
    """MATEMATIKA - untuk test RAG"""
    filename = "matematika.pdf"
    
    doc = SimpleDocTemplate(filename, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    # Judul
    title = Paragraph("MATEMATIKA", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 0.5*inch))
    
    content = [
        ("ALJABAR", """
        Aljabar adalah cabang matematika yang menggunakan huruf dan simbol untuk mewakili bilangan dalam persamaan dan rumus.
        
        VARIABEL DAN KONSTANTA:
        
        1. VARIABEL
        Variabel adalah huruf yang mewakili bilangan yang nilainya dapat berubah.
        Contoh: x, y, z, a, b
        
        2. KONSTANTA
        Konstanta adalah bilangan yang nilainya tetap.
        Contoh: 5, -3, π, e
        
        OPERASI ALJABAR:
        
        1. PENJUMLAHAN DAN PENGURANGAN
        • Suku sejenis dapat dijumlah atau dikurang
        • 3x + 5x = 8x
        • 7y - 2y = 5y
        • 4x + 3y tidak dapat disederhanakan (suku tidak sejenis)
        
        2. PERKALIAN
        • Perkalian variabel: x × x = x²
        • Perkalian koefisien: 3x × 4y = 12xy
        • Distributif: a(b + c) = ab + ac
        
        3. PEMBAGIAN
        • x⁶ ÷ x² = x⁴
        • 15x³ ÷ 3x = 5x²
        
        PERSAMAAN LINEAR:
        
        Persamaan linear adalah persamaan yang pangkat tertinggi variabelnya adalah 1.
        Bentuk umum: ax + b = c
        
        Contoh penyelesaian:
        2x + 5 = 13
        2x = 13 - 5
        2x = 8
        x = 4
        """),
        
        ("GEOMETRI", """
        Geometri adalah cabang matematika yang mempelajari bentuk, ukuran, posisi, dan sifat-sifat ruang.
        
        BANGUN DATAR:
        
        1. PERSEGI
        • Semua sisi sama panjang
        • Semua sudut 90°
        • Luas = s × s = s²
        • Keliling = 4s
        
        2. PERSEGI PANJANG
        • Sisi berhadapan sama panjang
        • Semua sudut 90°
        • Luas = p × l
        • Keliling = 2(p + l)
        
        3. SEGITIGA
        • Memiliki 3 sisi dan 3 sudut
        • Jumlah sudut = 180°
        • Luas = ½ × alas × tinggi
        • Keliling = a + b + c
        
        4. LINGKARAN
        • Semua titik berjarak sama dari pusat
        • Luas = πr²
        • Keliling = 2πr
        • Diameter = 2 × jari-jari
        
        BANGUN RUANG:
        
        1. KUBUS
        • Semua sisi berbentuk persegi
        • Volume = s³
        • Luas permukaan = 6s²
        
        2. BALOK
        • Memiliki 6 sisi berbentuk persegi panjang
        • Volume = p × l × t
        • Luas permukaan = 2(pl + pt + lt)
        
        3. TABUNG
        • Memiliki 2 lingkaran sebagai alas dan tutup
        • Volume = πr²t
        • Luas permukaan = 2πr(r + t)
        """),
        
        ("STATISTIKA", """
        Statistika adalah ilmu yang mempelajari cara mengumpulkan, mengolah, menganalisis, dan menyajikan data.
        
        JENIS DATA:
        
        1. DATA KUALITATIF
        Data yang berupa kategori atau kualitas.
        Contoh: warna, jenis kelamin, agama
        
        2. DATA KUANTITATIF
        Data yang berupa bilangan.
        Contoh: tinggi badan, berat badan, nilai ujian
        
        UKURAN PEMUSATAN DATA:
        
        1. MEAN (RATA-RATA)
        Mean = (jumlah semua data) ÷ (banyak data)
        Contoh: data 5, 7, 8, 6, 9
        Mean = (5+7+8+6+9) ÷ 5 = 35 ÷ 5 = 7
        
        2. MEDIAN (NILAI TENGAH)
        Nilai yang berada di tengah setelah data diurutkan.
        Contoh: data 5, 6, 7, 8, 9
        Median = 7
        
        3. MODUS
        Nilai yang paling sering muncul.
        Contoh: data 5, 6, 7, 6, 8, 6
        Modus = 6
        
        PENYAJIAN DATA:
        
        1. TABEL
        Menyajikan data dalam bentuk baris dan kolom
        
        2. DIAGRAM BATANG
        Menggunakan batang untuk menunjukkan frekuensi data
        
        3. DIAGRAM LINGKARAN
        Menggunakan lingkaran yang dibagi menjadi sektor-sektor
        
        4. HISTOGRAM
        Diagram batang untuk data berkelompok
        """),
        
        ("PELUANG", """
        Peluang adalah kemungkinan terjadinya suatu kejadian.
        
        RUANG SAMPEL DAN KEJADIAN:
        
        1. RUANG SAMPEL (S)
        Himpunan semua kemungkinan hasil dari suatu percobaan.
        Contoh: melempar dadu, S = {1, 2, 3, 4, 5, 6}
        
        2. KEJADIAN (A)
        Subset dari ruang sampel.
        Contoh: kejadian muncul bilangan genap = {2, 4, 6}
        
        RUMUS PELUANG:
        
        P(A) = n(A) / n(S)
        
        Dimana:
        • P(A) = peluang kejadian A
        • n(A) = banyak anggota kejadian A
        • n(S) = banyak anggota ruang sampel
        
        SIFAT-SIFAT PELUANG:
        
        1. 0 ≤ P(A) ≤ 1
        2. P(kejadian pasti) = 1
        3. P(kejadian mustahil) = 0
        4. P(A') = 1 - P(A), dimana A' adalah komplemen A
        
        CONTOH SOAL:
        
        Sebuah dadu dilempar sekali. Berapa peluang muncul bilangan prima?
        
        Penyelesaian:
        • S = {1, 2, 3, 4, 5, 6}, n(S) = 6
        • Bilangan prima = {2, 3, 5}, n(A) = 3
        • P(A) = 3/6 = 1/2 = 0,5
        
        PELUANG KEJADIAN MAJEMUK:
        
        1. PELUANG GABUNGAN
        P(A ∪ B) = P(A) + P(B) - P(A ∩ B)
        
        2. PELUANG IRISAN
        P(A ∩ B) = P(A) × P(B|A)
        """)
    ]
    
    for judul, isi in content:
        subtitle = Paragraph(judul, styles['Heading2'])
        story.append(subtitle)
        story.append(Spacer(1, 0.2*inch))
        
        paragraf = Paragraph(isi.replace("\n", "<br/>"), styles['Normal'])
        story.append(paragraf)
        story.append(Spacer(1, 0.3*inch))
    
    doc.build(story)
    print(f"✅ PDF '{filename}' berhasil dibuat!")
    return filename

def buat_pdf_ipa():
    """IPA (ILMU PENGETAHUAN ALAM) - untuk test RAG"""
    filename = "ipa.pdf"
    
    doc = SimpleDocTemplate(filename, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    # Judul
    title = Paragraph("ILMU PENGETAHUAN ALAM", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 0.5*inch))
    
    content = [
        ("FISIKA - GERAK", """
        Gerak adalah perubahan posisi suatu benda terhadap titik acuan dalam selang waktu tertentu.
        
        JENIS-JENIS GERAK:
        
        1. GERAK LURUS BERATURAN (GLB)
        • Kecepatan tetap (konstan)
        • Percepatan = 0
        • Rumus: s = v × t
        • Grafik v-t berupa garis lurus mendatar
        
        2. GERAK LURUS BERUBAH BERATURAN (GLBB)
        • Percepatan tetap (konstan)
        • Rumus: v = v₀ + at
        • Rumus: s = v₀t + ½at²
        • Rumus: v² = v₀² + 2as
        
        BESARAN DALAM GERAK:
        
        1. JARAK DAN PERPINDAHAN
        • Jarak: panjang lintasan yang ditempuh (skalar)
        • Perpindahan: perubahan posisi (vektor)
        
        2. KELAJUAN DAN KECEPATAN
        • Kelajuan: jarak dibagi waktu (skalar)
        • Kecepatan: perpindahan dibagi waktu (vektor)
        
        3. PERCEPATAN
        • Percepatan: perubahan kecepatan dibagi waktu
        • Rumus: a = (v - v₀) / t
        • Satuan: m/s²
        
        GERAK JATUH BEBAS:
        • Gerak GLBB dengan percepatan = g = 9,8 m/s²
        • Kecepatan awal = 0
        • Rumus: h = ½gt²
        • Rumus: v = gt
        """),
        
        ("KIMIA - ATOM DAN MOLEKUL", """
        Atom adalah partikel terkecil dari suatu unsur yang masih memiliki sifat unsur tersebut.
        
        STRUKTUR ATOM:
        
        1. INTI ATOM (NUKLEUS)
        • Terletak di pusat atom
        • Mengandung proton dan neutron
        • Bermuatan positif
        • Massa sangat besar dibanding elektron
        
        2. KULIT ELEKTRON
        • Elektron mengelilingi inti atom
        • Bermuatan negatif
        • Massa sangat kecil
        • Menentukan sifat kimia atom
        
        PARTIKEL PENYUSUN ATOM:
        
        1. PROTON
        • Bermuatan +1
        • Massa = 1 sma (satuan massa atom)
        • Menentukan nomor atom
        
        2. NEUTRON
        • Bermuatan netral (0)
        • Massa = 1 sma
        • Bersama proton membentuk inti atom
        
        3. ELEKTRON
        • Bermuatan -1
        • Massa = 1/1840 sma (sangat kecil)
        • Menentukan sifat kimia
        
        NOMOR ATOM DAN MASSA ATOM:
        
        • Nomor atom (Z) = jumlah proton
        • Nomor massa (A) = jumlah proton + neutron
        • Atom netral: jumlah proton = jumlah elektron
        
        MOLEKUL:
        
        Molekul adalah gabungan dua atau lebih atom yang terikat secara kimia.
        
        Contoh:
        • H₂O (air): 2 atom H + 1 atom O
        • CO₂ (karbon dioksida): 1 atom C + 2 atom O
        • NaCl (garam): 1 atom Na + 1 atom Cl
        
        IKATAN KIMIA:
        
        1. IKATAN IONIK
        • Terjadi antara logam dan non-logam
        • Transfer elektron
        • Contoh: NaCl, MgO
        
        2. IKATAN KOVALEN
        • Terjadi antara non-logam
        • Pemakaian bersama elektron
        • Contoh: H₂O, CO₂, CH₄
        """),
        
        ("BIOLOGI - SISTEM PENCERNAAN", """
        Sistem pencernaan adalah sistem organ yang berfungsi mencerna makanan menjadi zat-zat yang dapat diserap tubuh.
        
        PROSES PENCERNAAN:
        
        1. PENCERNAAN MEKANIK
        • Pemecahan makanan secara fisik
        • Terjadi di mulut (pengunyahan)
        • Terjadi di lambung (gerakan peristaltik)
        
        2. PENCERNAAN KIMIAWI
        • Pemecahan makanan oleh enzim
        • Mengubah molekul besar menjadi molekul kecil
        • Terjadi di mulut, lambung, dan usus halus
        
        ORGAN PENCERNAAN:
        
        1. MULUT
        • Gigi: memotong dan mengunyah
        • Lidah: membantu menelan
        • Kelenjar ludah: menghasilkan enzim amilase
        • Amilase: mencerna karbohidrat (amilum → maltosa)
        
        2. LAMBUNG
        • Menghasilkan asam lambung (HCl)
        • Menghasilkan enzim pepsin
        • Pepsin: mencerna protein
        • Membunuh bakteri berbahaya
        
        3. USUS HALUS
        • Duodenum: pencernaan utama
        • Jejunum dan ileum: penyerapan
        • Menghasilkan berbagai enzim pencernaan
        • Memiliki vili untuk memperluas permukaan
        
        4. USUS BESAR
        • Menyerap air dan mineral
        • Membentuk feses
        • Mengandung bakteri menguntungkan
        
        KELENJAR PENCERNAAN:
        
        1. HATI
        • Menghasilkan empedu
        • Empedu: mengemulsikan lemak
        • Detoksifikasi racun
        • Menyimpan glikogen
        
        2. PANKREAS
        • Menghasilkan enzim lipase, tripsin, kimotripsin
        • Lipase: mencerna lemak
        • Tripsin dan kimotripsin: mencerna protein
        • Menghasilkan hormon insulin
        """),
        
        ("EKOLOGI", """
        Ekologi adalah ilmu yang mempelajari hubungan antara makhluk hidup dengan lingkungannya.
        
        KOMPONEN EKOSISTEM:
        
        1. KOMPONEN BIOTIK
        Semua makhluk hidup dalam ekosistem.
        
        • PRODUSEN (AUTOTROF)
        - Membuat makanan sendiri melalui fotosintesis
        - Contoh: tumbuhan hijau, alga
        
        • KONSUMEN (HETEROTROF)
        - Konsumen I: herbivora (pemakan tumbuhan)
        - Konsumen II: karnivora (pemakan daging)
        - Konsumen III: karnivora tingkat tinggi
        
        • PENGURAI (DEKOMPOSER)
        - Menguraikan organisme mati
        - Contoh: bakteri, jamur
        
        2. KOMPONEN ABIOTIK
        Semua benda mati dalam ekosistem.
        Contoh: air, udara, tanah, suhu, cahaya
        
        ALIRAN ENERGI:
        
        Matahari → Produsen → Konsumen I → Konsumen II → Konsumen III
        
        • Energi mengalir satu arah
        • Setiap perpindahan, energi berkurang
        • Piramida energi: semakin ke atas semakin kecil
        
        RANTAI MAKANAN DAN JARING MAKANAN:
        
        1. RANTAI MAKANAN
        Aliran makanan dari satu organisme ke organisme lain.
        Contoh: Rumput → Kelinci → Ular → Elang
        
        2. JARING MAKANAN
        Kumpulan rantai makanan yang saling berhubungan.
        
        SIKLUS MATERI:
        
        1. SIKLUS AIR
        Evaporasi → Kondensasi → Presipitasi → Infiltrasi
        
        2. SIKLUS KARBON
        CO₂ di atmosfer → Fotosintesis → Respirasi → CO₂
        
        3. SIKLUS NITROGEN
        Fiksasi nitrogen → Nitrifikasi → Denitrifikasi
        
        KESEIMBANGAN EKOSISTEM:
        
        • Populasi organisme saling mempengaruhi
        • Predator mengontrol populasi prey
        • Gangguan dapat merusak keseimbangan
        • Contoh: peningkatan populasi tikus karena berkurangnya ular
        """)
    ]
    
    for judul, isi in content:
        subtitle = Paragraph(judul, styles['Heading2'])
        story.append(subtitle)
        story.append(Spacer(1, 0.2*inch))
        
        paragraf = Paragraph(isi.replace("\n", "<br/>"), styles['Normal'])
        story.append(paragraf)
        story.append(Spacer(1, 0.3*inch))
    
    doc.build(story)
    print(f"✅ PDF '{filename}' berhasil dibuat!")
    return filename

def buat_pdf_komputer():
    """KOMPUTER - untuk test RAG"""
    filename = "komputer.pdf"
    
    doc = SimpleDocTemplate(filename, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    # Judul
    title = Paragraph("ILMU KOMPUTER", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 0.5*inch))
    
    content = [
        ("ALGORITMA DAN PEMROGRAMAN", """
        Algoritma adalah langkah-langkah sistematis untuk menyelesaikan suatu masalah.
        
        KARAKTERISTIK ALGORITMA:
        
        1. INPUT
        • Memiliki 0 atau lebih masukan
        • Data yang diperlukan untuk memproses
        
        2. OUTPUT
        • Memiliki 1 atau lebih keluaran
        • Hasil dari pemrosesan input
        
        3. DEFINITENESS (JELAS)
        • Setiap langkah harus jelas dan tidak ambigu
        • Dapat dipahami dengan tepat
        
        4. FINITENESS (TERBATAS)
        • Algoritma harus berakhir setelah menjalankan sejumlah langkah
        • Tidak boleh infinite loop
        
        5. EFFECTIVENESS (EFEKTIF)
        • Setiap langkah harus dapat dilaksanakan
        • Menggunakan sumber daya yang wajar
        
        STRUKTUR KONTROL:
        
        1. SEQUENCE (BERURUTAN)
        Langkah-langkah dilakukan secara berurutan.
        Contoh:
        1. Baca nilai A
        2. Baca nilai B  
        3. Hitung C = A + B
        4. Tampilkan C
        
        2. SELECTION (PERCABANGAN)
        Pemilihan langkah berdasarkan kondisi.
        
        • IF-THEN
        Jika kondisi benar, jalankan aksi
        
        • IF-THEN-ELSE
        Jika kondisi benar jalankan aksi1, selain itu jalankan aksi2
        
        3. ITERATION (PERULANGAN)
        Mengulang langkah-langkah tertentu.
        
        • FOR: perulangan dengan jumlah tertentu
        • WHILE: perulangan selama kondisi benar
        • REPEAT-UNTIL: perulangan sampai kondisi benar
        
        FLOWCHART:
        
        Diagram alir yang menggambarkan langkah-langkah algoritma.
        
        Simbol-simbol:
        • Oval: Start/End
        • Persegi panjang: Proses
        • Belah ketupat: Keputusan
        • Jajar genjang: Input/Output
        • Lingkaran: Konektor
        """),
        
        ("STRUKTUR DATA", """
        Struktur data adalah cara mengorganisasi dan menyimpan data agar dapat digunakan secara efisien.
        
        ARRAY (LARIK):
        
        • Kumpulan elemen dengan tipe data sama
        • Elemen diakses menggunakan indeks
        • Ukuran tetap (static)
        • Contoh: A[1], A[2], A[3], ..., A[n]
        
        Operasi pada Array:
        1. Traversal: mengunjungi setiap elemen
        2. Search: mencari elemen tertentu
        3. Insert: menambah elemen
        4. Delete: menghapus elemen
        5. Sort: mengurutkan elemen
        
        LINKED LIST:
        
        • Kumpulan node yang saling terhubung
        • Setiap node berisi data dan pointer ke node berikutnya
        • Ukuran dinamis
        • Tidak memerlukan memori yang berurutan
        
        Jenis Linked List:
        1. Single Linked List: pointer ke node berikutnya
        2. Double Linked List: pointer ke node sebelum dan sesudah
        3. Circular Linked List: node terakhir menunjuk ke node pertama
        
        STACK (TUMPUKAN):
        
        • Struktur data LIFO (Last In First Out)
        • Elemen terakhir yang masuk, pertama yang keluar
        • Operasi utama: PUSH (menambah) dan POP (mengambil)
        
        Aplikasi Stack:
        • Function call management
        • Undo operation
        • Expression evaluation
        • Browser history
        
        QUEUE (ANTRIAN):
        
        • Struktur data FIFO (First In First Out)
        • Elemen pertama yang masuk, pertama yang keluar
        • Operasi utama: ENQUEUE (menambah) dan DEQUEUE (mengambil)
        
        Aplikasi Queue:
        • Process scheduling
        • Printer queue
        • Breadth-first search
        • Buffer untuk data stream
        """),
        
        ("DATABASE", """
        Database adalah kumpulan data yang terorganisir dan dapat diakses secara elektronik.
        
        KONSEP DATABASE:
        
        1. DATA
        • Fakta mentah yang belum diolah
        • Contoh: nama, alamat, tanggal lahir
        
        2. INFORMASI
        • Data yang sudah diolah menjadi berguna
        • Contoh: laporan penjualan, daftar nilai siswa
        
        3. DATABASE MANAGEMENT SYSTEM (DBMS)
        • Software untuk mengelola database
        • Contoh: MySQL, PostgreSQL, Oracle, SQL Server
        
        MODEL RELASIONAL:
        
        • Data disimpan dalam tabel-tabel yang saling berhubungan.
        • TABEL: Terdiri dari baris (record) dan kolom (field).
        • PRIMARY KEY: Kolom unik yang mengidentifikasi setiap baris.
        • FOREIGN KEY: Kunci dari satu tabel yang merujuk ke Primary Key di tabel lain untuk membangun relasi.
        
        SQL (STRUCTURED QUERY LANGUAGE):
        
        • Bahasa standar untuk berinteraksi dengan database relasional.
        • Perintah utama: SELECT (mengambil data), INSERT (menyisipkan data), UPDATE (memperbarui data), DELETE (menghapus data).
        """),

        ("JARINGAN KOMPUTER", """
        Jaringan komputer adalah dua atau lebih komputer yang terhubung untuk berbagi sumber daya dan data.
        
        JENIS-JENIS JARINGAN:
        
        1. LAN (Local Area Network)
        • Mencakup area geografis kecil (gedung, sekolah).
        
        2. MAN (Metropolitan Area Network)
        • Mencakup area yang lebih besar seperti kota.
        
        3. WAN (Wide Area Network)
        • Mencakup area geografis yang sangat luas (negara, benua), contohnya adalah Internet.
        
        TOPOLOGI JARINGAN:
        
        • Cara komputer terhubung dalam jaringan.
        • Contoh: Bus, Star, Ring, Mesh.
        
        PROTOKOL JARINGAN:
        
        • Aturan yang mengatur komunikasi data.
        • TCP/IP (Transmission Control Protocol/Internet Protocol) adalah protokol utama di Internet.
        • HTTP (Hypertext Transfer Protocol): untuk web.
        • FTP (File Transfer Protocol): untuk transfer file.
        """)
    ]
    
    for judul, isi in content:
        subtitle = Paragraph(judul, styles['Heading2'])
        story.append(subtitle)
        story.append(Spacer(1, 0.2*inch))
        
        # Ganti newline dengan tag <br/> agar baris baru berfungsi di ReportLab
        paragraf = Paragraph(isi.replace("\n", "<br/>"), styles['Normal'])
        story.append(paragraf)
        story.append(Spacer(1, 0.3*inch))
    
    doc.build(story)
    print(f"✅ PDF '{filename}' berhasil dibuat!")
    return filename

# --- BAGIAN UTAMA UNTUK MENJALANKAN SEMUA FUNGSI ---
if __name__ == "__main__":
    print("Memulai proses pembuatan PDF...")
    
    # Membuat semua file PDF
    buat_pdf_bahasa_indonesia()
    buat_pdf_matematika()
    buat_pdf_ipa()
    buat_pdf_komputer()
    
    print("\nSemua file PDF telah berhasil dibuat.")