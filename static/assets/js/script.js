$(window).scroll(function() {    
    var scroll = $(window).scrollTop();

    if (scroll >= 200) {
        $(".theame-header").addClass("sticky-header");
    } else {
        $(".theame-header").removeClass("sticky-header");
    }
});


// client-slider-end
  
$(document).ready(function(){
    $('.counter').each(function(){
        $(this).prop('Counter',0).animate({
            Counter: $(this).text()
        },{
            duration: 3500,
            easing: 'swing',
            step: function (now){
                $(this).text(Math.ceil(now));
            }
        });
    });
});

// counter-js-end

// agent-hm-start
    $('#agent-hm-slide').owlCarousel({
    autoplay:true,
    loop:true,
    margin:10,
    dots:false,
    nav:false,
    autoplayHoverPause:true,
    autoplayTimeout:2000,
    responsiveClass:true,
    responsive:{
        0:{
            items:1,
        },
        991:{
            items:3,
        },
        767:{
            items:2,
        },
        1000:{
            items:4,
        }
    }
});
// agent-hm-end

// banner-slider-start

$('#home-banner-slider').owlCarousel({
	autoplay:true,
	loop:true,
	margin:0,
	dots:true,
	nav:false,
	animateOut: 'fadeOut',
	animateIn: 'fadeIn',
	items:1
});


// banner-slider-end

// agent-slider-start
$('#agent-slider').owlCarousel({
    margin: 0,
    center: true,
    autoplay:false,
    loop: true,
    dots: false,
    nav: true,
    navText: ['<span class="fas fa-chevron-left owl-arrows"></span>', '<span class="fas fa-chevron-right owl-arrows"></span>'],
    responsive: {
    0: {
       items: 1
    },
    767: {
       items: 1,
    },
    768: {
       items: 3,
    },
    1000: {
       items: 3,
    }
    }
});
// agent-slider-end

// testimonial-slider-start
$('#testimonial-slider').owlCarousel({
    margin: 10,
    autoplay:true,
    loop: true,
    nav: false,
    dots: false,
    dots: false,
    responsive: {
    0: {
       items: 1
    },
    991: {
       items: 2,
    },
    1500: {
       items: 3,
    },
    1600: {
		items: 4,
	}
    }
});
// testimonial-slider-end

// partner-slider-start

$('#partner-slider').owlCarousel({
    margin: 10,
    autoplay:true,
    loop: true,
    dots: false,
    nav: false,
    autoplayTimeout: 2000,
    smartSpeed: 800,
    responsive: {
    0: {
       items: 1
    },
    600: {
       items: 2,
    },
    768: {
       items: 3,
    },
    1000: {
       items: 4,
    }
    }
});
// partner-slider-end

// testimonial-slider-start
$('#location-slider').owlCarousel({
    margin: 10,
    center: true,
    autoplay:false,
    loop: true,
    dots: false,
    nav: false,
    responsive: {
    0: {
       items: 1
    },
    767: {
       items: 1,
    },
    768: {
       items: 3,
    },
    1000: {
       items: 3,
    }
    }
});
// testimonial-slider-end


// project-slider-start

$('#project-slider').owlCarousel({
    autoplay:false,
    loop:true,
    margin:10,
    dots:true,
    nav:false,
    navText: ['<span class="fas fa-arrow-alt-circle-left"></span>','<span class="fas fa-arrow-alt-circle-right"></span>'],
    items:1
    });
// project-slider-end

// gallery-slider-start

$('#gallery-slider').owlCarousel({
    autoplay:false,
    loop:true,
    margin:0,
    dots:false,
    nav:true,
    navText: ['<span class="far fa-chevron-left owl-arrow"></span>','<span class="far fa-chevron-right owl-arrow"></span>'],
    items:1
    });
// gallery-slider-end




// review-star
$(document).ready(function() {
    $('#stars li').on('click', function() {
        var onStar = parseInt($(this).data('value'), 10); // The star currently selected
        var stars = $(this).parent().children('li.star');

        for (i = 0; i < stars.length; i++) {
            $(stars[i]).removeClass('selected');
        }

        for (i = 0; i < onStar; i++) {
            $(stars[i]).addClass('selected');
        }
    });


});
// review-star-end



// calendar-slider-start
$('#calendar-slider').owlCarousel({
    margin: 5,
    autoplay:false,
    loop: true,
    dots: false,
    nav: false,
    navText: ['<span class="far fa-chevron-left owl-arrow"></span>','<span class="far fa-chevron-right owl-arrow"></span>'],
    responsive: {
     480: {
       items: 3
    },
     575: {
       items: 4
    },
    767: {
       items: 5,
    },
    991: {
       items: 4,
    },
    1000: {
       items: 3,
    },
    1199: {
       items: 3.5,
    },
    1600: {
       items: 5,
    }
    }
});
// calendar-slider-end








//  const inputBox = document.getElementById("price-filter");const newDiv = document.getElementById("price-box");inputBox.addEventListener("click", function() {    if (newDiv.style.display === "none" || newDiv.style.display === "") {        newDiv.style.display = "block";    } else {        newDiv.style.display = "none";    }});