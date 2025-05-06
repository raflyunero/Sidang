// Fungsi untuk menangani tombol Enter
function handleKey(event) {
    if (event.key === "Enter") sendMessage();
  }
  
  // Fungsi untuk mengirim pesan
  async function sendMessage() {
    const input = document.getElementById("userInput");
    const message = input.value.trim();
    if (!message) return;
  
    const chatBody = document.getElementById("chatBody");
  
    // Tampilkan pesan user dengan style
    const userMsg = document.createElement("div");
    userMsg.className = "message user-message";
    userMsg.textContent = message;
    chatBody.appendChild(userMsg);
  
    input.value = "";
  
    // Pesan bot sedang mengetik
    const typingMsg = document.createElement("div");
    typingMsg.className = "message typing-message";
    typingMsg.textContent = "Mengetik...";
    chatBody.appendChild(typingMsg);
    chatBody.scrollTop = chatBody.scrollHeight; // Scroll ke bawah setelah pesan baru ditambahkan
  
    // Simulasikan waktu delay untuk menampilkan jawaban dari bot
    setTimeout(async () => {
      // Kirim permintaan ke backend untuk mendapatkan jawaban
      try {
        const res = await fetch("/ask", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message })
        });
        const data = await res.json();
        
        // Hapus pesan "Mengetik..."
        typingMsg.remove();
  
        // Tampilkan pesan dari chatbot
        const botMsg = document.createElement("div");
        botMsg.className = "message bot-message";
        botMsg.textContent = data.reply;
        chatBody.appendChild(botMsg);
        chatBody.scrollTop = chatBody.scrollHeight; // Scroll ke bawah setelah pesan baru ditambahkan
      } catch {
        // Jika terjadi kesalahan pada server
        typingMsg.remove();
        const botMsg = document.createElement("div");
        botMsg.className = "message bot-message";
        botMsg.textContent = "Terjadi kesalahan pada server.";
        chatBody.appendChild(botMsg);
        chatBody.scrollTop = chatBody.scrollHeight; // Scroll ke bawah setelah pesan baru ditambahkan
      }
    }, 1000); // Delay 1 detik untuk menampilkan balasan bot
  }
  
  // Fungsi untuk menghapus semua pesan
  function clearChat() {
    const chatBody = document.getElementById("chatBody");
    chatBody.innerHTML = ""; // Menghapus semua pesan
  
    // Tambahkan pesan otomatis "Hi 👋"
    const botMsg = document.createElement("div");
    botMsg.className = "message bot-message";
    botMsg.textContent = "Hi 👋, ada yang bisa saya bantu?";
    chatBody.appendChild(botMsg);
  }
    
  // Tambahkan pesan otomatis "Hi 👋" saat halaman pertama kali dibuka
  window.onload = clearChat;
  