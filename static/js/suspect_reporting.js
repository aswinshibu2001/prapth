const imageInput = document.getElementById('imageInput');
    const uploadedImage = document.getElementById('uploadedImage');
    document.addEventListener('DOMContentLoaded', function() {
    imageInput.onchange = function(e) {
      if (e.target.files && e.target.files[0]) {
        // Get the uploaded image file
        const imageFile = e.target.files[0];
  
        // Create a URL object to preview the image
        const imageUrl = URL.createObjectURL(imageFile);
  
        // Set the image source of the uploadedImage element
        uploadedImage.src = imageUrl;
  
        // Display the uploaded image
        uploadedImage.style.display = 'block';
      }
    };
});