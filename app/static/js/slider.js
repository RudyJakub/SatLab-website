// prosta implementacja fadeIn/Out podczas scrolla


// config
const bottomOffset = -200; // callable fadeIn/Out offset from bottom in px
const fadeOffset = 5; // 10px in one direction

function fade() {
    var windowBottom = $(this).scrollTop() + $(this).outerHeight();
    $(".fade").each(function() {

      // Check the location of each desired element 
      var objectBottom = $(this).offset().top + $(this).innerHeight()/2 + bottomOffset;
      var direction = $(this).attr('direction') == 'left' ? `translateX(-${fadeOffset}px)` : `translateX(${fadeOffset}px)`; //
      
      // If the element is completely within bounds of the window, fade it in 
      if (objectBottom < windowBottom) { //object comes into view (scrolling down)
        if ($(this).css("opacity")==0) {
          $(this).css('opacity', '1').css('transform', 'translateX(0)');
        }
        
      } else { //=object goes out of view (scrolling up)
        if ($(this).css("opacity")==1) {$(this).css('opacity', '0').css('transform', direction);}
      }
    });
}


// FADE ON SCROLL
$(window).on("load",function() {
    fade();
    $(window).scroll(function() {
        fade();
    }).scroll(); //invoke scroll-handler on page-load
});

