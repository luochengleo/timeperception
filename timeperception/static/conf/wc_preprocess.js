/**
 * @author Wang Chao
 * v. 0.0.1
 */
//get page id
// var current_url = window.location.href;
// //alert("current url = " + current_url);
// var id_re = /\?id=(\d+)/;
// var wc_page_id = "NoneID";
// if(id_re.test(current_url)){
// //alert(RegExp.$1);
// wc_page_id = RegExp.$1;
// }

// var wc_user = getCookie("userCookie");
var studentID = getCookie("studentID");

function getCookie(c_name) {
    if (document.cookie.length > 0) {
        c_start = document.cookie.indexOf(c_name + "=")
        if (c_start != -1) {
            c_start = c_start + c_name.length + 1
            c_end = document.cookie.indexOf(";", c_start)
            if (c_end == -1) c_end = document.cookie.length
            return unescape(document.cookie.substring(c_start, c_end))
        }
    }
    return ""
}

function nextQueryPage() {
    window.location.href = "/NextPage?studentID=" + studentID + "&currentQueryID=" + currentQueryID;
}


 
 