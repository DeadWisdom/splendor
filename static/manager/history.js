var historyCollection = splendor.collection({url: 'ws://' + location.host + location.pathname}).subscribe();


(function() {
    var panel = null;

    function summonEvent(event) {
        var item = panel.find("#event-" + event._id).manifest(function() {
                return $('.event.prototype').clone()
                    .removeClass('prototype')
                    .attr('id', 'event-' + event._id)
                    .prependTo(panel.children('.content'));
            });

        if (event._created)
            item.fadeOut('fast').fadeIn();

        item.find('.uri').append(event.uri);
        item.find('.action').append(event.action);
        setTimeAbbrValue(item.find('.utc abbr'), event.utc);

        var data = item.find('.data').empty();
        for(var k in event.data) {
            data.append($('<dt>' + k + '</dt>'));
            data.append($('<dd>' + JSON.stringify(event.data[k]) + '</dd>'));
        }
    }

    function setRoutes(events) {
        for(var i = 0; i < events.length; i++) {
            summonEvent(events[i]);
        }
    }

    historyCollection.on('update', function(msg) {
        msg._created = true;
        summonEvent(msg);
    })

    $(document).on('nav:history', function() {
        panel = summonPanel({title: 'History', id: 'history'});

        $.ajax({
            url: window.location.href,
            dataType: 'json',
            cache: false,
            success: function(data) {
                setRoutes(data.contents);
            }
        });
    });
})();


// Time Abbr //
function setTimeAbbrValue(abbr, value) {
    abbr.attr('title', value);
    updateTimeAbbr(abbr);
}

function updateTimeAbbr(abbr) {
    if (abbr.closest('.prototype').length > 0) return;
    var current = abbr.text();
    var update = moment.utc(abbr.attr('title')).local().fromNow();
    if (current == update) return;
    abbr.text( update );
    if (abbr.hasClass('updated'))
        return abbr.fadeOut('fast').fadeIn();
    else
        return abbr.addClass('updated');
}

function updateTimeAbbrDelayed(abbr, delay) {
    setTimeout(function() {
        updateTimeAbbr(abbr);
    }, delay);
}

function updateAllTimeAbbrs() {
    $('abbr.ago').each(function(index) {
        updateTimeAbbrDelayed( $(this), index * 50 );
    });
}

// Update all time abbrs every 15 seconds
$(function() {
    setInterval(updateAllTimeAbbrs, 15 * 1000);
});




