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


// Sets the image overlay height in Gallery

function getWindowHeight() {
    var windowHeight = $(window).height();
    return windowHeight;
};

function adjustOverlayHeight() {
    var defaultHeight = getWindowHeight()*0.9;
    $('#overlay-image').css("height", defaultHeight);
};

$('.gallery-image').on('click', adjustOverlayHeight);
$(window).on('resize',adjustOverlayHeight);


// Displays and closes the overlay in Gallery

function overlayOffset() {
    var scrollOffset = $(window).scrollTop();
    $("#overlay-container").css("top", scrollOffset + getWindowHeight()*0.05);
};

$('.gallery-image').on('click', function(){
    var image = '<img class="img-fluid" id="image-on-overlay" src="' + $(this).attr('src') + '"></img>';
    $('#overlay-container').css("visibility", "visible");
    $('#overlay-container').css("top", overlayOffset());
    $('#overlay-image').append(image);
    // AJAX request here
    $.getJSON('/getphotodetails',{
        img: $(this).attr('id')
    }, function(data) {
        $("#title").text(data.Title);
        $("#desc").text(data.Description);
        $("#uploadDate").text(data.Upload_Date);
        $("#captureDate").text(data.Capture_Date);
    });
});

$('#overlay-close').on('click', function(){
    $('#overlay-container').css("visibility", "hidden");
    $('#overlay-image').empty();
});

$(window).on('resize', overlayOffset());