document.addEventListener('DOMContentLoaded', () => {
  const askBtn = document.getElementById('askAI');
  const input = document.getElementById('chatInput');
  const chatWindow = document.getElementById('chatWindow');

  if (askBtn && input && chatWindow) {
    askBtn.addEventListener('click', async () => {
      const message = input.value.trim();
      if (!message) return;
      chatWindow.innerHTML += `<p><strong>You:</strong> ${message}</p>`;
      const formData = new FormData();
      formData.append('message', message);
      formData.append('csrfmiddlewaretoken', window.csrfToken);

      const response = await fetch('/chatbot/guidance/', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      chatWindow.innerHTML += `<p><strong>AI:</strong> ${data.reply}</p>`;
      input.value = '';
    });
  }

  const startVoiceBtn = document.getElementById('startVoice');
  if (startVoiceBtn) {
    startVoiceBtn.addEventListener('click', () => {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (!SpeechRecognition) {
        alert('Speech recognition is not supported in this browser.');
        return;
      }
      const recognition = new SpeechRecognition();
      recognition.lang = 'en-US';
      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        const descriptionField = document.getElementById('id_description');
        if (descriptionField) {
          descriptionField.value = `${descriptionField.value} ${transcript}`.trim();
        }
      };
      recognition.start();
    });
  }
});
