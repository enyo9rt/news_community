$(document).ready(function () {
    get_comment();
    get_like();
})

function comments() {
        var now = new Date()
        var year = now.getFullYear();
        var month = ('0' + (now.getMonth() + 1)).slice(-2);
        var day = ('0' + now.getDate()).slice(-2);
        var hours = ('0' + now.getHours()).slice(-2);
        var minutes = ('0' + now.getMinutes()).slice(-2);
        var seconds = ('0' + now.getSeconds()).slice(-2);
        var time_string = year + '-' + month  + '-' + day + ' ' + hours + ':' + minutes  + ':' + seconds;
        let comment_name = $('#comment_name').val()
        let comment_content = $('#comment_content').val()

        if (!comment_name || !comment_content) {
                alert('작성을 완료해 주세요!');
        } else {
            $.ajax({
                    type: "POST",
                    url: "/api/comment",
                    data: {comment_name_give : comment_name, comment_give : comment_content, time_give : time_string},
                    success: function (response) {
                        alert(response["msg"]);
                        window.location.reload()
                    }
            })
        }
}

function get_comment() {
        $.ajax({
            type: "GET",
            url: "/api/comment",
            data: {},
            success: function (response) {
                let comments = response['comments']
                for (let i = 0; i < comments.length; i++) {
                    let comment_name = comments[i]['comment_name']
                    let comment_content = comments[i]['comment_content']
                    let time = comments[i]['time']
                    let temp_html = ` <tr>
                                          <td>${comment_name}</td>
                                          <td>${comment_content}</td>
                                          <td>${time}</td>
                                      </tr>`
                    $('#comments').append(temp_html)
                }
            }
        })
}

function like() {
    let like_result = $('#like_result').text();
    $.ajax({
            type: "POST",
            url: "/api/like",
            data: {like_give : like_result},
            success: function (response) {
                alert(response["msg"]);
                window.location.reload()
            }

    })
}
function get_like() {
    $.ajax({
        type: 'GET',
        url: '/api/like',
        data: {},
        success: function (response) {
            let new_like = response['new_like'];
            let temp_html = `<div class="new_like">${new_like}</div>`
            $('#like_result').replaceWith(temp_html);
        }
    });
}