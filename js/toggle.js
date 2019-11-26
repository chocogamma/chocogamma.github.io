$(function() {
  window.addEventListener('scroll', function() {
    let pos = showPosition(document.body);
    if (pos < 50) {
      $('.toggle-top').fadeOut(900);
    } else {
      $('.toggle-top').fadeIn(500);
    }
  });

  $('.toggle-top').hover(function() {
    $(this).css('opacity', 0.8);
  }, function() {
    $(this).css('opacity', 1);
  });

  $('.toggle-top').click(function() {
    $('html, body').animate({scrollTop: 0}, 900);
  });

  function showPosition(elm) {
    let parent = elm.parentNode;
    let pos = (elm.scrollTop || parent.scrollTop) / (parent.scrollHeight - parent.clientHeight) * 100;
    return pos;
  };
});
