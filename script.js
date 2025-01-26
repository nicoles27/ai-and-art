document.addEventListener("DOMContentLoaded", function () {
    var canvas = document.getElementById("signature-pad");
    var signaturePad = new SignaturePad(canvas);

    function clearSignature() {
        signaturePad.clear();
    }

    document.getElementById("clear-signature").addEventListener("click", function () {
        clearSignature();
    });

    document.getElementById("consent-form").addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent default form submission

        // Check if signature is empty
        if (signaturePad.isEmpty()) {
            alert("Please provide a signature.");
            return;
        }

        // Convert signature to a base64 image and store it in a hidden input field
        var signatureData = signaturePad.toDataURL("image/png");
        document.getElementById("signature-data").value = signatureData;

        // Create form data
        var formData = new FormData(this);

        // Send form data to Formspree
        fetch("https://formspree.io/f/xldgrwzq", {
            method: "POST",
            body: formData,
            headers: { "Accept": "application/json" }
        })
        .then(response => response.json())
        .then(data => {
            alert("Form submitted successfully!");
            document.getElementById("consent-form").reset();
            clearSignature();
        })
        .catch(error => console.error("Error:", error));
    });
});