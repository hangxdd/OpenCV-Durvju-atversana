// Get references to the video element and the 2D context of the canvas
var video = document.getElementById('video');
var canvas = document.createElement('canvas');
var context = canvas.getContext('2d');

// Initialize the array to store the captured images and the image index
var images = [];
var imageIndex = 0;

// Get the user ID and the number of existing images for the user
var userId = document.getElementById('my-form').elements['user_id'].value;
var imagesCount = parseInt(document.getElementById('my-form').dataset.imagesCount);

// Initialize the image index in the session storage
sessionStorage.setItem('imageIndex_' + userId, imagesCount);

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
        var imageIndex = parseInt(sessionStorage.getItem('imageIndex_' + userId)) || 0;
        imageIndex++;
        sessionStorage.setItem('imageIndex_' + userId, imageIndex);

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
        imagesCount++;
    }

    // If the "Save" button is clicked
    if (targetId === 'save') {
        var imageIndex = parseInt(sessionStorage.getItem('imageIndex_' + userId)) || 0;
        var unique_filename = `captured_image${imageIndex}`;
        var formData = new FormData(document.getElementById('my-form'));
        images.forEach(function(image, index) {
            var block = image.split(";");
            var contentType = block[0].split(":")[1];
            var realData = block[1].split(",")[1];
            var blob = b64toBlob(realData, contentType);
            formData.append('captured_image' + (imagesCount + index), blob);
            imagesCount = imageIndex;
        });

        // Stop the camera
        var stream = video.srcObject;
        var tracks = stream.getTracks();
        for (var i = 0; i < tracks.length; i++) {
            var track = tracks[i];
            track.stop();
        }
        video.srcObject = null;

        // Send the form data and the captured images to your Django view
        var xhr = new XMLHttpRequest();
        var user_id = document.getElementById('my-form').elements['user_id'].value;
        xhr.open('POST', '/edit_user/' + user_id + '/', true);
        xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));  // Add the CSRF token
        xhr.send(formData);

        xhr.addEventListener('load', function() {
            if (xhr.status >= 200 && xhr.status < 300) {
                // The request has been completed successfully
                location.reload();
            }
        });

        document.getElementById('overlay').style.display = 'none';
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

// Function to convert base64 data to a blob
function b64toBlob(b64Data, contentType, sliceSize) {
    contentType = contentType || '';
    sliceSize = sliceSize || 512;
    var byteCharacters = atob(b64Data);
    var byteArrays = [];
    for (var offset = 0; offset < byteCharacters.length; offset += sliceSize) {
        var slice = byteCharacters.slice(offset, offset + sliceSize);
        var byteNumbers = new Array(slice.length);
        for (var i = 0; i < slice.length; i++) {
            byteNumbers[i] = slice.charCodeAt(i);
        }
        var byteArray = new Uint8Array(byteNumbers);
        byteArrays.push(byteArray);
    }
    var blob = new Blob(byteArrays, {type: contentType});
    return blob;
}

// Function to get a cookie by name
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}