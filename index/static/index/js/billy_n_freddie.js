jQuery(window).scroll(function() {
var window_width = $(window).width();
  if(window_width < 480 && window_width > 300) {
        if (jQuery(this).scrollTop() > 100) {
            jQuery('.billy').stop().animate({ right: '-20px' });
            jQuery('.freddie').stop().animate({ left: '5px' });
       } else {
            jQuery('.billy').stop().animate({ right: '-200px' });
            jQuery('.freddie').stop().animate({ left: '-200px' });
       }
  }
  else if(window_width <= 300){
          if (jQuery(this).scrollTop() > 100) {
            jQuery('.billy').stop().animate({ right: '-40px' });
            jQuery('.freddie').stop().animate({ left: '0px' });
       } else {
            jQuery('.billy').stop().animate({ right: '-150px' });
            jQuery('.freddie').stop().animate({ left: '-100px' });
       }
  }
  else{
        if (jQuery(this).scrollTop() > 100) {
            jQuery('.billy').stop().animate({ right: '300px' });
            jQuery('.freddie').stop().animate({ left: '400px' });
       } else {
            jQuery('.billy').stop().animate({ right: '-600px' });
            jQuery('.freddie').stop().animate({ left: '-600px' });
       }
  }
});