$(function () {
    $("div.wtf").slice(0, 2).show();
    $("#loadMore").on('click', function (e) {
        e.preventDefault();
        $("div.wtf:hidden").slice(0, 1).slideDown();
        if ($("div.wtf:hidden").length == 0) {
            $("#loadMore").fadeOut('fast');
        }
        $('html,body').animate({
            scrollTop: $(this).offset().top
        }, 50);
    });
});

$('a[href=#top]').click(function () {
    $('body,html').animate({
        scrollTop: 0
    }, 600);
    return false;
});

$(window).scroll(function () {
    if ($(this).scrollTop() > 600) {
        $('.totop a').fadeIn();
    } else {
        $('.totop a').fadeOut();
    }
});