$(function() {
  $('#inputs').focus(function() {
    $(this).keydown(function(event) {
      if(event.keyCode == 13) {
        event.preventDefault();
        $('#search').click();
      };
    });
  });

  $('#search').click(function() {
    let keywords = $('#inputs').val().split(' ');
    while ($.inArray('', keywords) != -1) {
      keywords.splice($.inArray('', keywords), 1);
    };
    for (let i = 0; i < keywords.length; i++) {
      keywords[i] = keywords[i].toLowerCase();
    }
    if (keywords.length != 0) {
      let first = true;
      let url = '/page/tags.html?';
      for (let value of keywords) {
        if (first) {
          url += 'q=' + value;
          first = false;
        } else {
          url += '&q=' + value;
        };
      };
      window.location.href = url;
    };
  });
});
