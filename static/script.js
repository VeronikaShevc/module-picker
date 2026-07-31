const checkboxes = document.querySelectorAll('input[type="checkbox"]');
const counter = document.getElementById('selected-count');

function updateCount() {
    let count = 0;
    checkboxes.forEach(box => {
        if (box.checked) count++;
    });
    counter.textContent = count + " modules selected";
}

checkboxes.forEach(box => {
    box.addEventListener('change', updateCount);
});

updateCount();