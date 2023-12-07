// Get references to the video element and the 2D context of the canvas
var video = document.getElementById('video');
var canvas = document.createElement('canvas');
var context = canvas.getContext('2d');

// Initialize the array to store the captured images and the image index
var images = [];
var imageIndex = 0;

// Initialize the image index in the session storage
sessionStorage.setItem('imageIndex', imageIndex);

// Function to start the camera
function startCamera() {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
            video.srcObject = stream;
            video.play().catch(function(error) {
                console.log('Failed to start video playback:', error);
            });
        });
    }
}

// Event listener for click events
document.body.addEventListener('click', function(e) {
    var targetId = e.target.id;

    // If the "Capture Images" button is clicked
    if (targetId === 'capture-images') {
        document.getElementById('overlay').style.display = 'block';
        startCamera();
    }

    // If the "Close Overlay" button is clicked
    if (targetId === 'close-overlay') {
        var stream = video.srcObject;
        var tracks = stream.getTracks();

        for (var i = 0; i < tracks.length; i++) {
            var track = tracks[i];
            track.stop();
        }

        video.srcObject = null;
        document.getElementById('overlay').style.display = 'none';
    }

    // If the "Capture" button is clicked
    if (targetId === 'capture') {
        var imageIndex = parseInt(sessionStorage.getItem('imageIndex')) || 0;
        imageIndex++;
        sessionStorage.setItem('imageIndex', imageIndex);

        // Capture the image from the video stream
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.save();
        context.scale(-1, 1);
        context.drawImage(video, 0, 0, canvas.width * -1, canvas.height);
        context.restore();
        var dataUrl = canvas.toDataURL('image/png');
        images.push(dataUrl);

        // Create the image container and append it to the DOM
        var imgContainer = document.createElement('div');
        imgContainer.className = 'flex items-center mt-4';

        var checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.name = 'delete_images';
        checkbox.value = 'captured_image' + imageIndex;
        imgContainer.appendChild(checkbox);

        var img = document.createElement('img');
        img.src = dataUrl;
        img.className = 'h-24 w-24 object-cover ml-4';
        imgContainer.appendChild(img);

        var imgDetails = document.createElement('p');
        imgDetails.className = 'ml-4';
        var size = Math.round((dataUrl.length * 3/4) / 1024);  // Size in kilobytes
        imgDetails.textContent = 'captured_image' + imageIndex + '.png (' + size + ' KB)';
        imgContainer.appendChild(imgDetails);

        document.getElementById('captured-images').appendChild(imgContainer);
    }

    // If the "Save" button is clicked
    if (targetId === 'save') {
        // Stop the camera
        var stream = video.srcObject;
        var tracks = stream.getTracks();
        for (var i = 0; i < tracks.length; i++) {
            var track = tracks[i];
            track.stop();
        }
        video.srcObject = null;
        document.getElementById('overlay').style.display = 'none';

        // Get the form element
        var form = document.getElementById('my-form');

        // For each captured image
        for (var i = 0; i < images.length; i++) {
            // Create a hidden input element
            var input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'captured_image' + i;
            input.value = images[i];

            // Append the hidden input element to the form
            form.appendChild(input);
        }
    }

    // If the "Delete Selected" button is clicked
    if (targetId === 'delete-selected') {
        // Get all the checkboxes for the captured images
        var checkboxes = document.querySelectorAll('input[name="delete_images"]');
        // Loop through the checkboxes
        for (var i = 0; i < checkboxes.length; i++) {
            var checkbox = checkboxes[i];
            // If the checkbox is checked
            if (checkbox.checked) {
                // Remove the corresponding image from the images array
                var imageIndex = parseInt(checkbox.value.replace('captured_image', ''));
                images.splice(imageIndex, 1);
                // Remove the corresponding image from the DOM
                var imgContainer = checkbox.parentNode;
                imgContainer.parentNode.removeChild(imgContainer);
            }
        }
    }
});