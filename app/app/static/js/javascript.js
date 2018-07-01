// To enable main-navbar element transparency when scrolling
$(document).ready(function() {

    var navbar = $('#main-navbar');
    var container = $('#main-container');

    // The order of adding and removing the classes matters here
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

// To center splash-intro message @index.html and keep centred on window resize
function splashIntro() {
    var splashImgHeight = $('#splash-image-div').height();
    $('#splash-intro').css('margin-top',splashImgHeight/2.2);
};

$(document).ready(splashIntro);
$(window).on('resize', splashIntro);


// Display image overlay in Gallery

function windowHeight() {
    var height = $(window).height();
    return height;
}

$(document).ready(windowHeight);
$(window).on('resize', windowHeight);

$('.gallery-image').on('click', function(){
    var image = '<img class="img-fluid" style="height:100%;max-width:100%" src="' + $(this).attr('src') + '"></img>';
    $('#overlay-container').css("visibility", "visible");
    $('#overlay-image').append(image);
    $('#overlay-image').css("height", windowHeight()*0.9);
    //var overlayImgHeight = $('#overlay-image').height();
    //$('#overlay-container').css("height",overlayImgHeight);
});

$('#overlay-close').on('click', function(){
    $('#overlay-container').css("visibility", "hidden");
    $('#overlay-image').empty();
});