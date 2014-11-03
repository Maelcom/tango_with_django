$overlay = $('<div id="overlay"></div>');
$modal = $('<div id="modal"></div>');
$modal_content = $('<div id="modal_content"></div>');
$close = $('<a id="close">Close</a>');

$modal.append($close, $modal_content);

$(document).ready(function() {
    $("#about-btn").click( function() {
        $('#msg').append('o');
    });
    $('#like').click(function() {
        var cat_id = $(this).attr('cat_id');
        $.get('/rango/like_category/', {cat_id: cat_id}, function (data, textStatus, jqXHR) {
            if (data.likes) {
                $('#like-count').html(data.likes);
                $('#like').prop('disabled', true);
            }
            else if (data.login_required) {
                $('body').append($overlay, $modal);
                var modal_content = $('#modal_content');
                modal_content.load(data.login_required, function() {
                    modal_content.on('click', '#login_button', function(event) {
                        event.preventDefault();
                        var form = $('#signin_form');
                        $.post(form.attr('action'), form.serialize())
                            .done(function(data) {
                                if (data.login_success) {
                                    window.location.reload();
                                }
                                else {
                                    $('#modal_content').html(data);
                                }
                            });
                    });
                    $('#modal').on('click', '#close', function() {
                        $('#overlay, #modal').remove();
                    });
                });
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
