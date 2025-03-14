def get_prompt_template(num_questions):
    if num_questions == 1:
        template = """
Kamu adalah guru profesional yang ahli membuat soal ujian berkualitas tinggi.

Kriteria Pembuatan Soal:
- SANGAT PENTING: Hasilkan HANYA 1 pertanyaan dan 1 jawaban, tidak lebih!
- Pertanyaan harus mendalam dan menguji pemahaman konseptual
- Jawaban singkat, akurat, dan berbasis dokumen (maks 3 kalimat)
- Gunakan Bahasa Indonesia yang baku dan jelas

Konteks Dokumen:
{context}

PENTING: 
- Output harus dalam format JSON valid yang dapat diparse oleh Python
- Array "questions" harus HANYA mengandung 1 objek pertanyaan-jawaban
- Jangan sertakan penjelasan atau teks apapun di luar format JSON
- Jika tidak bisa membuat soal dari dokumen, hasilkan JSON dengan pesan error

Format JSON yang dihasilkan harus PERSIS sebagai berikut:
{{
  "questions": [
    {{
      "question": "Pertanyaan yang spesifik dan mendalam",
      "answer": "Jawaban yang singkat dan faktual"
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

Kriteria Pembuatan Soal:
- Hasilkan TEPAT {num_questions} pasangan pertanyaan dan jawaban
- Pertanyaan harus mendalam dan menguji pemahaman konseptual
- Jawaban singkat, akurat, dan berbasis dokumen (maks 3 kalimat)
- Gunakan Bahasa Indonesia yang baku dan jelas

Konteks Dokumen:
{context}

PENTING: 
- Output harus dalam format JSON valid yang dapat diparse oleh Python
- Jangan sertakan penjelasan atau teks apapun di luar format JSON
- Jika tidak bisa membuat soal dari dokumen, hasilkan JSON dengan pesan error

Format JSON yang dihasilkan harus sebagai berikut:
{{
  "questions": [
    {{
      "question": "Pertanyaan 1 yang spesifik dan mendalam",
      "answer": "Jawaban 1 yang singkat dan faktual"
    }},
    ...
  ],
  "metadata": {{
    "count": {num_questions},
    "status": "success"
  }}
}}
"""
    return template