$(document).ready(function() {
    var canvas = document.getElementById('canvas');
    var ctx = canvas.getContext('2d');
    var image = document.getElementById('image');
    var output_image = document.getElementById('output_image');
    var parentDiv = document.querySelector('.image-section');
    var originalFilename = 'filename';
    var cropRect = {};
    var isDragging = false;
    var originalImageWidth, originalImageHeight;
    var resizedImageWidth, resizedImageHeight;
    var filename;

    // Add an event listener to the image to wait for it to load
    image.addEventListener('load', function() {
        originalImageWidth = image.width;
        originalImageHeight = image.height;

        // Resize the image to fit the canvas while maintaining the aspect ratio
        var canvasWidth = canvas.width;
        var canvasHeight = canvas.height;
        var aspectRatio = originalImageWidth / originalImageHeight;
        if (aspectRatio > canvasWidth / canvasHeight) {
            resizedImageWidth = canvasWidth;
            resizedImageHeight = canvasWidth / aspectRatio;
        } else {
            resizedImageWidth = canvasHeight * aspectRatio;
            resizedImageHeight = canvasHeight;
        }

        canvas.width = resizedImageWidth;
        canvas.height = resizedImageHeight;
        ctx.drawImage(image, 0, 0, resizedImageWidth, resizedImageHeight);
    });

    $("#imageUpload").change(function() {
        var formData = new FormData($('#image-form')[0]);
        $.ajax({
            type: 'POST',
            url: '/Crop_btn/upload_image',
            data: formData,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                filename = data.filename;
                image.src = '/Crop_btn/get_original_image/' + filename;
                console.log('Success upload!');
            }
        });
    });

    canvas.addEventListener('mousedown', function(event) {
        cropRect.startX = event.offsetX;
        cropRect.startY = event.offsetY;
        isDragging = true;
    });

    canvas.addEventListener('mousemove', function(event) {
        if (isDragging) {
            cropRect.endX = event.offsetX;
            cropRect.endY = event.offsetY;
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(image, 0, 0, resizedImageWidth, resizedImageHeight);
            ctx.strokeStyle = 'red';
            ctx.strokeRect(cropRect.startX, cropRect.startY, cropRect.endX - cropRect.startX, cropRect.endY - cropRect.startY);
        }
    });

    canvas.addEventListener('mouseup', function(event) {
        isDragging = false;
        cropRect.endX = event.offsetX;
        cropRect.endY = event.offsetY;
        $('#crop-button').prop('disabled', false);
    });

    $('#crop-button').on('click', function(event) {
        event.preventDefault();
        var x1 = cropRect.startX;
        var y1 = cropRect.startY;
        var x2 = cropRect.endX;
        var y2 = cropRect.endY;
        if (!x1 ||!y1 ||!x2 ||!y2) {
            alert('Please select a crop area');
            return;
        }

        // Scale the crop coordinates to the original image size
        x1 = x1 * originalImageWidth / resizedImageWidth;
        y1 = y1 * originalImageHeight / resizedImageHeight;
        x2 = x2 * originalImageWidth / resizedImageWidth;
        y2 = y2 * originalImageHeight / resizedImageHeight;

        $.ajax({
            type: 'POST',
            url: '/Crop_btn/crop_image',
            data: JSON.stringify({ x1: x1, y1: y1, x2: x2, y2: y2, filename: filename }),
            contentType: 'application/json',
            success: function(data) {
                $('#saveOriginalImage').show();
                $('.output-section').show();
                parentDiv.style.display = 'flex';
                originalFilename = data.filename;
                output_image.src = '/Crop_btn/get_image/' + data.filename;

                console.log('Success Crop!');
            }
        });
    });

    document.getElementById('saveOriginalImage').addEventListener('click', function() {
        // Create a new Blob object from the original image URL
        fetch('/Crop_btn/get_image/' + originalFilename)
            .then(function(response) {
                return response.blob();
            })
            .then(function(blob) {
                // Create a new URL object from the Blob object
                var url = URL.createObjectURL(blob);
                // Create a new link element
                var link = document.createElement('a');
                // Set the href attribute of the link element to the new URL
                link.href = url;
                // Set the download attribute of the link element to the original image filename
                link.download = originalFilename;
                // Programmatically click the link element to download the image
                link.click();
                // Revoke the object URL after the download is complete
                URL.revokeObjectURL(url);
            });
    });
});