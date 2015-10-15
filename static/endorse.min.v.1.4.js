if (typeof JSON == "undefined" || !JSON) {
    var jsonScript = document.createElement("script");
    jsonScript.src = "http://www.sogou.com/js/comment/json2.v.1.0.js";
    document.getElementsByTagName("head")[0].appendChild(jsonScript)
}
function initEndorseShow(e) {
    if (!e) {
        return
    }
    var h = (function () {
        var w, i = 3, x = document.createElement("div"), u = x.getElementsByTagName("i");
        while (x.innerHTML = "<!--[if gt IE " + (++i) + "]><i></i><![endif]-->", u[0]) {
        }
        return i > 4 ? i : w
    }());
    if (h == 6 || (h == 7 && ($(e).attr("from") == "struct" || $(e).attr("from") == "vr"))) {
        $(e).parent().hide()
    }
    var b = e.textContent || e.innerText;
    if (!b) {
        return
    }
    b = b.replace("<![CDATA[", "").replace("]]>", "");
    var s = JSON.parse(b);
    var m = s.count;
    var c = e.parentNode.getElementsByTagName("li")[0];
    if (m && m != "0") {
        c.getElementsByTagName("a")[0].innerHTML = handleEndorseCountShow(m)
    }
    var t = s.me;
    var l = s.friends;
    if (t || l) {
        var r = l ? "�����޹�" : "���޹�";
        var a = document.createElement("li");
        a.className = "fb-laud";
        a.innerHTML = r;
        e.parentNode.appendChild(a);
        if (l) {
            if (t) {
                c.getElementsByTagName("a")[0].className = "on-laud";
                var d = {};
                d.uid = userinfo.puid;
                d.nickname = userinfo.username;
                d.headurl = userinfo.headurl;
                l.splice(parseInt(t), 0, d)
            }
            for (var o = 0; o < l.length && o < 4; o++) {
                var k = l[o];
                var q = document.createElement("li");
                q.className = "fb-pic";
                var j = document.createElement("a");
                j.href = "javascript:void(0)";
                j.setAttribute("uid", k.uid);
                j.setAttribute("title", k.nickname);
                var n = document.createElement("img");
                n.setAttribute("src", k.headurl);
                q.appendChild(j);
                j.appendChild(n);
                e.parentNode.appendChild(q)
            }
        } else {
            if (t) {
                c.getElementsByTagName("a")[0].className = "on-laud";
                var p = document.createElement("li");
                p.className = "fb-pic";
                var g = document.createElement("a");
                g.href = "javascript:void(0)";
                g.setAttribute("uid", userinfo.puid);
                g.setAttribute("title", userinfo.username);
                var f = document.createElement("img");
                f.setAttribute("src", userinfo.headurl);
                p.appendChild(g);
                g.appendChild(f);
                e.parentNode.appendChild(p)
            }
        }
    }
}
function handleEndorseCountShow(c) {
    var b = /^(\d+)\d{4}$/;
    if (b.test(c)) {
        var a = b.exec(c);
        c = a[1] + "��"
    }
    return c
}
define("", ["$"], function (f) {
    var b = $s.cookie("SUV");
    var d = "0";
    if (typeof(userinfo) != "undefined" && userinfo.puid) {
        d = userinfo.puid
    }
    f(function () {
        var p = $s.cookie("uigs_loginbtn_tologin");
        if (p && d != "0") {
            $s.cookie("uigs_loginbtn_tologin", "", -1, "www.sogou.com");
            h(oldQuery, "right_cmt", 0, d)
        }
        f("#loginBtn").click(function () {
            $s.cookie("uigs_loginbtn_tologin", "1", 5 * 60 * 1000, "www.sogou.com");
            h(oldQuery, "right_cmt", 0, d)
        });
        var x = $s.cookie("single_ret_endorse_tologin");
        if (x && d != "0") {
            $s.cookie("single_ret_endorse_tologin", "", -1, "www.sogou.com");
            var w = f("a[zandocid='" + x + "']").get(0);
            if (w && w.className != "on-laud") {
                c(w)
            }
            h(oldQuery, "single_ret_endorse", 2, d)
        }
        var u = 0, t = 0;
        setTimeout(function () {
            if (u > 0 && t > 0) {
                h(oldQuery, "single_ret_endorse", 6, d, "pv.gif", "&t_e_c=" + u + "&e_r_c=" + t)
            }
        }, 200);
        f(".fb .laud-ico a").each(function () {
            var D = "��ϲ��";
            if (this.className == "on-laud") {
                D = "ȡ��ϲ��"
            }
            this.setAttribute("title", D);
            f(this).click(function () {
                c(this);
                return false
            });
            var B = this.textContent || this.innerText;
            try {
                B = parseInt(B);
                if (B > 0) {
                    t++;
                    u += B
                }
            } catch (C) {
            }
        });
        if (a()) {
            if ($s.cookie("endorse_friendship_update") != userinfo.puid && userinfo.puid.indexOf("@qq.sohu.com") != -1) {
                var s = {};
                s.nickname = userinfo.username;
                s.headurl = userinfo.headurl;
                var z = "login" + uuid;
                var n = +new Date;
                (new Image()).src = "http://www.sogou.com/zan/api?op=login&type=endorse&docid=" + userinfo.puid + "&detail=" + encodeURIComponent(JSON.stringify(s)) + "&uuid=" + z + "&t=" + n;
                $s.cookie("endorse_friendship_update", userinfo.puid, 30 * 60 * 1000, "www.sogou.com")
            }
        } else {
            if ($s.cookie("endorse_friendship_update")) {
                $s.cookie("endorse_friendship_update", "", -1, "www.sogou.com")
            }
        }
        var A = 0;
        var r = [], o = [], y = {};
        f(".rt-fb .fb-pic a").each(function () {
            var D = f(this).attr("uid");
            if (D != userinfo.puid) {
                A++;
                var E = false;
                var G = f(this).parent().parent().get(0);
                for (var C = 0; C < r.length; C++) {
                    if (r[C] == G) {
                        E = true;
                        break
                    }
                }
                if (!E) {
                    r.push(G);
                    var B = f(this).parent().siblings(".laud-ico").find("a").attr("zanurl");
                    if (!y[B]) {
                        o.push(B);
                        y[B] = 1;
                        var F = f(this).parent().parent().parent().parent();
                        if (F) {
                            F.find("h3 a").click(function () {
                                h(oldQuery, "single_ret_endorse", 10, d)
                            })
                        }
                    }
                }
            }
            f(this).click(function () {
                h(oldQuery, "single_ret_endorse", 11, d)
            })
        });
        if (A > 0 && r.length > 0 && o.length > 0) {
            h(oldQuery, "single_ret_endorse", 9, d, "pv.gif", "&t_f_l_f=" + A + "&ret_count=" + r.length + "&ret_url_count=" + o.length)
        }
        var q = location.hash;
        if (q && q.length > 1) {
            q = q.substring(1);
            var m = f("a[zandocid='" + q + "']");
            if (m.length > 0) {
                var v = m.parent().parent().parent().parent().offset().top;
                v = v - 50;
                if (v > 0) {
                    setTimeout(function () {
                        f(document).scrollTop(v)
                    }, 500)
                }
            }
        }
    });
    function c(m) {
        if (!a()) {
            i();
            h(oldQuery, "single_ret_endorse", 1, d);
            var r = m.getAttribute("zandocid") || "1";
            $s.cookie("single_ret_endorse_tologin", r, 3 * 60 * 1000, "www.sogou.com");
            return
        }
        var u = userinfo.puid;
        var y = m.getAttribute("zandocid");
        var q, w;
        var p = f("#" + y + "").attr("from");
        if (p && p == "java") {
            q = decodeURIComponent(m.getAttribute("zanurl"));
            w = decodeURIComponent(m.getAttribute("zantitle"))
        } else {
            q = m.getAttribute("zanurl");
            w = m.getAttribute("zantitle")
        }
        var n = w.replace(/<em><!--red_beg-->/g, "").replace(/<!--red_end--><\/em>/g, "");
        var t = "add";
        if (m.className == "on-laud") {
            t = "del";
            h(oldQuery, "single_ret_endorse", 5, d)
        } else {
            h(oldQuery, "single_ret_endorse", 4, d, "", "&url=" + m.getAttribute("zanurl") + "&domain=" + j(q))
        }
        var s = {};
        s.url = q;
        s.title = n;
        s.query = l();
        s.url_type = "0";
        var o = +new Date;
        var x = t + uuid;
        var v = "op=" + t + "&type=endorse&uid=" + u + "&docid=" + y + "&detail=" + encodeURIComponent(JSON.stringify(s)) + "&uuid=" + x + "&t=" + o;
        f.ajax({type: "GET", url: "/zan/api", data: v, dataType: "html", success: function (z) {
            if (!z) {
                return
            }
            var A = JSON.parse(z);
            if (A.code != "ok") {
                return
            }
            k(m)
        }})
    }

    function j(n) {
        var m = document.createElement("a");
        m.href = n;
        return m.hostname
    }

    function k(o) {
        var m = o.textContent || o.innerText || "0";
        var n = true;
        if (m.indexOf("��") == -1) {
            m = parseInt(m)
        } else {
            n = false
        }
        if (o.className == "on-laud") {
            o.className = "";
            o.setAttribute("title", "��ϲ��");
            if (n && m > 0) {
                m -= 1
            }
            e(o)
        } else {
            o.className = "on-laud";
            o.setAttribute("title", "ȡ��ϲ��");
            if (n) {
                m += 1
            }
            e(o, "add")
        }
        o.innerHTML = m == 0 ? "" : m
    }

    function e(s, t) {
        t = t || "cancel";
        if (t == "add") {
            var m = f(s).parent().siblings(".fb-laud,.fb-pic");
            if (m.length == 0) {
                var n = document.createElement("li");
                n.className = "fb-laud";
                n.innerHTML = "���޹�";
                var q = document.createElement("li");
                q.className = "fb-pic";
                var r = document.createElement("a");
                r.setAttribute("href", "javascript:void(0);");
                r.setAttribute("uid", userinfo.puid);
                r.setAttribute("title", userinfo.username);
                var o = document.createElement("img");
                o.setAttribute("src", userinfo.headurl);
                r.appendChild(o);
                q.appendChild(r);
                f(s).parent().parent().append(n).append(q)
            } else {
                var q = document.createElement("li");
                q.className = "fb-pic";
                var r = document.createElement("a");
                r.setAttribute("href", "javascript:void(0);");
                r.setAttribute("uid", userinfo.puid);
                r.setAttribute("title", userinfo.username);
                var o = document.createElement("img");
                o.setAttribute("src", userinfo.headurl);
                r.appendChild(o);
                q.appendChild(r);
                f(s).parent().siblings(".fb-laud").after(q);
                if (m.length == 5) {
                    f(s).parent().siblings(".fb-pic:last").remove()
                }
            }
        } else {
            var p = f(s).parent().siblings(".fb-pic");
            if (p.length == 1) {
                f(s).parent().siblings(".fb-laud").remove()
            } else {
                f(s).parent().siblings(".fb-laud").text("�����޹�")
            }
            p.each(function () {
                var u = f(this).children("a").attr("uid");
                if (u == userinfo.puid) {
                    f(this).remove()
                }
            })
        }
    }

    function l() {
        var m = f("#common_qc_container strong em").text();
        if (!m) {
            m = oldQuery
        }
        return m
    }

    function a() {
        if (typeof(userinfo) != "undefined" && userinfo.username && userinfo.headurl && userinfo.ip && userinfo.puid) {
            return true
        }
        return false
    }

    function i() {
        if (!g) {
            return
        }
        var t = f(".wrap");
        var v = "http://www.sogou.com/login/qq_login_callback_page.html";
        g();
        var r = f(".wrap").height();
        var o = document.body.scrollTop | document.documentElement.scrollTop;
        var p = o + 0;
        var m = o + 113;
        var s = "https://account.sogou.com/connect/login?provider=qq&client_id=2017&ru=" + encodeURIComponent(v) + "&hun=0&oa=0", n = f('<div style="top:' + p + "px;height:" + r + 'px"/>').addClass("login-skin"), w = f('<div style="top:' + m + 'px"/>').addClass("login-pop"), q = f("<iframe/>").attr("src", s).css({width: 510, height: 500, border: 0}), u = f("<a/>").attr({id: "loginCloseBtn", href: "javascript:void(0)", "class": "del"});
        w.append(u);
        w.append(q);
        t.append(n);
        t.append(w);
        u.bind("click.closebox", function () {
            n.remove();
            w.remove();
            $s.cookie("single_ret_endorse_tologin", "", -1, "www.sogou.com");
            h(oldQuery, "single_ret_endorse", 3, d)
        })
    }

    function g() {
        if (f("#loginStyle").length > 0) {
            return
        }
        var n = ".login-skin{position: absolute;top:0;left:0;width: 100%;height: 100%;z-index: 1111111117;background-color: #000;opacity:0.4;filter:alpha(opacity=40);}.login-pop{background-color: #fff;border: 1px solid #ebebeb;width: 510px;height: 500px;position: absolute;margin-left:-225px;left: 50%;top: 113px;font-family: Microsoft YaHei;z-index: 1111111118;}.del{position: absolute;width: 20px;height: 20px;z-index: 4;top: 13px;right: 13px;display: block;background: url(/images/skin/del.gif) no-repeat;_background: url(/images/skin/del.gif) no-repeat;background-position: 0 0;}.del:hover{background-position: -41px 0;}";
        var m = f("<style/>").attr({id: "loginStyle", type: "text/css"});
        f("body").append(m);
        if (m[0].styleSheet) {
            m[0].styleSheet.cssText = n
        } else {
            m[0].appendChild(document.createTextNode(n))
        }
    }

    function h(r, o, s, m, p, n) {
        try {
            imgurl = ["http://pb.sogou.com/", p || "cl.gif", "?uigs_productid=webapp"];
            imgurl.push("&query=");
            imgurl.push(encodeURIComponent(r));
            imgurl.push("&type=");
            imgurl.push(o);
            imgurl.push("&pos=");
            imgurl.push(s);
            imgurl.push("&uid=");
            imgurl.push(m);
            imgurl.push("&suv=");
            imgurl.push(b);
            imgurl.push(n || "");
            imgurl.push("&uigs_t=");
            imgurl.push((new Date()).getTime());
            (new Image()).src = imgurl.join("")
        } catch (q) {
        }
    }
});