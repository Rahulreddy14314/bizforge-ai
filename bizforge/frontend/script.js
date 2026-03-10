const API_BASE = 'http://localhost:8000/api';

document.addEventListener('DOMContentLoaded', () => {
    // Tab Switching Logic
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            // Add active class to clicked tab and corresponding content
            btn.classList.add('active');
            const targetId = btn.getAttribute('data-target');
            document.getElementById(targetId).classList.add('active');
        });
    });

    // Helper function to manage loading state
    const setLoader = (containerId, isLoading) => {
        const container = document.getElementById(containerId);
        if (!container) return;
        const loader = container.querySelector('.loader');
        if (isLoading) {
            container.style.display = 'block';
            if (loader) loader.style.display = 'block';
        } else {
            if (loader) loader.style.display = 'none';
        }
    };

    // 0. Startup Idea Generator
    const ideaForm = document.getElementById('idea-form');
    if (ideaForm) {
        ideaForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const data = {
                keywords: document.getElementById('idea-keywords').value
            };

            setLoader('idea-results', true);
            const textEl = document.getElementById('idea-text');
            textEl.textContent = '';

            try {
                const res = await fetch(`${API_BASE}/generate-idea`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                const result = await res.json();

                setLoader('idea-results', false);
                textEl.textContent = result.idea;
            } catch (err) {
                setLoader('idea-results', false);
                textEl.textContent = `Error: ${err.message}`;
            }
        });
    }

    // 1. Brand Names Generator
    const brandForm = document.getElementById('brand-form');
    if (brandForm) {
        brandForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const data = {
                industry: document.getElementById('brand-industry').value,
                keywords: document.getElementById('brand-keywords').value,
                tone: document.getElementById('brand-tone').value,
                language: document.getElementById('brand-language').value
            };

            setLoader('brand-results', true);
            const listEl = document.querySelector('#brand-results .results-list');
            listEl.innerHTML = ''; // clear old

            try {
                const res = await fetch(`${API_BASE}/generate-brand`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                const result = await res.json();

                setLoader('brand-results', false);
                if (result.names) {
                    result.names.forEach(name => {
                        const li = document.createElement('li');
                        li.textContent = name.replace(/^[\d\.\-\*]\s*/, ''); // cleanup list artifacts
                        listEl.appendChild(li);
                    });
                }
            } catch (err) {
                setLoader('brand-results', false);
                listEl.innerHTML = `<li>Error: ${err.message}</li>`;
            }
        });
    }

    // 2. Logo Generator
    const logoForm = document.getElementById('logo-form');
    if (logoForm) {
        logoForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const data = {
                brand_name: document.getElementById('logo-name').value,
                industry: document.getElementById('logo-industry').value,
                style: document.getElementById('logo-style').value
            };

            setLoader('logo-results', true);
            document.getElementById('logo-img').src = '';
            document.getElementById('logo-prompt').textContent = '';

            try {
                const res = await fetch(`${API_BASE}/generate-logo`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                const result = await res.json();

                setLoader('logo-results', false);
                document.getElementById('logo-prompt').textContent = result.prompt;

                if (result.image_data) {
                    document.getElementById('logo-img').src = result.image_data;
                } else if (result.error) {
                    alert(result.error);
                }
            } catch (err) {
                setLoader('logo-results', false);
                alert("Error generating logo: " + err.message);
            }
        });
    }

    // 3. Color Palette Generator
    const colorsForm = document.getElementById('colors-form');
    if (colorsForm) {
        colorsForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const data = {
                industry: document.getElementById('color-industry').value,
                vibes: document.getElementById('color-vibes').value
            };

            setLoader('colors-results', true);
            const gridEl = document.getElementById('palette-grid');
            gridEl.innerHTML = '';

            try {
                const res = await fetch(`${API_BASE}/get-colors`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                const result = await res.json();

                setLoader('colors-results', false);
                if (result.colors && Array.isArray(result.colors)) {
                    result.colors.forEach(color => {
                        const swatch = document.createElement('div');
                        swatch.className = 'color-swatch';
                        swatch.style.backgroundColor = color;

                        const hex = document.createElement('span');
                        hex.className = 'color-hex';
                        hex.textContent = color.toUpperCase();

                        swatch.appendChild(hex);
                        gridEl.appendChild(swatch);
                    });
                }
            } catch (err) {
                setLoader('colors-results', false);
                gridEl.innerHTML = `<p>Error fetching colors: ${err.message}</p>`;
            }
        });
    }

    // 4. Marketing Content Generator
    const contentForm = document.getElementById('content-form');
    if (contentForm) {
        contentForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const data = {
                product: document.getElementById('content-product').value,
                content_type: document.getElementById('content-type').value,
                tone: document.getElementById('content-tone').value
            };

            setLoader('content-results', true);
            const textEl = document.getElementById('content-text');
            textEl.textContent = '';

            try {
                const res = await fetch(`${API_BASE}/generate-content`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                const result = await res.json();

                setLoader('content-results', false);
                textEl.textContent = result.content;
            } catch (err) {
                setLoader('content-results', false);
                textEl.textContent = `Error: ${err.message}`;
            }
        });
    }

    // 5. Sentiment Analyzer
    const sentimentForm = document.getElementById('sentiment-form');
    if (sentimentForm) {
        sentimentForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const data = {
                text: document.getElementById('sentiment-text').value
            };

            setLoader('sentiment-results', true);
            const badgeEl = document.getElementById('sentiment-badge');
            const confEl = document.getElementById('sentiment-confidence');
            const rewriteEl = document.getElementById('sentiment-rewrite');

            // clear old visual states
            badgeEl.className = 'badge';
            badgeEl.textContent = '...';
            confEl.textContent = '...';
            rewriteEl.textContent = '...';

            try {
                const res = await fetch(`${API_BASE}/analyze-sentiment`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                const result = await res.json();

                setLoader('sentiment-results', false);

                // Set Badge Style
                let st = (result.sentiment || "Unknown").toLowerCase();
                badgeEl.textContent = result.sentiment;
                badgeEl.classList.add('badge');
                if (st.includes('pos')) badgeEl.classList.add('positive');
                else if (st.includes('neg')) badgeEl.classList.add('negative');
                else badgeEl.classList.add('neutral');

                confEl.textContent = result.confidence || '-';
                rewriteEl.textContent = result.rewritten || 'No rewrite provided.';

            } catch (err) {
                setLoader('sentiment-results', false);
                badgeEl.textContent = 'Error';
                rewriteEl.textContent = `Error: ${err.message}`;
            }
        });
    }

    // 6. AI Chat (Granite)
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');
    const messagesContainer = document.getElementById('chat-messages');
    let chatHistory = [];

    const appendMessage = (text, role) => {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${role}`;

        const bubble = document.createElement('div');
        bubble.className = 'bubble';
        bubble.textContent = text;

        msgDiv.appendChild(bubble);
        messagesContainer.appendChild(msgDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    };

    const handleChatSubmit = async () => {
        const text = chatInput.value.trim();
        if (!text) return;

        appendMessage(text, 'user');
        chatInput.value = '';

        const payload = {
            message: text,
            history: chatHistory
        };

        // Add loading state message
        const loadingId = 'msg-' + Date.now();
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'message assistant';
        loadingDiv.id = loadingId;
        loadingDiv.innerHTML = `<div class="bubble"><i class="fa-solid fa-spinner fa-spin"></i> Thinking...</div>`;
        messagesContainer.appendChild(loadingDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        try {
            const res = await fetch(`${API_BASE}/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const result = await res.json();

            document.getElementById(loadingId).remove();
            appendMessage(result.reply, 'assistant');

            // Update history
            chatHistory.push({ user: text, assistant: result.reply });

        } catch (err) {
            document.getElementById(loadingId).remove();
            appendMessage('Error communicating with the chat service.', 'assistant');
        }
    };

    if (sendBtn && chatInput) {
        sendBtn.addEventListener('click', handleChatSubmit);
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') handleChatSubmit();
        });
    }

    // 7. Voice Input Recording (Optional Extra for Transcribe)
    const voiceBtn = document.getElementById('voice-btn');
    if (voiceBtn && navigator.mediaDevices) {
        let mediaRecorder;
        let audioChunks = [];
        let isRecording = false;

        voiceBtn.addEventListener('click', async () => {
            if (isRecording) {
                // Stop recording
                mediaRecorder.stop();
                voiceBtn.classList.remove('recording');
                isRecording = false;
            } else {
                // Start recording
                try {
                    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                    mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
                    audioChunks = [];

                    mediaRecorder.addEventListener('dataavailable', event => {
                        audioChunks.push(event.data);
                    });

                    mediaRecorder.addEventListener('stop', async () => {
                        const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                        const formData = new FormData();
                        formData.append('audio', audioBlob, 'recording.webm');

                        chatInput.value = "Transcribing...";

                        try {
                            const response = await fetch(`${API_BASE}/transcribe-voice`, {
                                method: 'POST',
                                body: formData
                            });
                            const result = await response.json();
                            chatInput.value = result.text || "";
                        } catch (e) {
                            alert("Transcription error" + e);
                            chatInput.value = "";
                        }

                        // Stop all tracks to release mic
                        stream.getTracks().forEach(track => track.stop());
                    });

                    mediaRecorder.start();
                    voiceBtn.classList.add('recording');
                    isRecording = true;
                    setTimeout(() => {
                        if (isRecording) {
                            mediaRecorder.stop();
                            voiceBtn.classList.remove('recording');
                            isRecording = false;
                        }
                    }, 10000); // 10 second limit
                } catch (err) {
                    alert('Mic access denied or unavailable: ' + err);
                }
            }
        });
    }
});
