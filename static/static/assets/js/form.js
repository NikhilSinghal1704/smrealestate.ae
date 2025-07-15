



$(document).ready(function() {
    $('#contact-form').submit(function(e) {
        e.preventDefault();  // Prevent the default form submission

        $.ajax({
            type: 'POST',
            url: '/contact/',  // Update the URL to match your view's URL
            data: $(this).serialize(),
            success: function(response) {
                if (response.success) {
                    // alert(response.success);
                    // Handle success, e.g., clear form fields
                    Swal.fire(
                        'Good job!',
                        'Contact submitted successfully!',
                        'success'
                      )
                }
            },
            error: function(response) {
                if (response.responseJSON && response.responseJSON.errors) {
                    // Handle form validation errors, e.g., display error messages
                    
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: 'Form submission failed. Please check the fields.!',
                        
                      })
                }
            }
        });
    });
});





$(document).ready(function() {
    $("#book-form").on("submit", function(event) {
        event.preventDefault();  
        
        $.ajax({
            type: "POST",
            url: "/bookappointment/",  
            data: $(this).serialize(),
            success: function(response) {
                
                Swal.fire(
                    'Good job!',
                    'Appointment submitted successfully!',
                    'success'
                  )
                
            },
            error: function(data) {
                
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Form submission failed. Please check the fields.!',
                    
                  })
                
            }
        });
    });
});





$(document).ready(function() {
		
    $('.comprassion-button').on('click', function() {
        var product_id = $(this).data('product-id');
        var csrf_token = $('[name=csrfmiddlewaretoken]').val();

        $.ajax({
            url: '/add_to_comparission/'+product_id+'/',
            method: 'GET',
            
            success: function(response) {
                
                Swal.fire(
                    'Good job!',
                    'add in comparison list !',
                    'success'
                  )
                
            }
        });
    });
});




$(document).ready(function() {
    
    $('.favorite-button').on('click', function() {
        
        var product_id = $(this).data('product-id');
        var csrf_token = $('[name=csrfmiddlewaretoken]').val();

        $.ajax({
            url: '/add_to_favorites/'+product_id+'/',
            method: 'GET',
            
            success: function(response) {
                Swal.fire(
                    'Good job!',
                    'add in favorite list !',
                    'success'
                  )
                
                
            }
        });
    });
});



$(document).ready(function() {
    
    $('#clear-button').on('click', function() {
        // var product_id = $(this).data('product-id');
        // var csrf_token = $('[name=csrfmiddlewaretoken]').val();

        $.ajax({
            url: '/clear_session_list/',
            method: 'GET',
            
            success: function(response) {
                
            }
        });
    });
});






function validateFile() {
    const rimg = document.getElementById('rimg');
    const validationMessage = document.getElementById('validationMessage');

    if (rimg.files.length > 0) {
        const selectedFile = rimg.files[0];
        const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];

        if (allowedTypes.includes(selectedFile.type)) {
            validationMessage.textContent = "";
        } else {
            validationMessage.textContent = "Invalid file type. Please select an image file.";
            rimg.value = ''; // Clear the input field
        }
    } else {
        validationMessage.textContent = "No file selected.";
    }
}

















