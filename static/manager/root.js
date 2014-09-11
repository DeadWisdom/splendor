var appCollection = splendor.collection({url: 'ws://' + location.host + location.pathname}).subscribe();


(function() {
    var panel = null;
    var actions = [
        {label: 'Add', key: 'add', icon: 'plus'}
    ];

    function findRoute(url) {
        var search = url.replace(/([^\w])/g, '\\$1');
        return panel.find("[url=" + search + "]");
    }

    function summonRoute(url, route) {
        var item = findRoute(url).manifest(function() {
                return $('.route.prototype').clone()
                    .removeClass('prototype')
                    .attr('url', url)
                    .appendTo(panel.children('.content'));
            });

        item.find('.url').append(url);

        var data = item.find('.data').empty();
        for(var k in route) {
            data.append($('<dt>' + k + '</dt>'));
            data.append($('<dd>' + JSON.stringify(route[k]) + '</dd>'));
        }
    }

    function setRoutes(routes) {
        for(var i = 0; i < routes.length; i++) {
            var url = routes[i][0];
            var route = routes[i][1];

            summonRoute(url, route);
        }
    }

    appCollection.on('visit', function(msg) {
        var color = '#aaefbb';
        if (msg.method == 'POST') {
            color = '#aabbef';
        } else if (msg.method == 'SOCKET') {
            color = '#efaaef';
        }
        console.log(msg);

        findRoute(msg.concrete).css('backgroundColor', color).stop(true).animate({backgroundColor: '#fafafa'}, 300);
    });

    $(document).on('nav:root', function() {
        panel = summonPanel({title: 'Root', id: 'root', actions: actions});

        panel.on('add', function() {
            summonPanel({title: 'Add Resource', id: 'add-resource'});
            console.log("Add");
        });

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