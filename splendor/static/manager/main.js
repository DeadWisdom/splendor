

$(document).on('nav', function(e) {
    $(document).trigger('nav:' + e.module);
});

$(document).on('nav:library', function() {
    var panel = summonPanel({title: 'Library', id: 'library'});
});

// Helpers //
$.fn.manifest = function(fn) {
    if (this.length == 0) {
        return fn();
    }
    return this;
}

/*(function() {
    _responses = {};

    function router(method) {
        return function(path, data, success) {
            if (!success) {
                success = data;
                data = null;
            }

            return splendor.route({ method: 'get', path: path, data: data, success: success });
        }
    }

    function on_response(result) {

    }

    window.splendor = {
        next_request_id: 1,

        route : function(opts) {
            opts = $.extend({
                method: 'get',
                dataType: 'json',
                headers: {},
            }, opts);

            opts.method = opts.method.toLowerCase();

            if (socket.connected) {
                socket.emit('ajax', opts);
            } else {
                if (method == 'get' && method == 'post') {
                    opts.type = opts.method;
                    opts.method = null;
                } else {
                    opts.headers['X-METHOD'] = method;
                    opts.type = 'post';
                }

                opts.url = window.SPLENDOR_BASE + opts.path;
                opts.path = null;

                $.ajax(opts);
            }
        },
        get: router('get'),
        post: router('post'),
        del: router('del'),
        put: router('put'),
        patch: router('patch'),
        head: router('head'),
    }
})();*/

/*
// Sockets
var socket = new WebSocket('ws://' + location.host);

socket.onopen = function () {
  socket.send('ping');
};

socket.onmessage = function (e) {
  console.log('Server: ', e.data);
};

function Splendor() {
    this.socket = new WebSocket('ws://' + location.host);
}

$.extend(Splendor.prototype, {
    open : function() {

    },
    on : function(message, fn) {

    },
    subscribe : function() {

    }
});
*/