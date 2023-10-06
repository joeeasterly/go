'use strict';

function QRCode(r) {
    var n, t, o, e, a = [],
        f = [],
        i = Math.max,
        u = Math.min,
        h = Math.abs,
        v = Math.ceil,
        c = /^[0-9]*$/,
        s = /^[A-Z0-9 $%*+.\/:-]*$/,
        l = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:",
        g = [
            [-1, 7, 10, 15, 20, 26, 18, 20, 24, 30, 18, 20, 24, 26, 30, 22, 24, 28, 30, 28, 28, 28, 28, 30, 30, 26, 28, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30],
            [-1, 10, 16, 26, 18, 24, 16, 18, 22, 22, 26, 30, 22, 22, 24, 24, 28, 28, 26, 26, 26, 26, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28],
            [-1, 13, 22, 18, 26, 18, 24, 18, 22, 20, 24, 28, 26, 24, 20, 30, 24, 28, 28, 26, 30, 28, 30, 30, 30, 30, 28, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30],
            [-1, 17, 28, 22, 16, 22, 28, 26, 26, 24, 28, 24, 28, 22, 24, 24, 30, 28, 28, 26, 28, 30, 24, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]
        ],
        d = [
            [-1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 4, 4, 4, 4, 4, 6, 6, 6, 6, 7, 8, 8, 9, 9, 10, 12, 12, 12, 13, 14, 15, 16, 17, 18, 19, 19, 20, 21, 22, 24, 25],
            [-1, 1, 1, 1, 2, 2, 4, 4, 4, 5, 5, 5, 8, 9, 9, 10, 10, 11, 13, 14, 16, 17, 17, 18, 20, 21, 23, 25, 26, 28, 29, 31, 33, 35, 37, 38, 40, 43, 45, 47, 49],
            [-1, 1, 1, 2, 2, 4, 4, 6, 6, 8, 8, 8, 10, 12, 16, 12, 17, 16, 18, 21, 20, 23, 23, 25, 27, 29, 34, 34, 35, 38, 40, 43, 45, 48, 51, 53, 56, 59, 62, 65, 68],
            [-1, 1, 1, 2, 4, 4, 4, 5, 6, 8, 8, 11, 11, 16, 16, 18, 16, 19, 21, 25, 25, 25, 34, 30, 32, 35, 37, 40, 42, 45, 48, 51, 54, 57, 60, 63, 66, 70, 74, 77, 81]
        ],
        m = {
            L: [0, 1],
            M: [1, 0],
            Q: [2, 3],
            H: [3, 2]
        },
        p = function(r, n) {
            for (var t = 0, o = 8; o--;) t = t << 1 ^ 285 * (t >>> 7) ^ (n >>> o & 1) * r;
            return t
        },
        C = function(r, n) {
            for (var t = [], o = r.length, e = o; e;)
                for (var a = r[o - e--] ^ t.shift(), f = n.length; f--;) t[f] ^= p(n[f], a);
            return t
        },
        w = function(r) {
            for (var n = [function() {
                    return 0 == (t + o) % 2
                }, function() {
                    return 0 == t % 2
                }, function() {
                    return 0 == o % 3
                }, function() {
                    return 0 == (t + o) % 3
                }, function() {
                    return 0 == ((t / 2 | 0) + (o / 3 | 0)) % 2
                }, function() {
                    return 0 == t * o % 2 + t * o % 3
                }, function() {
                    return 0 == (t * o % 2 + t * o % 3) % 2
                }, function() {
                    return 0 == ((t + o) % 2 + t * o % 3) % 2
                }][r], t = e; t--;)
                for (var o = e; o--;) f[t][o] || (a[t][o] ^= n())
        },
        b = function() {
            for (var r = function(r, n) {
                    n[6] || (r += e), n.shift(), n.push(r)
                }, n = function(n, o, a) {
                    return n && (r(o, a), o = 0), r(o += e, a), t(a)
                }, t = function(r) {
                    var n = r[5],
                        t = n > 0 && r[4] == n && r[3] == 3 * n && r[2] == n && r[1] == n;
                    return (t && r[6] >= 4 * n && r[0] >= n ? 1 : 0) + (t && r[0] >= 4 * n && r[6] >= n ? 1 : 0)
                }, o = 0, f = e * e, i = 0, u = e; u--;) {
                for (var c = [0, 0, 0, 0, 0, 0, 0], s = [0, 0, 0, 0, 0, 0, 0], l = !1, g = !1, d = 0, m = 0, p = e; p--;) {
                    a[u][p] == l ? 5 == ++d ? o += 3 : d > 5 && o++ : (r(d, c), o += 40 * t(c), d = 1, l = a[u][p]), a[p][u] == g ? 5 == ++m ? o += 3 : m > 5 && o++ : (r(m, s), o += 40 * t(s), m = 1, g = a[p][u]);
                    var C = a[u][p];
                    C && i++, p && u && C == a[u][p - 1] && C == a[u - 1][p] && C == a[u - 1][p - 1] && (o += 3)
                }
                o += 40 * n(l, d, c) + 40 * n(g, m, s)
            }
            return o += 10 * (v(h(20 * i - 10 * f) / f) - 1)
        },
        A = function(r, n, t) {
            for (; n--;) t.push(r >>> n & 1)
        },
        M = function(r, n) {
            return r.numBitsCharCount[(n + 7) / 17 | 0]
        },
        B = function(r, n) {
            return 0 != (r >>> n & 1)
        },
        x = function(r, n) {
            for (var t = 0, o = r.length; o--;) {
                var e = r[o],
                    a = M(e, n);
                if (1 << a <= e.numChars) return 1 / 0;
                t += 4 + a + e.bitData.length
            }
            return t
        },
        D = function(r) {
            if (r < 1 || r > 40) throw "Version number out of range";
            var n = (16 * r + 128) * r + 64;
            if (r >= 2) {
                var t = r / 7 | 2;
                n -= (25 * t - 10) * t - 55, r >= 7 && (n -= 36)
            }
            return n
        },
        I = function(r, n) {
            for (var t = 2; - 2 <= t; t--)
                for (var o = 2; - 2 <= o; o--) E(r + o, n + t, 1 != i(h(o), h(t)))
        },
        H = function(r, n) {
            for (var t = 4; - 4 <= t; t--)
                for (var o = 4; - 4 <= o; o--) {
                    var a = i(h(o), h(t)),
                        f = r + o,
                        u = n + t;
                    0 <= f && f < e && 0 <= u && u < e && E(f, u, 2 != a && 4 != a)
                }
        },
        $ = function(r) {
            for (var n = t[1] << 3 | r, o = n, a = 10; a--;) o = o << 1 ^ 1335 * (o >>> 9);
            var f = 21522 ^ (n << 10 | o);
            if (f >>> 15 != 0) throw "Assertion error";
            for (a = 0; a <= 5; a++) E(8, a, B(f, a));
            E(8, 7, B(f, 6)), E(8, 8, B(f, 7)), E(7, 8, B(f, 8));
            for (a = 9; a < 15; a++) E(14 - a, 8, B(f, a));
            for (a = 0; a < 8; a++) E(e - 1 - a, 8, B(f, a));
            for (a = 8; a < 15; a++) E(8, e - 15 + a, B(f, a));
            E(8, e - 8, 1)
        },
        O = function() {
            for (var r = e; r--;) E(6, r, 0 == r % 2), E(r, 6, 0 == r % 2);
            for (var t = function() {
                    var r = [];
                    if (n > 1)
                        for (var t = 2 + (n / 7 | 0), o = 32 == n ? 26 : 2 * v((e - 13) / (2 * t - 2)); t--;) r[t] = t * o + 6;
                    return r
                }(), o = r = t.length; o--;)
                for (var a = r; a--;) 0 == a && 0 == o || 0 == a && o == r - 1 || a == r - 1 && 0 == o || I(t[a], t[o]);
            H(3, 3), H(e - 4, 3), H(3, e - 4), $(0),
                function() {
                    if (!(7 > n)) {
                        for (var r = n, t = 12; t--;) r = r << 1 ^ 7973 * (r >>> 11);
                        var o = n << 12 | r;
                        if (t = 18, o >>> 18 != 0) throw "Assertion error";
                        for (; t--;) {
                            var a = e - 11 + t % 3,
                                f = t / 3 | 0,
                                i = B(o, t);
                            E(a, f, i), E(f, a, i)
                        }
                    }
                }()
        },
        Q = function(r) {
            if (r.length != V(n, t)) throw "Invalid argument";
            for (var o = d[t[0]][n], e = g[t[0]][n], a = D(n) / 8 | 0, f = o - a % o, i = a / o | 0, u = [], h = function(r) {
                    var n = 1,
                        t = [];
                    t[r - 1] = 1;
                    for (var o = 0; o < r; o++) {
                        for (var e = 0; e < r; e++) t[e] = p(t[e], n) ^ t[e + 1];
                        n = p(n, 2)
                    }
                    return t
                }(e), v = 0, c = 0; v < o; v++) {
                var s = r.slice(c, c + i - e + (v < f ? 0 : 1));
                c += s.length;
                var l = C(s, h);
                v < f && s.push(0), u.push(s.concat(l))
            }
            var m = [];
            for (v = 0; v < u[0].length; v++)
                for (var w = 0; w < u.length; w++)(v != i - e || w >= f) && m.push(u[w][v]);
            return m
        },
        S = function(r) {
            for (var n = [], t = (r = encodeURI(r), 0); t < r.length; t++) "%" != r.charAt(t) ? n.push(r.charCodeAt(t)) : (n.push(parseInt(r.substr(t + 1, 2), 16)), t += 2);
            return n
        },
        V = function(r, n) {
            return (D(r) / 8 | 0) - g[n[0]][r] * d[n[0]][r]
        },
        E = function(r, n, t) {
            a[n][r] = t ? 1 : 0, f[n][r] = 1
        },
        R = function(r) {
            for (var n = [], t = 0, o = r; t < o.length; t++) {
                var e = o[t];
                A(e, 8, n)
            }
            return {
                modeBits: 4,
                numBitsCharCount: [8, 16, 16],
                numChars: r.length,
                bitData: n
            }
        },
        Z = function(r) {
            if (!c.test(r)) throw "String contains non-numeric characters";
            for (var n = [], t = 0; t < r.length;) {
                var o = u(r.length - t, 3);
                A(parseInt(r.substr(t, o), 10), 3 * o + 1, n), t += o
            }
            return {
                modeBits: 1,
                numBitsCharCount: [10, 12, 14],
                numChars: r.length,
                bitData: n
            }
        },
        z = function(r) {
            if (!s.test(r)) throw "String contains unencodable characters in alphanumeric mode";
            var n, t = [];
            for (n = 0; n + 2 <= r.length; n += 2) {
                var o = 45 * l.indexOf(r.charAt(n));
                o += l.indexOf(r.charAt(n + 1)), A(o, 11, t)
            }
            return n < r.length && A(l.indexOf(r.charAt(n)), 6, t), {
                modeBits: 2,
                numBitsCharCount: [9, 11, 13],
                numChars: r.length,
                bitData: t
            }
        },
        L = function(r, n, t, o) {
            var e = function(r) {
                return "" == r ? [] : c.test(r) ? [Z(r)] : s.test(r) ? [z(r)] : [R(S(r))]
            }(r);
            return U(e, n, t, o)
        },
        N = function(r, i, u, h) {
            t = i, o = h;
            for (var v = e = 4 * (n = r) + 17; v--;) a[v] = [], f[v] = [];
            if (O(), function(r) {
                    for (var n = 0, t = 1, o = e - 1, i = o; i > 0; i -= 2) {
                        6 == i && --i;
                        for (var u = 0 > (t = -t) ? o : 0, h = 0; h < e; ++h) {
                            for (var v = i; v > i - 2; --v) f[u][v] || (a[u][v] = B(r[n >>> 3], 7 - (7 & n)), ++n);
                            u += t
                        }
                    }
                }(Q(u)), 0 > o) {
                var c = 1e9;
                for (v = 8; v--;) {
                    w(v), $(v);
                    var s = b();
                    c > s && (c = s, o = v), w(v)
                }
            }
            w(o), $(o), f = []
        },
        U = function(r, n, t, o, e, a) {
            if (void 0 === e && (e = 1), void 0 === a && (a = 40), void 0 === o && (o = -1), void 0 === t && (t = !0), !(1 <= e && e <= a && a <= 40) || o < -1 || o > 7) throw "Invalid value";
            for (var f = [], i = 236, h = [], v = e;;) {
                var c = x(r, v);
                if (c <= 8 * V(v, n)) break;
                if (v >= a) throw "Data too long";
                v++
            }
            if (t)
                for (var s = (l = [m.H, m.Q, m.M]).length; s--;) c <= 8 * V(v, l[s]) && (n = l[s]);
            for (var l = 0; l < r.length; l++) {
                var g = r[l];
                A(g.modeBits, 4, f), A(g.numChars, M(g, v), f);
                for (var d = 0, p = g.bitData; d < p.length; d++) f.push(p[d])
            }
            if (f.length != c) throw "Assertion error";
            var C = 8 * V(v, n);
            if (f.length > C) throw "Assertion error";
            if (A(0, u(4, C - f.length), f), A(0, (8 - f.length % 8) % 8, f), f.length % 8 != 0) throw "Assertion error";
            for (; f.length < C;) A(i, 8, f), i ^= 253;
            for (s = f.length; s--;) h[s >>> 3] |= f[s] << 7 - (7 & s);
            return N(v, n, h, o)
        };
        
    return function() {
        function n(r) {
            return /^#[0-9a-f]{3}(?:[0-9a-f]{3})?$/i.test(r)
        }

        function t(r, n) {
            for (var t in r = document.createElementNS(s, r), n || {}) r.setAttribute(t, n[t]);
            return r
        }
        var o, f, i, u, v, c, s = "http://www.w3.org/2000/svg",
            l = "",
            g = "string" == typeof r ? {
                msg: r
            } : r || {},
            d = g.pal || ["#000"],
            p = h(g.dim) || 256,
            C = [1, 0, 0, 1, c = (c = h(g.pad)) > -1 ? c : 4, c],
            w = n(w = d[0]) ? w : "#000",
            b = n(b = d[1]) ? b : 0,
            A = g.vrb ? 0 : 1;
        for (L(g.msg || "", m[g.ecl] || m.M, 0 == g.ecb ? 0 : 1, g.mtx), v = e + 2 * c, i = e; i--;)
            for (u = 0, f = e; f--;) a[i][f] && (A ? (u++, a[i][f - 1] || (l += "M" + f + "," + i + "h" + u + "v1h-" + u + "v-1z", u = 0)) : l += "M" + f + "," + i + "h1v1h-1v-1z");
        return o = t("svg", {
            viewBox: [0, 0, v, v].join(" "),
            width: p,
            height: p,
            fill: w,
            "shape-rendering": "crispEdges",
            xmlns: s,
            version: "1.1"
        }), b && o.appendChild(t("path", {
            fill: b,
            d: "M0,0V" + v + "H" + v + "V0H0Z"
        })), o.appendChild(t("path", {
            transform: "matrix(" + C + ")",
            d: l
        })), o
    }()
}