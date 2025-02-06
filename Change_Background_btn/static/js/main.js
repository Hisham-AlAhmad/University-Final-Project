$(document).ready(function() {
    var canvas = document.getElementById('canvas');
    var ctx = canvas.getContext('2d');
    var image = document.getElementById('image');
    var parentDiv = document.querySelector('.image-section');
    var userImageContainer = document.getElementById('user-image-container');
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
            url: "{{ url_for('Change_Background_btn.upload_image') }}",
            data: formData,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                filename = data.filename;
                console.log(filename);
                image.src = '/Change_Background_btn/get_original_image/' + filename;
                console.log('Success upload!');
            }
        });
    });

    // this one here is for the user
    // Add an event listener to the file input field
    document.getElementById('user-imageUpload').addEventListener('change', function(event) {
        // Get the uploaded file
        var file = this.files[0];
                
        // Create a new FormData object
        var formData = new FormData();
        formData.append('user_image', file);
                
        // Send the file to the server using AJAX
        $.ajax({
            type: 'POST',
            url: "{{ url_for('Change_Background_btn.user_upload_image') }}",
            data: formData,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                // Get the uploaded image filename with extension
                var filename = data.filename;
                console.log(filename);
                filename_no_extension = filename.split('.').slice(0, -1).join('.');
                console.log(filename_no_extension);
                // Create a new image element
                var img = document.getElementById('user_img');
                img.src = '/Change_Background_btn/get_user_background/' + filename;
                img.style.width = '200px';
                img.style.height = '200px';
                img.classList.add('user-background-image');

                // Create a new link element
                var link = document.getElementById('a_user');
                link.href = '#' + filename_no_extension;
                // Ensure the container is visible
                userImageContainer.style.display = 'flex';
                // Ensure the image is visible
                img.style.display = 'block';
            
                console.log('Success user background uploaded!');
            },
            error: function(xhr, status, error) {
                console.error('Error uploading user image: ' + error.message);
            }
        });
    });
    
    $("#user_img").click(function() {
        var formData = new FormData($('#image-form')[0]);
        var src = event.target.src;
        var extension = src.match(/\.(jpg|png|jpeg)$/i)[1];
        var image_background = event.target.id + '.' + extension;
        console.log(image_background);
        var data = { filename: filename, image_background: image_background, is_user: true };
        $('.loader').show();
        $.ajax({
            type: 'POST',
            url: '/Change_Background_btn/change_background',
            data: JSON.stringify(data),
            contentType: 'application/json',
            success: function(data) {
                $('.loader').hide();
                $('#saveOriginalImage').show();
                $('.output-section').show();
                parentDiv.style.display = 'flex';
                originalFilename = data.filename;
                var img = new Image();
                img.src = '/Change_Background_btn/get_image/' + data.filename;
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
                console.log('Success changed background from user!');
            }
        });
    });

    document.querySelectorAll('.background-image').forEach(function(image) {
        image.addEventListener('click', function(event) {
            var src = event.target.src;
            var extension = src.match(/\.(jpg|png)$/i)[1];
            var image_background = event.target.id + '.' + extension;
            console.log(image_background);
            var data = { filename: filename, image_background: image_background, is_user: false };

            $('.loader').show();
            $.ajax({
                type: 'POST',
                url: '/Change_Background_btn/change_background',
                data: JSON.stringify(data),
                contentType: 'application/json',
                success: function(data) {
                    $('.loader').hide();
                    $('#saveOriginalImage').show();
                    $('.output-section').show();
                    parentDiv.style.display = 'flex';
                    originalFilename = data.filename;
                    var img = new Image();
                    img.src = '/Change_Background_btn/get_image/' + data.filename;
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
                    console.log('Success changed background from img!');
                }
            });
        });
    });

   
    document.getElementById('saveOriginalImage').addEventListener('click', function() {
        // Create a new Blob object from the original image URL
        fetch('/Change_Background_btn/get_image/' + originalFilename)
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
