$(function() {
  $.getJSON('/js/posturl.json', function(json) {
    let postUrl = Object.keys(json);
    let keyStart = 0;

    setTimeout(function(){
      keyStart = readPost(keyStart);
    }, 10);

    window.addEventListener('scroll', function() {
      let pos = showPosition(document.body);
      if ((pos == 100) && (keyStart < postUrl.length)) {
        setTimeout(function(){
          keyStart = readPost(keyStart);
        }, 200);
      };
    });

    function readPost(keyStart) {
      for (let key of postUrl.slice(keyStart, keyStart + 10)) {
        html = '<section class="indexlist container shadow">'
              + '<a class="overlay" href="/post/' + key + '"></a>'
              + '<div class="inner">'
              + '<header class="mb-2">' + json[key]['title'] + '</header>'
        for (let tag of json[key]['tags']) {
          html += '<a href="/page/tags.html?tag='
                + tag
                + '" class="text-muted bg-warning rounded-pill shadow-sm px-2 mr-2 text-decoration-none">'
                + tag
                + '</a>'
        }
        html += '</div></section>'
        $('main').append(html);
      }
      return keyStart + 10;
    };

    function showPosition(elm) {
      let parent = elm.parentNode;
      let pos = (elm.scrollTop || parent.scrollTop) / (parent.scrollHeight - parent.clientHeight) * 100;
      return pos;
    };
  });
});
