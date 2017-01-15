/**
 * Created by Ed on 13.1.2017.
 */


$(document).ready(function() {
    function update() {
        var channelName = $('#channelName').text();
        $('#chatList').load(
            '/update_chat/',
            {'channel_name': channelName, 'csrfmiddlewaretoken': $("ul.nav-sidebar > input[name=csrfmiddlewaretoken]").val()},
            function() {
                var chatArea  = $('.current-chat');
                chatArea.scrollTop = chatArea.scrollHeight;
            }
        );
    }

    $('.channel').click(function() {
        var channel_name = $(this).children("a").text();
        $('#contentDiv').load(
            '/join_channel/',
            {'channel_name': channel_name, 'csrfmiddlewaretoken': $("ul.nav-sidebar > input[name=csrfmiddlewaretoken]").val()},
            function() {
                $('.active').removeClass('active');
                $('a:contains("' + channel_name + '")').parent().addClass('active');
                clearInterval(interval);
                interval = setInterval(update, 2000);
            }
        );
    });
});