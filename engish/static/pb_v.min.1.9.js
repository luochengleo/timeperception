function m_s() {
    var n = (new Date).getTime(), c = escape(n * 1e3 + Math.round(Math.random() * 1e3));
    with (document)cookie.indexOf("SUV=") < 0 && (cookie = "SUV=" + c + ";path=/;expires=Sun, 29 July 2046 00:00:00 UTC;domain=sogou.com"), domain.indexOf(".sogou.com") >= 0 && (typeof uuid == "string" && uuid.length > 0 ? write('<img src="http://pv.sogou.com/pv.gif?uuid=' + uuid + "?t=" + c + "?r?=" + referrer + "\" width=1 height=1 style='position:absolute;top:-1px'>") : write('<img src="http://pv.sogou.com/pv.gif?t=' + c + "?r?=" + referrer + "\" width=1 height=1 style='position:absolute;top:-1px'>"))
}
function isIE() {
    var isIE = navigator.userAgent.indexOf("MSIE") > 0 ? !0 : !1;
    return isIE
}
function uigs_getCookie(A) {
    return uigs_cookieArray[A]
}
function uigs_getCookiePara() {
    var A = "";
    if (typeof uigs_para != "undefined" && typeof uigs_para.uigs_cookie != "undefined") {
        var B = uigs_para.uigs_cookie.split(",");
        for (i in B)typeof uigs_getCookie(B[i]) != "undefined" && B[i] != "SUV" && (A == "" ? A = B[i] + "=" + uigs_getCookie(B[i]) : A = A + "&" + B[i] + "=" + uigs_getCookie(B[i]))
    }
    return encodeURIComponent(A)
}
function uigs_getPingbackhead() {
    if (typeof uigs_para != "undefined" && typeof uigs_para.uigs_productid != "undefined") {
        uigs_c = escape((new Date).getTime() * 1e3 + Math.round(Math.random() * 1e3)), r = typeof encodeURIComponent == "function" ? encodeURIComponent(document.referrer) : document.referrer;
        var A = "?uigs_productid=" + uigs_para.uigs_productid + "&uigs_t=" + uigs_c;
        typeof uigs_para.uigs_cookie != "undefined" && (A += "&uigs_cookie=" + uigs_getCookiePara()), typeof uigs_para.uigs_uuid != "undefined" && (A += "&uigs_uuid=" + uigs_para.uigs_uuid);
        for (i in uigs_para)i != "uigs_cookie" && i != "uigs_uuid" && i != "uigs_productid" && (A += "&" + encodeURIComponent(i) + "=" + encodeURIComponent(uigs_para[i]));
        return A += "&uigs_version=" + uigs_version + "&uigs_refer=" + r, A
    }
    return""
}
function uigs_pv() {
    uigs_getCookie("SUV") || (uigs_c = escape((new Date).getTime() * 1e3 + Math.round(Math.random() * 1e3)), cookie = "SUV=" + uigs_c + ";path=/;expires=Tue, 19-Jan-2046 00:00:00 GMT;domain=sogou.com");
    if (typeof uigs_para != "undefined" && typeof uigs_para.uigs_productid != "undefined") {
        var C = uigs_staytime;
        uigs_staytime < 0 && (C = 0 - uigs_staytime);
        var A = uigs_pvpingbackurl + uigs_getPingbackhead(), B = uigs_pbs.length;
        uigs_pbs[B] = new Image, uigs_pbs[B].src = A
    }
}
function uigsPB(A, E) {
    if (typeof uigs_para != "undefined" && typeof uigs_para.uigs_productid != "undefined") {
        var D = uigs_staytime;
        uigs_staytime < 0 && (D = 0 - uigs_staytime);
        var B = uigs_clpingbackurl + uigs_getPingbackhead() + "&uigs_st=" + parseInt(((new Date).getTime() - D) / 1e3) + "&uigs_cl=" + encodeURIComponent(A);
        E && (B = B + "&txt=" + encodeURIComponent(E));
        var C = uigs_pbs.length;
        uigs_pbs[C] = new Image, uigs_pbs[C].src = B
    }
}
function uigs_iecompattest() {
    return document.compatMode && document.compatMode != "BackCompat" ? document.documentElement : document.body
}
m_s();
var sogou_last_mousedown_time = 0, sogou_mousemove_distance = 0, sogou_old_document_click = isIE() ? document.body.onclick : document.onclick, sogou_old_document_mousedown = document.onmousedown, sogou_old_document_mousemove = document.onmousemove;
isIE() ? document.body.onclick = function (evt) {
    uigs_para.mmc = (new Date).getTime() - sogou_last_mousedown_time, typeof sogou_old_document_click == "function" && sogou_old_document_click(evt)
} : document.onclick = function (evt) {
    uigs_para.mmc = (new Date).getTime() - sogou_last_mousedown_time, typeof sogou_old_document_click == "function" && sogou_old_document_click(evt)
}, document.onmousemove = function (evt) {
    uigs_para.mml = ++sogou_mousemove_distance, typeof sogou_old_document_mousemove == "function" && sogou_old_document_mousemove(evt)
}, document.onmousedown = function (evt) {
    sogou_last_mousedown_time = (new Date).getTime(), typeof sogou_old_document_mousedown == "function" && sogou_old_document_mousedown(evt)
};
var uigs_clpingbackurl = "http://pb.sogou.com/cl.gif", uigs_pvpingbackurl = "http://pb.sogou.com/pv.gif", uigs_version = "v1.1", uigs_staytime = (new Date).getTime();
typeof uigs_para != "undefined" && typeof uigs_para.uigs_clpingbackurl != "undefined" && uigs_para.uigs_clpingbackurl != "" && (uigs_clpingbackurl = uigs_para.uigs_clpingbackurl), typeof uigs_para != "undefined" && typeof uigs_para.uigs_pvpingbackurl != "undefined" && uigs_para.uigs_pvpingbackurl != "" && (uigs_pvpingbackurl = uigs_para.uigs_pvpingbackurl);
var uigs_cookieArray = {}, uigs_acookie = document.cookie.split("; "), uigs_pbs = new Array;
for (var i = 0; i < uigs_acookie.length; i++) {
    var arr = uigs_acookie[i].split("=");
    uigs_cookieArray[arr[0]] = arr[1]
}
uigs_d = escape((new Date).getTime() * 1e3 + Math.round(Math.random() * 1e3)), typeof uigs_para != "undefined" && typeof uigs_para.uigs_uuid == "undefined" && (uigs_para.uigs_uuid = uigs_d);
var uigs_spv;
if (typeof uigs_pvflag == "undefined" || !uigs_pvflag)uigs_spv || uigs_pv();
uigs_spv = 1, $uigs_d = document;
var uigs_oldclick = isIE() ? $uigs_d.body.onclick : $uigs_d.onclick;
isIE() ? $uigs_d.body.onclick = function (A) {
    var B;
    return uigs_oldclick && (B = uigs_oldclick(A)), uigs_clickit(A), B
} : $uigs_d.onclick = function (A) {
    var B;
    return uigs_oldclick && (B = uigs_oldclick(A)), uigs_clickit(A), B
};
var uigs_clickit = function (D) {
    if (typeof uigs_para != "undefined" && typeof uigs_para.uigs_productid != "undefined") {
        if (D && D.button != 0 || !D && window.event.button != 0)return;
        try {
            D = D || window.event;
            var G = D.target ? D.target : D.srcElement, C = "", H = "", A = "", E = "", F = "";
            while (C == "") {
                A = G.tagName.toUpperCase(), C || (C = G.uigs || G.getAttribute("uigs") || "");
                if (C && C == "nouigs")return;
                if (A == "A" || A == "LINK" || A == "AREA" || A == "INPUT" || A == "DIV")H = A;
                G.href && (E = G.href), A == "A" && G.innerHTML && (F = G.innerHTML);
                try {
                    if (H == uigs_para.uigs_pbtag) {
                        C = G.id || G.getAttribute("id") || "";
                        while (C == "") {
                            if (!G.parentNode)break;
                            G = G.parentNode;
                            if (!G.tagName)break;
                            C || (C = G.id || G.getAttribute("id") || "")
                        }
                        break
                    }
                } catch (B) {
                }
                if (!G.parentNode)break;
                G = G.parentNode;
                if (!G.tagName)break
            }
            (H && C || H && H == uigs_para.uigs_pbtag) && uigsPB(C + "&href=" + E, F)
        } catch (F) {
        }
    }
}, uigs_al = !1, uigs_judgeBottom = function () {
    try {
        var B = uigs_iecompattest().clientHeight, A = uigs_iecompattest().scrollHeight, F = uigs_iecompattest().scrollTop;
        if (F > 100 && A - B - F < 100 && !uigs_al) {
            uigs_al = !0;
            var C = "", D = uigs_staytime;
            uigs_staytime < 0 && (D = 0 - uigs_staytime), C = "tob=" + parseInt(((new Date).getTime() - D) / 1e3), uigsPB(C)
        }
    } catch (E) {
    }
};
window.setInterval(uigs_judgeBottom, 100)