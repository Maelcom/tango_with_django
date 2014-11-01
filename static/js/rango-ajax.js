$(document).ready(function() {
    $("#about-btn").click( function() {
        $('#msg').append('o');
    });
    $('#like').click(function() {
        var cat_id = $(this).attr('cat_id');
        $.get('/rango/like_category/', {cat_id: cat_id}, function (data, textStatus, jqXHR) {
            console.log('ajax response contents:');
            console.log(data);
            console.log(jqXHR);
            if (data.likes) {
                $('#like-count').html(data.likes);
            }
            else if (data.redirect) {
                console.log('redirecting to login');
                window.location.replace(data.redirect);
            }

        });
    });
});
