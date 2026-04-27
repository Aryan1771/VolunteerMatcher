(function () {
  const toggle = document.getElementById("chatbotToggle");
  const panel = document.getElementById("chatbotPanel");
  const closeButton = document.getElementById("chatbotClose");
  const form = document.getElementById("chatbotForm");
  const input = document.getElementById("chatbotInput");
  const messages = document.getElementById("chatbotMessages");

  if (!toggle || !panel || !form || !input || !messages) {
    return;
  }

  function openChat() {
    panel.classList.remove("hidden");
    toggle.setAttribute("aria-expanded", "true");
    input.focus();
  }

  function closeChat() {
    panel.classList.add("hidden");
    toggle.setAttribute("aria-expanded", "false");
  }

  function addMessage(text, sender) {
    const bubble = document.createElement("div");
    bubble.className = `chatbot-message ${sender}`;
    bubble.textContent = text;
    messages.appendChild(bubble);
    messages.scrollTop = messages.scrollHeight;
    return bubble;
  }

  toggle.addEventListener("click", () => {
    if (panel.classList.contains("hidden")) {
      openChat();
    } else {
      closeChat();
    }
  });

  closeButton.addEventListener("click", closeChat);

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const message = input.value.trim();
    if (!message) {
      return;
    }

    input.value = "";
    addMessage(message, "user");
    const typingBubble = addMessage("Thinking...", "bot");

    try {
      const data = await window.api.request("/api/chatbot/message", {
        method: "POST",
        body: JSON.stringify({ message }),
      });
      typingBubble.textContent = data.reply;
    } catch (error) {
      typingBubble.textContent = error.message;
      typingBubble.classList.add("error");
    }
  });
})();
