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
        var image = '<img class="img-fluid" id="image-on-overlay" src="/static/photos/' + $(this).attr('id') + '"></img>';
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

    var url = window.location.pathname; //determine if traffic is from photoblog or search
    var page = '';
    searchQuery = $('#searchQuery').text()

    if(url.substr(1,14)=='photoblog/area'){
        page = 'photoblog/area/' + searchQuery;
    }
    else if(url.substr(1,9)=='photoblog'){
        page = 'photoblog'
    }
    else{
        page = 'search'
    };

    // Checks if there are more photos in the next pagination batch.  If next page contains 0 images, then hide load more button
    function isMoreContent(pageNum){
        pageCount++;
        nextImageCount = 1;
        $.getJSON(url='/' + page + '/'+ pageCount, data='q=' + searchQuery, success=function(results){
            nextImageCount = results.image_names.length;
        }).then(function(){
            if(nextImageCount == 0){
                $('#loadMoreButton').css('visibility', 'hidden');
            };
        });
        pageCount--;
    };

    // The one that does the loading and append of new batch of images
    function loadMore(pageNum){
        pageCount++;
        //AJAX request
        $.getJSON(url='/' + page + '/'+ pageCount, data='q=' + searchQuery, success=function(results){
            images = results.image_names;
            images.forEach(FileName => {
                $('.card-columns').append('<div class="card"><img class="img-fluid gallery-image" id="' + FileName + '" src="static/photos/thumbnail/' + FileName + '"></div>');
            });
            /* Disabling incremental loading for areas to be shaded in virutal scratchmap
                as per: https://github.com/jsnarvasa/jsnarvasa.com/issues/4
                
            additional_geojson = results.geojson.features;
            country_boundaries.features = country_boundaries.features.concat(additional_geojson);
            // Refreshes the map, to load new boundaries
            remove_geojson_layer();
            add_geojson_layer(country_boundaries);
            */
        });
        isMoreContent(pageCount);
        $(window).on("load", function(){
            $(document).on('scroll', bindScroll);
        });
    };
    
    // Event handler for infinity scrolling, makes sure it's not triggered more than once
    function bindScroll(){
        if(!recentScroll && $(window).scrollTop() >= $(document).height() - $(window).height() - 10){
            $(window).off('scroll');
            recentScroll = true;
            window.setTimeout(() => { recentScroll = false; }, 2000);
            loadMore(pageCount);
        };
    };

    // The two event handlers to activate next page request
    $('#loadMoreButton').on('click', loadMore);
    $(window).on("load", function() {
        $(document).on('scroll',bindScroll);
    });

    // Page header text
    if(page=='photoblog'){
        $('h3.pageHeader').text('Photoblog');
        $('p.pageHeader').text("A virtual scratch map, where time and place meets, and a story is told...");
    }
    else{
        $('h3.pageHeader').text('Search Results for ' + searchQuery);
    };
});