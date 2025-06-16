document.addEventListener("DOMContentLoaded", function () {
  const chatForm = document.getElementById("chat-form");
  const userInput = document.getElementById("user-input");
  const chatMessages = document.getElementById("chat-messages");
  const typingIndicator = document.getElementById("typing-indicator");

  chatForm.addEventListener("submit", function (e) {
    e.preventDefault();

    const message = userInput.value.trim();
    if (message === "") return;

    // Add user message to chat
    addMessage("user", message);

    // Clear input
    userInput.value = "";

    // Show typing indicator
    showTypingIndicator();

    // Send message to backend
    fetch("/api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: message }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        // Hide typing indicator
        hideTypingIndicator();

        // Add bot response to chat with typing effect
        addMessage("bot", data.response, true);
      })
      .catch((error) => {
        hideTypingIndicator();
        addMessage(
          "system",
          "Sorry, there was an error processing your request."
        );
        console.error("Error:", error);
      });
  });

  function addMessage(sender, message, withTypingEffect = false) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${sender}`;

    const messageContent = document.createElement("div");
    messageContent.className = "message-content";

    const messagePara = document.createElement("p");

    if (sender === "bot" && withTypingEffect) {
      // Add empty paragraph for now
      messageContent.appendChild(messagePara);
      messageDiv.appendChild(messageContent);
      chatMessages.appendChild(messageDiv);

      // Apply typing effect
      typeMessage(message, messagePara);
    } else {
      // Regular message rendering
      if (sender === "bot") {
        messagePara.innerHTML = marked.parse(message);
      } else {
        messagePara.textContent = message;
      }

      messageContent.appendChild(messagePara);
      messageDiv.appendChild(messageContent);
      chatMessages.appendChild(messageDiv);
    }

    scrollToBottom();
  }

  function typeMessage(message, element, index = 0, speed = 20) {
    if (index < message.length) {
      // Append the next character
      element.textContent += message.charAt(index);

      // Scroll to keep up with the typing
      scrollToBottom();

      // Schedule the next character
      setTimeout(() => {
        typeMessage(message, element, index + 1, speed);
      }, speed);
    } else {
      // Apply markdown formatting after typing is complete
      element.innerHTML = marked.parse(message);
    }
  }

  function showTypingIndicator() {
    typingIndicator.classList.add("active");
  }

  function hideTypingIndicator() {
    typingIndicator.classList.remove("active");
  }

  function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
});
