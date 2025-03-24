(function () {
  $(window).scroll(function () { 
      var Num = $(window).scrollTop() / 500;
      var Num2 = $(window).scrollTop() * .0004; 
      var Num2mod = Num2 + 1;
      var Num3 = $(window).scrollTop() * .2; 
      var Num3mod = Num3 + 1;


      $('.heroEffects .shade').css('opacity', Num);
      $(".heroEffects .bg").css({"transform":"scale(" + Num2mod + ")"});
      $(".heroEffects .text").css({"margin-top":"-" + Num3mod + "px"});
  });
}.call(this));


const swiper = new Swiper('.swiper-container', {
  direction: 'vertical',
  mousewheel: {},
  effect: 'cube',
  keyboard: {
      enabled: true,
      onlyInViewport: false
  }
});
