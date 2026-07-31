// Setup

// Grab every checkbox on the page once & 2 areas we update.
var checkboxes = document.querySelectorAll('input[type="checkbox"]');
var counterText = document.getElementById('selected-count');
var selectedListArea = document.getElementById('selected-list');

// localStorage is the browser's own small storage box - it survives
// page reloads, unlike a normal JavaScript variable which would reset
// every time. We use it here so ticked modules aren't lost when a
// filter dropdown reloads the page.
// savedModules looks like: { "CS1002": "Object-Oriented Programming" }
var storedText = localStorage.getItem('passedModules');
var savedModules;
if (storedText) {
    savedModules = JSON.parse(storedText);
} else {
    savedModules = {};
}


// Functions 

// Runs once when the page loads. Re-ticks any checkbox that's
// currently visible AND was saved from before a filter change.
function restoreCheckboxes() {
    for (var i = 0; i < checkboxes.length; i++) {
        var box = checkboxes[i];
        var code = box.value;
        if (savedModules[code]) {
            box.checked = true;
        }
    }
}

// Rebuilds the "Your selections" list from scratch using savedModules.
// We rebuild the whole list rather than editing it piece by piece -
// with only a handful of ticked modules at a time, this is simple and
// fast enough, and much easier to get right than trying to patch an
// existing list in place.
function showSelectedList() {
    var codes = Object.keys(savedModules);

    if (codes.length === 0) {
        selectedListArea.innerHTML = "<p><em>No modules selected yet.</em></p>";
        return;
    }

    var html = "<p><strong>Your selections:</strong></p><ul>";
    for (var i = 0; i < codes.length; i++) {
        var code = codes[i];
        var name = savedModules[code];
        html += "<li>" + code + " - " + name;
        html += " <button type='button' onclick=\"removeOneSelection('" + code + "')\">Remove</button></li>";
    }
    html += "</ul>";
    selectedListArea.innerHTML = html;
}

// The main function - runs every time any checkbox is ticked/unticked.
// Syncs savedModules to match what's actually checked right now, then
// updates the counter, saves to localStorage, and redraws the list.
function updateEverything() {
    var countTicked = 0;

    for (var i = 0; i < checkboxes.length; i++) {
        var box = checkboxes[i];
        var code = box.value;

        if (box.checked) {
            countTicked = countTicked + 1;
            // allModuleNames comes from the HTML file - it only has
            // names for modules currently visible on this page. This
            // is why a module must be visible at least once while you
            // tick it - we can't look up a name we were never given.
            savedModules[code] = allModuleNames[code].name;
        } else {
            delete savedModules[code];
        }
    }

    counterText.textContent = countTicked + " modules selected";
    localStorage.setItem('passedModules', JSON.stringify(savedModules));
    showSelectedList();
}

// Called when someone clicks "Remove" in the selections list.
function removeOneSelection(code) {
    delete savedModules[code];
    localStorage.setItem('passedModules', JSON.stringify(savedModules));

    // If that module's checkbox is visible right now, untick it too,
    // so the checklist and the selections list stay in sync.
    for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].value === code) {
            checkboxes[i].checked = false;
        }
    }

    updateEverything();
}


// Wiring it all together 

// Whenever any checkbox changes, re-run updateEverything.
for (var i = 0; i < checkboxes.length; i++) {
    checkboxes[i].addEventListener('change', updateEverything);
}

// Run once immediately when the page loads.
restoreCheckboxes();
updateEverything();