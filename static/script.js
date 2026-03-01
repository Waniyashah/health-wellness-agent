// ============================================
// HEALTH WELLNESS AGENT - Chat UI Logic
// ============================================

(function () {
    "use strict";

    // --- DOM Elements ---
    const chatContainer = document.getElementById("chatContainer");
    const chatMessages = document.getElementById("chatMessages");
    const chatInput = document.getElementById("chatInput");
    const sendBtn = document.getElementById("sendBtn");
    const resetBtn = document.getElementById("resetBtn");
    const minimizeBtn = document.getElementById("minimizeBtn");
    const chatBubble = document.getElementById("chatBubble");
    const quickReplies = document.getElementById("quickReplies");

    // --- State ---
    let sessionId = generateId();
    let isWaiting = false;

    // --- Helpers ---
    function generateId() {
        return "s_" + Math.random().toString(36).slice(2, 11);
    }

    function getTime() {
        return new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
    }

    function escapeHtml(text) {
        const div = document.createElement("div");
        div.textContent = text;
        return div.innerHTML;
    }

    /** Convert basic markdown-like formatting to HTML */
    function formatMessage(text) {
        if (!text) return "";
        let html = escapeHtml(text);

        // Bold: **text** or __text__
        html = html.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
        html = html.replace(/__(.*?)__/g, "<strong>$1</strong>");

        // Headers: ### text
        html = html.replace(/^### (.+)$/gm, "<h4>$1</h4>");
        html = html.replace(/^## (.+)$/gm, "<h3>$1</h3>");

        // Bullet lists: - item
        html = html.replace(/^- (.+)$/gm, "<li>$1</li>");
        html = html.replace(/((?:<li>.*<\/li>\n?)+)/g, "<ul>$1</ul>");

        // Numbered lists: 1. item
        html = html.replace(/^\d+\.\s+(.+)$/gm, "<li>$1</li>");

        // Line breaks
        html = html.replace(/\n/g, "<br>");

        // Clean up <br> right after block elements
        html = html.replace(/<\/(h[34]|ul|ol|li)><br>/g, "</$1>");
        html = html.replace(/<br><(h[34]|ul|ol)/g, "<$1");

        return html;
    }

    // --- Scroll to bottom ---
    function scrollToBottom() {
        requestAnimationFrame(() => {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        });
    }

    // --- Add Bot Message ---
    function addBotMessage(text, skipAnimation) {
        const row = document.createElement("div");
        row.className = "message-row bot";

        row.innerHTML = `
            <div class="msg-avatar">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 2a4 4 0 0 1 4 4v1H8V6a4 4 0 0 1 4-4z"/>
                    <rect x="3" y="7" width="18" height="13" rx="3"/>
                    <circle cx="9" cy="13" r="1.5"/>
                    <circle cx="15" cy="13" r="1.5"/>
                    <path d="M9 17h6"/>
                </svg>
            </div>
            <div>
                <div class="message-bubble">${formatMessage(text)}</div>
                <div class="msg-time">${getTime()}</div>
            </div>
        `;

        if (skipAnimation) row.style.animation = "none";
        chatMessages.appendChild(row);
        scrollToBottom();
    }

    // --- Add User Message ---
    function addUserMessage(text) {
        const row = document.createElement("div");
        row.className = "message-row user";

        row.innerHTML = `
            <div>
                <div class="message-bubble">${escapeHtml(text)}</div>
                <div class="msg-time">${getTime()}</div>
            </div>
        `;

        chatMessages.appendChild(row);
        scrollToBottom();
    }

    // --- Add Typing Indicator ---
    function showTyping() {
        const row = document.createElement("div");
        row.className = "message-row bot";
        row.id = "typingRow";

        row.innerHTML = `
            <div class="msg-avatar">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 2a4 4 0 0 1 4 4v1H8V6a4 4 0 0 1 4-4z"/>
                    <rect x="3" y="7" width="18" height="13" rx="3"/>
                    <circle cx="9" cy="13" r="1.5"/>
                    <circle cx="15" cy="13" r="1.5"/>
                    <path d="M9 17h6"/>
                </svg>
            </div>
            <div class="message-bubble" style="padding: 6px 12px;">
                <div class="typing-indicator">
                    <span></span><span></span><span></span>
                </div>
            </div>
        `;

        chatMessages.appendChild(row);
        scrollToBottom();
    }

    function hideTyping() {
        const el = document.getElementById("typingRow");
        if (el) el.remove();
    }

    // --- Show Quick Replies ---
    function showQuickReplies(buttons) {
        quickReplies.innerHTML = "";
        buttons.forEach(function (label) {
            const btn = document.createElement("button");
            btn.className = "quick-reply-btn";
            btn.textContent = label;
            btn.addEventListener("click", function () {
                quickReplies.innerHTML = "";
                sendMessage(label);
            });
            quickReplies.appendChild(btn);
        });
    }

    function clearQuickReplies() {
        quickReplies.innerHTML = "";
    }

    // --- Show Context Panel ---
    function showContextPanel(ctx) {
        if (!ctx || Object.keys(ctx).length === 0) return;

        const panel = document.createElement("div");
        panel.className = "context-panel";

        let inner = `<h4>
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
            Session Context Updated
        </h4>`;

        if (ctx.goal) {
            const g = ctx.goal;
            inner += `<div class="context-item"><span class="label">Goal:</span><span class="value">${escapeHtml(g.action)} ${g.quantity}${g.metric} in ${escapeHtml(g.duration || "")}</span></div>`;
        }
        if (ctx.meal_plan) {
            inner += `<div class="context-item"><span class="label">Meals:</span><span class="value">${ctx.meal_plan.length} meals planned</span></div>`;
        }
        if (ctx.workout_plan) {
            const days = Object.keys(ctx.workout_plan).join(", ");
            inner += `<div class="context-item"><span class="label">Workouts:</span><span class="value">${escapeHtml(days)}</span></div>`;
        }
        if (ctx.progress_logs && ctx.progress_logs.length > 0) {
            inner += `<div class="context-item"><span class="label">Logs:</span><span class="value">${ctx.progress_logs.length} progress update(s)</span></div>`;
        }
        if (ctx.checkin_schedule) {
            inner += `<div class="context-item"><span class="label">Check-ins:</span><span class="value">${ctx.checkin_schedule.join(", ")}</span></div>`;
        }

        panel.innerHTML = inner;

        // Wrap in a bot message row
        const row = document.createElement("div");
        row.className = "message-row bot";
        row.innerHTML = `<div class="msg-avatar" style="opacity:0;pointer-events:none;"><svg viewBox="0 0 24 24"></svg></div>`;
        row.appendChild(panel);

        chatMessages.appendChild(row);
        scrollToBottom();
    }

    // --- Send Message ---
    async function sendMessage(text) {
        if (isWaiting) return;
        const message = (text || chatInput.value).trim();
        if (!message) return;

        // Show user bubble
        addUserMessage(message);
        chatInput.value = "";
        clearQuickReplies();

        // Show typing & disable input
        isWaiting = true;
        sendBtn.disabled = true;
        showTyping();

        try {
            const res = await fetch("/api/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: message, session_id: sessionId }),
            });

            hideTyping();

            if (!res.ok) {
                const err = await res.json().catch(() => ({}));
                throw new Error(err.error || "Server error " + res.status);
            }

            const data = await res.json();

            // Show bot reply
            addBotMessage(data.reply);

            // Show context panel if context was updated
            if (data.context && Object.keys(data.context).length > 0) {
                showContextPanel(data.context);
            }

            // Determine smart quick replies based on context
            updateQuickReplies(data.context);

        } catch (err) {
            hideTyping();
            addErrorMessage("Oops! " + err.message);
        } finally {
            isWaiting = false;
            sendBtn.disabled = false;
            chatInput.focus();
        }
    }

    function addErrorMessage(text) {
        const row = document.createElement("div");
        row.className = "message-row bot";
        row.innerHTML = `
            <div class="msg-avatar" style="background:#DC2626;">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" width="16" height="16"><path d="M12 9v4"/><path d="M12 17h.01"/><circle cx="12" cy="12" r="10"/></svg>
            </div>
            <div>
                <div class="message-bubble error-bubble">${escapeHtml(text)}</div>
            </div>
        `;
        chatMessages.appendChild(row);
        scrollToBottom();
    }

    // --- Smart Quick Replies ---
    function updateQuickReplies(ctx) {
        if (!ctx || Object.keys(ctx).length === 0) {
            // Initial suggestions
            showQuickReplies([
                "Create a diet plan",
                "Set a fitness goal",
                "Log my progress",
            ]);
            return;
        }

        const suggestions = [];
        if (!ctx.goal) suggestions.push("Set a fitness goal");
        if (!ctx.meal_plan) suggestions.push("Create a diet plan");
        if (!ctx.workout_plan) suggestions.push("Get workout plan");
        if (ctx.goal && ctx.meal_plan) suggestions.push("Log my progress");
        if (ctx.progress_logs && ctx.progress_logs.length > 0) suggestions.push("Get improvement tips");
        suggestions.push("Show my plan summary");

        showQuickReplies(suggestions.slice(0, 3));
    }

    // --- Reset Session ---
    async function resetSession() {
        try {
            await fetch("/api/reset", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ session_id: sessionId }),
            });
        } catch (_) { }

        sessionId = generateId();
        chatMessages.innerHTML = "";
        clearQuickReplies();
        showWelcome();
        chatInput.focus();
    }

    // --- Minimize / Restore ---
    function minimizeChat() {
        chatContainer.style.display = "none";
        chatBubble.style.display = "flex";
    }

    function restoreChat() {
        chatBubble.style.display = "none";
        chatContainer.style.display = "flex";
        chatContainer.style.animation = "slideUp 0.4s cubic-bezier(0.16,1,0.3,1)";
        chatInput.focus();
    }

    // --- Welcome Message ---
    function showWelcome() {
        addBotMessage(
            "Hi there! 👋 I'm your **Health & Wellness Assistant**.\n\nI can help you with:\n- 🥗 Personalized diet plans\n- 💪 Weekly workout routines\n- 📊 Progress tracking\n- 💡 Improvement suggestions\n\nWhat would you like to start with?",
            true
        );
        showQuickReplies([
            "Create a diet plan",
            "Set a fitness goal",
            "Log my progress",
        ]);
    }

    // --- Event Listeners ---
    sendBtn.addEventListener("click", function () {
        sendMessage();
    });

    chatInput.addEventListener("keydown", function (e) {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    resetBtn.addEventListener("click", function () {
        resetSession();
    });

    minimizeBtn.addEventListener("click", function () {
        minimizeChat();
    });

    chatBubble.addEventListener("click", function () {
        restoreChat();
    });

    // --- Init ---
    showWelcome();
    chatInput.focus();
})();
