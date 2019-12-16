$(document).ready(function() {

    $(window).scroll(function() {
        var viewPortSize = $(window).height();
        var splashImgHeight = $('#splash-image-div').height();

        if($(window).scrollTop() > splashImgHeight - viewPortSize + splashImgHeight * 0.2) {
            $('h3#intro-text').css('visibility', 'visible').hide().fadeIn(600, "swing");
            $('p#intro-text').css('visibility', 'visible').hide().fadeIn(1000, "swing");
            $(this).off('scroll');
        };
    });
    
});