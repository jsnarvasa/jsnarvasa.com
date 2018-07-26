$(document).ready(function() {

    //
    // Sets the image overlay height in Gallery
    //

    function getWindowHeight() {
        var windowHeight = $(window).height();
        return windowHeight;
    };

    function adjustOverlayHeight() {
        var defaultHeight = getWindowHeight()*0.9;
        $('#overlay-image').css("max-height", defaultHeight);
    };

    $('.card-columns').on('click', 'img.gallery-image', adjustOverlayHeight);
    $(window).on('resize',adjustOverlayHeight);
    
    //
    // Displays and closes the overlay in Gallery
    //

    function overlayOffset() {
        var scrollOffset = $(window).scrollTop();
        $("#overlay-container").css("top", scrollOffset + getWindowHeight()*0.05);
    };

    $('.card-columns').on('click', 'img.gallery-image', function(){
        var image = '<img class="img-fluid" id="image-on-overlay" src="static/photos/' + $(this).attr('id') + '"></img>';
        $('.overlay-background').css("visibility", "visible").hide().fadeIn(150);
        $('#overlay-container').css("visibility", "visible").hide().fadeIn(150);
        $('#overlay-container').css("top", overlayOffset());
        $('#overlay-image').append(image);
        // AJAX request here
        $.getJSON('/getphotodetails',{
            img: $(this).attr('id')
        }, function(data) {
            $("#caption").text(data.Caption);
            $("#location").text(data.City + ", " + data.Country);
            $("#uploadDate").text(data.Upload_Date);
            $("#captureDate").text(data.Capture_Date);
            $("#place").html("&mdash; " + data.Place);
        });
    });

    function closeOverlay() {
        $('#overlay-container').css("visibility", "hidden");
        $('.overlay-background').css("visibility", "hidden");
        $('#overlay-image').empty();
        $("#caption").empty();
        $("#location").empty();
        $("#uploadDate").empty();
        $("#captureDate").empty();
        $("#place").empty();
    };

    $('#overlay-close').on('click',closeOverlay);
    $('.overlay-background').on('click',closeOverlay);
    
    $(window).on('resize', overlayOffset());

    //
    // Used for infinity scrolling w/ pagination + AJAX
    //

    pageCount = 1
    var recentScroll = false;

    function loadMore(pageNum){
        //AJAX request
        $.getJSON(url='/gallery/'+ pageCount, success=function(images){
            images = images.image_names;
            images.forEach(FileName => {
                $('.card-columns').append('<div class="card"><img class="img-fluid gallery-image" id="' + FileName + '" src="static/photos/thumbnail/' + FileName + '"></div>');
            });
        });
        $(window).on("load", function(){
            $(document).on('scroll', bindScroll);
        });
    };
    
    function bindScroll(){
        if(!recentScroll && $(window).scrollTop() >= $(document).height() - $(window).height() - 10){
            $(window).off('scroll');
            pageCount++;
            loadMore(pageCount);
            recentScroll = true;
            window.setTimeout(() => { recentScroll = false; }, 2000);
        };
    };

    $(window).on("load", function() {
        $(document).on('scroll',bindScroll);
    });
});