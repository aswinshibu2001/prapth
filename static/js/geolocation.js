// geolocation.js

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function showPosition(position) {
    var latitude = position.coords.latitude;
    var longitude = position.coords.longitude;
    // You can do something with latitude and longitude, like populate hidden fields in the form
    document.getElementById("latitude").value = latitude;
    document.getElementById("longitude").value = longitude;
}
