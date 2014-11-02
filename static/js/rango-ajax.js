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
                $('#like').prop('disabled', true);
            }
            else if (data.redirect) {
                window.location.replace(data.redirect);
            }

        });
    });
    $('#suggestion').keyup(function() {
        var q = $(this).val();
        $.get('/rango/suggest_category/', {q: q}, function (data, textStatus, jqXHR) {
            console.log('ajax response contents:');
            console.log(data);
            console.log(jqXHR);
            if (data) {
                $('#suggested_cats').html(data);
            }
        });
    });
});
