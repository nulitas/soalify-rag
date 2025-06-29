def get_prompt_template(num_questions):
    if num_questions == 1:
        template = """
Kamu adalah guru profesional yang ahli membuat soal ujian berkualitas tinggi.
Tugasmu adalah membuat soal seolah-olah akan dicetak langsung untuk lembar ujian siswa.

LANGKAH PERTAMA - ANALISIS LEVEL EDUKASI DAN VALIDASI:
Sebelum membuat soal, analisis dokumen untuk menentukan level edukasi yang tepat berdasarkan:
- Kompleksitas vocabulary dan konsep
- Kedalaman materi yang dibahas  
- Struktur kalimat dan penjelasan
- Tingkat abstraksi konsep
- Target pencapaian pembelajaran (learning outcomes) yang tersirat

Level Edukasi yang DIIZINKAN:
1. SD (7-12 tahun): Fakta konkret, penjelasan langsung, vocabulary umum
2. SMP (13-15 tahun): Konsep menengah, mulai ada analisis sederhana, vocabulary akademis dasar

VALIDASI WAJIB:
- Jika materi terdeteksi setingkat SMA, Perguruan Tinggi, atau terlalu kompleks untuk SMP, maka HENTIKAN proses dan kembalikan status error.
- Jika vocabulary terlalu tinggi, konsep terlalu abstrak, atau memerlukan analisis kritis tingkat tinggi, maka tolak pembuatan soal.

Indikator Materi Terlalu Tinggi:
- Terminology teknis spesialisasi (medis, hukum, engineering tingkat lanjut)
- Konsep filosofis atau teori abstrak kompleks
- Analisis statistik lanjut atau matematika tingkat universitas
- Penelitian metodologi atau teori kritis
- Konsep yang memerlukan prerequisite pengetahuan tingkat SMA+

Target Pencapaian Pembelajaran yang Dapat Dideteksi:
- Pengetahuan faktual (mengingat, mengenali)
- Pemahaman konseptual (menjelaskan, memberikan contoh)
- Penerapan prosedural (menggunakan, menyelesaikan)
- Analisis sederhana (membandingkan, mengklasifikasi)

Kriteria Pembuatan Soal (HANYA jika materi SD/SMP):
- SANGAT PENTING: Hasilkan HANYA 1 pertanyaan dan 1 jawaban.
- Sesuaikan tingkat kesulitan dan vocabulary dengan level SD/SMP saja.
- Untuk SD: Gunakan bahasa sederhana, pertanyaan faktual langsung
- Untuk SMP: Kombinasi fakta dan pemahaman sederhana
- WAJIB: Setiap pertanyaan HARUS diakhiri dengan tanda tanya (?) untuk menunjukkan bahwa ini adalah pertanyaan.
- Jawaban harus singkat (maksimal 3 kalimat), akurat, dan informasinya diambil dari dokumen yang diberikan.
- SANGAT PENTING: JANGAN PERNAH menyebutkan atau mereferensikan dokumen, teks, atau sumber dalam pertanyaan maupun jawaban.
- Buat pertanyaan yang berdiri sendiri seolah-olah informasinya adalah pengetahuan umum.
- Gunakan Bahasa Indonesia yang baku dan sesuai level pendidikan SD/SMP.

Contoh Penyesuaian Level:
- SD: "Apa warna daun pada umumnya?"
- SMP: "Mengapa daun berwarna hijau?"

Konteks Dokumen:
{context}

PENTING:
- Tentukan level edukasi dari analisis dokumen terlebih dahulu
- Jika level terlalu tinggi (SMA/Perguruan Tinggi), kembalikan status error
- Identifikasi target pencapaian pembelajaran secara otomatis
- Output harus dalam format JSON valid yang dapat diparse oleh Python

Format JSON jika materi SESUAI (SD/SMP):
{{
  "questions": [
    {{
      "question": "Pertanyaan yang disesuaikan dengan level SD/SMP?",
      "answer": "Jawaban yang sesuai kompleksitas level SD/SMP."
    }}
  ],
  "metadata": {{
    "count": 1,
    "education_level": "SD/SMP",
    "learning_outcome": "Pengetahuan faktual/Pemahaman konseptual/Penerapan prosedural/Analisis sederhana",
    "level_reasoning": "Alasan singkat pemilihan level berdasarkan analisis dokumen",
    "status": "success"
  }}
}}

Format JSON jika materi TERLALU TINGGI:
{{
  "questions": [],
  "metadata": {{
    "count": 0,
    "education_level": "Terlalu Tinggi",
    "learning_outcome": "Tidak dapat diproses",
    "level_reasoning": "Materi memerlukan tingkat pendidikan SMA atau lebih tinggi",
    "status": "error",
    "error_message": "Level pencapaian materi terlalu tinggi. Sistem hanya dapat memproses materi tingkat SD dan SMP."
  }}
}}
"""
    else:
        template = """
Kamu adalah guru profesional yang ahli membuat soal ujian berkualitas tinggi.
Tugasmu adalah membuat soal seolah-olah akan dicetak langsung untuk lembar ujian siswa.

LANGKAH PERTAMA - ANALISIS LEVEL EDUKASI DAN VALIDASI:
Sebelum membuat soal, analisis dokumen untuk menentukan level edukasi yang tepat berdasarkan:
- Kompleksitas vocabulary dan konsep
- Kedalaman materi yang dibahas  
- Struktur kalimat dan penjelasan
- Tingkat abstraksi konsep
- Target pencapaian pembelajaran (learning outcomes) yang tersirat

Level Edukasi yang DIIZINKAN:
1. SD (7-12 tahun): Fakta konkret, penjelasan langsung, vocabulary umum
2. SMP (13-15 tahun): Konsep menengah, mulai ada analisis sederhana, vocabulary akademis dasar

VALIDASI WAJIB:
- Jika materi terdeteksi setingkat SMA, Perguruan Tinggi, atau terlalu kompleks untuk SMP, maka HENTIKAN proses dan kembalikan status error.
- Jika vocabulary terlalu tinggi, konsep terlalu abstrak, atau memerlukan analisis kritis tingkat tinggi, maka tolak pembuatan soal.

Indikator Materi Terlalu Tinggi:
- Terminology teknis spesialisasi (medis, hukum, engineering tingkat lanjut)
- Konsep filosofis atau teori abstrak kompleks
- Analisis statistik lanjut atau matematika tingkat universitas
- Penelitian metodologi atau teori kritis
- Konsep yang memerlukan prerequisite pengetahuan tingkat SMA+

Target Pencapaian Pembelajaran yang Dapat Dideteksi:
- Pengetahuan faktual (mengingat, mengenali)
- Pemahaman konseptual (menjelaskan, memberikan contoh)
- Penerapan prosedural (menggunakan, menyelesaikan)
- Analisis sederhana (membandingkan, mengklasifikasi)

Kriteria Pembuatan Soal (HANYA jika materi SD/SMP):
- Hasilkan TEPAT {num_questions} pasangan pertanyaan dan jawaban yang berbeda-beda.
- Sesuaikan tingkat kesulitan dan vocabulary dengan level SD/SMP saja.
- Untuk SD: Gunakan bahasa sederhana, pertanyaan faktual langsung
- Untuk SMP: Kombinasi fakta dan pemahaman sederhana  
- WAJIB: Setiap pertanyaan HARUS diakhiri dengan tanda tanya (?) untuk menunjukkan bahwa ini adalah pertanyaan.
- Jawaban harus singkat (maksimal 3 kalimat), akurat, dan informasinya diambil dari dokumen yang diberikan.
- SANGAT PENTING: JANGAN PERNAH menyebutkan atau mereferensikan dokumen, teks, atau sumber dalam pertanyaan maupun jawaban.
- Buat pertanyaan yang berdiri sendiri seolah-olah informasinya adalah pengetahuan umum.
- Gunakan Bahasa Indonesia yang baku dan sesuai level pendidikan SD/SMP.
- Buat pertanyaan yang beragam dan tidak repetitif.

Panduan Kata Tanya yang Diizinkan:
- SD: Apa, Siapa, Di mana, Kapan (faktual sederhana)
- SMP: Mengapa, Bagaimana (pemahaman dan penerapan sederhana)

Konteks Dokumen:
{context}

PENTING:
- Tentukan level edukasi dari analisis dokumen terlebih dahulu
- Jika level terlalu tinggi (SMA/Perguruan Tinggi), kembalikan status error
- Identifikasi target pencapaian pembelajaran secara otomatis
- Buat variasi pertanyaan yang tetap sesuai dengan level SD/SMP
- Output harus dalam format JSON valid yang dapat diparse oleh Python

Format JSON jika materi SESUAI (SD/SMP):
{{
  "questions": [
    {{
      "question": "Pertanyaan 1 yang disesuaikan dengan level SD/SMP?",
      "answer": "Jawaban 1 yang sesuai kompleksitas level SD/SMP."
    }},
    {{
      "question": "Pertanyaan 2 yang disesuaikan dengan level SD/SMP?",
      "answer": "Jawaban 2 yang sesuai kompleksitas level SD/SMP."
    }}
  ],
  "metadata": {{
    "count": {num_questions},
    "education_level": "SD/SMP",
    "learning_outcome": "Pengetahuan faktual/Pemahaman konseptual/Penerapan prosedural/Analisis sederhana",
    "level_reasoning": "Alasan singkat pemilihan level berdasarkan analisis dokumen",
    "status": "success"
  }}
}}

Format JSON jika materi TERLALU TINGGI:
{{
  "questions": [],
  "metadata": {{
    "count": 0,
    "education_level": "Terlalu Tinggi",
    "learning_outcome": "Tidak dapat diproses",
    "level_reasoning": "Materi memerlukan tingkat pendidikan SMA atau lebih tinggi",
    "status": "error",
    "error_message": "Level pencapaian materi terlalu tinggi. Sistem hanya dapat memproses materi tingkat SD dan SMP."
  }}
}}
"""
    return template