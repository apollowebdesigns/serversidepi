(function($){
    $(function(){
        var currentUrl = $(location).attr('href');
        var firstPosition = currentUrl.indexOf("1");
        var lastPosition = currentUrl.indexOf(":");
        //remove extra url for ui router params
        var removeSlash = currentUrl.length - 1;
        var secondUrl = currentUrl.toString().slice(0, removeSlash);
        var rawness = String.raw`:2222/html/min.php`;
        var calcUrl = secondUrl.concat(rawness);
        console.log("the current url is");
        console.log(calcUrl);
        $("#camera-screen").attr("src", calcUrl);
    });
})(jQuery);