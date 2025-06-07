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
        paragraf = Paragraph(isi, styles['Normal'])
        story.append(paragraf)
        story.append(Spacer(1, 0.3*inch))
    
    doc.build(story)
    print(f"✅ PDF '{filename}' berhasil dibuat!")
    return filename

def buat_pdf_sejarah():
    """SEJARAH INDONESIA - untuk test RAG"""
    filename = "sejarah_indonesia.pdf"
    
    doc = SimpleDocTemplate(filename, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    # Judul
    title = Paragraph("SEJARAH INDONESIA", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 0.5*inch))
    
    content = [
        ("MASA PRASEJARAH", """
        Masa prasejarah adalah masa ketika manusia belum mengenal tulisan. Di Indonesia, masa ini dibagi menjadi beberapa zaman.
        
        ZAMAN BATU:
        
        1. ZAMAN BATU TUA (PALEOLITIKUM)
        Manusia hidup dengan berburu dan mengumpulkan makanan. Alat-alat masih sangat sederhana.
        Contoh: kapak perimbas, kapak genggam
        Manusia purba: Pithecanthropus erectus (Homo erectus)
        
        2. ZAMAN BATU TENGAH (MESOLITIKUM)
        Manusia mulai menetap dan membuat alat dari tulang dan tanduk.
        Contoh: pebble tools, bone tools
        Kebudayaan: Kjokkenmoddinger (sampah dapur)
        
        3. ZAMAN BATU MUDA (NEOLITIKUM)
        Manusia sudah bercocok tanam dan membuat tembikar.
        Contoh: kapak persegi, kapak lonjong
        Kebudayaan: megalitikum (bangunan batu besar)
        
        4. ZAMAN LOGAM
        Manusia mengenal logam seperti perunggu dan besi.
        Contoh: nekara, perhiasan perunggu
        """),
        
        ("KERAJAAN HINDU-BUDDHA", """
        Kerajaan Hindu-Buddha berkembang di Indonesia sekitar abad ke-4 hingga ke-15 Masehi.
        
        KERAJAAN KUTAI (400-1635 M)
        • Kerajaan Hindu tertua di Indonesia
        • Terletak di Kalimantan Timur
        • Raja terkenal: Mulawarman
        • Bukti: Prasasti Yupa (dalam bahasa Sanskerta)
        
        KERAJAAN TARUMANAGARA (358-669 M)
        • Terletak di Jawa Barat
        • Raja terkenal: Purnawarman
        • Bukti: Prasasti Tugu, Prasasti Kebon Kopi
        
        KERAJAAN SRIWIJAYA (671-1377 M)
        • Kerajaan maritim di Sumatera Selatan
        • Pusat perdagangan dan penyebaran agama Buddha
        • Raja terkenal: Balaputradewa
        • Bukti: Prasasti Kedukan Bukit, Prasasti Talang Tuwo
        
        KERAJAAN MAJAPAHIT (1293-1527 M)
        • Kerajaan Hindu terbesar di Nusantara
        • Terletak di Jawa Timur
        • Raja terkenal: Hayam Wuruk
        • Mahapatih terkenal: Gajah Mada
        • Bukti: Kitab Negarakertagama, Kitab Pararaton
        """),
        
        ("KERAJAAN ISLAM", """
        Kerajaan Islam mulai berkembang di Indonesia pada abad ke-13 dan mencapai puncaknya pada abad ke-16-17.
        
        KERAJAAN SAMUDRA PASAI (1267-1521 M)
        • Kerajaan Islam pertama di Indonesia
        • Terletak di Aceh
        • Raja pertama: Marah Silu (Sultan Malik as-Saleh)
        
        KESULTANAN DEMAK (1475-1554 M)
        • Kerajaan Islam pertama di Jawa
        • Pendiri: Raden Patah
        • Berperan dalam penyebaran Islam di Jawa
        
        KESULTANAN MATARAM (1587-1755 M)
        • Kerajaan Islam terbesar di Jawa
        • Pendiri: Panembahan Senopati
        • Sultan terkenal: Sultan Agung Hanyokrokusumo
        • Menyerang VOC di Batavia (1628-1629)
        
        KESULTANAN ACEH (1496-1903 M)
        • Kerajaan Islam di ujung barat Indonesia
        • Sultan terkenal: Sultan Iskandar Muda
        • Menguasai perdagangan di Selat Malaka
        • Melawan kolonialisme Belanda dan Portugis
        """),
        
        ("MASA KOLONIAL", """
        Masa kolonial dimulai dengan kedatangan bangsa Eropa ke Indonesia pada abad ke-16.
        
        KEDATANGAN PORTUGIS (1512)
        • Dipimpin oleh Alfonso de Albuquerque
        • Menguasai Malaka dan Kepulauan Maluku
        • Tujuan: mencari rempah-rempah (Gold, Glory, Gospel)
        
        KEDATANGAN BELANDA (1596)
        • Dipimpin oleh Cornelis de Houtman
        • Membentuk VOC (Vereenigde Oostindische Compagnie) tahun 1602
        • Monopoli perdagangan rempah-rempah
        • Sistem tanam paksa (cultuurstelsel) oleh Johannes van den Bosch
        
        PERLAWANAN RAKYAT:
        
        1. Perang Diponegoro (1825-1830)
        • Dipimpin oleh Pangeran Diponegoro
        • Latar belakang: politik, ekonomi, dan agama
        • Berakhir dengan penangkapan Diponegoro
        
        2. Perang Padri (1821-1837)
        • Terjadi di Sumatera Barat
        • Dipimpin oleh Imam Bonjol, Tuanku Nan Renceh
        • Konflik antara kaum Padri dan kaum Adat
        
        3. Perang Aceh (1873-1904)
        • Perlawanan terlama terhadap Belanda
        • Dipimpin oleh Teuku Umar, Cut Nyak Dhien, Teuku Cik Ditiro
        • Menggunakan taktik perang gerilya
        """)
    ]
    
    for judul, isi in content:
        subtitle = Paragraph(judul, styles['Heading2'])
        story.append(subtitle)
        story.append(Spacer(1, 0.2*inch))
        
        paragraf = Paragraph(isi, styles['Normal'])
        story.append(paragraf)
        story.append(Spacer(1, 0.3*inch))
    
    doc.build(story)
    print(f"✅ PDF '{filename}' berhasil dibuat!")
    return filename

