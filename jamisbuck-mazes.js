var MersenneTwister;
MersenneTwister = (function() {
    a.prototype.N = 624;
    a.prototype.M = 397;
    a.prototype.MATRIX_A = 2567483615;
    a.prototype.UPPER_MASK = 2147483648;
    a.prototype.LOWER_MASK = 2147483647;
    function a(b) {
        this.mt = new Array(this.N);
        this.setSeed(b)
    }
    a.prototype.unsigned32 = function(b) {
        if (b < 0) {
            return (b ^ this.UPPER_MASK) + this.UPPER_MASK
        } else {
            return b
        }
    };
    a.prototype.subtraction32 = function(c, b) {
        if (c < b) {
            return this.unsigned32((4294967296 - (b - c)) % 4294967295)
        } else {
            return c - b
        }
    };
    a.prototype.addition32 = function(c, b) {
        return this.unsigned32((c + b) & 4294967295)
    };
    a.prototype.multiplication32 = function(e, c) {
        var b,
        d;
        d = 0;
        for (b = 0; b < 32; b++) {
            if ((e >>> b) & 1) {
                d = this.addition32(d, this.unsigned32(c << b))
            }
        }
        return d
    };
    a.prototype.setSeed = function(b) {
        if (!b || typeof b === "number") {
            return this.seedWithInteger(b)
        } else {
            return this.seedWithArray(b)
        }
    };
    a.prototype.defaultSeed = function() {
        var b;
        b = new Date();
        return b.getMinutes() * 60000 + b.getSeconds() * 1000 + b.getMilliseconds()
    };
    a.prototype.seedWithInteger = function(c) {
        var b;
        this.seed = c != null ? c: this.defaultSeed();
        this.mt[0] = this.unsigned32(this.seed & 4294967295);
        this.mti = 1;
        b = [];
        while (this.mti < this.N) {
            this.mt[this.mti] = this.addition32(this.multiplication32(1812433253, this.unsigned32(this.mt[this.mti - 1] ^ (this.mt[this.mti - 1] >>> 30))), this.mti);
            this.mti[this.mti] = this.unsigned32(this.mt[this.mti] & 4294967295);
            b.push(this.mti++)
        }
        return b
    };
    a.prototype.seedWithArray = function(f) {
        var e,
        d,
        b,
        c;
        this.seedWithInteger(19650218);
        e = 1;
        d = 0;
        b = this.N > f.length ? this.N: f.length;
        while (b > 0) {
            c = this.multiplication32(this.unsigned32(this.mt[e - 1] ^ (this.mt[e - 1] >>> 30)), 1664525);
            this.mt[e] = this.addition32(this.addition32(this.unsigned32(this.mt[e] ^ c), f[d]), d);
            this.mt[e] = this.unsigned32(this.mt[e] & 4294967295);
            e++;
            d++;
            if (e >= this.N) {
                this.mt[0] = this.mt[this.N - 1];
                e = 1
            }
            if (d >= f.length) {
                d = 0
            }
            b--
        }
        b = this.N - 1;
        while (b > 0) {
            this.mt[e] = this.subtraction32(
              this.unsigned32(this.mt[e] ^
                this.multiplication32(this.unsigned32(this.mt[e - 1] ^ (this.mt[e - 1] >>> 30)), 1566083941)
              ), e
            );
            this.mt[e] = this.unsigned32(this.mt[e] & 4294967295);
            e++;
            if (e >= this.N) {
                this.mt[0] = this.mt[this.N - 1];
                e = 1
            }
        }
        return this.mt[0] = 2147483648
    };
    a.prototype.nextInteger = function(b) {
        var c,
        d,
        e;
        if ((b != null ? b: 1) < 1) {
            return 0
        }
        d = [0, this.MATRIX_A];
        if (this.mti >= this.N) {
            c = 0;
            while (c < this.N - this.M) {
                e = this.unsigned32((this.mt[c] & this.UPPER_MASK) | (this.mt[c + 1] & this.LOWER_MASK));
                this.mt[c] = this.unsigned32(this.mt[c + this.M] ^ (e >>> 1) ^ d[e & 1]);
                c++
            }
            while (c < this.N - 1) {
                e = this.unsigned32((this.mt[c] & this.UPPER_MASK) | (this.mt[c + 1] & this.LOWER_MASK));
                this.mt[c] = this.unsigned32(this.mt[c + this.M - this.N] ^ (e >>> 1) ^ d[e & 1]);
                c++
            }
            e = this.unsigned32((this.mt[this.N - 1] & this.UPPER_MASK) | (this.mt[0] & this.LOWER_MASK));
            this.mt[this.N - 1] = this.unsigned32(this.mt[this.M - 1] ^ (e >>> 1) ^ d[e & 1]);
            this.mti = 0
        }
        e = this.mt[this.mti++];
        e = this.unsigned32(e ^ (e >>> 11));
        e = this.unsigned32(e ^ ((e << 7) & 2636928640));
        e = this.unsigned32(e ^ ((e << 15) & 4022730752));
        return this.unsigned32(e ^ (e >>> 18)) % (b != null ? b: 4294967296)
    };
    a.prototype.nextFloat = function() {
        return this.nextInteger() / 4294967295
    };
    a.prototype.nextBoolean = function() {
        return this.nextInteger() % 2 === 0
    };
    return a
})();

