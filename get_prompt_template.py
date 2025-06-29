def get_prompt_template(num_questions, target_learning_outcome=None):
    """
    Generate prompt template with optional target learning outcome
    
    Args:
        num_questions: Number of questions to generate
        target_learning_outcome: Optional specific learning outcome target
                                Options: "pengetahuan_faktual", "pemahaman_konseptual", 
                                        "penerapan_prosedural", "analisis_sederhana", "auto"
    """
    
    # Learning outcome mapping
    learning_outcomes = {
        "pengetahuan_faktual": {
            "description": "Pengetahuan faktual (mengingat, mengenali)",
            "question_types": "Apa, Siapa, Di mana, Kapan",
            "focus": "Mengingat fakta, data, informasi spesifik dari dokumen"
        },
        "pemahaman_konseptual": {
            "description": "Pemahaman konseptual (menjelaskan, memberikan contoh)",
            "question_types": "Mengapa, Bagaimana, Jelaskan",
            "focus": "Memahami konsep, dapat menjelaskan dengan kata-kata sendiri"
        },
        "penerapan_prosedural": {
            "description": "Penerapan prosedural (menggunakan, menyelesaikan)",
            "question_types": "Bagaimana cara, Sebutkan langkah-langkah",
            "focus": "Menerapkan prosedur atau langkah-langkah yang dipelajari"
        },
        "analisis_sederhana": {
            "description": "Analisis sederhana (membandingkan, mengklasifikasi)",
            "question_types": "Bandingkan, Klasifikasikan, Bedakan",
            "focus": "Menganalisis hubungan antar konsep pada level sederhana"
        }
    }
    
    # Build learning outcome instruction
    if target_learning_outcome and target_learning_outcome != "auto":
        if target_learning_outcome in learning_outcomes:
            outcome_instruction = f"""
TARGET CAPAIAN PEMBELAJARAN SPESIFIK:
User telah menentukan target capaian pembelajaran: {learning_outcomes[target_learning_outcome]['description']}

FOKUS PEMBUATAN SOAL:
- Prioritas utama: {learning_outcomes[target_learning_outcome]['focus']}
- Jenis pertanyaan yang diutamakan: {learning_outcomes[target_learning_outcome]['question_types']}
- Semua pertanyaan harus mengarah pada pencapaian target pembelajaran ini
- Tetap sesuaikan dengan level pendidikan (SD/SMP) yang terdeteksi dari dokumen
"""
        else:
            outcome_instruction = """
TARGET CAPAIAN PEMBELAJARAN: AUTO DETECT
Sistem akan mendeteksi target capaian pembelajaran secara otomatis berdasarkan analisis dokumen.
"""
    else:
        outcome_instruction = """
TARGET CAPAIAN PEMBELAJARAN: AUTO DETECT  
Sistem akan mendeteksi target capaian pembelajaran secara otomatis berdasarkan analisis dokumen.
"""

    if num_questions == 1:
        template = f"""
Kamu adalah guru profesional yang ahli membuat soal ujian berkualitas tinggi.
Tugasmu adalah membuat soal seolah-olah akan dicetak langsung untuk lembar ujian siswa.

{outcome_instruction}

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

Konteks Dokumen:
{{context}}

PENTING:
- Tentukan level edukasi dari analisis dokumen terlebih dahulu
- Jika level terlalu tinggi (SMA/Perguruan Tinggi), kembalikan status error
- Identifikasi target pencapaian pembelajaran secara otomatis ATAU ikuti target yang diberikan user
- Output harus dalam format JSON valid yang dapat diparse oleh Python

Format JSON jika materi SESUAI (SD/SMP):
{{{{
  "questions": [
    {{{{
      "question": "Pertanyaan yang disesuaikan dengan level SD/SMP dan target capaian pembelajaran?",
      "answer": "Jawaban yang sesuai kompleksitas level SD/SMP.",
      "learning_outcome_achieved": "Pencapaian pembelajaran spesifik dari pertanyaan ini"
    }}}}
  ],
  "metadata": {{{{
    "count": 1,
    "education_level": "SD/SMP",
    "target_learning_outcome": "{'User-specified' if target_learning_outcome and target_learning_outcome != 'auto' else 'Auto-detected'}",
    "actual_learning_outcome": "Pencapaian pembelajaran yang benar-benar dicapai",
    "level_reasoning": "Alasan singkat pemilihan level berdasarkan analisis dokumen",
    "outcome_reasoning": "Alasan pemilihan target capaian pembelajaran",
    "status": "success"
  }}}}
}}}}

Format JSON jika materi TERLALU TINGGI:
{{{{
  "questions": [],
  "metadata": {{{{
    "count": 0,
    "education_level": "Terlalu Tinggi",
    "target_learning_outcome": "{'User-specified' if target_learning_outcome and target_learning_outcome != 'auto' else 'Auto-detected'}",
    "actual_learning_outcome": "Tidak dapat diproses",
    "level_reasoning": "Materi memerlukan tingkat pendidikan SMA atau lebih tinggi",
    "outcome_reasoning": "Level materi terlalu tinggi untuk diproses",
    "status": "error",
    "error_message": "Level pencapaian materi terlalu tinggi. Sistem hanya dapat memproses materi tingkat SD dan SMP."
  }}}}
}}}}
"""
    else:
        template = f"""
Kamu adalah guru profesional yang ahli membuat soal ujian berkualitas tinggi.
Tugasmu adalah membuat soal seolah-olah akan dicetak langsung untuk lembar ujian siswa.

{outcome_instruction}

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
- Hasilkan TEPAT {{num_questions}} pasangan pertanyaan dan jawaban yang berbeda-beda.
- Sesuaikan tingkat kesulitan dan vocabulary dengan level SD/SMP saja.
- Untuk SD: Gunakan bahasa sederhana, pertanyaan faktual langsung
- Untuk SMP: Kombinasi fakta dan pemahaman sederhana  
- WAJIB: Setiap pertanyaan HARUS diakhiri dengan tanda tanya (?) untuk menunjukkan bahwa ini adalah pertanyaan.
- Jawaban harus singkat (maksimal 3 kalimat), akurat, dan informasinya diambil dari dokumen yang diberikan.
- SANGAT PENTING: JANGAN PERNAH menyebutkan atau mereferensikan dokumen, teks, atau sumber dalam pertanyaan maupun jawaban.
- Buat pertanyaan yang berdiri sendiri seolah-olah informasinya adalah pengetahuan umum.
- Gunakan Bahasa Indonesia yang baku dan sesuai level pendidikan SD/SMP.
- Buat pertanyaan yang beragam dan tidak repetitif.

Panduan Distribusi Soal Berdasarkan Target Capaian:
- Jika target spesifik diberikan user: Semua soal fokus pada target tersebut
- Jika auto-detect: Distribusikan soal secara seimbang sesuai analisis dokumen
- Pastikan setiap soal jelas mencapai target pembelajaran yang ditentukan

Konteks Dokumen:
{{context}}

PENTING:
- Tentukan level edukasi dari analisis dokumen terlebih dahulu
- Jika level terlalu tinggi (SMA/Perguruan Tinggi), kembalikan status error
- Identifikasi target pencapaian pembelajaran secara otomatis ATAU ikuti target yang diberikan user
- Buat variasi pertanyaan yang tetap sesuai dengan level SD/SMP dan target capaian
- Output harus dalam format JSON valid yang dapat diparse oleh Python

Format JSON jika materi SESUAI (SD/SMP):
{{{{
  "questions": [
    {{{{
      "question": "Pertanyaan 1 yang disesuaikan dengan level SD/SMP dan target capaian pembelajaran?",
      "answer": "Jawaban 1 yang sesuai kompleksitas level SD/SMP.",
      "learning_outcome_achieved": "Pencapaian pembelajaran spesifik dari pertanyaan ini"
    }}}},
    {{{{
      "question": "Pertanyaan 2 yang disesuaikan dengan level SD/SMP dan target capaian pembelajaran?",
      "answer": "Jawaban 2 yang sesuai kompleksitas level SD/SMP.",
      "learning_outcome_achieved": "Pencapaian pembelajaran spesifik dari pertanyaan ini"
    }}}}
  ],
  "metadata": {{{{
    "count": {{num_questions}},
    "education_level": "SD/SMP",
    "target_learning_outcome": "{'User-specified' if target_learning_outcome and target_learning_outcome != 'auto' else 'Auto-detected'}",
    "actual_learning_outcome": "Pencapaian pembelajaran yang benar-benar dicapai secara keseluruhan",
    "level_reasoning": "Alasan singkat pemilihan level berdasarkan analisis dokumen",
    "outcome_reasoning": "Alasan pemilihan/distribusi target capaian pembelajaran",
    "status": "success"
  }}}}
}}}}

Format JSON jika materi TERLALU TINGGI:
{{{{
  "questions": [],
  "metadata": {{{{
    "count": 0,
    "education_level": "Terlalu Tinggi",
    "target_learning_outcome": "{'User-specified' if target_learning_outcome and target_learning_outcome != 'auto' else 'Auto-detected'}",
    "actual_learning_outcome": "Tidak dapat diproses",
    "level_reasoning": "Materi memerlukan tingkat pendidikan SMA atau lebih tinggi",
    "outcome_reasoning": "Level materi terlalu tinggi untuk diproses",
    "status": "error",
    "error_message": "Level pencapaian materi terlalu tinggi. Sistem hanya dapat memproses materi tingkat SD dan SMP."
  }}}}
}}}}
"""
    return template