document.getElementById("reportBtn").addEventListener("click", function() {
    var reportForm = document.getElementById("reportForm");
    if (reportForm.style.display === "none") {
        reportForm.style.display = "block";
    } else {
        reportForm.style.display = "none";
    }
});

document.getElementById("missingPersonForm").addEventListener("submit", function(event) {
    event.preventDefault(); 
    alert("Form submitted successfully!");
});