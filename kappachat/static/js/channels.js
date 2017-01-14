/**
 * Created by Ed on 13.1.2017.
 */


$(document).ready(function() {
    $('.channel').click(function() {
        var channel_name = $(this).children("a").text();
        $('#contentDiv').load(
            '/join_channel/',
            {'channel_name': channel_name, 'csrfmiddlewaretoken': $("ul.nav-sidebar > input[name=csrfmiddlewaretoken]").val()},
            function() {
                $('.active').removeClass('active');
                $('a:contains("' + channel_name + '")').parent().addClass('active');
            }
        );
    });
});