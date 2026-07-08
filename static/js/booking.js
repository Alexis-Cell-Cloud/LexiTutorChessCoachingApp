document.addEventListener('DOMContentLoaded', function () {
    const dateInput = document.getElementById(bookingConfig.dateFieldId);
    const timeInput = document.getElementById(bookingConfig.timeFieldId);
    const slotGrid = document.getElementById('slot-grid');
    const slotHint = document.getElementById('slot-hint');
    const onlineWarning = document.getElementById('online-warning');

    const startHour = 6;
    const endHour = 23;

    dateInput.addEventListener('change', function () {
        const selectedDate = dateInput.value;
        if (!selectedDate) return;

        slotHint.textContent = 'Loading available times...';
        slotGrid.innerHTML = '';

        fetch(`/booking/available-slots/?date=${selectedDate}`)
            .then(response => response.json())
            .then(data => {
                buildSlotGrid(data.blocked_hours);
                slotHint.textContent = 'Select a start time:';
            })
            .catch(() => {
                slotHint.textContent = 'Could not load times. Please try again.';
            });
    });

    function buildSlotGrid(blockedHours) {
        slotGrid.innerHTML = '';
        timeInput.value = '';

        for (let hour = startHour; hour <= endHour; hour++) {
            const hourStr = hour.toString().padStart(2, '0') + ':00';
            const button = document.createElement('button');
            button.type = 'button';
            button.textContent = formatHour(hour);
            button.className = 'slot-button';

            const isBlocked = blockedHours.includes(hourStr);

            if (isBlocked) {
                button.disabled = true;
                button.classList.add('slot-blocked');
            } else {
                button.addEventListener('click', function () {
                    selectSlot(hourStr, hour, button);
                });
            }

            slotGrid.appendChild(button);
        }
    }

    function selectSlot(hourStr, hour, button) {
        timeInput.value = hourStr;

        document.querySelectorAll('.slot-button').forEach(b => b.classList.remove('slot-selected'));
        button.classList.add('slot-selected');

        if (hour < 8 || hour >= 20) {
            onlineWarning.style.display = 'block';
        } else {
            onlineWarning.style.display = 'none';
        }
    }

    function formatHour(hour) {
        const period = hour >= 12 ? 'PM' : 'AM';
        let displayHour = hour % 12;
        if (displayHour === 0) displayHour = 12;
        return `${displayHour}:00 ${period}`;
    }
});