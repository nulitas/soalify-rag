"""
Generator PDF Lengkap untuk Materi Bahasa Indonesia Sekolah Dasar (SD)
Menggabungkan materi kelas 1-6, tata bahasa, dan kosakata
menjadi satu dokumen yang komprehensif.
"""

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor

def buat_pdf_rangkuman_lengkap():
    """
    Membuat satu PDF yang berisi rangkuman lengkap materi Bahasa Indonesia SD,
    mencakup semua kelas, tata bahasa, dan kosakata.
    """
    filename = "rangkuman_lengkap_bahasa_indonesia_sd.pdf"
    
    # Inisialisasi dokumen dengan margin
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=inch/2,
        leftMargin=inch/2,
        topMargin=inch/2,
        bottomMargin=inch/2
    )
    
    story = []
    styles = getSampleStyleSheet()
    
    # Kustomisasi style untuk judul utama dan subjudul
    styles['Title'].fontSize = 24
    styles['Title'].leading = 28
    styles['Heading1'].fontSize = 18
    styles['Heading1'].textColor = HexColor('#1E3A8A') # Biru tua
    styles['Heading2'].fontSize = 14
    styles['Heading2'].textColor = HexColor('#1D4ED8') # Biru
    styles['Heading3'].fontSize = 12
    styles['Heading3'].fontName = 'Helvetica-Bold'

    # --- HALAMAN JUDUL ---
    title = Paragraph("Rangkuman Lengkap<br/>Bahasa Indonesia<br/>Sekolah Dasar (Kelas 1-6)", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 1.5 * inch))
    
    author = Paragraph("Disusun untuk mempermudah proses belajar dan mengajar.", styles['Normal'])
    story.append(author)
    story.append(PageBreak())

    # --- BAGIAN 1: MATERI PEMBELAJARAN PER KELAS ---
    main_title_1 = Paragraph("BAGIAN 1: MATERI PEMBELAJARAN", styles['Heading1'])
    story.append(main_title_1)
    story.append(Spacer(1, 0.3 * inch))

    materi_per_kelas = [
        ("KELAS 1: MENGENAL HURUF & KATA", """
        <b>HURUF VOKAL:</b> A, I, U, E, O (Contoh: Aku, Ibu, Ular, Elang, Orang)<br/>
        <b>HURUF KONSONAN:</b> B, C, D, F, G, H, J, K, L, M, N, P, Q, R, S, T, V, W, X, Y, Z (Contoh: Buku, Cinta, Dadu)<br/>
        <b>SUKU KATA:</b> Penggabungan huruf menjadi suku kata (Contoh: BA-PA → Bapa, MA-MA → Mama, A-DI-K → Adik)<br/>
        <b>KATA SEDERHANA:</b> Kata-kata dasar terkait keluarga, binatang, buah, dan warna.<br/>
        <b>KALIMAT SEDERHANA:</b> Kalimat pendek dengan subjek dan predikat (Contoh: Aku suka makan. Ayah pergi kerja.)
        """),
        ("KELAS 2: MEMBACA & MENULIS", """
        <b>MEMBACA LANCAR:</b> Membaca kata dengan suku kata banyak dan lafal yang tepat.<br/>
        <b>MENULIS TEGAK BERSAMBUNG:</b> Latihan menulis rapi dengan huruf kapital dan kecil.<br/>
        <b>KALIMAT TANYA:</b> Menggunakan kata tanya Apa, Siapa, Di mana, Kapan, Mengapa, Bagaimana.<br/>
        <b>DONGENG SEDERHANA:</b> Memahami isi cerita dan pesan moral dari dongeng seperti "Kancil dan Buaya".<br/>
        <b>PUISI ANAK:</b> Belajar membaca puisi sederhana dengan ekspresi yang sesuai.
        """),
        ("KELAS 3: KOSAKATA & KALIMAT", """
        <b>KOSAKATA BARU:</b> Mengenal sinonim (persamaan kata) dan antonim (lawan kata).<br/>
        <b>JENIS KATA:</b> Membedakan kata benda (meja), kata kerja (makan), dan kata sifat (baik).<br/>
        <b>UNSUR KALIMAT (SPOK):</b> Memahami Subjek, Predikat, Objek, dan Keterangan. (Contoh: Ani (S) membaca (P) buku (O) di perpustakaan (K)).<br/>
        <b>JENIS KALIMAT:</b> Mengenal kalimat berita, tanya, perintah, dan seru.<br/>
        <b>PANTUN ANAK:</b> Memahami struktur pantun (sampiran dan isi).
        """),
        ("KELAS 4: PARAGRAF & KARANGAN", """
        <b>PARAGRAF:</b> Menentukan kalimat utama dan kalimat penjelas dalam sebuah paragraf.<br/>
        <b>KARANGAN SEDERHANA:</b> Menulis karangan deskripsi (menggambarkan) dan narasi (menceritakan).<br/>
        <b>SURAT PRIBADI:</b> Mempelajari bagian-bagian surat dan cara menulis surat untuk teman atau keluarga.<br/>
        <b>TEKS PETUNJUK:</b> Memahami dan membuat teks petunjuk penggunaan sesuatu.<br/>
        <b>KAMUS KECIL:</b> Menggunakan kamus untuk mencari arti kata, termasuk kata berimbuhan dan kata majemuk.
        """),
        ("KELAS 5: WACANA & TEKS", """
        <b>JENIS TEKS:</b> Membedakan berbagai jenis teks seperti cerita, informasi, prosedur, deskripsi, dan eksplanasi.<br/>
        <b>UNSUR INTRINSIK CERITA:</b> Menganalisis tema, tokoh, alur, latar, dan amanat dalam sebuah cerita.<br/>
        <b>PUISI DAN PANTUN:</b> Mempelajari rima, irama, dan jenis-jenis puisi serta pantun.<br/>
        <b>DRAMA SEDERHANA:</b> Mengenal naskah drama, dialog, dan bermain peran.<br/>
        <b>LAPORAN SEDERHANA:</b> Menulis laporan pengamatan atau kegiatan secara objektif dan faktual.
        """),
        ("KELAS 6: SASTRA & BAHASA", """
        <b>KARYA SASTRA INDONESIA:</b> Mengenal cerita rakyat, legenda, mitos, dan hikayat dari berbagai daerah.<br/>
        <b>ANALISIS PUISI:</b> Memahami majas (personifikasi, metafora), diksi (pilihan kata), dan tema puisi.<br/>
        <b>TEKS NONFIKSI:</b> Membedakan fakta dan opini dalam teks seperti biografi, artikel, dan editorial.<br/>
        <b>PIDATO:</b> Mempelajari struktur pidato (pembukaan, isi, penutup) dan teknik berpidato.<br/>
        <b>TATA BAHASA LANJUTAN:</b> Menggunakan kalimat efektif, Ejaan Yang Disempurnakan (EYD), dan tanda baca dengan benar.
        """)
    ]
    
    for judul, isi in materi_per_kelas:
        story.append(Paragraph(judul, styles['Heading2']))
        story.append(Spacer(1, 0.1 * inch))
        story.append(Paragraph(isi, styles['Normal']))
        story.append(Spacer(1, 0.2 * inch))

    story.append(PageBreak())

    # --- BAGIAN 2: TATA BAHASA ---
    main_title_2 = Paragraph("BAGIAN 2: POKOK-POKOK TATA BAHASA", styles['Heading1'])
    story.append(main_title_2)
    story.append(Spacer(1, 0.3 * inch))

    tata_bahasa = [
        ("JENIS KATA (KELAS KATA)", """
        <b>1. KATA BENDA (NOMINA):</b> Kata yang mengacu pada orang, tempat, hewan, atau benda. (Contoh: guru, pasar, kucing, meja).<br/>
        <b>2. KATA KERJA (VERBA):</b> Kata yang menyatakan perbuatan atau tindakan. (Contoh: menulis, dibaca, berlari).<br/>
        <b>3. KATA SIFAT (ADJEKTIVA):</b> Kata yang menerangkan sifat atau keadaan suatu benda. (Contoh: besar, rajin, merah).<br/>
        <b>4. KATA BILANGAN (NUMERALIA):</b> Kata yang menyatakan jumlah. (Contoh: satu, kedua, setengah).
        """),
        ("STRUKTUR KALIMAT", """
        <b>UNSUR KALIMAT:</b> S (Subjek), P (Predikat), O (Objek), K (Keterangan), Pel (Pelengkap).<br/>
        <b>JENIS KALIMAT DASAR:</b><br/>
        • <b>Kalimat Berita:</b> Memberi informasi. (Contoh: Hari ini hujan.)<br/>
        • <b>Kalimat Tanya:</b> Meminta jawaban. (Contoh: Apakah kamu sudah makan?)<br/>
        • <b>Kalimat Perintah:</b> Menyuruh melakukan sesuatu. (Contoh: Tutup jendela itu!)<br/>
        <b>KALIMAT MAJEMUK:</b> Gabungan dua kalimat atau lebih.<br/>
        • <b>Setara:</b> dihubungkan dengan 'dan', 'atau', 'tetapi'.<br/>
        • <b>Bertingkat:</b> dihubungkan dengan 'karena', 'ketika', 'jika'.
        """),
        ("EJAAN & TANDA BACA (EYD)", """
        <b>HURUF KAPITAL:</b> Digunakan pada awal kalimat, nama orang, tempat, hari, bulan, dan judul.<br/>
        <b>TANDA BACA:</b><br/>
        • <b>Titik (.):</b> Akhir kalimat berita.<br/>
        • <b>Koma (,):</b> Memisahkan unsur dalam perincian.<br/>
        • <b>Tanda Tanya (?):</b> Akhir kalimat tanya.<br/>
        • <b>Tanda Seru (!):</b> Akhir kalimat perintah atau seruan.<br/>
        <b>PENULISAN KATA DEPAN:</b> 'di', 'ke', 'dari' ditulis terpisah dari kata yang mengikutinya jika menunjukkan tempat. (Contoh: di rumah, ke sekolah).
        """)
    ]
    
    for judul, isi in tata_bahasa:
        story.append(Paragraph(judul, styles['Heading2']))
        story.append(Spacer(1, 0.1 * inch))
        story.append(Paragraph(isi, styles['Normal']))
        story.append(Spacer(1, 0.2 * inch))

    story.append(PageBreak())

    # --- BAGIAN 3: KAMUS KOSAKATA DASAR ---
    main_title_3 = Paragraph("BAGIAN 3: KAMUS KOSAKATA DASAR", styles['Heading1'])
    story.append(main_title_3)
    story.append(Spacer(1, 0.3 * inch))

    kosakata = [
        ("TEMA: KELUARGA", "<b>Ayah:</b> Orang tua laki-laki.<br/><b>Ibu:</b> Orang tua perempuan.<br/><b>Kakak:</b> Saudara yang lebih tua.<br/><b>Adik:</b> Saudara yang lebih muda.<br/><b>Kakek:</b> Ayah dari orang tua kita.<br/><b>Nenek:</b> Ibu dari orang tua kita."),
        ("TEMA: SEKOLAH", "<b>Guru:</b> Orang yang mengajar.<br/><b>Murid:</b> Orang yang belajar.<br/><b>Kelas:</b> Ruang untuk belajar.<br/><b>Perpustakaan:</b> Tempat membaca dan meminjam buku.<br/><b>Belajar:</b> Kegiatan menuntut ilmu."),
        ("TEMA: ALAM", "<b>Gunung:</b> Dataran yang sangat tinggi.<br/><b>Sungai:</b> Aliran air yang besar.<br/><b>Laut:</b> Kumpulan air asin yang sangat luas.<br/><b>Hujan:</b> Air yang turun dari langit.<br/><b>Matahari:</b> Bintang yang menjadi pusat tata surya."),
        ("TEMA: SIFAT", "<b>Rajin:</b> Suka bekerja dan belajar.<br/><b>Jujur:</b> Berkata apa adanya.<br/><b>Baik:</b> Suka menolong.<br/><b>Sopan:</b> Menghormati orang lain.<br/><b>Pintar:</b> Cepat mengerti pelajaran.")
    ]

    for judul, isi in kosakata:
        story.append(Paragraph(judul, styles['Heading3']))
        story.append(Spacer(1, 0.1 * inch))
        story.append(Paragraph(isi, styles['Normal']))
        story.append(Spacer(1, 0.2 * inch))

    # --- PENUTUP ---
    story.append(Spacer(1, 0.5 * inch))
    footer = Paragraph(
        "<i>Rangkuman ini dibuat untuk menjadi panduan belajar yang praktis. Teruslah berlatih untuk menguasai Bahasa Indonesia dengan baik!</i>",
        styles['Italic']
    )
    story.append(footer)

    # Membangun PDF
    try:
        doc.build(story)
        print(f"✅ PDF '{filename}' berhasil dibuat!")
        print("📄 File ini berisi rangkuman lengkap materi, tata bahasa, dan kosakata.")
    except Exception as e:
        print(f"❌ Terjadi kesalahan saat membuat PDF: {e}")

# Jalankan fungsi utama
if __name__ == "__main__":
    print("📚 Memulai proses pembuatan PDF Rangkuman Lengkap Bahasa Indonesia SD...")
    print("=" * 60)
    buat_pdf_rangkuman_lengkap()
    print("=" * 60)
    print("🎯 Proses selesai.")
