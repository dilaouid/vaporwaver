var onRequest = false;

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
            $('#img').val(e.target.result.split(',')[1]);
        }
        reader.readAsDataURL(input.files[0]);
    }
}

$('input[type=file]').change(function(){
    readURL(this);
});

$('#importFileStyleBtn').on('click', function(){
    $('#importFile').click();
});

$('.processBtn').on('click', () => {
    if (onRequest === true) { return; }
    onRequest = true;
    let form = $('#form');
    $('.errorMsg').addClass('d-none');
    $('#process').addClass('d-none');
    $('#spinner').removeClass('d-none');
    $.ajax({
        type: "POST",
        url: form.attr( 'action' ),
        data: form.serialize(),
        success: function( data ) {
            if (data.success === 0) {
                $('.errorMsg').removeClass('d-none').html(`<span>${data.msg}</span>`);
            } else {
                $('#preview').attr('src', data.base64)
            }
            $('#process').removeClass('d-none');
            $('#spinner').addClass('d-none');
            onRequest = false;
        }
    });
});