def buat_pdf_biologi():
    """BIOLOGI - untuk test RAG"""
    filename = "biologi.pdf"
    
    doc = SimpleDocTemplate(filename, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    # Judul
    title = Paragraph("BIOLOGI", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 0.5*inch))
    
    content = [
        ("SEL", """
        Sel adalah unit struktural dan fungsional terkecil dari makhluk hidup. Semua makhluk hidup tersusun atas sel.
        
        TEORI SEL:
        1. Sel adalah unit struktural terkecil makhluk hidup
        2. Sel adalah unit fungsional terkecil makhluk hidup  
        3. Sel berasal dari sel sebelumnya (omnis cellula e cellula)
        
        JENIS-JENIS SEL:
        
        1. SEL PROKARIOTIK
        • Tidak memiliki inti sel yang jelas (tidak bermembran)
        • Materi genetik tersebar di sitoplasma
        • Contoh: bakteri, archaea
        • Organisme: Escherichia coli, Streptococcus
        
        2. SEL EUKARIOTIK
        • Memiliki inti sel yang jelas (bermembran)
        • Materi genetik berada dalam inti sel
        • Memiliki berbagai organel bermembran
        • Contoh: sel tumbuhan, sel hewan, sel jamur
        
        ORGANEL SEL:
        
        1. INTI SEL (NUKLEUS)
        • Mengatur seluruh aktivitas sel
        • Mengandung DNA dan RNA
        • Tempat replikasi DNA dan transkripsi
        
        2. MITOKONDRIA
        • Penghasil energi (ATP) sel
        • Disebut "rumah tenaga" sel
        • Memiliki DNA sendiri
        
        3. RIBOSOM
        • Tempat sintesis protein
        • Terdapat di sitoplasma dan retikulum endoplasma
        
        4. RETIKULUM ENDOPLASMA (RE)
        • RE kasar: memiliki ribosom, sintesis protein
        • RE halus: tidak memiliki ribosom, sintesis lipid
        """),
        
        ("SISTEM PENCERNAAN", """
        Sistem pencernaan adalah sistem organ yang berfungsi menerima makanan, mencerna, menyerap sari makanan, dan mengeluarkan sisa makanan.
        
        ORGAN PENCERNAAN:
        
        1. MULUT
        • Tempat masuknya makanan
        • Terjadi pencernaan mekanik (pengunyahan) dan kimiawi (enzim amilase)
        • Gigi: memotong dan mengunyah makanan
        • Lidah: membantu menelan dan merasakan
        
        2. KERONGKONGAN (ESOFAGUS)
        • Menyalurkan makanan dari mulut ke lambung
        • Panjang sekitar 25 cm
        • Terjadi gerakan peristaltik
        
        3. LAMBUNG
        • Menyimpan makanan sementara
        • Mencerna protein dengan enzim pepsin
        • Menghasilkan asam lambung (HCl)
        • Membunuh bakteri berbahaya
        
        4. USUS HALUS
        • Terdiri dari duodenum, jejunum, ileum
        • Tempat penyerapan sari makanan utama
        • Panjang sekitar 6-7 meter
        • Memiliki vili dan mikrovili untuk memperluas permukaan
        
        5. USUS BESAR
        • Menyerap air dan elektrolit
        • Membentuk feses
        • Mengandung bakteri baik (flora normal)
        
        KELENJAR PENCERNAAN:
        
        1. HATI
        • Menghasilkan empedu untuk mencerna lemak
        • Menetralkan racun (detoksifikasi)
        • Menyimpan glikogen
        
        2. PANKREAS
        • Menghasilkan enzim pencernaan
        • Menghasilkan hormon insulin dan glukagon
        • Mengatur kadar gula darah
        """),
        
        ("SISTEM PERNAPASAN", """
        Sistem pernapasan adalah sistem organ yang berfungsi untuk pertukaran gas (oksigen dan karbon dioksida) antara tubuh dengan lingkungan.
        
        ORGAN PERNAPASAN:
        
        1. HIDUNG
        • Jalan masuk udara
        • Menyaring, menghangatkan, dan melembabkan udara
        • Memiliki bulu hidung dan lendir
        
        2. FARING
        • Persimpangan saluran pernapasan dan pencernaan
        • Tempat bertemunya udara dan makanan
        
        3. LARING
        • Kotak suara
        • Mengandung pita suara untuk menghasilkan suara
        • Memiliki epiglotis untuk menutup saat menelan
        
        4. TRAKEA
        • Batang tenggorokan
        • Panjang sekitar 12 cm
        • Diperkuat oleh cincin tulang rawan
        
        5. BRONKUS
        • Percabangan trakea
        • Bronkus kanan dan kiri masuk ke paru-paru
        
        6. BRONKIOLUS
        • Percabangan bronkus yang lebih kecil
        • Menuju ke alveolus
        
        7. ALVEOLUS
        • Kantong udara kecil di ujung bronkiolus
        • Tempat pertukaran gas
        • Dikelilingi kapiler darah
        • Jumlah sekitar 300 juta di kedua paru-paru
        
        MEKANISME PERNAPASAN:
        
        1. INSPIRASI (menghirup)
        • Diafragma berkontraksi dan turun
        • Otot antar tulang rusuk berkontraksi
        • Rongga dada membesar
        • Udara masuk ke paru-paru
        
        2. EKSPIRASI (menghembuskan)
        • Diafragma relaksasi dan naik
        • Otot antar tulang rusuk relaksasi
        • Rongga dada mengecil
        • Udara keluar dari paru-paru
        """),
        
        ("SISTEM PEREDARAN DARAH", """
        Sistem peredaran darah adalah sistem organ yang berfungsi mengedarkan darah ke seluruh tubuh untuk mengangkut oksigen, nutrisi, dan zat-zat penting lainnya.
        
        KOMPONEN DARAH:
        
        1. PLASMA DARAH
        • Bagian cair darah (55% dari volume darah)
        • Mengandung air, protein, glukosa, dan zat terlarut lainnya
        • Mengangkut zat-zat makanan dan sisa metabolisme
        
        2. SEL DARAH MERAH (ERITROSIT)
        • Mengangkut oksigen dan karbon dioksida
        • Mengandung hemoglobin
        • Berbentuk cakram bikonkaf
        • Jumlah: 4-5 juta per mm³ darah
        
        3. SEL DARAH PUTIH (LEUKOSIT)
        • Sistem pertahanan tubuh
        • Melawan infeksi dan penyakit
        • Jumlah: 4.000-11.000 per mm³ darah
        • Jenis: neutrofil, limfosit, monosit, eosinofil, basofil
        
        4. KEPING DARAH (TROMBOSIT)
        • Berperan dalam pembekuan darah
        • Mencegah pendarahan berlebihan
        • Jumlah: 150.000-450.000 per mm³ darah
        
        ORGAN PEREDARAN DARAH:
        
        1. JANTUNG
        • Pompa darah
        • Memiliki 4 ruang: 2 atrium dan 2 ventrikel
        • Atrium kanan: menerima darah kotor
        • Ventrikel kanan: memompa darah ke paru-paru
        • Atrium kiri: menerima darah bersih dari paru-paru
        • Ventrikel kiri: memompa darah ke seluruh tubuh
        
        2. PEMBULUH DARAH
        • Arteri: membawa darah dari jantung
        • Vena: membawa darah ke jantung
        • Kapiler: tempat pertukaran zat
        
        PEREDARAN DARAH:
        
        1. PEREDARAN DARAH KECIL (PULMONAL)
        Jantung → Paru-paru → Jantung
        
        2. PEREDARAN DARAH BESAR (SISTEMIK)
        Jantung → Seluruh tubuh → Jantung
        """)
    ]
    
    for judul, isi in content:
        subtitle = Paragraph(judul, styles['Heading2'])
        story.append(subtitle)
        story.append(Spacer(1, 0.2*inch))
        
        paragraf = Paragraph(isi, styles['Normal'])
        story.append(paragraf)
        story.append(Spacer(1, 0.3*inch))
    
    doc.build(story)
    print(f"✅ PDF '{filename}' berhasil dibuat!")
    return filename

