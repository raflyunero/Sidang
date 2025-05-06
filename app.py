from flask import Flask, request, jsonify, send_from_directory, redirect, url_for, session, render_template, flash
from flask_cors import CORS
from dotenv import load_dotenv
import bcrypt
import openai
import os

app = Flask(__name__, static_folder="static", static_url_path="")
CORS(app)

# Load environment variables
load_dotenv()

# Hash the admin password securely
hashed_password = bcrypt.hashpw("BORI_GUANTENG".encode('utf-8'), bcrypt.gensalt())

# Load environment variables for admin username and password
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')  # Default to 'admin' if not in .env
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'BORI_GUANTENG')  # Default to 'BORI_GUANTENG' if not in .env

# Kunci API OpenAI

# Route untuk logout
@app.route("/logout")
def logout():
    session.pop("logged_in", None)  # Menghapus sesi login
    return redirect(url_for("login"))  # Arahkan kembali ke halaman login

# Fungsi untuk membatasi topik hanya seputar UNDIP
def get_undip_response(user_message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4.1-nano",  # atau model lainnya jika kamu punya akses
            messages=[{
                    "role": "system",
                    "content": ("Kamu adalah chatbot akademik Undip yang menjawab dengan bahasa santai, gaul, dan seperti anak muda zaman sekarang. Jawaban tetap sopan, singkat, jelas, dan tetap sesuai konteks akademik."
                        "Kamu adalah chatbot yang hanya menjawab pertanyaan tentang Universitas Diponegoro (UNDIP) dan beserta informasi di setiap fakultas seperti nama dosen, "
                        "termasuk fakultas, program studi, layanan akademik, jadwal kuliah, pendaftaran, beasiswa, dan sejenisnya. "
                        "Jika ada pertanyaan di luar topik UNDIP, tolak dengan sopan."
                    ),
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("Error:", e)
        return "Maaf, terjadi kesalahan saat menghubungi server."

# Route untuk halaman utama
@app.route("/")
def index():
    return send_from_directory("static", "index.html")

# Route API untuk chatbot
@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_message = data.get("message", "")
    reply = get_undip_response(user_message)
    return jsonify({"reply": reply})

# Route untuk halaman admin
@app.route("/admin")
def admin():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("admin.html")

# Fungsi untuk memverifikasi password
def verify_password(input_password, stored_hash):
    return bcrypt.checkpw(input_password.encode('utf-8'), stored_hash)

# Route untuk halaman login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Cek apakah username dan password cocok
        if username == ADMIN_USERNAME and verify_password(password, hashed_password):
            session["logged_in"] = True
            session["change_password"] = False  # Pastikan user tidak diminta mengganti password
            return redirect(url_for("admin"))
        else:
            flash("Login gagal! Username atau password salah.", "error")  # Flash error message
            return redirect(url_for("login"))

    return render_template("login.html")

# Run server
if __name__ == "__main__":
    app.secret_key = 'your_secret_key'  # Tambahkan secret key untuk session
    app.run(debug=True)
