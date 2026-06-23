const API_URL = "http://localhost:8000";

const chatMessages = document.getElementById("chat-messages");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const pdfUpload = document.getElementById("pdf-upload");
const fileList = document.getElementById("file-list");
const resetBtn = document.getElementById("reset-btn");
const toast = document.getElementById("toast");

// Helper to show toasts
function showToast(message, duration = 3000) {
    toast.textContent = message;
    toast.classList.remove("hidden");
    setTimeout(() => toast.classList.add("hidden"), duration);
}

// Add message to chat UI
function addMessage(text, role) {
    const msgDiv = document.createElement("div");
    msgDiv.className = `message ${role}`;
    
    const avatar = document.createElement("div");
    avatar.className = "avatar";
    avatar.textContent = role === "bot" ? "🤖" : "👤";
    
    const content = document.createElement("div");
    content.className = "content";
    content.textContent = text;
    
    msgDiv.appendChild(avatar);
    msgDiv.appendChild(content);
    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Handle sending message
async function handleSend() {
    const text = userInput.value.trim();
    if (!text) return;

    addMessage(text, "user");
    userInput.value = "";
    
    // Typing indicator effect (optional, here just showing raw delay)
    const botMsgId = Date.now();
    addMessage("Thinking...", "bot");
    const lastMsg = chatMessages.lastElementChild.querySelector(".content");

    try {
        const response = await fetch(`${API_URL}/query`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ prompt: text })
        });
        
        const data = await response.json();
        lastMsg.textContent = data.answer;
    } catch (error) {
        lastMsg.textContent = "Error: Could not connect to the backend.";
    }
}

// Handle file upload
pdfUpload.addEventListener("change", async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    const fileItem = document.createElement("div");
    fileItem.className = "file-item";
    fileItem.innerHTML = `<span>📄</span> <span>${file.filename || file.name} (uploading...)</span>`;
    fileList.appendChild(fileItem);

    try {
        const response = await fetch(`${API_URL}/upload`, {
            method: "POST",
            body: formData
        });
        
        if (response.ok) {
            fileItem.innerHTML = `<span>📄</span> <span>${file.filename || file.name}</span>`;
            showToast("Document indexed successfully!");
        } else {
            fileItem.remove();
            showToast("Upload failed.");
        }
    } catch (error) {
        fileItem.remove();
        showToast("Error uploading file.");
    }
});

// Handle reset
resetBtn.addEventListener("click", async () => {
    if (confirm("Reset knowledge base and chat?")) {
        await fetch(`${API_URL}/reset`, { method: "POST" });
        fileList.innerHTML = "";
        chatMessages.innerHTML = `
            <div class="message bot">
                <div class="avatar">🤖</div>
                <div class="content">Database reset. Ready for new documents!</div>
            </div>
        `;
        showToast("Database cleared.");
    }
});

// Event listeners
sendBtn.addEventListener("click", handleSend);
userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        handleSend();
    }
});

// Initial health check
fetch(API_URL).catch(() => showToast("Backend offline. Please start the server.", 5000));
