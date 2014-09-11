function loadModule() {
    var state = History.getState();
    var path = state.url.split('/');
    var module = path[path.length - 1];
    
    $('section').not('.prototype').remove();

    $('nav a').each(function() {
        $(this).toggleClass('selected', $(this).attr('href') == module);
    });

    var e = $.Event('nav');
    e.module = module;
    e.state = state;
    $(document).trigger(e)
}

// When a user clicks on a nav link, push it as a History state.
$(document).on('click', 'nav a', function(e) {
    var urlPath = '/splendor/' + $(this).attr('href');
    var title = "Splendor - Admin - " + $(this).text();
    History.pushState(null, title, urlPath);
    e.preventDefault();
});

// When the page loads or there is a state change, load the module
History.Adapter.bind(window, 'statechange', loadModule);
$(loadModule);