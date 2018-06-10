$(document).ready(function() {

    var navbar = $('.navbar');
    var container = $('#main-container');
    var origOffsetY = navbar.offset().top;


    function scroll() {
        if ($(window).scrollTop() >= origOffsetY) {
            container.addClass('navbar-scroll-padding');
            navbar.addClass('fixed-top');
        } else {
            navbar.removeClass('fixed-top');
            container.removeClass('navbar-scroll-padding');
        }
    };

    document.onscroll = scroll;

});