def buat_semua_pdf():
    """Membuat semua PDF untuk testing"""
    print("🔧 Membuat 3 PDF mata pelajaran untuk testing...")
    
    try:
        pdf_files = []
        
        # Buat PDF Bahasa Indonesia
        print("\n📝 Membuat PDF Bahasa Indonesia...")
        pdf1 = buat_pdf_bahasa_indonesia()
        pdf_files.append(pdf1)
        
        # Buat PDF Sejarah
        print("\n📜 Membuat PDF Sejarah Indonesia...")
        pdf2 = buat_pdf_sejarah()
        pdf_files.append(pdf2)
        
        # Buat PDF Biologi
        print("\n🧬 Membuat PDF Biologi...")
        pdf3 = buat_pdf_biologi()
        pdf_files.append(pdf3)
        
        print(f"\n📚 BERHASIL! Total {len(pdf_files)} PDF telah dibuat:")
        for i, pdf in enumerate(pdf_files, 1):
            print(f"   {i}. {pdf}")
            
        print("\n💡 Cara menggunakan:")
        print("1. Pindahkan semua PDF ke folder DATA_PATH")
        print("2. Jalankan process_documents() untuk setiap PDF")
        print("3. Gunakan query_rag() untuk generate pertanyaan-jawaban")
        print("\n🎯 Cocok untuk testing RAG dengan 3 domain pengetahuan berbeda!")
        
        return pdf_files
        
    except Exception as e:
        print(f"❌ Error membuat PDF: {str(e)}")
        print("💡 Pastikan reportlab sudah terinstall: pip install reportlab")
        return []

if __name__ == "__main__":
    buat_semua_pdf()