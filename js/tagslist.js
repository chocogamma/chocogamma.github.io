$(function() {
  let locationSearch = decodeURIComponent(location.search).substring(1).split('&');
  let locationSearchQ = []
  let locationSearchT = []
  for (let value of locationSearch) {
    if (value.startsWith('q')) {
      locationSearchQ.push(value.substring(2));
    } else if (value.startsWith('tag')) {
      locationSearchT.push(value.substring(4));
    };
  };

  if (locationSearchQ.length != 0) {
    let text = 'Search for: ';
    let first = true;
    for (let value of locationSearchQ) {
      if (first) {
        text += value;
        first = false;
      } else {
        text += ' & ' + value;
      };
    };
    $('section.tagscloud header').text(text)
  }

  $.getJSON('/js/posturl.json', function(json) {
    let postUrl = Object.keys(json);
    let keyStart = 0;
    let tagscloud = [];
    let postUrlReverse = $.extend({}, postUrl);
    postUrlReverse = Object.assign([], postUrlReverse).reverse()
    for (let key of postUrlReverse) {
      for (let value of json[key]['tags']) {
        if ($.inArray(value.trim(), tagscloud) == -1) {
          tagscloud.push(value);
        };
      };
    };

    html = '';
    for (let tag of tagscloud) {
      if ($.inArray(tag.trim(), locationSearchT) == -1) {
        html += '<span class="text-muted bg-warning rounded-pill shadow-sm px-2 mr-2 text-decoration-none">'
              + tag
              + '</span>'
      } else {
        html += '<span class="text-muted border border-warning bg-white rounded-pill shadow-sm px-2 mr-2 text-decoration-none">'
              + tag
              + '</span>'
      }
    };
    $(html).insertAfter('section.tagscloud header');

    for (let tagspan of $('section.tagscloud span')) {
      tagspan.addEventListener('click', function() {
        if ((locationSearchQ.length == 0) && (locationSearchT.length == 0)) {
          window.location.href = '/page/tags.html?tag=' + tagspan.innerHTML.trim();
        } else if ($.inArray(tagspan.innerHTML.trim(), locationSearchT) == -1) {
          window.location.href = location.href + '&tag=' + tagspan.innerHTML.trim();
        } else {
          let first = true;
          let url = '/page/tags.html?';
          for (let search of locationSearchQ) {
            if (first) {
              url += 'q=' + search;
              first = false;
            } else {
              url += '&q=' + search;
            };
          };
          for (let tag of locationSearchT) {
            if (tag.trim() != tagspan.innerHTML.trim()) {
              if (first) {
                url += 'tag=' + tag.trim();
                first = false;
              } else {
                url += '&tag=' + tag.trim();
              };
            };
          };
          window.location.href = url;
        };
      });
    };

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
      let time = 0
      let item = 0
      for (let key of postUrl.slice(keyStart)) {
        if (checkQT(key)) {
          html = '<section class="tagslist container shadow">'
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
          time += 1;
        }
        item += 1;
        if (time == 10) {
          break;
        }
      }
      return keyStart + item;
    };

    function checkQT(key) {
      let check = true;
      if (locationSearchQ.length != 0) {
        for (let value of locationSearchQ) {
          if (!(json[key]['title'].toLowerCase().includes(value.trim()))) {
            check = false;
            break;
          }
        }
      }
      if (locationSearchT.length != 0) {
        for (let value of locationSearchT) {
          if ($.inArray(value.trim(), json[key]['tags']) == -1) {
            check = false;
            break;
          }
        }
      }
      if (key == 'hello-world.html') {
        check = true;
      }
      return check;
    }

    function showPosition(elm) {
      let parent = elm.parentNode;
      let pos = (elm.scrollTop || parent.scrollTop) / (parent.scrollHeight - parent.clientHeight) * 100;
      return pos;
    };
  });
});
