$(document).ready(function () {

})

// 댓글 작성 함수 -hj
function post_comment() {
            const comment_value = $('#comment').val()
            const date = new Date().toISOString()
            $.ajax({
                type: "POST",
                url: "/comment",
                data: {
                    comment_give: comment_value,
                    date_give: date
                },
                success: function (response) {
                    alert(response['msg'])
                    $('#comment').val('')
                }
            })
        }