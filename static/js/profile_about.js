
function sign_out() {
    $.removeCookie('mytoken', {path: '/'});
    alert('로그아웃!')
    window.location.href = "/"
}

// Select the input element using
// document.querySelector
var input = document.querySelector(
  "#file-with-js>.file-label>.file-input"
);

// Bind an listener to onChange event of the input
input.onchange = function () {
    if(input.files.length > 0){
        var fileNameContainer =
            document.querySelector(
              "#file-with-js>.file-label>.file-name"
            );
        // set the inner text of fileNameContainer
        // to the name of the file
        fileNameContainer.textContent =
          input.files[0].name;
    }
}

// 이미지 삭제 후 파일 이름 기본 이미지 처리
const to_default_img = () => {
        document.getElementById("input-pic").value=null;
        var fileNameContainer =
        document.querySelector(
          "#file-with-js>.file-label>.file-name"
        );
        // set the inner text of fileNameContainer
        // to the name of the file
        fileNameContainer.textContent = '기본 이미지'
}

function update_profile() {
    let name = $('#input-name').val()
    let file = $('#input-pic')[0].files[0]
    let about = $("#textarea-about").val()
    let form_data = new FormData()
    form_data.append("file_give", file)
    form_data.append("name_give", name)
    form_data.append("about_give", about)
    console.log(name, file, about, form_data)

    $.ajax({
        type: "POST",
        url: "/update_profile",
        data: form_data,
        cache: false,
        contentType: false,
        processData: false,
        success: function (response) {
            if (response["result"] == "success") {
                alert(response["msg"])
                window.location.reload()
            }
        }
    });
}

// 북마크 기사 가져오기
function posts_get(user_id) {
    $("#comment-box").empty()
    $.ajax({
        type: "GET",
        url: `/posts_get?user_id_give=${user_id}`,
        data: {},
        success: function (response) {
            console.log(response["msg"])
            if (response["result"] == "success") {
                let posts = response["posts"].reverse()
                for (let i = 0; i < posts.length; i++) {
                        let post = posts[i]
                        let temp_html = `<div class="bookmark_post box" id="${post["post_id"]}">
                                            <a href="/detail/${post["post_id"]}">${post["title"]}</a>
                                        </div>`
                        $("#comment-box").append(temp_html)
                    }
            }
        }
    })
}

// 프로필 탭
function toggle_tab(type) {
    console.log(type)
    let $li_tab = $(`#${type}`)
    if (`${type}`=="posts") {
        $li_tab.addClass("is-active").siblings().removeClass("is-active")
        posts_get(now_user_id)
    } else if (`${type}`=="comments") {
        $li_tab.addClass("is-active").siblings().removeClass("is-active")
        comments_get(now_user_id,"")
    }
}