document.querySelectorAll('select').forEach(dropdown => {
    if (dropdown.options.namedItem('Pass')) {
        dropdown.value = 'Pass'; // Select the 'Pass' option if it exists
    } else {
        dropdown.selectedIndex = 0; // Optionally, select the first option if 'Pass' is not available
    }
});