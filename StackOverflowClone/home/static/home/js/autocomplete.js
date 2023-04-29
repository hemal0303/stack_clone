var Autocomplete = function() {
    "use strict";

    function t(t, e) {
        if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
    }

    function e(t, e) {
        for (var n = 0; n < e.length; n++) {
            var s = e[n];
            s.enumerable = s.enumerable || !1, s.configurable = !0, "value" in s && (s.writable = !0), Object.defineProperty(t, s.key, s)
        }
    }

    function n(t, e, n) {
        return e in t ? Object.defineProperty(t, e, {
            value: n,
            enumerable: !0,
            configurable: !0,
            writable: !0
        }) : t[e] = n, t
    }
    var s = function(t, e) {
            return t.matches ? t.matches(e) : t.msMatchesSelector ? t.msMatchesSelector(e) : t.webkitMatchesSelector ? t.webkitMatchesSelector(e) : null
        },
        i = function(t, e) {
            return t.closest ? t.closest(e) : function(t, e) {
                for (var n = t; n && 1 === n.nodeType;) {
                    if (s(n, e)) return n;
                    n = n.parentNode
                }
                return null
            }(t, e)
        },
        o = function(t) {
            return Boolean(t && "function" == typeof t.then)
        },
        u = function e() {
            var s = this,
                u = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {},
                l = u.search,
                r = u.autoSelect,
                a = void 0 !== r && r,
                c = u.setValue,
                d = void 0 === c ? function() {} : c,
                h = u.setAttribute,
                p = void 0 === h ? function() {} : h,
                b = u.onUpdate,
                f = void 0 === b ? function() {} : b,
                v = u.onSubmit,
                L = void 0 === v ? function() {} : v,
                m = u.onShow,
                g = void 0 === m ? function() {} : m,
                y = u.autocorrect,
                w = void 0 !== y && y,
                R = u.onHide,
                S = void 0 === R ? function() {} : R,
                x = u.onLoading,
                A = void 0 === x ? function() {} : x,
                E = u.onLoaded,
                k = void 0 === E ? function() {} : E,
                I = u.submitOnEnter,
                C = void 0 !== I && I;
            t(this, e), n(this, "value", ""), n(this, "searchCounter", 0), n(this, "results", []), n(this, "selectedIndex", -1), n(this, "selectedResult", null), n(this, "destroy", (function() {
                s.search = null, s.setValue = null, s.setAttribute = null, s.onUpdate = null, s.onSubmit = null, s.autocorrect = null, s.onShow = null, s.onHide = null, s.onLoading = null, s.onLoaded = null
            })), n(this, "handleInput", (function(t) {
                var e = t.target.value;
                s.updateResults(e), s.value = e
            })), n(this, "handleKeyDown", (function(t) {
                var e = t.key;
                switch (e) {
                    case "Up":
                    case "Down":
                    case "ArrowUp":
                    case "ArrowDown":
                        var n = "ArrowUp" === e || "Up" === e ? s.selectedIndex - 1 : s.selectedIndex + 1;
                        t.preventDefault(), s.handleArrows(n);
                        break;
                    case "Tab":
                        s.selectResult();
                        break;
                    case "Enter":
                        var i = t.target.getAttribute("aria-activedescendant").length > 0;
                        s.selectedResult = s.results[s.selectedIndex] || s.selectedResult, s.selectResult(), s.submitOnEnter ? s.selectedResult && s.onSubmit(s.selectedResult) : i ? t.preventDefault() : (s.selectedResult && s.onSubmit(s.selectedResult), s.selectedResult = null);
                        break;
                    case "Esc":
                    case "Escape":
                        s.hideResults(), s.setValue();
                        break;
                    default:
                        return
                }
            })), n(this, "handleFocus", (function(t) {
                var e = t.target.value;
                s.updateResults(e), s.value = e
            })), n(this, "handleBlur", (function() {
                s.hideResults()
            })), n(this, "handleResultMouseDown", (function(t) {
                t.preventDefault()
            })), n(this, "handleResultClick", (function(t) {
                var e = t.target,
                    n = i(e, "[data-result-index]");
                if (n) {
                    s.selectedIndex = parseInt(n.dataset.resultIndex, 10);
                    var o = s.results[s.selectedIndex];
                    s.selectResult(), s.onSubmit(o)
                }
            })), n(this, "handleArrows", (function(t) {
                var e = s.results.length;
                s.selectedIndex = (t % e + e) % e, s.onUpdate(s.results, s.selectedIndex)
            })), n(this, "selectResult", (function() {
                var t = s.results[s.selectedIndex];
                t && s.setValue(t), s.hideResults()
            })), n(this, "updateResults", (function(t) {
                var e = ++s.searchCounter;
                s.onLoading(), s.search(t).then((function(t) {
                    e === s.searchCounter && (s.results = t, s.onLoaded(), 0 !== s.results.length ? (s.selectedIndex = s.autoSelect ? 0 : -1, s.onUpdate(s.results, s.selectedIndex), s.showResults()) : s.hideResults())
                }))
            })), n(this, "showResults", (function() {
                s.setAttribute("aria-expanded", !0), s.onShow()
            })), n(this, "hideResults", (function() {
                s.selectedIndex = -1, s.results = [], s.setAttribute("aria-expanded", !1), s.setAttribute("aria-activedescendant", ""), s.onUpdate(s.results, s.selectedIndex), s.onHide()
            })), n(this, "checkSelectedResultVisible", (function(t) {
                var e = t.querySelector('[data-result-index="'.concat(s.selectedIndex, '"]'));
                if (e) {
                    var n = t.getBoundingClientRect(),
                        i = e.getBoundingClientRect();
                    i.top < n.top ? t.scrollTop -= n.top - i.top : i.bottom > n.bottom && (t.scrollTop += i.bottom - n.bottom)
                }
            })), this.search = o(l) ? l : function(t) {
                return Promise.resolve(l(t))
            }, this.autoSelect = a, this.setValue = d, this.setAttribute = p, this.onUpdate = f, this.onSubmit = L, this.autocorrect = w, this.onShow = g, this.onHide = S, this.onLoading = A, this.onLoaded = k, this.submitOnEnter = C
        },
        l = 0,
        r = function() {
            var t = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : "";
            return "".concat(t).concat(++l)
        },
        a = function(t, e) {
            var n = t.getBoundingClientRect(),
                s = e.getBoundingClientRect();
            return n.bottom + s.height > window.innerHeight && window.innerHeight - n.bottom < n.top && window.pageYOffset + n.top - s.height > 0 ? "above" : "below"
        },
        c = function(t, e, n) {
            var s;
            return function() {
                var i = this,
                    o = arguments,
                    u = function() {
                        s = null, n || t.apply(i, o)
                    },
                    l = n && !s;
                clearTimeout(s), s = setTimeout(u, e), l && t.apply(i, o)
            }
        },
        d = function(t) {
            if (null == t ? void 0 : t.length) {
                var e = t.startsWith("#");
                return {
                    attribute: e ? "aria-labelledby" : "aria-label",
                    content: e ? t.substring(1) : t
                }
            }
        },
        h = function() {
            function n(e, s, i) {
                t(this, n), this.id = "".concat(i, "-result-").concat(e), this.class = "".concat(i, "-result"), this["data-result-index"] = e, this.role = "option", e === s && (this["aria-selected"] = "true")
            }
            var s, i, o;
            return s = n, (i = [{
                key: "toString",
                value: function() {
                    var t = this;
                    return Object.keys(this).reduce((function(e, n) {
                        return "".concat(e, " ").concat(n, '="').concat(t[n], '"')
                    }), "")
                }
            }]) && e(s.prototype, i), o && e(s, o), n
        }();
    return function e(s) {
        var i = this,
            o = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : {},
            l = o.search,
            p = o.onSubmit,
            b = void 0 === p ? function() {} : p,
            f = o.onUpdate,
            v = void 0 === f ? function() {} : f,
            L = o.baseClass,
            m = void 0 === L ? "autocomplete" : L,
            g = o.autocorrect,
            y = void 0 !== g && g,
            w = o.autoSelect,
            R = o.getResultValue,
            S = void 0 === R ? function(t) {
                return t
            } : R,
            x = o.renderResult,
            A = o.debounceTime,
            E = void 0 === A ? 0 : A,
            k = o.resultListLabel,
            I = o.submitOnEnter,
            C = void 0 !== I && I;
        t(this, e), n(this, "expanded", !1), n(this, "loading", !1), n(this, "position", {}), n(this, "resetPosition", !0), n(this, "initialize", (function() {
            i.root.style.position = "relative", i.input.setAttribute("role", "combobox"), i.input.setAttribute("autocomplete", "off"), i.input.setAttribute("autocapitalize", "off"), i.autocorrect && i.input.setAttribute("autocorrect", "on"), i.input.setAttribute("spellcheck", "false"), i.input.setAttribute("aria-autocomplete", "list"), i.input.setAttribute("aria-haspopup", "listbox"), i.input.setAttribute("aria-expanded", "false"), i.resultList.setAttribute("role", "listbox");
            var t = d(i.resultListLabel);
            t && i.resultList.setAttribute(t.attribute, t.content), i.resultList.style.position = "absolute", i.resultList.style.zIndex = "1", i.resultList.style.width = "100%", i.resultList.style.boxSizing = "border-box", i.resultList.id || (i.resultList.id = r("".concat(i.baseClass, "-result-list-"))), i.input.setAttribute("aria-owns", i.resultList.id), document.body.addEventListener("click", i.handleDocumentClick), i.input.addEventListener("input", i.core.handleInput), i.input.addEventListener("keydown", i.core.handleKeyDown), i.input.addEventListener("focus", i.core.handleFocus), i.input.addEventListener("blur", i.core.handleBlur), i.resultList.addEventListener("mousedown", i.core.handleResultMouseDown), i.resultList.addEventListener("click", i.core.handleResultClick), i.updateStyle()
        })), n(this, "destroy", (function() {
            document.body.removeEventListener("click", i.handleDocumentClick), i.input.removeEventListener("input", i.core.handleInput), i.input.removeEventListener("keydown", i.core.handleKeyDown), i.input.removeEventListener("focus", i.core.handleFocus), i.input.removeEventListener("blur", i.core.handleBlur), i.resultList.removeEventListener("mousedown", i.core.handleResultMouseDown), i.resultList.removeEventListener("click", i.core.handleResultClick), i.root = null, i.input = null, i.resultList = null, i.getResultValue = null, i.onUpdate = null, i.renderResult = null, i.core.destroy(), i.core = null
        })), n(this, "setAttribute", (function(t, e) {
            i.input.setAttribute(t, e)
        })), n(this, "setValue", (function(t) {
            i.input.value = t ? i.getResultValue(t) : ""
        })), n(this, "renderResult", (function(t, e) {
            return "<li ".concat(e, ">").concat(i.getResultValue(t), "</li>")
        })), n(this, "handleUpdate", (function(t, e) {
            i.resultList.innerHTML = "", t.forEach((function(t, n) {
                var s = new h(n, e, i.baseClass),
                    o = i.renderResult(t, s);
                "string" == typeof o ? i.resultList.insertAdjacentHTML("beforeend", o) : i.resultList.insertAdjacentElement("beforeend", o)
            })), i.input.setAttribute("aria-activedescendant", e > -1 ? "".concat(i.baseClass, "-result-").concat(e) : ""), i.resetPosition && (i.resetPosition = !1, i.position = a(i.input, i.resultList), i.updateStyle()), i.core.checkSelectedResultVisible(i.resultList), i.onUpdate(t, e)
        })), n(this, "handleShow", (function() {
            i.expanded = !0, i.updateStyle()
        })), n(this, "handleHide", (function() {
            i.expanded = !1, i.resetPosition = !0, i.updateStyle()
        })), n(this, "handleLoading", (function() {
            i.loading = !0, i.updateStyle()
        })), n(this, "handleLoaded", (function() {
            i.loading = !1, i.updateStyle()
        })), n(this, "handleDocumentClick", (function(t) {
            i.root.contains(t.target) || i.core.hideResults()
        })), n(this, "updateStyle", (function() {
            i.root.dataset.expanded = i.expanded, i.root.dataset.loading = i.loading, i.root.dataset.position = i.position, i.resultList.style.visibility = i.expanded ? "visible" : "hidden", i.resultList.style.pointerEvents = i.expanded ? "auto" : "none", "below" === i.position ? (i.resultList.style.bottom = null, i.resultList.style.top = "100%") : (i.resultList.style.top = null, i.resultList.style.bottom = "100%")
        })), this.root = "string" == typeof s ? document.querySelector(s) : s, this.input = this.root.querySelector("input"), this.resultList = this.root.querySelector("ul"), this.baseClass = m, this.autocorrect = y, this.getResultValue = S, this.onUpdate = v, "function" == typeof x && (this.renderResult = x), this.resultListLabel = k, this.submitOnEnter = C;
        var U = new u({
            search: l,
            autoSelect: w,
            setValue: this.setValue,
            setAttribute: this.setAttribute,
            onUpdate: this.handleUpdate,
            autocorrect: this.autocorrect,
            onSubmit: b,
            onShow: this.handleShow,
            onHide: this.handleHide,
            onLoading: this.handleLoading,
            onLoaded: this.handleLoaded,
            submitOnEnter: this.submitOnEnter
        });
        E > 0 && (U.handleInput = c(U.handleInput, E)), this.core = U, this.initialize()
    }
}();