document.addEventListener('DOMContentLoaded', function () {
    const container = document.getElementById('postPaymentContact');
    if (!container) return;

    const toggleBtn = document.getElementById('contactToggleBtn');
    const panel = document.getElementById('contactPanel');
    const input = document.getElementById('contactMessageInput');
    const whatsappBtn = document.getElementById('whatsappBtn');
    const emailBtn = document.getElementById('emailBtn');

    const WHATSAPP_NUMBER = '2349034055540'; // no +, no leading 0
    const EMAIL_ADDRESS = 'chesscoachlife@gmail.com';

    const clientName = container.dataset.clientName;
    const game = container.dataset.game;
    const date = container.dataset.date;
    const time = container.dataset.time;

    toggleBtn.addEventListener('click', function () {
        panel.classList.toggle('open');
        if (panel.classList.contains('open')) input.focus();
    });

    function buildMessage() {
        const typed = input.value.trim();
        if (typed) return typed;
        return `Hi, this is ${clientName}. I just booked a ${game} session on ${date} at ${time} and wanted to reach out.`;
    }

    function openWhatsApp() {
        const message = buildMessage();
        const url = `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(message)}`;
        window.open(url, '_blank', 'noopener');
    }

    whatsappBtn.addEventListener('click', openWhatsApp);

    input.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            openWhatsApp();
        }
    });

    emailBtn.addEventListener('click', function (e) {
        e.preventDefault();
        const message = buildMessage();
        const subject = encodeURIComponent(`LexiTutor booking - ${game} on ${date}`);
        const body = encodeURIComponent(message);
        window.location.href = `mailto:${EMAIL_ADDRESS}?subject=${subject}&body=${body}`;
    });
});