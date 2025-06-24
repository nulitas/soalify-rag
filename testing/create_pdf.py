from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
import os

def buat_pdf_matematika_bertingkat():
    """MATEMATIKA BERTINGKAT - TK sampai Perkuliahan"""
    filename = "matematika_bertingkat.pdf"
    
    doc = SimpleDocTemplate(filename, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    # Judul
    title = Paragraph("MATEMATIKA: DARI TK HINGGA PERKULIAHAN", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 0.5*inch))
    
    content = [
        ("MENGENAL ANGKA", """
        <b>ANGKA 1-10</b><br/>
        Belajar mengenal angka dan menghitung benda:<br/>
        • 1 (satu) = 🍎<br/>
        • 2 (dua) = 🍎🍎<br/>
        • 3 (tiga) = 🍎🍎🍎<br/>
        • 4 (empat) = 🍎🍎🍎🍎<br/>
        • 5 (lima) = 🍎🍎🍎🍎🍎<br/><br/>
        
        <b>PENJUMLAHAN SEDERHANA</b><br/>
        • 1 + 1 = 2<br/>
        • 2 + 1 = 3<br/>
        • 3 + 2 = 5<br/><br/>
        
        <b>BENTUK DASAR</b><br/>
        • Lingkaran ⭕<br/>
        • Persegi ⬜<br/>
        • Segitiga 🔺
        """),
        
        ("OPERASI DASAR", """
        <b>PENJUMLAHAN DAN PENGURANGAN</b><br/>
        • 25 + 17 = 42<br/>
        • 50 - 23 = 27<br/>
        • Penjumlahan bersusun ke bawah<br/>
        • Pengurangan dengan meminjam<br/><br/>
        
        <b>PERKALIAN DAN PEMBAGIAN</b><br/>
        • Tabel perkalian 1-10<br/>
        • 7 × 8 = 56<br/>
        • 72 ÷ 9 = 8<br/>
        • Perkalian bersusun<br/><br/>
        
        <b>BANGUN DATAR</b><br/>
        • Persegi: Luas = s × s<br/>
        • Persegi panjang: Luas = p × l<br/>
        • Segitiga: Luas = ½ × a × t<br/>
        • Lingkaran: Luas = π × r²
        """),
        
        ("ALJABAR DASAR", """
        <b>BILANGAN BULAT</b><br/>
        • Bilangan positif: 1, 2, 3, ...<br/>
        • Bilangan negatif: -1, -2, -3, ...<br/>
        • Operasi: 5 + (-3) = 2<br/>
        • Operasi: (-4) × (-2) = 8<br/><br/>
        
        <b>ALJABAR SEDERHANA</b><br/>
        • Variabel: x, y, z<br/>
        • Suku sejenis: 3x + 5x = 8x<br/>
        • Persamaan linear: 2x + 5 = 13<br/>
        • Penyelesaian: x = 4<br/><br/>
        
        <b>GEOMETRI</b><br/>
        • Sudut: lancip, tumpul, siku-siku<br/>
        • Teorema Pythagoras: a² + b² = c²<br/>
        • Bangun ruang: kubus, balok, tabung
        """),
        
        ("FUNGSI DAN TRIGONOMETRI", """
        <b>FUNGSI</b><br/>
        • Definisi: f(x) = 2x + 3<br/>
        • Domain dan range<br/>
        • Fungsi linear: y = mx + c<br/>
        • Fungsi kuadrat: y = ax² + bx + c<br/><br/>
        
        <b>TRIGONOMETRI</b><br/>
        • sin θ = depan/miring<br/>
        • cos θ = samping/miring<br/>
        • tan θ = depan/samping<br/>
        • Identitas: sin²θ + cos²θ = 1<br/><br/>
        
        <b>LOGARITMA</b><br/>
        • log₁₀ 100 = 2<br/>
        • ln e = 1<br/>
        • Sifat: log(a×b) = log a + log b
        """),
        
        ("KALKULUS", """
        <b>LIMIT</b><br/>
        • lim(x→a) f(x) = L<br/>
        • lim(x→∞) (1/x) = 0<br/>
        • Limit tak hingga<br/>
        • Kontinuitas fungsi<br/><br/>
        
        <b>TURUNAN (DIFERENSIAL)</b><br/>
        • f'(x) = lim(h→0) [f(x+h) - f(x)]/h<br/>
        • d/dx (xⁿ) = n·xⁿ⁻¹<br/>
        • d/dx (sin x) = cos x<br/>
        • Aturan rantai: (f∘g)'(x) = f'(g(x))·g'(x)<br/><br/>
        
        <b>INTEGRAL</b><br/>
        • ∫ f(x) dx = F(x) + C<br/>
        • ∫ xⁿ dx = xⁿ⁺¹/(n+1) + C<br/>
        • ∫ₐᵇ f(x) dx = F(b) - F(a)<br/>
        • Aplikasi: luas daerah, volume benda putar<br/><br/>
        
        <b>PERSAMAAN DIFERENSIAL</b><br/>
        • dy/dx = f(x,y)<br/>
        • Solusi umum dan khusus<br/>
        • Aplikasi dalam fisika dan teknik
        """),
        
        ("MATEMATIKA DISKRIT", """
        <b>TEORI GRAF</b><br/>
        • Vertex (simpul) dan edge (sisi)<br/>
        • Graf berarah dan tak berarah<br/>
        • Shortest path algorithms<br/>
        • Aplikasi dalam jaringan komputer<br/><br/>
        
        <b>KOMBINATORIKA</b><br/>
        • Permutasi: P(n,r) = n!/(n-r)!<br/>
        • Kombinasi: C(n,r) = n!/[r!(n-r)!]<br/>
        • Prinsip pigeonhole<br/>
        • Generating functions<br/><br/>
        
        <b>TEORI BILANGAN</b><br/>
        • Bilangan prima dan komposit<br/>
        • Algoritma Euclidean: GCD(a,b)<br/>
        • Modular arithmetic<br/>
        • Aplikasi dalam kriptografi
        """)
    ]
    
    for judul, isi in content:
        # Subjudul dengan warna berbeda
        subtitle = Paragraph(judul, styles['Heading2'])
        story.append(subtitle)
        story.append(Spacer(1, 0.2*inch))
        
        # Isi konten
        paragraf = Paragraph(isi, styles['Normal'])
        story.append(paragraf)
        story.append(Spacer(1, 0.4*inch))
    
    # Footer
    footer = Paragraph(
        "<i>Materi ini disusun secara bertingkat untuk membantu pemahaman matematika dari dasar hingga lanjut.</i>", 
        styles['Normal']
    )
    story.append(footer)
    
    doc.build(story)
    print(f"✅ PDF '{filename}' berhasil dibuat!")
    return filename

