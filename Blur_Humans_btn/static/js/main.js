const inputv = document.querySelector("#blur_ratio");
const perc = document.getElementById("percentage");
inputv.addEventListener("input",() => {perc.innerHTML = inputv.value +"%";});
var parentDiv = document.querySelector('.image-section');
var originalFilename = 'filename';
// Init
$(document).ready(function () {
    $('.image-section').hide();
    $('.loader').hide();
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload").change(function () {
    $('.image-section').show();
    readURL(this);
    });
    
    $('#btn-blur').click(function () {
        var form_data = new FormData($('#upload-file')[0]);
        // Show loading animation
        $(this).hide();
        $('.loader').show();
        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/blur',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                parentDiv.style.display = 'flex';
                $('.loader').hide();
                $('.output-section').show();
                $('#saveOriginalImage').show();
                $('#btn-blur').show();
                // getting the 'filename' from the flask responce
                var filename = data.filename;
                originalFilename = filename;
                // Create an image element and set its source to the filename
                var img = document.createElement('img');
                img.src = '/uploads/output/' + filename; 
                // Add the image element to the #imagePreview div
                $('#imagePreview2').html(img);
                // Resize the image using the Image object
                var imgObj = new Image();
                imgObj.src = '/uploads/output/' + filename;
                imgObj.onload = function() {
                    var canvas = document.createElement('canvas');
                    canvas.width = 256;
                    canvas.height = 256;
                    var ctx = canvas.getContext('2d');
                    ctx.drawImage(imgObj, 0, 0, 256, 256);
                    var resizedImage = canvas.toDataURL('image/png');
                    var imgElement = document.createElement('img');
                    imgElement.src = resizedImage;
                    imgElement.alt = 'Resized Image';
                    document.getElementById('imagePreview2').innerHTML = '';
                    document.getElementById('imagePreview2').appendChild(imgElement);
                };
                console.log('Success!');
            },
        });
    });
});
// Add a click event listener to the "Save Original Image" button
document.getElementById('saveOriginalImage').addEventListener('click', function() {
    // Create a new Blob object from the original image URL
    fetch('/uploads/output/' + originalFilename)
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