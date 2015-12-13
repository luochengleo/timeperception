var kmap = new (function jsAnalyzXML() {
    var C = window.location.toString().split("?")[1].split("&"), F = ["pid", "w", "mfp"], G = ["dupppid=1", "dr=1"], D = 0, B = ["?ie=utf8"], A, E = this;
    for (; D < C.length; D++) {
        for (A = 0; A < F.length; A++) {
            if (C[D].indexOf(F[A] + "=") == 0) {
                B.push(C[D]);
                if (G[A]) {
                    B.push(G[A])
                }
                break
            }
        }
    }
    B.push("p=71330100&dp=1");
    this.parseXML = function (I) {
        var H;
        if (window.DOMParser) {
            H = new DOMParser().parseFromString(I, "text/xml")
        } else {
            H = new ActiveXObject("Microsoft.XMLDOM");
            H.async = "false";
            H.loadXML(I)
        }
        return H.documentElement
    };
    this.xml2json = function (J) {
        var M, I;
        I = H(J);
        M = K(I, {});
        function H(O) {
            var N;
            if (window.DOMParser) {
                N = new window.DOMParser().parseFromString(O, "text/xml")
            } else {
                N = new ActiveXObject("Microsoft.XMLDOM");
                N.async = "false";
                N.loadXML(O)
            }
            return(N.nodeType == 9) ? N.documentElement : N
        }

        function L(P, R) {
            var N, Q, O;
            for (Q = 0, O = P.length; Q < O; Q++) {
                N = P[Q];
                if (N.nodeType === 2) {
                    R[N.nodeName] = N.nodeValue
                }
            }
        }

        function K(N, Q) {
            if (!N) {
                return{}
            }
            Q = Q || {};
            var W = N.nodeType, X = N.nodeName, U = N.nodeValue;
            if (W == 1) {
                var R, O, T = N.childNodes, V, P, S;
                L(N.attributes, Q);
                for (R = 0, O = T.length; R < O; R++) {
                    V = T[R];
                    S = V.nodeName;
                    P = K(V, {});
                    if (typeof P === "string") {
                        Q._text = P
                    } else {
                        if (typeof P === "object") {
                            if (Q[S]) {
                                if (!(Q[S] instanceof Array)) {
                                    Q[S] = [Q[S]]
                                }
                                Q[S].push(P)
                            } else {
                                Q[S] = P
                            }
                        }
                    }
                }
                return Q
            } else {
                if (W === 3 || W === 4) {
                    if (!(/^\s+$/.test(U))) {
                        return U
                    }
                }
            }
        }

        return M
    };
    this.splicelink = function (M, J, I, H, K, O, L) {
        var N = B.concat(["query=" + encodeURIComponent(M)]);
        if (J) {
            N.push("oriId=" + J)
        }
        if (I) {
            N.push("clickId=" + I)
        }
        if (H) {
            N.push("clickArea=" + H)
        }
        if (K) {
            N.push("kmaptype=" + encodeURIComponent(K))
        }
        if (typeof (O) != "undefined") {
            N.push("pos=" + O)
        }
        if (typeof (L) != "undefined") {
            N.push("songpos=" + L)
        }
        return N.join("&")
    };
    this.first = function (I, H) {
        if (I) {
            return I.getElementsByTagName(H)[0]
        }
        return null
    };
    this.all = function (I, H) {
        if (I) {
            return I.getElementsByTagName(H)
        }
        return null
    };
    this.attr = function (J, I) {
        if (!J) {
            return""
        }
        var H = J.getAttribute(I);
        if (!H && I.indexOf("id") >= 0) {
            H = J.getAttribute("sg2oids")
        }
        return H || ""
    };
    this.tagtext = function (H) {
        if (!H || H.firstChild == null) {
            return""
        }
        return H.firstChild.nodeValue
    };
    this.tagtxt = function (J) {
        if (!J || !J.firstChild) {
            return""
        }
        for (var H = 0; H < J.childNodes.length; H++) {
            var I = J.childNodes[H];
            if (I.nodeType == 4) {
                return I.nodeValue
            }
        }
        return J.firstChild.nodeValue
    };
    this.exist = function (K, I, H) {
        var J;
        if (H) {
            J = K.getAttribute(I)
        } else {
            J = K.getElementsByTagName(I)
        }
        if (J == null || J == "") {
            return false
        }
        return true
    };
    this.bind = function (J, H, I) {
        if (J) {
            return J.addEventListener ? J.addEventListener(H, I, false) : J.attachEvent("on" + H, I)
        }
    };
    this.pos = function (I) {
        var H = I.offsetLeft, J = I.offsetTop;
        while (I = I.offsetParent) {
            H += I.offsetLeft;
            J += I.offsetTop
        }
        return[H, J]
    };
    this.feedlink = function (M, N, J, I, L, K) {
        var H = $s.$c("a", M, N);
        H.href = "#";
        H.innerHTML = I || "����";
        H.setAttribute("hidefocus", true);
        H.style.outline = "none";
        if (L) {
            if (K) {
                H.parentNode.style.display = "none"
            } else {
                H.style.display = "none"
            }
        }
        return H
    };
    this.hidefocus = function (H, J, I, K) {
        H.href = I;
        H.innerHTML = J;
        H.setAttribute("hidefocus", true);
        H.style.outline = "none";
        H.target = "_blank";
        H.id = K
    };
    this.wholequery = function (H, I) {
        if (I) {
            return H
        } else {
            return H + " " + I
        }
    };
    this.imghandle = function (L, M, K, H) {
        var I = "/images/kmap/default" + ((H == 90) ? 90 : 70) + ".png";
        L.onerror = function () {
            L.src = I;
            L.style.visibility = "visible";
            L.style.marginLeft = "0px";
            L.style.marginTop = "0px";
            return
        };
        L.src = M || I;
        L.onload = function () {
            L.style.visibility = "hidden";
            J(L);
            L.style.visibility = "visible"
        };
        function J(N) {
            if (N.height == 0) {
                setTimeout(function () {
                    J(N)
                }, 50);
                return
            }
            if (K != N.width) {
                var O = Math.floor((N.width - K) / 2);
                L.style.marginLeft = (-O) + "px"
            }
            if (H != N.height) {
                var O = Math.floor((N.height - H) / 2);
                L.style.marginTop = (-O) + "px"
            }
        }
    };
    this.imageHandle = function (M, N, J, H) {
        var I = "/images/kmap/default" + ((H == 90) ? 90 : 70) + ".png";
        M.onerror = function () {
            M.src = I;
            M.style.visibility = "visible";
            M.style.marginLeft = "0px";
            M.style.marginTop = "0px";
            M.width = J;
            return
        };
        M.onload = function () {
            M.style.visibility = "hidden";
            L(M, J, H);
            M.style.visibility = "visible"
        };
        M.src = N || I;
        function L(P, O, Q) {
            if (P.height == 0) {
                setTimeout(function () {
                    L(P, O, Q)
                }, 50);
                return
            }
            var R = K(P.width, P.height, O, Q);
            P.style.marginLeft = -R.ml + "px";
            P.style.marginTop = -R.mt + "px";
            if (R.height) {
                P.height = R.height
            }
            if (R.width) {
                P.width = R.width
            }
        }

        function K(P, S, O, R) {
            var U, Q, T = {};
            if (S * O < P * R && (S > R || P > O)) {
                P = P * R / S;
                U = (P - O) / 2;
                Q = 0;
                if (S != R) {
                    T.height = R
                }
            } else {
                S = S * O / P;
                Q = S - R;
                if (Q > S * 0.16) {
                    Q = S * 0.08
                } else {
                    Q /= 2
                }
                U = 0;
                if (P != O) {
                    T.width = O
                }
            }
            T.ml = parseInt(U);
            T.mt = parseInt(Q);
            return T
        }
    };
    this.isWrap = function (J, I) {
        J.innerHTML = J.innerHTML + I.substring(0, 1);
        var H = J.offsetHeight;
        J.innerHTML = J.innerHTML + I.substring(1);
        if (H > J.offsetHeight - 3) {
            return false
        }
        return true
    };
    this.len = function (H) {
        if (H) {
            return H.replace(/<.*?>/g, "").replace(/[^\x00-\xff]/g, "rr").replace(/&nbsp;/g, " ").length
        }
        return 0
    };
    this.cutLength = function (K, H, I, J) {
        I = I || "..";
        J = J || 2;
        if (this.len(K) > H) {
            do {
                K = K.substring(0, K.length - 1)
            } while (K && (this.len(K) + J > H));
            if (K.lastIndexOf("</") != K.lastIndexOf("<")) {
                K = K.substring(0, K.lastIndexOf("<")) + K.substring(K.lastIndexOf(">") + 1)
            }
            return K + I
        }
        return K
    };
    this.q2b = function (N) {
        try {
            var I = [], J = 0, H = N.length, L, K;
            for (; J < H; J++) {
                L = N.charCodeAt(J);
                if (L > 65280 && L < 65375) {
                    I.push(String.fromCharCode(L - 65248))
                } else {
                    I.push(N.charAt(J))
                }
            }
            return I.join("")
        } catch (M) {
            return N
        }
    };
    this.dommouseact = function (K, J, H, I) {
        K.onmouseover = function () {
            I.className = H
        };
        K.onmouseout = function () {
            I.className = J
        }
    };
    this.tupudissatisfied = function (I, J, H) {
        $s.$(I).target = "_blank";
        if ($s.$(J)) {
            $s.$(I).scenehtml.value = $s.$(J).outerHTML
        } else {
            $s.$(I).scenehtml.value = ""
        }
        $s.$(I).content.value = H;
        $s.$(I).action = "http://www.sogou.com/complain/tupu/front/index.php";
        $s.$(I).submit()
    };
    this.kmapPB = function (J, I) {
        var H = [];
        H.push("http://pb.sogou.com/pv.gif?uigs_productid=kmap&type=", J, I);
        H.push("&sab=", sab, "&k_uuid=", uuid, "&gbkQuery=", encodeURIComponent(gbkQuery));
        if (typeof uigs_para != "undefined" && (J == "left" || J == "right")) {
            H.push("&abtestid=", uigs_para.abtestid, "&query=", encodeURIComponent(uigs_para.query), "&loc=", uigs_para.loc, "&uigs_uuid=", uigs_para.uigs_uuid)
        }
        (new Image()).src = H.join("")
    };
    this.speedStat = function (K) {
        var I, M, J, L, H;
        I = kmap.loadInitEnd - kmap.loadInitBegin;
        M = kmap.loadLeftEnd - kmap.loadLeftBegin;
        J = kmap.leftDone - kmap.loadLeftEnd;
        L = kmap.leftDone - kmap.loadInitBegin;
        H = "&template=" + K;
        if (!isNaN(I)) {
            H += "&initload=" + I
        }
        if (!isNaN(M)) {
            H += "&leftload=" + M
        }
        if (!isNaN(J)) {
            H += "&leftrun=" + J
        }
        if (!isNaN(L)) {
            H += "&total=" + L
        }
        this.kmapPB("speed_stat", H)
    };
    this.cutRankList = function (I) {
        var J = $s.$("right"), H = $s.$("main"), L, K;
        if (!J || !H) {
            return
        }
        L = J.scrollHeight;
        K = H.scrollHeight;
        if (L < K) {
            return
        }
        if (I) {
            I.style.display = "none"
        }
    };
    this.cutAds = function () {
        var P = $s.$("right"), L = $s.$("main"), H, O, M, I = [], J, K;
        if (!P || !L) {
            return
        }
        H = P.scrollHeight;
        O = L.scrollHeight;
        M = $s.$$(P, "div");
        for (var N = 0; N < M.length; N++) {
            if (M[N].id == "bdfs0" && M[N].className == "b_rb" && M[N].style.display != "none") {
                I.push(M[N])
            }
        }
        if (!I) {
            return
        }
        J = Math.round((H - O) / 90);
        K = (I.length - J <= 0) ? 1 : I.length - J;
        for (var N = K; N < I.length; N++) {
            if (I[N]) {
                I[N].style.display = "none"
            }
        }
    };
    this.cutQueryList = function (P) {
        if (!P) {
            return
        }
        var Q = $s.$("right"), L = $s.$("main"), H, O, I, M = [], K, J;
        if (!Q || !L) {
            return
        }
        H = Q.scrollHeight;
        O = L.scrollHeight;
        I = $s.$$(P, "div");
        for (var N = 0; N < I.length; N++) {
            if (I[N].id == "kmap-query-td-b" && I[N].className == "td-b" && I[N].style.display != "none") {
                M.push(I[N])
            }
        }
        K = Math.ceil((H - O) / 85);
        J = (M.length - K <= 0) ? 1 : M.length - K;
        for (var N = J; N < M.length; N++) {
            if (M[N]) {
                M[N].style.display = "none"
            }
        }
        H = Q.scrollHeight;
        if (H > O) {
            P.style.display = "none"
        }
    }
})();