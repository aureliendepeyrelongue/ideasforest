$('.likes-button').click(function (e) {
    e.preventDefault()
    href = $(this).attr('href')
    likesNumberContainer = $($(this).find(".likes-number-container")[0])
    previousLikesNumber = parseInt(likesNumberContainer.html())
    self = $(this)
    $.ajax({
        type: 'GET',
        url: href,
        success: function (response) {
            if (response.liked) {
                likesNumber = previousLikesNumber + 1
                self.addClass('liked')
            }
            else {
                likesNumber = previousLikesNumber - 1
                self.removeClass('liked')
            }
            likesNumberContainer.html(likesNumber)
            console.log("success", response)
            console.log(previousLikesNumber)

        },
        error: function (response) {
            console.log("erreur", response)
        }
    });
})
