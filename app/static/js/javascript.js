$(document).ready(function() {

    var navbar = $('#main-navbar');
    var container = $('#main-container');


    function scroll() {
        if ($(window).scrollTop() > 0) {
            container.addClass('navbar-scroll-padding');
            navbar.addClass('navbar-opacity');
            navbar.addClass('fixed-top');
        } else {
            navbar.removeClass('fixed-top');
            navbar.removeClass('navbar-opacity');
            container.removeClass('navbar-scroll-padding');
        }
    };

    document.onscroll = scroll;

});

// To center splash-intro message @index.html
function splashIntro() {
    var splashImgHeight = $('#splash-image-div').height();
    $('#splash-intro').css('margin-top',splashImgHeight/2.2);
};

$(document).ready(splashIntro);
$(window).on('resize', splashIntro);