var Maze;
Maze = (function() {
    function a(d, b, c) {
        this.width = d;
        this.height = b;
        c != null ? c: c = {};
        this.callback = c.callback ||
        function(g, e, f) {};
        this.grid = new a.Grid(this.width, this.height);
        this.rand = c.rng || new MersenneTwister(c.seed)
    }
    a.prototype.randomBoolean = function() {
        return this.rand.nextBoolean()
    };
    a.prototype.randomElement = function(b) {
        return b[this.rand.nextInteger(b.length)]
    };
    a.prototype.removeRandomElement = function(c) {
        var b;
        b = c.splice(this.rand.nextInteger(c.length), 1);
        if (b) {
            return b[0]
        }
    };
    a.prototype.randomizeList = function(e) {
        var c,
        b,
        d;
        c = e.length - 1;
        while (c > 0) {
            b = this.rand.nextInteger(c + 1);
            d = [e[b], e[c]],
            e[c] = d[0],
            e[b] = d[1];
            c--
        }
        return e
    };
    a.prototype.randomDirections = function() {
        return this.randomizeList([1, 2, 4, 8])
    };
    a.prototype.generate = function() {
        var b;
        b = [];
        while (true) {
            if (!this.step()) {
                break
            }
        }
        return b
    };
    a.prototype.isEast = function(b, c) {
        return this.grid.isMarked(b, c, a.Direction.E)
    };
    a.prototype.isWest = function(b, c) {
        return this.grid.isMarked(b, c, a.Direction.W)
    };
    a.prototype.isNorth = function(b, c) {
        return this.grid.isMarked(b, c, a.Direction.N)
    };
    a.prototype.isSouth = function(b, c) {
        return this.grid.isMarked(b, c, a.Direction.S)
    };
    a.prototype.isValid = function(b, c) {
        return (0 <= b && b < this.width) && (0 <= c && c < this.height)
    };
    a.prototype.carve = function(b, d, c) {
        return this.grid.mark(b, d, c)
    };
    a.prototype.uncarve = function(b, d, c) {
        return this.grid.clear(b, d, c)
    };
    a.prototype.isSet = function(b, d, c) {
        return this.grid.isMarked(b, d, c)
    };
    a.prototype.isBlank = function(b, c) {
        return this.grid.at(b, c) === 0
    };
    return a
})();
Maze.Algorithms = {};
Maze.Direction = {
    N: 1,
    S: 2,
    E: 4,
    W: 8,
    dx: {
        1: 0,
        2: 0,
        4: 1,
        8: -1
    },
    dy: {
        1: -1,
        2: 1,
        4: 0,
        8: 0
    },
    opposite: {
        1: 2,
        2: 1,
        4: 8,
        8: 4
    }
};
Maze.Grid = (function() {
    function a(d, c) {
        var b,
        e;
        this.width = d;
        this.height = c;
        this.data = (function() {
            var g,
            f;
            f = [];
            for (e = 1, g = this.height; (1 <= g ? e <= g: e >= g); (1 <= g ? e += 1: e -= 1)) {
                f.push((function() {
                    var i,
                    h;
                    h = [];
                    for (b = 1, i = this.width; (1 <= i ? b <= i: b >= i); (1 <= i ? b += 1: b -= 1)) {
                        h.push(0)
                    }
                    return h
                }).call(this))
            }
            return f
        }).call(this)
    }
    a.prototype.at = function(b, c) {
        return this.data[c][b]
    };
    a.prototype.mark = function(b, d, c) {
        return this.data[d][b] |= c
    };
    a.prototype.clear = function(b, d, c) {
        return this.data[d][b] &= ~c
    };
    a.prototype.isMarked = function(b, d, c) {
        return (this.data[d][b] & c) === c
    };
    return a
})();
var __bind = function(a, b) {
    return function() {
        return a.apply(b, arguments)
    }
};
Maze.createWidget = function(algorithm, width, height, options) {
    var ACTIONS,
    defaultCallback,
    element,
    gridClass,
    html,
    id,
    mazeClass,
    updateWalls,
    _ref,
    _ref2;
    options != null ? options: options = {};
    updateWalls = function(maze, x, y, classes) {
        if (maze.isEast(x, y)) {
            classes.push("e")
        }
        if (maze.isWest(x, y)) {
            classes.push("w")
        }
        if (maze.isSouth(x, y)) {
            classes.push("s")
        }
        if (maze.isNorth(x, y)) {
            return classes.push("n")
        }
    };
    ACTIONS = {
        AldousBroder: function(maze, x, y, classes) {
            if (maze.isCurrent(x, y)) {
                return classes.push("cursor")
            } else {
                if (!maze.isBlank(x, y)) {
                    classes.push("in");
                    return updateWalls(maze, x, y, classes)
                }
            }
        },
        GrowingTree: function(maze, x, y, classes) {
            if (!maze.isBlank(x, y)) {
                if (maze.inQueue(x, y)) {
                    classes.push("f")
                } else {
                    classes.push("in")
                }
                return updateWalls(maze, x, y, classes)
            }
        },
        HuntAndKill: function(maze, x, y, classes) {
            if (maze.isCurrent(x, y)) {
                classes.push("cursor")
            }
            if (!maze.isBlank(x, y)) {
                classes.push("in");
                return updateWalls(maze, x, y, classes)
            }
        },
        Prim: function(maze, x, y, classes) {
            if (maze.isFrontier(x, y)) {
                return classes.push("f")
            } else {
                if (maze.isInside(x, y)) {
                    classes.push("in");
                    return updateWalls(maze, x, y, classes)
                }
            }
        },
        RecursiveBacktracker: function(maze, x, y, classes) {
            if (maze.isStack(x, y)) {
                classes.push("f")
            } else {
                classes.push("in")
            }
            return updateWalls(maze, x, y, classes)
        },
        RecursiveDivision: function(maze, x, y, classes) {
            return updateWalls(maze, x, y, classes)
        },
        Wilson: function(maze, x, y, classes) {
            if (maze.isCurrent(x, y)) {
                classes.push("cursor");
                return updateWalls(maze, x, y, classes)
            } else {
                if (!maze.isBlank(x, y)) {
                    classes.push("in");
                    return updateWalls(maze, x, y, classes)
                } else {
                    if (maze.isVisited(x, y)) {
                        return classes.push("f")
                    }
                }
            }
        },
        "default": function(maze, x, y, classes) {
            if (!maze.isBlank(x, y)) {
                classes.push("in");
                return updateWalls(maze, x, y, classes)
            }
        }
    };
    defaultCallback = function(maze, x, y) {
        var cell,
        classes;
        classes = []; (ACTIONS[algorithm] || ACTIONS["default"])(maze, x, y, classes);
        cell = document.getElementById("" + maze.element.id + "_y" + y + "x" + x);
        return cell.className = classes.join(" ")
    };
    id = options.id || algorithm.toLowerCase(); (_ref = options.callback) != null ? _ref: options.callback = defaultCallback; (_ref2 = options.interval) != null ? _ref2: options.interval = 50;
    mazeClass = "maze";
    if (options["class"]) {
        mazeClass += " " + options["class"]
    }
    gridClass = "grid";
    if (options.wallwise) {
        gridClass += " invert"
    }
    html = '<div id="' + id + '" class="' + mazeClass + '">\n  <div id="' + id + '_grid" class="' + gridClass + '"></div>\n  <div class="operations">\n    <a id="' + id + '_reset" href="#" onclick="document.getElementById(\'' + id + '\').mazeReset(); return false;">Reset</a>\n    <a id="' + id + '_step" href="#" onclick="document.getElementById(\'' + id + '\').mazeStep(); return false;">Step</a>\n    <a id="' + id + '_run" href="#" onclick="document.getElementById(\'' + id + "').mazeRun(); return false;\">Run</a>\n  </div>\n</div>";
    document.write(html);
    element = document.getElementById(id);
    element.addClassName = function(el, name) {
        var className,
        classNames,
        _i,
        _len;
        classNames = el.className.split(" ");
        for (_i = 0, _len = classNames.length; _i < _len; _i++) {
            className = classNames[_i];
            if (className === name) {
                return
            }
        }
        return el.className += " " + name
    };
    element.removeClassName = function(el, name) {
        var className,
        classNames,
        _i,
        _len,
        _results;
        if (el.className.length > 0) {
            classNames = el.className.split(" ");
            el.className = "";
            _results = [];
            for (_i = 0, _len = classNames.length; _i < _len; _i++) {
                className = classNames[_i];
                _results.push(className !== name ? (el.className.length > 0 ? el.className += " ": void 0, el.className += className) : void 0)
            }
            return _results
        }
    };
    element.mazeRun = function() {
        if (this.mazeStepInterval != null) {
            clearInterval(this.mazeStepInterval);
            return this.mazeStepInterval = null
        } else {
            return this.mazeStepInterval = setInterval((__bind(function() {
                return this.mazeStep()
            },
            this)), options.interval)
        }
    };
    element.mazeStep = function() {
        if (!this.maze.step()) {
            if (this.mazeStepInterval != null) {
                clearInterval(this.mazeStepInterval);
                this.mazeStepInterval = null
            }
            this.addClassName(document.getElementById("" + this.id + "_step"), "disabled");
            return this.addClassName(document.getElementById("" + this.id + "_run"), "disabled")
        }
    };
    element.mazeReset = function() {
        var grid,
        gridElement,
        row_id,
        value,
        x,
        y,
        _ref,
        _ref2;
        if (this.mazeStepInterval != null) {
            clearInterval(this.mazeStepInterval);
            this.mazeStepInterval = null
        }
        if (options.input) {
            value = document.getElementById(options.input).value;
            eval("this.__input = {" + value + "}")
        }
        this.maze = new Maze.Algorithms[algorithm](width, height, {
            callback: options.callback,
            seed: options.seed,
            rng: options.rng,
            input: this.__input
        });
        this.maze.element = this;
        grid = "";
        for (y = 0, _ref = this.maze.height; (0 <= _ref ? y < _ref: y > _ref); (0 <= _ref ? y += 1: y -= 1)) {
            row_id = "" + this.id + "_y" + y;
            grid += "<div class='row' id='" + row_id + "'>";
            for (x = 0, _ref2 = this.maze.width; (0 <= _ref2 ? x < _ref2: x > _ref2); (0 <= _ref2 ? x += 1: x -= 1)) {
                grid += "<div id='" + row_id + "x" + x + "'></div>"
            }
            grid += "</div>"
        }
        gridElement = document.getElementById("" + this.id + "_grid");
        gridElement.innerHTML = grid;
        this.removeClassName(document.getElementById("" + this.id + "_step"), "disabled");
        return this.removeClassName(document.getElementById("" + this.id + "_run"), "disabled")
    };
    return element.mazeReset()
};
var __hasProp = Object.prototype.hasOwnProperty,
__extends = function(d, b) {
    for (var a in b) {
        if (__hasProp.call(b, a)) {
            d[a] = b[a]
        }
    }
    function c() {
        this.constructor = d
    }
    c.prototype = b.prototype;
    d.prototype = new c;
    d.__super__ = b.prototype;
    return d
};
Maze.Algorithms.AldousBroder = (function() {
    __extends(a, Maze);
    a.prototype.IN = 16;
    function a(d, b, c) {
        a.__super__.constructor.apply(this, arguments);
        this.state = 0;
        this.remaining = this.width * this.height
    }
    a.prototype.isCurrent = function(b, c) {
        return this.x === b && this.y === c
    };
    a.prototype.startStep = function() {
        this.x = this.rand.nextInteger(this.width);
        this.y = this.rand.nextInteger(this.height);
        this.carve(this.x, this.y, this.IN);
        this.callback(this, this.x, this.y);
        this.remaining--;
        return this.state = 1
    };
    a.prototype.runStep = function() {
        var b,
        g,
        f,
        j,
        h,
        d,
        i,
        e,
        c;
        if (this.remaining > 0) {
            e = this.randomDirections();
            for (d = 0, i = e.length; d < i; d++) {
                b = e[d];
                g = this.x + Maze.Direction.dx[b];
                f = this.y + Maze.Direction.dy[b];
                if (this.isValid(g, f)) {
                    c = [this.x, this.y, g, f],
                    j = c[0],
                    h = c[1],
                    this.x = c[2],
                    this.y = c[3];
                    if (this.isBlank(g, f)) {
                        this.carve(j, h, b);
                        this.carve(this.x, this.y, Maze.Direction.opposite[b]);
                        this.remaining--;
                        if (this.remaining === 0) {
                            delete this.x;
                            delete this.y
                        }
                    }
                    this.callback(this, j, h);
                    this.callback(this, g, f);
                    break
                }
            }
        }
        return this.remaining > 0
    };
    a.prototype.step = function() {
        switch (this.state) {
        case 0:
            this.startStep();
            break;
        case 1:
            this.runStep()
        }
        return this.remaining > 0
    };
    return a
})();
var __hasProp = Object.prototype.hasOwnProperty,
__extends = function(d, b) {
    for (var a in b) {
        if (__hasProp.call(b, a)) {
            d[a] = b[a]
        }
    }
    function c() {
        this.constructor = d
    }
    c.prototype = b.prototype;
    d.prototype = new c;
    d.__super__ = b.prototype;
    return d
};
Maze.Algorithms.RecursiveBacktracker = (function() {
    __extends(a, Maze);
    a.prototype.IN = 16;
    a.prototype.STACK = 32;
    a.prototype.START = 1;
    a.prototype.RUN = 2;
    a.prototype.DONE = 3;
    function a(d, b, c) {
        a.__super__.constructor.apply(this, arguments);
        this.state = this.START;
        this.stack = []
    }
    a.prototype.step = function() {
        switch (this.state) {
        case this.START:
            this.startStep();
            break;
        case this.RUN:
            this.runStep()
        }
        return this.state !== this.DONE
    };
    a.prototype.startStep = function() {
        var b,
        d,
        c;
        c = [this.rand.nextInteger(this.width), this.rand.nextInteger(this.height)],
        b = c[0],
        d = c[1];
        this.carve(b, d, this.IN | this.STACK);
        this.callback(this, b, d);
        this.stack.push({
            x: b,
            y: d,
            dirs: this.randomDirections()
        });
        return this.state = this.RUN
    };
    a.prototype.runStep = function() {
        var d,
        c,
        b,
        e;
        while (true) {
            d = this.stack[this.stack.length - 1];
            c = d.dirs.pop();
            b = d.x + Maze.Direction.dx[c];
            e = d.y + Maze.Direction.dy[c];
            if (this.isValid(b, e) && this.isBlank(b, e)) {
                this.stack.push({
                    x: b,
                    y: e,
                    dirs: this.randomDirections()
                });
                this.carve(d.x, d.y, c);
                this.callback(this, d.x, d.y);
                this.carve(b, e, Maze.Direction.opposite[c] | this.STACK);
                this.callback(this, b, e);
                break
            }
            if (d.dirs.length === 0) {
                this.uncarve(d.x, d.y, this.STACK);
                this.callback(this, d.x, d.y);
                this.stack.pop();
                break
            }
        }
        if (this.stack.length === 0) {
            return this.state = this.DONE
        }
    };
    a.prototype.isStack = function(b, c) {
        return this.isSet(b, c, this.STACK)
    };
    return a
})();
var __hasProp = Object.prototype.hasOwnProperty,
__extends = function(d, b) {
    for (var a in b) {
        if (__hasProp.call(b, a)) {
            d[a] = b[a]
        }
    }
    function c() {
        this.constructor = d
    }
    c.prototype = b.prototype;
    d.prototype = new c;
    d.__super__ = b.prototype;
    return d
};
Maze.Algorithms.BinaryTree = (function() {
    __extends(a, Maze);
    a.prototype.IN = 16;
    function a(d, b, c) {
        a.__super__.constructor.apply(this, arguments);
        this.x = 0;
        this.y = 0
    }
    a.prototype.step = function() {
        var d,
        c,
        b,
        e;
        if (this.y >= this.height) {
            return false
        }
        c = [];
        if (this.y > 0) {
            c.push(Maze.Direction.N)
        }
        if (this.x > 0) {
            c.push(Maze.Direction.W)
        }
        d = this.randomElement(c);
        if (d) {
            b = this.x + Maze.Direction.dx[d];
            e = this.y + Maze.Direction.dy[d];
            this.carve(this.x, this.y, d);
            this.carve(b, e, Maze.Direction.opposite[d]);
            this.callback(this, b, e)
        } else {
            this.carve(this.x, this.y, this.IN)
        }
        this.callback(this, this.x, this.y);
        this.x++;
        if (this.x >= this.width) {
            this.x = 0;
            this.y++
        }
        return this.y < this.height
    };
    return a
})();
var __hasProp = Object.prototype.hasOwnProperty,
__extends = function(d, b) {
    for (var a in b) {
        if (__hasProp.call(b, a)) {
            d[a] = b[a]
        }
    }
    function c() {
        this.constructor = d
    }
    c.prototype = b.prototype;
    d.prototype = new c;
    d.__super__ = b.prototype;
    return d
};
Maze.Algorithms.RecursiveDivision = (function() {
    __extends(a, Maze);
    a.prototype.HORIZONTAL = 1;
    a.prototype.VERTICAL = 2;
    function a(d, b, c) {
        a.__super__.constructor.apply(this, arguments);
        this.stack = [{
            x: 0,
            y: 0,
            width: this.width,
            height: this.height
        }]
    }
    a.prototype.chooseOrientation = function(c, b) {
        if (c < b) {
            return this.HORIZONTAL
        } else {
            if (b < c) {
                return this.VERTICAL
            } else {
                if (this.rand.nextBoolean()) {
                    return this.HORIZONTAL
                } else {
                    return this.VERTICAL
                }
            }
        }
    };
    a.prototype.step = function() {
        var e,
        r,
        q,
        p,
        b,
        d,
        j,
        i,
        f,
        o,
        n,
        l,
        c,
        h,
        g,
        m,
        k;
        if (this.stack.length > 0) {
            l = this.stack.pop();
            b = this.chooseOrientation(l.width, l.height) === this.HORIZONTAL;
            h = l.x + (b ? 0: this.rand.nextInteger(l.width - 2));
            g = l.y + (b ? this.rand.nextInteger(l.height - 2) : 0);
            o = h + (b ? this.rand.nextInteger(l.width) : 0);
            n = g + (b ? 0: this.rand.nextInteger(l.height));
            r = b ? 1: 0;
            q = b ? 0: 1;
            d = b ? l.width: l.height;
            e = b ? Maze.Direction.S: Maze.Direction.E;
            f = Maze.Direction.opposite[e];
            while (d > 0) {
                if (h !== o || g !== n) {
                    this.carve(h, g, e);
                    this.callback(this, h, g);
                    j = h + Maze.Direction.dx[e];
                    i = g + Maze.Direction.dy[e];
                    this.carve(j, i, f);
                    this.callback(this, j, i)
                }
                h += r;
                g += q;
                d -= 1
            }
            c = b ? l.width: h - l.x + 1;
            p = b ? g - l.y + 1: l.height;
            if (c >= 2 && p >= 2) {
                this.stack.push({
                    x: l.x,
                    y: l.y,
                    width: c,
                    height: p
                })
            }
            m = b ? l.x: h + 1;
            k = b ? g + 1: l.y;
            c = b ? l.width: l.x + l.width - h - 1;
            p = b ? l.y + l.height - g - 1: l.height;
            if (c >= 2 && p >= 2) {
                this.stack.push({
                    x: m,
                    y: k,
                    width: c,
                    height: p
                })
            }
        }
        return this.stack.length > 0
    };
    return a
})();
var __hasProp = Object.prototype.hasOwnProperty,
__extends = function(d, b) {
    for (var a in b) {
        if (__hasProp.call(b, a)) {
            d[a] = b[a]
        }
    }
    function c() {
        this.constructor = d
    }
    c.prototype = b.prototype;
    d.prototype = new c;
    d.__super__ = b.prototype;
    return d
},
__bind = function(a, b) {
    return function() {
        return a.apply(b, arguments)
    }
};
Maze.Algorithms.Eller = (function() {
    __extends(a, Maze);
    a.prototype.IN = 32;
    a.prototype.HORIZONTAL = 0;
    a.prototype.VERTICAL = 1;
    function a(d, b, c) {
        a.__super__.constructor.apply(this, arguments);
        this.state = new Maze.Algorithms.Eller.State(this.width).populate();
        this.row = 0;
        this.pending = true;
        this.initializeRow()
    }
    a.prototype.initializeRow = function() {
        this.column = 0;
        return this.mode = this.HORIZONTAL
    };
    a.prototype.isFinal = function() {
        return this.row + 1 === this.height
    };
    a.prototype.isIn = function(b, c) {
        return this.isValid(b, c) && this.isSet(b, c, this.IN)
    };
    a.prototype.horizontalStep = function() {
        var b;
        b = false;
        while (! (b || this.column + 1 >= this.width)) {
            b = true;
            if (!this.state.isSame(this.column, this.column + 1) && (this.isFinal() || this.rand.nextBoolean())) {
                this.state.merge(this.column, this.column + 1);
                this.carve(this.column, this.row, Maze.Direction.E);
                this.callback(this, this.column, this.row);
                this.carve(this.column + 1, this.row, Maze.Direction.W);
                this.callback(this, this.column + 1, this.row)
            } else {
                if (this.isBlank(this.column, this.row)) {
                    this.carve(this.column, this.row, this.IN);
                    this.callback(this, this.column, this.row)
                } else {
                    b = false
                }
            }
            this.column += 1
        }
        if (this.column + 1 >= this.width) {
            if (this.isBlank(this.column, this.row)) {
                this.carve(this.column, this.row, this.IN);
                this.callback(this, this.column, this.row)
            }
            if (this.isFinal()) {
                return this.pending = false
            } else {
                this.mode = this.VERTICAL;
                this.next_state = this.state.next();
                return this.verticals = this.computeVerticals()
            }
        }
    };
    a.prototype.computeVerticals = function() {
        var b;
        b = [];
        this.state.foreach(__bind(function(f, e) {
            var c,
            d;
            d = 1 + this.rand.nextInteger(e.length - 1);
            c = this.randomizeList(e).slice(0, d);
            return b = b.concat(c)
        },
        this));
        return b.sort(function(d, c) {
            return d - c
        })
    };
    a.prototype.verticalStep = function() {
        var b;
        b = this.verticals.pop();
        this.next_state.add(b, this.state.setFor(b));
        this.carve(b, this.row, Maze.Direction.S);
        this.callback(this, b, this.row);
        this.carve(b, this.row + 1, Maze.Direction.N);
        this.callback(this, b, this.row + 1);
        if (this.verticals.length === 0) {
            this.state = this.next_state.populate();
            this.row += 1;
            return this.initializeRow()
        }
    };
    a.prototype.step = function() {
        switch (this.mode) {
        case this.HORIZONTAL:
            this.horizontalStep();
            break;
        case this.VERTICAL:
            this.verticalStep()
        }
        return this.pending
    };
    return a
})();
Maze.Algorithms.Eller.State = (function() {
    function a(c, b) {
        var d;
        this.width = c;
        this.counter = b; (d = this.counter) != null ? d: this.counter = 0;
        this.sets = {};
        this.cells = []
    }
    a.prototype.next = function() {
        return new Maze.Algorithms.Eller.State(this.width, this.counter)
    };
    a.prototype.populate = function() {
        var b,
        e,
        c,
        d;
        b = 0;
        while (b < this.width) {
            if (!this.cells[b]) {
                e = (this.counter += 1); ((d = (c = this.sets)[e]) != null ? d: c[e] = []).push(b);
                this.cells[b] = e
            }
            b += 1
        }
        return this
    };
    a.prototype.merge = function(h, i) {
        var b,
        g,
        d,
        f,
        c,
        e;
        g = this.cells[h];
        d = this.cells[i];
        this.sets[g] = this.sets[g].concat(this.sets[d]);
        e = this.sets[d];
        for (f = 0, c = e.length; f < c; f++) {
            b = e[f];
            this.cells[b] = g
        }
        return delete this.sets[d]
    };
    a.prototype.isSame = function(d, c) {
        return this.cells[d] === this.cells[c]
    };
    a.prototype.add = function(b, e) {
        var c,
        d;
        this.cells[b] = e; ((d = (c = this.sets)[e]) != null ? d: c[e] = []).push(b);
        return this
    };
    a.prototype.setFor = function(b) {
        return this.cells[b]
    };
    a.prototype.foreach = function(c) {
        var f,
        e,
        d,
        b;
        d = this.sets;
        b = [];
        for (f in d) {
            e = d[f];
            b.push(c(f, e))
        }
        return b
    };
    return a
})();
var __hasProp = Object.prototype.hasOwnProperty,
__extends = function(d, b) {
    for (var a in b) {
        if (__hasProp.call(b, a)) {
            d[a] = b[a]
        }
    }
    function c() {
        this.constructor = d
    }
    c.prototype = b.prototype;
    d.prototype = new c;
    d.__super__ = b.prototype;
    return d
};
Maze.Algorithms.GrowingTree = (function() {
    __extends(a, Maze);
    a.prototype.QUEUE = 16;
    function a(e, b, c) {
        var d,
        g,
        f,
        h;
        a.__super__.constructor.apply(this, arguments);
        this.cells = [];
        this.state = 0;
        this.weights = (f = c.input) != null ? f: {
            random: 50
        };
        this.totalWeights = 0;
        h = this.weights;
        for (d in h) {
            g = h[d];
            this.totalWeights += g
        }
    }
    a.prototype.inQueue = function(b, c) {
        return this.isSet(b, c, this.QUEUE)
    };
    a.prototype.enqueue = function(b, c) {
        this.carve(b, c, this.QUEUE);
        this.cells.push({
            x: b,
            y: c
        });
        return this.callback(this, b, c)
    };
    a.prototype.nextCell = function() {
        var c,
        b,
        f,
        e,
        d;
        f = this.rand.nextInteger(this.totalWeights);
        c = 0;
        d = this.weights;
        for (b in d) {
            e = d[b];
            c += e;
            if (c > f) {
                switch (b) {
                case "random":
                    return this.rand.nextInteger(this.cells.length);
                case "newest":
                    return this.cells.length - 1;
                case "oldest":
                    return 0;
                case "middle":
                    return Math.floor(this.cells.length / 2);
                default:
                    throw "invalid weight key `" + b + "'"
                }
            }
        }
        throw "[bug] shouldn't get here"
    };
    a.prototype.startStep = function() {
        this.enqueue(this.rand.nextInteger(this.width), this.rand.nextInteger(this.height));
        return this.state = 1
    };
    a.prototype.runStep = function() {
        var c,
        h,
        e,
        b,
        i,
        g,
        d,
        f;
        e = this.nextCell();
        c = this.cells[e];
        f = this.randomDirections();
        for (g = 0, d = f.length; g < d; g++) {
            h = f[g];
            b = c.x + Maze.Direction.dx[h];
            i = c.y + Maze.Direction.dy[h];
            if (this.isValid(b, i) && this.isBlank(b, i)) {
                this.carve(c.x, c.y, h);
                this.carve(b, i, Maze.Direction.opposite[h]);
                this.enqueue(b, i);
                this.callback(this, c.x, c.y);
                this.callback(this, b, i);
                return
            }
        }
        this.cells.splice(e, 1);
        this.uncarve(c.x, c.y, this.QUEUE);
        return this.callback(this, c.x, c.y)
    };
    a.prototype.step = function() {
        switch (this.state) {
        case 0:
            this.startStep();
            break;
        case 1:
            this.runStep()
        }
        return this.cells.length > 0
    };
    return a
})();
var __hasProp = Object.prototype.hasOwnProperty,
__extends = function(d, b) {
    for (var a in b) {
        if (__hasProp.call(b, a)) {
            d[a] = b[a]
        }
    }
    function c() {
        this.constructor = d
    }
    c.prototype = b.prototype;
    d.prototype = new c;
    d.__super__ = b.prototype;
    return d
};
Maze.Algorithms.HuntAndKill = (function() {
    __extends(a, Maze);
    a.prototype.IN = 16;
    function a(d, b, c) {
        a.__super__.constructor.apply(this, arguments);
        this.state = 0
    }
    a.prototype.isCurrent = function(b, c) {
        return this.x === b && this.y === c
    };
    a.prototype.isWalking = function() {
        return this.state === 1
    };
    a.prototype.isHunting = function() {
        return this.state === 2
    };
    a.prototype.startStep = function() {
        this.x = this.rand.nextInteger(this.width);
        this.y = this.rand.nextInteger(this.height);
        this.carve(this.x, this.y, this.IN);
        this.callback(this, this.x, this.y);
        return this.state = 1
    };
    a.prototype.walkStep = function() {
        var i,
        g,
        f,
        k,
        h,
        d,
        j,
        e,
        c,
        b;
        e = this.randomDirections();
        for (d = 0, j = e.length; d < j; d++) {
            i = e[d];
            g = this.x + Maze.Direction.dx[i];
            f = this.y + Maze.Direction.dy[i];
            if (this.isValid(g, f) && this.isBlank(g, f)) {
                c = [this.x, this.y, g, f],
                k = c[0],
                h = c[1],
                this.x = c[2],
                this.y = c[3];
                this.carve(k, h, i);
                this.carve(g, f, Maze.Direction.opposite[i]);
                this.callback(this, k, h);
                this.callback(this, g, f);
                return
            }
        }
        b = [this.x, this.y],
        k = b[0],
        h = b[1];
        delete this.x;
        delete this.y;
        this.callback(this, k, h);
        this.x = 0;
        this.y = 0;
        this.callback(this, 0, 0);
        return this.state = 2
    };
    a.prototype.huntStep = function() {
        var f,
        d,
        c,
        h,
        b,
        g,
        e;
        if (this.isBlank(this.x, this.y)) {
            d = [];
            if (this.y > 0 && !this.isBlank(this.x, this.y - 1)) {
                d.push(Maze.Direction.N)
            }
            if (this.x > 0 && !this.isBlank(this.x - 1, this.y)) {
                d.push(Maze.Direction.W)
            }
            if (this.y + 1 < this.height && !this.isBlank(this.x, this.y + 1)) {
                d.push(Maze.Direction.S)
            }
            if (this.x + 1 < this.width && !this.isBlank(this.x + 1, this.y)) {
                d.push(Maze.Direction.E)
            }
            f = this.randomElement(d);
            if (f) {
                c = this.x + Maze.Direction.dx[f];
                h = this.y + Maze.Direction.dy[f];
                this.carve(this.x, this.y, f);
                this.carve(c, h, Maze.Direction.opposite[f]);
                this.state = 1;
                this.callback(this, c, h);
                this.callback(this, this.x, this.y);
                return
            }
        }
        e = [this.x, this.y, this.x + 1, this.y],
        b = e[0],
        g = e[1],
        this.x = e[2],
        this.y = e[3];
        if (this.x >= this.width) {
            this.x = 0;
            this.y++
        }
        if (this.y >= this.height) {
            this.state = 3;
            delete this.x;
            delete this.y
        } else {
            this.callback(this, this.x, this.y)
        }
        return this.callback(this, b, g)
    };
    a.prototype.step = function() {
        switch (this.state) {
        case 0:
            this.startStep();
            break;
        case 1:
            this.walkStep();
            break;
        case 2:
            this.huntStep()
        }
        return this.state !== 3
    };
    return a
})();
var __hasProp = Object.prototype.hasOwnProperty,
__extends = function(d, b) {
    for (var a in b) {
        if (__hasProp.call(b, a)) {
            d[a] = b[a]
        }
    }
    function c() {
        this.constructor = d
    }
    c.prototype = b.prototype;
    d.prototype = new c;
    d.__super__ = b.prototype;
    return d
};
Maze.Algorithms.Kruskal = (function() {
    __extends(a, Maze);
    function a(e, c, d) {
        var b,
        h,
        f,
        g;
        a.__super__.constructor.apply(this, arguments);
        this.sets = [];
        this.edges = [];
        for (h = 0, f = this.height; (0 <= f ? h < f: h > f); (0 <= f ? h += 1: h -= 1)) {
            this.sets.push([]);
            for (b = 0, g = this.width; (0 <= g ? b < g: b > g); (0 <= g ? b += 1: b -= 1)) {
                this.sets[h].push(new Maze.Algorithms.Kruskal.Tree());
                if (h > 0) {
                    this.edges.push({
                        x: b,
                        y: h,
                        direction: Maze.Direction.N
                    })
                }
                if (b > 0) {
                    this.edges.push({
                        x: b,
                        y: h,
                        direction: Maze.Direction.W
                    })
                }
            }
        }
        this.randomizeList(this.edges)
    }
    a.prototype.step = function() {
        var e,
        b,
        f,
        d,
        c;
        while (this.edges.length > 0) {
            e = this.edges.pop();
            b = e.x + Maze.Direction.dx[e.direction];
            f = e.y + Maze.Direction.dy[e.direction];
            d = this.sets[e.y][e.x];
            c = this.sets[f][b];
            if (!d.isConnectedTo(c)) {
                d.connect(c);
                this.carve(e.x, e.y, e.direction);
                this.callback(this, e.x, e.y);
                this.carve(b, f, Maze.Direction.opposite[e.direction]);
                this.callback(this, b, f);
                break
            }
        }
        return this.edges.length > 0
    };
    return a
})();
Maze.Algorithms.Kruskal.Tree = (function() {
    function a() {
        this.up = null
    }
    a.prototype.root = function() {
        if (this.up) {
            return this.up.root()
        } else {
            return this
        }
    };
    a.prototype.isConnectedTo = function(b) {
        return this.root() === b.root()
    };
    a.prototype.connect = function(b) {
        return b.root().up = this
    };
    return a
})();
var __hasProp = Object.prototype.hasOwnProperty,
__extends = function(d, b) {
    for (var a in b) {
        if (__hasProp.call(b, a)) {
            d[a] = b[a]
        }
    }
    function c() {
        this.constructor = d
    }
    c.prototype = b.prototype;
    d.prototype = new c;
    d.__super__ = b.prototype;
    return d
};
Maze.Algorithms.Prim = (function() {
    __extends(a, Maze);
    a.prototype.IN = 16;
    a.prototype.FRONTIER = 32;
    a.prototype.START = 1;
    a.prototype.EXPAND = 2;
    a.prototype.DONE = 3;
    function a(d, b, c) {
        a.__super__.constructor.apply(this, arguments);
        this.frontierCells = [];
        this.state = this.START
    }
    a.prototype.isOutside = function(b, c) {
        return this.isValid(b, c) && this.isBlank(b, c)
    };
    a.prototype.isInside = function(b, c) {
        return this.isValid(b, c) && this.isSet(b, c, this.IN)
    };
    a.prototype.isFrontier = function(b, c) {
        return this.isValid(b, c) && this.isSet(b, c, this.FRONTIER)
    };
    a.prototype.addFrontier = function(b, c) {
        if (this.isOutside(b, c)) {
            this.frontierCells.push({
                x: b,
                y: c
            });
            this.carve(b, c, this.FRONTIER);
            return this.callback(this, b, c)
        }
    };
    a.prototype.markCell = function(b, c) {
        this.carve(b, c, this.IN);
        this.uncarve(b, c, this.FRONTIER);
        this.callback(this, b, c);
        this.addFrontier(b - 1, c);
        this.addFrontier(b + 1, c);
        this.addFrontier(b, c - 1);
        return this.addFrontier(b, c + 1)
    };
    a.prototype.findNeighborsOf = function(b, d) {
        var c;
        c = [];
        if (this.isInside(b - 1, d)) {
            c.push(Maze.Direction.W)
        }
        if (this.isInside(b + 1, d)) {
            c.push(Maze.Direction.E)
        }
        if (this.isInside(b, d - 1)) {
            c.push(Maze.Direction.N)
        }
        if (this.isInside(b, d + 1)) {
            c.push(Maze.Direction.S)
        }
        return c
    };
    a.prototype.startStep = function() {
        this.markCell(this.rand.nextInteger(this.width), this.rand.nextInteger(this.height));
        return this.state = this.EXPAND
    };
    a.prototype.expandStep = function() {
        var c,
        d,
        b,
        e;
        c = this.removeRandomElement(this.frontierCells);
        d = this.randomElement(this.findNeighborsOf(c.x, c.y));
        b = c.x + Maze.Direction.dx[d];
        e = c.y + Maze.Direction.dy[d];
        this.carve(b, e, Maze.Direction.opposite[d]);
        this.callback(this, b, e);
        this.carve(c.x, c.y, d);
        this.markCell(c.x, c.y);
        if (this.frontierCells.length === 0) {
            return this.state = this.DONE
        }
    };
    a.prototype.step = function() {
        switch (this.state) {
        case this.START:
            this.startStep();
            break;
        case this.EXPAND:
            this.expandStep()
        }
        return this.state !== this.DONE
    };
    return a
})();
var __hasProp = Object.prototype.hasOwnProperty,
__extends = function(d, b) {
    for (var a in b) {
        if (__hasProp.call(b, a)) {
            d[a] = b[a]
        }
    }
    function c() {
        this.constructor = d
    }
    c.prototype = b.prototype;
    d.prototype = new c;
    d.__super__ = b.prototype;
    return d
};
Maze.Algorithms.Sidewinder = (function() {
    __extends(a, Maze);
    a.prototype.IN = 16;
    function a(d, b, c) {
        a.__super__.constructor.apply(this, arguments);
        this.x = 0;
        this.y = 0;
        this.runStart = 0;
        this.state = 0
    }
    a.prototype.startStep = function() {
        this.carve(this.x, this.y, this.IN);
        this.callback(this, this.x, this.y);
        return this.state = 1
    };
    a.prototype.runStep = function() {
        var b;
        if (this.y > 0 && (this.x + 1 >= this.width || this.randomBoolean())) {
            b = this.runStart + this.rand.nextInteger(this.x - this.runStart + 1);
            this.carve(b, this.y, Maze.Direction.N);
            this.carve(b, this.y - 1, Maze.Direction.S);
            this.callback(this, b, this.y);
            this.callback(this, b, this.y - 1);
            this.runStart = this.x + 1
        } else {
            if (this.x + 1 < this.width) {
                this.carve(this.x, this.y, Maze.Direction.E);
                this.carve(this.x + 1, this.y, Maze.Direction.W);
                this.callback(this, this.x, this.y);
                this.callback(this, this.x + 1, this.y)
            } else {
                this.carve(this.x, this.y, this.IN);
                this.callback(this, this.x, this.y)
            }
        }
        this.x++;
        if (this.x >= this.width) {
            this.x = 0;
            this.runStart = 0;
            return this.y++
        }
    };
    a.prototype.step = function() {
        if (this.y >= this.height) {
            return false
        }
        switch (this.state) {
        case 0:
            this.startStep();
            break;
        case 1:
            this.runStep()
        }
        return this.y < this.height
    };
    return a
})();
var __hasProp = Object.prototype.hasOwnProperty,
__extends = function(d, b) {
    for (var a in b) {
        if (__hasProp.call(b, a)) {
            d[a] = b[a]
        }
    }
    function c() {
        this.constructor = d
    }
    c.prototype = b.prototype;
    d.prototype = new c;
    d.__super__ = b.prototype;
    return d
};
Maze.Algorithms.Wilson = (function() {
    __extends(a, Maze);
    a.prototype.IN = 16;
    function a(d, b, c) {
        a.__super__.constructor.apply(this, arguments);
        this.state = 0;
        this.remaining = this.width * this.height;
        this.visits = {}
    }
    a.prototype.isCurrent = function(b, c) {
        return this.x === b && this.y === c
    };
    a.prototype.isVisited = function(b, c) {
        return this.visits["" + b + ":" + c] != null
    };
    a.prototype.addVisit = function(b, d, c) {
        return this.visits["" + b + ":" + d] = c != null ? c: 0
    };
    a.prototype.exitTaken = function(b, c) {
        return this.visits["" + b + ":" + c]
    };
    a.prototype.startStep = function() {
        var b,
        c;
        b = this.rand.nextInteger(this.width);
        c = this.rand.nextInteger(this.height);
        this.carve(b, c, this.IN);
        this.callback(this, b, c);
        this.remaining--;
        return this.state = 1
    };
    a.prototype.startWalkStep = function() {
        var b;
        this.visits = {};
        b = [];
        while (true) {
            this.x = this.rand.nextInteger(this.width);
            this.y = this.rand.nextInteger(this.height);
            if (this.isBlank(this.x, this.y)) {
                this.state = 2;
                this.start = {
                    x: this.x,
                    y: this.y
                };
                this.addVisit(this.x, this.y);
                this.callback(this, this.x, this.y);
                break
            }
        }
        return b
    };
    a.prototype.walkStep = function() {
        var i,
        g,
        f,
        k,
        h,
        d,
        j,
        e,
        b,
        c;
        e = this.randomDirections();
        c = [];
        for (d = 0, j = e.length; d < j; d++) {
            i = e[d];
            g = this.x + Maze.Direction.dx[i];
            f = this.y + Maze.Direction.dy[i];
            if (this.isValid(g, f)) {
                b = [this.x, this.y, g, f],
                k = b[0],
                h = b[1],
                this.x = b[2],
                this.y = b[3];
                this.addVisit(k, h, i);
                this.callback(this, k, h);
                this.callback(this, g, f);
                if (!this.isBlank(g, f)) {
                    this.x = this.start.x;
                    this.y = this.start.y;
                    this.state = 3
                }
                break
            }
        }
        return c
    };
    a.prototype.resetVisits = function() {
        var d,
        e,
        b,
        h,
        f,
        g,
        c;
        f = this.visits;
        c = [];
        for (e in f) {
            d = f[e];
            g = e.split(":"),
            b = g[0],
            h = g[1];
            delete this.visits[e];
            c.push(this.callback(this, b, h))
        }
        return c
    };
    a.prototype.runStep = function() {
        var d,
        c,
        g,
        b,
        f,
        e;
        if (this.remaining > 0) {
            d = this.exitTaken(this.x, this.y);
            c = this.x + Maze.Direction.dx[d];
            g = this.y + Maze.Direction.dy[d];
            if (!this.isBlank(c, g)) {
                this.resetVisits();
                this.state = 1
            }
            this.carve(this.x, this.y, d);
            this.carve(c, g, Maze.Direction.opposite[d]);
            e = [this.x, this.y, c, g],
            b = e[0],
            f = e[1],
            this.x = e[2],
            this.y = e[3];
            if (this.state === 1) {
                delete this.x;
                delete this.y
            }
            this.callback(this, b, f);
            this.callback(this, c, g);
            this.remaining--
        }
        return this.remaining > 0
    };
    a.prototype.step = function() {
        if (this.remaining > 0) {
            switch (this.state) {
            case 0:
                this.startStep();
                break;
            case 1:
                this.startWalkStep();
                break;
            case 2:
                this.walkStep();
                break;
            case 3:
                this.runStep()
            }
        }
        return this.remaining > 0
    };
    return a
})();