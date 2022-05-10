// 댓글 작성 함수 -hj
function post_comment() {
    const comment_value = $('#comment').val()
    const date = new Date().toISOString()
    $.ajax({
        type: "POST",
        url: "/comment",
        data: {
            comment_give: comment_value,
            date_give: date,
            id_give: now_post_id
        },
        success: function (response) {
            alert(response['msg'])
            $('#comment').val('')
            comments_get("",now_post_id)
        }
    })
}

function delete_comment() {
    $.ajax({
        type: "POST",
        url: "/comment/delete",
        data: {
            id_give: post_id
        },
        success: function (response) {
            alert(response['msg'])
            window.location.reload()
        }
    })
}

// 댓글 작성 시간 단위
function time2str(date) {
    let today = new Date()
    let time = (today - date) / 1000 / 60  // 분

    if (time < 60) {
        return parseInt(time) + "분 전"
    }
    time = time / 60  // 시간
    if (time < 24) {
        return parseInt(time) + "시간 전"
    }
    time = time / 24
    if (time < 7) {
        return parseInt(time) + "일 전"
    }
    return `${date.getFullYear()}년 ${date.getMonth() + 1}월 ${date.getDate()}일`
}

// 좋아요 갯수 단위
function num2str(count) {
    if (count > 10000) {
        return parseInt(count / 1000) + "K"
    }
    if (count > 500) {
        return parseInt(count / 100) / 10 + "K"
    }
    if (count == 0) {
        return ""
    }
    return count
}

function comments_get(user_id, post_id) {
    console.log(user_id, post_id)
    if (user_id == undefined) {
        user_id = ""
    }
    else if (post_id == undefined) {
        post_id = ""
    }
    $("#comment-box").empty()
    $.ajax({
        type: "GET",
        url: `/comments_get?user_id_give=${user_id}&post_id_give=${post_id}`,
        data: {},
        success: function (response) {
            if (response["result"] == "success") {
                let comments = response["comments"]
                for (let i = 0; i < comments.length; i++) {
                    let comment = comments[i]
                    let time = time2str(new Date(comment["date"]))
                    let count = num2str(comment["count_like"])
                    let icon = comment['like_by_me'] ? "fa-heart" : "fa-heart-o"
                    let temp_html = `<div class="box" id="${comment["_id"]}">
                                        <article class="media">
                                            <div class="media-left">
                                                <a class="image is-64x64" href="/profile/${comment['user_id']}">
                                                    <img class="is-rounded" src="/static/${comment['profile_pic_real']}"
                                                         alt="Image">
                                                </a>
                                            </div>
                                            <div class="media-content">
                                                <div class="content">
                                                    <p>
                                                        <strong>${comment['nick_name']}</strong> <small>@${comment['user_id']}</small> <small>${time}</small>
                                                        <br>
                                                        ${comment['comment']}
                                                    </p>
                                                </div>
                                                <nav class="level is-mobile">
                                                    <div class="level-left">
                                                        <a class="level-item like_icon" aria-label="like" onclick="toggle_like('${comment['_id']}')">
                                                            <span class="icon is-small"><i class="fa ${icon}"
                                                                                           aria-hidden="true"></i></span>&nbsp;<span class="like-num">${count}</span>
                                                        </a>
                                                    </div>

                                                </nav>
                                            </div>
                                        </article>
                                    </div>`
                    $("#comment-box").append(temp_html)
                }
            }
        }
    })
}

function bookmarked(post_id) {
    console.log(post_id)
    $("#bookmark").empty()
    $.ajax({
        type: "GET",
        url: `/bookmarked?post_id_give=${post_id}`,
        data: {},
        success: function (response) {
            if (response["result"] == "success") {
                let bookmark_by_me = response["bookmark_by_me"]
                console.log(bookmark_by_me)
                let icon = bookmark_by_me ? "fa-bookmark" : "fa-bookmark-o"
                let temp_html = `<div id="${post_id}" class="bookmark">
                                    <a class="level-item is-sparta" aria-label="bookmark"
                                           onclick="toggle_bookmark(${post_id})">
                                                    <span class="icon is-small"><i class="fa fa-solid ${icon}"
                                                                                   aria-hidden="true"></i></span>
                                    </a>
                                  </div>`
                $("#bookmark").append(temp_html)
            }
        }
    })
}


// 좋아요, 좋아요 취소
function toggle_like(comment_id) {
    console.log(comment_id)
    let $a_like = $(`#${comment_id} a[aria-label='like']`)
    let $i_like = $(`#${comment_id} a[aria-label='like']`).find("i")
    if ($i_like.hasClass("fa-heart")) {
        $.ajax({
            type: "POST",
            url: "/like_update",
            data: {
                comment_id_give: comment_id,
                action_give: "unlike"
            },
            success: function (response) {
                console.log("unlike")
                $i_like.addClass("fa-heart-o").removeClass("fa-heart")
                $a_like.find("span.like-num").text(num2str(response["count"]))
            }
        })
    } else {
        $.ajax({
            type: "POST",
            url: "/like_update",
            data: {
                comment_id_give: comment_id,
                action_give: "like"
            },
            success: function (response) {
                console.log("like")
                $i_like.addClass("fa-heart").removeClass("fa-heart-o")
                $a_like.find("span.like-num").text(num2str(response["count"]))
            }
        })

    }
}

// 북마크, 북마크 취소
function toggle_bookmark(post_id) {
    console.log(post_id)
    let $i_bookmark = $(`#${post_id} a[aria-label='bookmark']`).find("i")
    if ($i_bookmark.hasClass("fa-bookmark")) {
        $.ajax({
            type: "POST",
            url: "/bookmark",
            data: {
                post_id_give: post_id,
                action_give: "unbookmark"
            },
            success: function (response) {
                console.log("unbookmark")
                $i_bookmark.addClass("fa-bookmark-o").removeClass("fa-bookmark")
            }
        })
    } else {
        $.ajax({
            type: "POST",
            url: "/bookmark",
            data: {
                post_id_give: post_id,
                action_give: "bookmark"
            },
            success: function (response) {
                console.log("bookmark")
                $i_bookmark.addClass("fa-bookmark").removeClass("fa-bookmark-o")
            }
        })

    }
}