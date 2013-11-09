jQuery(document).ready(function (e) {
    setTimeout(function () {
        showTwitterFeeds();
        animateAdoptMarks();
        animateAnnotateMarks();
    }, 600)


    showTwitterFeeds();
});

function showTwitterFeeds() {
    $("#twitter").getTwitter({
        userName: "penguinlifeline",
        numTweets: 1,
        loaderText: "",
        slideIn: true,
        showHeading: false,
        headingText: "Latest Tweets",
        showProfileLink: false
    });
}


function animateAnnotateMarks() {

    stopAnnotation();


    $('#mark0').animate({'opacity': 0}, 500).animate({'opacity': 1}, 400, 'easeOutBounce');
    $('#mark1').animate({'opacity': 0}, 700).animate({'opacity': 1}, 400, 'easeOutBounce');
    $('#mark2').animate({'opacity': 0}, 900).animate({'opacity': 1}, 400, 'easeOutBounce');
    $('#mark3').animate({'opacity': 0}, 1100).animate({'opacity': 1}, 400, 'easeOutBounce');
    $('#mark4').animate({'opacity': 0}, 1300).animate({'opacity': 1}, 400, 'easeOutBounce');
    $('#mark5').animate({'opacity': 0}, 1500).animate({'opacity': 1}, 400, 'easeOutBounce');
    $('#mark6').animate({'opacity': 0}, 1700).animate({'opacity': 1}, 400, 'easeOutBounce');
    $('#mark7').animate({'opacity': 0}, 2100).animate({'opacity': 1}, 400, 'easeOutBounce');
}

function animateAdoptMarks() {
    $('#mark8').stop(true, true, true).animate();
    $('#mark8').animate({'opacity': 0}, 500).animate({'opacity': 1}, 800, 'easeOutBounce');
}

function stopAdopt() {
    $('#mark8').stop(true, true, true).animate();
}

function stopAnnotation() {
    for (var i = 0; i < 8; i++) {
        $('#mark' + i).stop(true, true, true).animate();
    }
}
