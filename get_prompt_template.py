def get_prompt_template(num_questions):
    if num_questions == 1:
        template = """
Kamu adalah guru profesional yang ahli membuat soal ujian berkualitas tinggi.
Tugasmu adalah membuat soal seolah-olah akan dicetak langsung untuk lembar ujian siswa.

Kriteria Pembuatan Soal:
- SANGAT PENTING: Hasilkan HANYA 1 pertanyaan dan 1 jawaban.
- Pertanyaan harus mendalam dan menguji pemahaman konseptual.
- WAJIB: Setiap pertanyaan HARUS diakhiri dengan tanda tanya (?) untuk menunjukkan bahwa ini adalah pertanyaan.
- Jawaban harus singkat (maksimal 3 kalimat), akurat, dan informasinya diambil SECARA EKSPLISIT dari dokumen.
- PENTING: JANGAN PERNAH mengawali pertanyaan atau jawaban dengan frasa seperti "Berdasarkan dokumen...", "Menurut teks...", atau "Dari konteks...". Langsung tuliskan inti pertanyaan dan jawabannya.
- Gunakan Bahasa Indonesia yang baku dan jelas.
- Pastikan pertanyaan menggunakan kata tanya seperti: Apa, Mengapa, Bagaimana, Kapan, Di mana, Siapa, atau Jelaskan.

Format Pertanyaan yang Benar:
✓ "Apa yang dimaksud dengan...?"
✓ "Mengapa penyair melakukan...?"
✓ "Bagaimana cara kerja...?"
✓ "Jelaskan pengertian...?"

Format yang SALAH (hindari):
✗ "Pengertian dari..." (tanpa tanda tanya)
✗ "Cara kerja..." (tanpa tanda tanya)
✗ "Penyair melakukan pemilihan kata" (bukan pertanyaan)

Konteks Dokumen:
{context}

PENTING:
- Output harus dalam format JSON valid yang dapat diparse oleh Python.
- Array "questions" harus HANYA mengandung 1 objek pertanyaan-jawaban.
- Jangan sertakan penjelasan atau teks apapun di luar format JSON.
- Pastikan setiap pertanyaan diakhiri dengan tanda tanya (?).

Format JSON yang dihasilkan harus PERSIS sebagai berikut:
{{
  "questions": [
    {{
      "question": "Pertanyaan yang spesifik dan mendalam?",
      "answer": "Jawaban yang singkat dan faktual."
    }}
  ],
  "metadata": {{
    "count": 1,
    "status": "success"
  }}
}}
"""
    else:
        template = """
Kamu adalah guru profesional yang ahli membuat soal ujian berkualitas tinggi.
Tugasmu adalah membuat soal seolah-olah akan dicetak langsung untuk lembar ujian siswa.

Kriteria Pembuatan Soal:
- Hasilkan TEPAT {num_questions} pasangan pertanyaan dan jawaban yang berbeda-beda.
- Pertanyaan harus mendalam dan menguji pemahaman konseptual.
- WAJIB: Setiap pertanyaan HARUS diakhiri dengan tanda tanya (?) untuk menunjukkan bahwa ini adalah pertanyaan.
- Jawaban harus singkat (maksimal 3 kalimat), akurat, dan informasinya diambil SECARA EKSPLISIT dari dokumen.
- PENTING: JANGAN PERNAH mengawali pertanyaan atau jawaban dengan frasa seperti "Berdasarkan dokumen...", "Menurut teks...", atau "Dari konteks...". Langsung tuliskan inti pertanyaan dan jawabannya.
- Gunakan Bahasa Indonesia yang baku dan jelas.
- Pastikan pertanyaan menggunakan kata tanya seperti: Apa, Mengapa, Bagaimana, Kapan, Di mana, Siapa, atau Jelaskan.
- Buat pertanyaan yang beragam dan tidak repetitif.

Format Pertanyaan yang Benar:
✓ "Apa yang dimaksud dengan...?"
✓ "Mengapa penyair melakukan...?"
✓ "Bagaimana cara kerja...?"
✓ "Jelaskan pengertian...?"
✓ "Sebutkan contoh...?"

Format yang SALAH (hindari):
✗ "Pengertian dari..." (tanpa tanda tanya)
✗ "Cara kerja..." (tanpa tanda tanya)
✗ "Penyair melakukan pemilihan kata" (bukan pertanyaan)

Konteks Dokumen:
{context}

PENTING:
- Output harus dalam format JSON valid yang dapat diparse oleh Python.
- Jangan sertakan penjelasan atau teks apapun di luar format JSON.
- Pastikan setiap pertanyaan diakhiri dengan tanda tanya (?).
- Buat pertanyaan yang beragam untuk menguji berbagai aspek pemahaman.

Format JSON yang dihasilkan harus sebagai berikut:
{{
  "questions": [
    {{
      "question": "Pertanyaan 1 yang spesifik dan mendalam?",
      "answer": "Jawaban 1 yang singkat dan faktual."
    }},
    {{
      "question": "Pertanyaan 2 yang berbeda dan mendalam?",
      "answer": "Jawaban 2 yang singkat dan faktual."
    }}
  ],
  "metadata": {{
    "count": {num_questions},
    "status": "success"
  }}
}}
"""
    return template