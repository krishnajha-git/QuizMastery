function copyUrl() {
    var copyText = document.getElementById("quiz-url");
    copyText.select();
    copyText.setSelectionRange(0, 99999); /* For mobile devices */
    document.execCommand("copy");
    alert("Copied the URL: " + copyText.value);
}

function exitQuiz() {
    window.history.back(); // Redirect to the previous page
}