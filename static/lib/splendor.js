(function() {
    var Socket = _class("Socket", {
        url: null,
        init : function() {
            var ws = new WebSocket(this.url);
            ws.onopen = this.onopen.bind(this);
            ws.onerror = this.onerror.bind(this);
            ws.onclose = this.onclose.bind(this);
            ws.onmessage = this.onmessage.bind(this);
            this.ws = ws;
            this.handlers = {};

            if (this.on) {
                var events = this.on;
                delete this.on;
                for(var k in events) {
                    this.on(k, events[k]);
                }
            }
        },
        onmessage : function(e) {
            var msg = jQuery.parseJSON(e.data);
            this.trigger('message', [msg, e]);
        },
        onclose : function(e) {
            Socket.open -= 1;
            this.trigger('close', [e]);
        },
        onopen : function(e) {
            Socket.open += 1;
            this.trigger('open', [e]);
        },
        onerror : function(e) {
            this.trigger('error', [e]);
        },
        send : function(data) {
            this.ws.send(data);
        },
        close : function() {
            this.ws.close();
        },
        trigger : function(name, args) {
            var fns = this.handlers[name];
            if (fns === undefined)
                return 0;
            for(var i = 0; i < fns.length; i++) {
                fns[i].apply(this, args);
            }
            return fns.length;
        },
        on : function(name, func) {
            if (this.handlers[name] === undefined)
                this.handlers[name] = [];
            this.handlers[name].push(func);
        }
    });

    Socket.open = 0;
    Socket.registry = {};
    Socket.create = _super.override(Socket.create, function(opts) {
        if (!Socket.registry[opts.url])
            Socket.registry[opts.url] = _super(opts);
        return Socket.registry[opts.url];
    });

    var Collection = _class("Collection", {
        url: null,
        init : function() {
            this.handlers = {};
            this.socket = null;
        },
        onMessage : function(msg) {
            if (msg.action) {
                this.trigger(msg.action, [msg]);
            }
            
            this.trigger('message', [msg]);
        },
        create : function(data) {
            this.send("create", data);
        },
        edit : function(data) {
            this.send("edit", data);
        },
        del : function(data) {
            this.send("delete", data);
        },
        reorder : function(data) {
            this.send("reorder", data);
        },
        move : function(data) {
            this.send("move", data);
        },
        send : function(action, data) {
            console.log("send", action, data);
        },
        trigger : function(name, args) {
            var fns = this.handlers[name];
            if (fns === undefined)
                return 0;
            for(var i = 0; i < fns.length; i++) {
                fns[i].apply(this, args);
            }
            return fns.length;
        },
        on : function(name, func) {
            if (this.handlers[name] === undefined)
                this.handlers[name] = [];
            this.handlers[name].push(func);
        },
        subscribe : function() {
            this.socket = Socket({
                url: this.url,
                on: {
                    open: function() {
                        console.log(" * subscribed", this.url);
                    },
                    message: this.onMessage.bind(this)
                }
            });
            return this;
        }
    });

    window.splendor = {
        socket: Socket,
        collection: Collection
    };
})();
