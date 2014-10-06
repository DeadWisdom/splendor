

function summonPanel(opts) {
    var opts = $.extend({
        title: 'Panel',
        actions: [],
        id: null
    }, opts);

    var src = $('#' + opts.id).manifest(function() {
        return $('section.prototype').clone()
                .removeClass('prototype')
                .attr('id', opts.id)
                .appendTo(document.body);
    });
    
    src.find('.title').text(opts.title);

    var action_bar = src.children('.actions').empty();
    $.each(opts.actions, function(i) {
        addAction(src, action_bar, this);
    });

    if (action_bar.children().length > 0)
        src.addClass("hasActions");
    else
        src.removeClass("hasActions");

    return src;
}

function addAction(panel, bar, action) {
    var src = bar.children('.' + action.key).manifest(function() {
        return $('section.prototype .actions > a').clone()
                .addClass(action.key)
                .appendTo(bar)
                .empty()
                .append(action.label).addClass('icon-' + (action.icon || action.key));
    });

    src.click(function(e) {
        panel.trigger(action.key, [e]);
        e.preventDefault();
    });
}