$(function() {
    // When we're using HTTPS, use WSS too.
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/chat" + window.location.pathname);
    chatsock.onmessage = function(message) {
        console.log(message.data);
        var data = JSON.parse(message.data);
        var chat = $("#chat")
        var ele = $('<tr></tr>')

        ele.append(
            $("<td></td>").text(data.created)
        )
        ele.append(
            $("<td></td>").text(data.user)
        )
        ele.append(
            $("<td></td>").text(data.content)
        )

        chat.append(ele)
    };

    $("#chatform").on("submit", function(event) {
        console.log('Submi');
        var message = {
            user: $('#handle').val(),
            content: $('#message').val(),
            room: 'public'
        }
        console.log(message);
        chatsock.send(JSON.stringify(message));
        $("#message").val('').focus();
        return false;
    });
});
