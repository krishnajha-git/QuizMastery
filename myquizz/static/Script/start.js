function updateOrderAndSubmit(selectElement) {
    const selectedOption = selectElement.options[selectElement.selectedIndex];
    const orderField = document.getElementById('order-field');

    // Set the 'order' field based on the selected option
    if (selectedOption.text.includes('DESC')) {
        orderField.value = 'desc';
    } else {
        orderField.value = 'asc';
    }

    // Submit the form
    selectElement.form.submit();
}
function confirmDelete(button) {
    if (confirm("Are you sure you want to delete this quiz?")) {
        // Find the form associated with the delete button and submit it
        button.closest('form').submit();
    }
}
function confirmDelete1(button) {
    if (confirm("Are you sure you want to delete this question?")) {
        // Find the form associated with the delete button and submit it
        button.closest('form').submit();
    }
}
function updateOption(inputId, outputId) {
    const inputValue = document.getElementById(inputId).value;
    document.getElementById(outputId).textContent = inputValue;
}