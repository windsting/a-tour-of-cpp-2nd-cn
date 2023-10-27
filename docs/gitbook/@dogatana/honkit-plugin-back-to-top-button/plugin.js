let buttonHtml;
let animateTime;

// create button html at start
window.gitbook.events.bind('start', function(e, config) {
    const plugin = 'back-to-top-button';
    let icon = '<i class="fa fa-arrow-up"></i>';

    // check configuration
    if (config && config[plugin]) {
        if (config[plugin]['icon']) {
            icon = config[plugin]['icon'];
        }
        if (config[plugin]['animate']) {
            const time = Number(config[plugin]['animate']);
            if (!isNaN(time) && time >= 0) {
                animateTime = time;
            }
        }
    }
    buttonHtml = '<div class="back-to-top">' + icon + '</i></div>';
});

window.gitbook.events.on('page.change', function() {
    $(".book").append(buttonHtml);
    $(".back-to-top").hide();

	$('.book-body,.body-inner').on('scroll', function () {
		if ($(this).scrollTop() > 100) {
			$('.back-to-top').fadeIn();
		} else {
			$('.back-to-top').fadeOut();
		}
	});

	$('.back-to-top').click(function () {
		$('.book-body,.body-inner').animate({
			scrollTop: 0
		}, animateTime);
		return false;
	});
});
