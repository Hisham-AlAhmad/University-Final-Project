$(document).ready(function() {
    var canvas = document.getElementById('canvas');
    var ctx = canvas.getContext('2d');
    var image = document.getElementById('image');
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
        // var fileInput = $(this)[0];
        // var filename = fileInput.files[0].name;
        // filename = changeExtension(filename);
        var formData = new FormData($('#image-form')[0]);
        $.ajax({
            type: 'POST',
            url: "{{ url_for('Enhance_btn.upload_image') }}",
            data: formData,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                filename = data.filename;
                console.log(filename);
                image.src = '/Enhance_btn/get_original_image/' + filename;
                console.log('Success upload!');
            }
        });
    });

    $('#enhance-button').on('click', function(event) {
        $.ajax({
            type: 'POST',
            url: '/Enhance_btn/enhance_image',
            data: JSON.stringify({filename: filename }),
            contentType: 'application/json',
            success: function(data) {
                $('#saveOriginalImage').show();
                $('.output-section').show();
                parentDiv.style.display = 'flex';
                originalFilename = filename;
                var img = new Image();
                img.src = '/Enhance_btn/get_image/' + filename;
                // adding the image with the aspect ratio
                img.onload = function() {
                    var canvas = document.createElement('canvas');
                    var ctx = canvas.getContext('2d');
                    var aspectRatio = img.width / img.height;
                    var canvasWidth, canvasHeight;
                    if (aspectRatio > 1) {
                        canvasWidth = 500;
                        canvasHeight = canvasWidth / aspectRatio;
                    } else {
                        canvasHeight = 500;
                        canvasWidth = canvasHeight * aspectRatio;
                    }
                    canvas.width = canvasWidth;
                    canvas.height = canvasHeight;
                    // drawImage(image, start_x, start_y, width, height)
                    ctx.drawImage(img, 0, 0, canvasWidth, canvasHeight);
                    var resizedImage = canvas.toDataURL('image/png');
                    var imgElement = document.createElement('img');
                    imgElement.src = resizedImage;
                    imgElement.alt = 'Resized Image';
                    document.getElementById('imagePreview').innerHTML = '';
                    document.getElementById('imagePreview').appendChild(imgElement);
                };
                console.log('Success Crop!');
            }
        });
    });

    document.getElementById('saveOriginalImage').addEventListener('click', function() {
        // Create a new Blob object from the original image URL
        fetch('/Enhance_btn/get_image/' + originalFilename)
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