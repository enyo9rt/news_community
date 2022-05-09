// 이번에 새로 만드는 댓글 post 하게 해주는 함수

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