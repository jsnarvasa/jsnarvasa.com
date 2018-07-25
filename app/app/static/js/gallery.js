// JS only to be loaded in gallery.html

$(document).ready(function() {
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
        if(!recentScroll && $(window).scrollTop() + $(window).height() > $(document).height()-20){
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