$(function() {
  window.addEventListener('scroll', function() {
    let pos = showPosition();
    $('.percentage-text').text(Math.round(pos) + ' %');
    $('.percentage-bar').css('width', pos + '%');
  });

  // function showPosition(elm) {
  //   let parent = elm.parentNode;
  //   let pos = (elm.scrollTop || parent.scrollTop) / (parent.scrollHeight - parent.clientHeight) * 100;
  //   return pos;
  // };

  // function showPosition() {
  //   let winScroll = document.body.scrollTop || document.documentElement.scrollTop;
  //   let height = document.documentElement.scrollHeight - document.documentElement.clientHeight
  //   return winScroll / height * 100
  // };

  function showPosition() {
    return $(window).scrollTop() / ($(document).height() - $(window).height()) * 100;
  }
});
