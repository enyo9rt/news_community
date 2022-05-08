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
                let title = news_list[i]['title'];
                let contents = news_list[i]['explain']
                let image_url = news_list[i]['image_url'];
                let html_data = `<div class="col">
                                        <div class="card h-100">
                                            <img src=${image_url}
                                                 class="card-img-top">
                                            <div class="card-body">
                                                <a href="comments"><h5 class="card-title">${title}</h5></a>
                                                <p class="card-text">${contents}</p>
                                                <p class="mycomment">조회수 0</p>
                                            </div>
                                        </div>
                                    </div>`;
                $('#cards-box').append(html_data);
            }
        }
    })
}