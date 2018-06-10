$(document).ready(function() {

    var navbar = $('.navbar');
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