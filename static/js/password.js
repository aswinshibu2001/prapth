function resetPasswordRequest() {
    var email = document.querySelector('.input-box input[type="email"]').value;

    if (emailIsValid(email) && emailExistsInDatabase(email)) {
        document.querySelector('.reset-password-section').style.display = 'block';
    } else {
        alert("Invalid email or email not found.");
    }
}

function resetPassword() {
    var newPassword = document.getElementById('newPassword').value;
    var confirmPassword = document.getElementById('confirmPassword').value;

    if (newPassword === confirmPassword) {
        alert("Password reset successfully.");
    } else {
        alert("Passwords do not match. Please try again.");
    }
}

function emailIsValid(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function emailExistsInDatabase(email) {
    return true;
}