# Fungsi untuk membuat materi yang lebih fokus (alternatif)
def buat_pdf_matematika_fokus():
    """MATEMATIKA FOKUS - Hanya konsep inti tiap tingkat"""
    filename = "matematika_fokus.pdf"
    
    doc = SimpleDocTemplate(filename, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    title = Paragraph("MATEMATIKA: KONSEP INTI TIAP TINGKAT", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 0.5*inch))
    
    content = [
        ("TK: Menghitung 1-10", "Belajar angka dasar dan menghitung benda sederhana."),
        ("SD: Operasi Hitung", "Penjumlahan, pengurangan, perkalian, pembagian."),
        ("SMP: Aljabar Dasar", "Variabel, persamaan linear, geometri dasar."),
        ("SMA: Fungsi & Grafik", "Fungsi matematika, trigonometri, logaritma."),
        ("S1: Kalkulus", "Limit, turunan, integral, aplikasi."),
        ("S2: Matematika Lanjut", "Analisis real, aljabar abstrak, topologi.")
    ]
    
    for tingkat, deskripsi in content:
        # Tingkat
        tingkat_para = Paragraph(f"<b>{tingkat}</b>", styles['Heading3'])
        story.append(tingkat_para)
        
        # Deskripsi
        desc_para = Paragraph(deskripsi, styles['Normal'])
        story.append(desc_para)
        story.append(Spacer(1, 0.3*inch))
    
    doc.build(story)
    print(f"✅ PDF '{filename}' berhasil dibuat!")
    return filename

# Jalankan fungsi
if __name__ == "__main__":
    print("Membuat PDF Matematika Bertingkat...")
    buat_pdf_matematika_bertingkat()
    
    print("\nMembuat PDF Matematika Fokus...")
    buat_pdf_matematika_fokus()
    
    print("\n✅ Semua PDF berhasil dibuat!")
    print("📄 File yang dihasilkan:")
    print("   - matematika_bertingkat.pdf (Detail)")
    print("   - matematika_fokus.pdf (Ringkas)")