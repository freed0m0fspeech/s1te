$('#test_button').on('click', function(e) {
    e.preventDefault();

    window.Telegram.Login.auth(
        { bot_id: '2037332308', request_access: true },
        (data) => {
            if (!data) {
                // authorization failed
                console.log('telegram authorization failed')
            }else {
                // Here you would want to validate data like described there https://core.telegram.org/widgets/login#checking-authorization
                // console.log(data)
                sendAuthDataToServer(data)
            }
        }
    );

function sendAuthDataToServer (data){
    const csrf_token = $('input[name=csrfmiddlewaretoken]').val();
    const request_data = data
    // const type = 'telegram'

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader('X-CSRFToken', csrf_token)
        }
    });

    $.ajax({
        type: 'post',
        url: '/freedom_of_speech/auth/telegram',
        data: request_data,
        success: function(data, status, jqXHR) {
            // location.reload();
            // $('#constitution_text_span').text(data);
            console.log('authorized');
        }
    });
}
    // window.open("https://oauth.telegram.org/auth?bot_id=2037332308&origin=http://127.0.0.1/freedom_of_speech/auth&embed=1&request_access=write&return_to=http://127.0.0.1/freedom_of_speech/auth")

    // const csrf_token = $('input[name=csrfmiddlewaretoken]').val();
    // const name = $('#contact-name').val();
    // const role = $('#contact-role').val();
    // const testimonial = $('#contact-testimonial').val();
    // const type = 'testimonial';


    // $.ajax({
    //     type: 'get',
    //     url: '',
    //     data: {
    //         type: type,
    //         name: name,
    //         role: role,
    //         testimonial: testimonial,
    //     },
    //     success: function(data, status, jqXHR) {
    //         print(data)
    //     }
    // });
});
