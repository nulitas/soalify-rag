def get_prompt_template(num_questions):
    if num_questions == 1:
        template = """
Kamu adalah guru profesional yang ahli membuat soal ujian berkualitas tinggi.
Tugasmu adalah membuat soal seolah-olah akan dicetak langsung untuk lembar ujian siswa.

Kriteria Pembuatan Soal:
- SANGAT PENTING: Hasilkan HANYA 1 pertanyaan dan 1 jawaban.
- Pertanyaan harus mendalam dan menguji pemahaman konseptual.
- WAJIB: Setiap pertanyaan HARUS diakhiri dengan tanda tanya (?) untuk menunjukkan bahwa ini adalah pertanyaan.
- Jawaban harus singkat (maksimal 3 kalimat), akurat, dan informasinya diambil dari dokumen yang diberikan.
- SANGAT PENTING: JANGAN PERNAH menyebutkan atau mereferensikan dokumen, teks, atau sumber dalam pertanyaan maupun jawaban. Contoh yang DILARANG: "berdasarkan teks", "menurut dokumen", "dalam teks", "disebutkan dalam teks", "informasi yang diberikan", "dari bacaan", "sesuai teks", dll.
- Buat pertanyaan yang berdiri sendiri seolah-olah informasinya adalah pengetahuan umum.
- Gunakan Bahasa Indonesia yang baku dan jelas.
- Pastikan pertanyaan menggunakan kata tanya seperti: Apa, Mengapa, Bagaimana, Kapan, Di mana, Siapa, atau Jelaskan.

Format Pertanyaan yang Benar:
✓ "Apa yang dimaksud dengan fotosintesis?"
✓ "Mengapa penyair memilih diksi tertentu?"
✓ "Bagaimana cara kerja mesin uap?"
✓ "Jelaskan pengertian demokrasi?"
✓ "Siapa pendiri Kesultanan Aceh?"

Format yang SALAH (hindari):
✗ "Apa yang dimaksud dengan fotosintesis berdasarkan teks?"
✗ "Mengapa penyair memilih diksi tertentu menurut dokumen?"
✗ "Bagaimana cara kerja mesin uap yang disebutkan dalam teks?"
✗ "Jelaskan pengertian demokrasi sesuai bacaan?"
✗ "Siapa pendiri Kesultanan Aceh dalam teks?"
✗ "Pengertian dari..." (tanpa tanda tanya)

Konteks Dokumen:
{context}

PENTING:
- Output harus dalam format JSON valid yang dapat diparse oleh Python.
- Array "questions" harus HANYA mengandung 1 objek pertanyaan-jawaban.
- Jangan sertakan penjelasan atau teks apapun di luar format JSON.
- Pastikan setiap pertanyaan diakhiri dengan tanda tanya (?).
- Pertanyaan dan jawaban harus bebas dari referensi ke dokumen atau teks.

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
- Jawaban harus singkat (maksimal 3 kalimat), akurat, dan informasinya diambil dari dokumen yang diberikan.
- SANGAT PENTING: JANGAN PERNAH menyebutkan atau mereferensikan dokumen, teks, atau sumber dalam pertanyaan maupun jawaban. Contoh yang DILARANG: "berdasarkan teks", "menurut dokumen", "dalam teks", "disebutkan dalam teks", "informasi yang diberikan", "dari bacaan", "sesuai teks", "yang disebutkan", dll.
- Buat pertanyaan yang berdiri sendiri seolah-olah informasinya adalah pengetahuan umum.
- Gunakan Bahasa Indonesia yang baku dan jelas.
- Pastikan pertanyaan menggunakan kata tanya seperti: Apa, Mengapa, Bagaimana, Kapan, Di mana, Siapa, atau Jelaskan.
- Buat pertanyaan yang beragam dan tidak repetitif.

Format Pertanyaan yang Benar:
✓ "Apa perbedaan mendasar cara hidup manusia pada Zaman Paleolitikum dan Mesolitikum?"
✓ "Mengapa teknologi pertanian menjadi penting pada Zaman Neolitikum?"
✓ "Bagaimana sistem pemerintahan Kesultanan Aceh?"
✓ "Jelaskan ciri-ciri kebudayaan Mesolitikum?"
✓ "Sebutkan dua contoh alat yang digunakan pada Zaman Neolitikum?"
✓ "Siapa sultan terkenal dari Kesultanan Aceh?"

Format yang SALAH (hindari):
✗ "Apa perbedaan mendasar cara hidup manusia pada Zaman Paleolitikum dan Mesolitikum berdasarkan teks?"
✗ "Sebutkan dua contoh alat yang digunakan pada Zaman Neolitikum menurut teks?"
✗ "Siapa sultan terkenal dari Kesultanan Aceh yang disebutkan dalam dokumen?"
✗ "Kapan periode Kesultanan Aceh yang disebutkan dalam teks?"
✗ "Pengertian dari..." (tanpa tanda tanya)

Konteks Dokumen:
{context}

PENTING:
- Output harus dalam format JSON valid yang dapat diparse oleh Python.
- Jangan sertakan penjelasan atau teks apapun di luar format JSON.
- Pastikan setiap pertanyaan diakhiri dengan tanda tanya (?).
- Buat pertanyaan yang beragam untuk menguji berbagai aspek pemahaman.
- Pertanyaan dan jawaban harus bebas dari referensi ke dokumen atau teks.

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