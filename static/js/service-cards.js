document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.service-card').forEach(function (card) {
        card.addEventListener('click', function () {
            card.classList.toggle('expanded');
            const hint = card.querySelector('.expand-hint');
            if (hint) {
                hint.textContent = card.classList.contains('expanded') ? 'Tap to collapse' : 'Tap for details';
            }
        });
    });
});