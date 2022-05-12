$(document).ready(function () {
  listing();
});

const listing = () => {
    $.ajax({
        type: 'GET',
        url: '/news',
        data: {},
        success: function (response) {
            let news_list = response['news_list'];
            $('#cards-box').empty();


            for (let i = 0; i < news_list.length; i++) {
                let post_id = news_list[i]['post_id'];
                let title = news_list[i]['title'];
                let contents = news_list[i]['explain']
                let image_url = news_list[i]['image_url'];
                let view = news_list[i]['view']
                let html_data = `<div class="col">
                                        <div class="card h-100">
                                            <img class="card-image-box" src=${image_url}
                                                 class="card-img-top">
                                            <div class="card-body">
                                                <a href="/detail/${post_id}"><h5 class="card-title">${title}</h5></a>
                                                <p class="card-text">${contents}</p>
                                                <p class="mycomment">조회수: ${view}</p>
                                            </div>
                                        </div>
                                    </div>`;
                $('#cards-box').append(html_data);
            }
        }
    })
}