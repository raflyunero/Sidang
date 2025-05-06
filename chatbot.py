import openai

api_key = os.getenv ("OPENAI_API_KEY")

def chatbot():
    print("Chatbot UNDIP: Halo! Ketik 'exit' untuk keluar.")

    while True:
        user_input = input("Kamu   : ")
        if user_input.lower() == 'exit':
            print("Chatbot: Sampai jumpa!")
            break

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4.1-nano",
                messages=[
                    {"role": "system", "content": ( "Kamu adalah chatbot akademik Undip yang menjawab dengan bahasa santai, gaul, dan seperti anak muda zaman sekarang. Jawaban tetap sopan, singkat, jelas, dan tetap sesuai konteks akademik."
                        "Kamu adalah chatbot akademik resmi Universitas Diponegoro (UNDIP). "
                        "Jawablah hanya pertanyaan yang berkaitan dengan UNDIP, seperti fakultas, jurusan, jadwal akademik, pendaftaran, beasiswa, dan hal-hal terkait kampus. "
                        "Jika ada pertanyaan di luar konteks UNDIP (misalnya tentang artis, politik, atau topik umum lainnya), tolak secara sopan dengan mengatakan: "
                        "'Maaf, saya hanya bisa membantu pertanyaan seputar Universitas Diponegoro (UNDIP).' "
                    )},
                    {"role": "user", "content": user_input}
                ]
            )
            print("Chatbot:", response['choices'][0]['message']['content'])
        except Exception as e:
            print("Terjadi kesalahan:", e)

if __name__ == "__main__":
    chatbot()
