/*global jQuery */
/* Contents
// ------------------------------------------------>
	1.  Background INSERT
	2.  HEADER AFFIX
	3.	AJAX MAILCHIMP
	4.  AJAX CAMPAIGN MONITOR 
	5.  OWL CAROUSEL
	6.  SCROLL TO
	7.  WOW
	8.  Youtube Background
*/
// import WOW from 'wow.js'
// window.WOW = require('wowjs').WOW;

(function($) {
    "use strict";

    /* ------------------  Background INSERT ------------------ */

    var $bgSection = $(".bg-section");

    $bgSection.each(function() {
        var bgSrc = $(this).children("img").attr("src");
        var bgUrl = 'url(' + bgSrc + ')';
        $(this).parent().css("backgroundImage", bgUrl);
        $(this).parent().addClass("bg-section");
        $(this).remove();
    });

    /* ------------------ OWL CAROUSEL ------------------ */

    $(".carousel").each(function() {
        var $Carousel = $(this);
        $Carousel.owlCarousel({
            loop: $Carousel.data('loop'),
            autoplay: $Carousel.data("autoplay"),
            margin: $Carousel.data('space'),
            nav: $Carousel.data('nav'),
            dots: $Carousel.data('dots'),
            dotsSpeed: $Carousel.data('speed'),
            responsive: {
                0: {
                    items: 1
                },
                600: {
                    items: $Carousel.data('slide-res')
                },
                1000: {
                    items: $Carousel.data('slide'),
                }
            }
        });
    });

    /* ------------------  WOW Animated ------------------ */
    var wow = new WOW({

        boxClass: 'wow', // animated element css class (default is wow)
        animateClass: 'animated', // animation css class (default is animated)
        offset: 50, // distance to the element when triggering the animation (default is 0)
        mobile: false, // trigger animations on mobile devices (default is true)
        live: true // act on asynchronously loaded content (default is true)

    });

    wow.init();

    /* ------------------  AJAX CAMPAIGN MONITOR  ------------------ */

    $('#campaignmonitor').submit(function(e) {
        e.preventDefault();
        $.getJSON(
            this.action + "?callback=?",
            $(this).serialize(),
            function(data) {
                if (data.Status === 400) {
                    alert("Error: " + data.Message);
                } else { // 200
                    alert("Success: " + data.Message);
                }
            });
    });

    /* ------------------  SCROLL TO ------------------ */

    var aScroll = $('a[data-scroll="scrollTo"]');
    aScroll.on('click', function(event) {
        var target = $($(this).attr('href'));
        if (target.length) {
            event.preventDefault();
            $('html, body').animate({
                scrollTop: target.offset().top-100
            }, 1000);
        }
    });

    /* ------------------  Youtube Background  ------------------ */
    $(".bg-ytvideo").each(function() {

        var vidId = $(this).data("vid-id"),
            vidAutoPlay = $(this).data("autoplay"),
            vidStartAt = $(this).data("start-at"),
            vidMute = $(this).data("mute"),
            vidOpacity = $(this).data("opacity"),
            vidShowPluginLogo = $(this).data("plugin-logo"),
            vidShowControls = $(this).data("controls"),
            vidFallBackImg = $(this).data("fall-cover");

        if (vidAutoPlay === "" || vidAutoPlay === null || vidAutoPlay === undefined) {
            vidAutoPlay = true;
        }
        if (vidStartAt === "" || vidStartAt === null || vidStartAt === undefined) {
            vidStartAt = 0;
        }
        if (vidMute === "" || vidMute === null || vidMute === undefined) {
            vidMute = true;
        }
        if (vidOpacity === "" || vidOpacity === null || vidOpacity === undefined) {
            vidOpacity = 1;
        }
        if (vidShowPluginLogo === "" || vidShowPluginLogo === null || vidShowPluginLogo === undefined) {
            vidShowPluginLogo = false;
        }
        if (vidShowControls === "" || vidShowControls === null || vidShowControls === undefined) {
            vidShowControls = false;
        }
        if (vidFallBackImg === "" || vidFallBackImg === null || vidFallBackImg === undefined) {
            vidFallBackImg = "";
        }

        $(this).data(
            "property",
            "{videoURL:'http://youtu.be/" + vidId + "',containment:'self',autoPlay:" + vidAutoPlay + ", mute:" + vidMute + ", startAt:" + vidStartAt + ", opacity:" + vidOpacity + ",showYTLogo:" + vidShowPluginLogo + ",showControls:" + vidShowControls + ",stopMovieOnBlur:false,mobileFallbackImage:'" + vidFallBackImg + "'}"
        );
    });

}(jQuery));

// <!-- Google Analytics -->

(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

ga('create', 'UA-89540131-1', 'auto');
ga('send', 'pageview');

// <!-- End Google Analytics -->