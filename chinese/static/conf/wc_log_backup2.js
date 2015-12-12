/**
 * @author Wang Chao
 * v. 0.0.1
 */

var current_page_url = window.location.href;
var current_site = get_set(current_page_url);
var server_site = current_site;
var check_state = 0;//init state
var satisfy_num = 0;
var satisfy_limit = 3;
var mouse_tracking_info = "";
var mouse_tracking_count = 0;
var mouse_tracking_group_limit = 100;
var mouse_tracking_baseline_stamp = (new Date()).getTime();
var mouse_tracking_time_stamp = mouse_tracking_baseline_stamp;
var mouse_tracking_pos_stamp = { 'x': 0, 'y': 0 };
var mouse_tracking_scroll_stamp = {'scrollX': 0, 'scrollY': 0};
var mouse_tracking_least_move_interval = 20;//ms
var mouse_tracking_least_move_distance = 20;//px 

//var page_change_id = setInterval(page_change, 3000);
//var mouse_tracking_id=setInterval(log_mouse_tracking, 1000);
document.onmousemove = log_mouse_tracking;
send_mouse_info(formInfo("BEGIN_SEARCH", ""));

var original_query = '';

window.onload = function () {
    original_query = $('#kw').attr("value");
}

var isTargetWindow = true;
$(window).focus(function () {
    isTargetWindow = true;
    send_mouse_info(formInfo("JUMP_IN", ""));
    mouse_tracking_time_stamp = (new Date()).getTime();
});

$(window).blur(function () {
    if (isTargetWindow) {
        send_mouse_info(formInfo("JUMP_OUT", ""));
        isTargetWindow = false;
    }
});

function get_set(url_str) {
    var ret = "10.0.17.201";
    var site_re = /http:\/\/([\w\.]+):8080\//;
    if (site_re.test(url_str)) {
        ret = RegExp.$1;
    }
    return ret;
}

$(window).scroll(function () {
    var c_left = $(this).scrollLeft();
    var c_top = $(this).scrollTop();
    var new_x = mouse_tracking_pos_stamp.x + c_left - mouse_tracking_scroll_stamp.scrollX;
    var new_y = mouse_tracking_pos_stamp.y + c_top - mouse_tracking_scroll_stamp.scrollY;
    var message = "FROM\t" + "x=" + mouse_tracking_pos_stamp.x + "\ty=" + mouse_tracking_pos_stamp.y + "\tTO\tx=" + new_x + "\t" + "y=" + new_y;
    mouse_tracking_scroll_stamp.scrollX = c_left;
    mouse_tracking_scroll_stamp.scrollY = c_top;
    mouse_tracking_pos_stamp.x = new_x;
    mouse_tracking_pos_stamp.y = new_y;
    send_mouse_info(formInfo("SCROLL", message));
});

window.onbeforeunload = function (e) {
    mouse_tracking_count = mouse_tracking_group_limit;
    send_mouse_info(formInfo("SEARCH_END", ""));
    return '完成1个查询任务,请再接再厉!';
    return ''
};

$(function () {
    $('.WCExamButton')
        .css({backgroundPosition: "0 0"})
        .mouseover(function () {
            if ($(this).get(0).disabled == false) {
                $(this).stop().animate({backgroundPosition: "(0 -250px)"}, {duration: 500})
            }
        })
        .mouseout(function () {
            if ($(this).get(0).disabled == false) {
                $(this).stop().animate({backgroundPosition: "(0 0)"}, {duration: 500})
            }
        })
        .click(function () {
            if ($(this).get(0).disabled == false) {
                if (satisfy_num < satisfy_limit) {
                    $(this).removeClass("button green").addClass("button gray");
                    $(this).removeClass("button orange").addClass("button gray");
                    examining_message($(this).get(0));
                    if (check_state == 4) {
                        satisfy_num += 1;
                    }
                }
            }
        })
});


$(function () {
    $('a')
        .hover(function () {
            base_link_message($(this).get(0), "HOVER", "anchor");
        })

});

$(function () {
    $('a')
        .click(function () {
            base_link_message($(this).get(0), "CLICK", "anchor");
        })

});

$(function () {
    $('img')
        .hover(function () {
            base_link_message($(this).get(0), "HOVER", "image");
        })
});

$(function () {
    $('img')
        .click(function () {
            base_link_message($(this).get(0), "CLICK", "image");
        })
});

function show_display_coordinate() {
    wc_result_vec = $('.WCResult');
    var info = "";
    for (var i = 0; i < wc_result_vec.size(); i++) {
        info += "result=" + i;
        info += "\tx=" + wc_result_vec.get(i).offsetLeft;
        info += "\ty=" + wc_result_vec.get(i).offsetTop;
        info += "\twidth=" + wc_result_vec.get(i).offsetWidth;
        info += "\theight=" + wc_result_vec.get(i).offsetHeight;
        info += "\n";
        //var oa=document.createAttribute("style");
        //wc_result_vec.get(i).attributes.setNamedItem(oa);
        //wc_result_vec.get(i).setAttribute("style","background-color: #aaa;border: solid 3px #f00;");
    }
    alert(info);
}

function display_examining_button() {
    if (check_state == 0) {
        //show_display_coordinate();
        check_state = 1;//first check
        client_time = (new Date()).getTime();
        $('.WCExamButton').addClass("button green");
        $('.WCOverButton').text("请标记您认为检验过的结果");
        send_mouse_info(formInfo("OVER", "check_state=" + check_state + '\tclient_time=' + client_time));
    } else if (check_state == 1) {
        check_state = 2;//second check
        $('.WCOverButton').text("请给出搜索满意程度的评价");
        send_mouse_info(formInfo("OVER", "check_state=" + check_state));
        wc_reveal();
    } else if (check_state == 2) {
        check_state = 3;//second check
        var satisfy_score = $('#wcstar').raty('score');
        send_mouse_info(formInfo("SATISFY", "score=" + satisfy_score));
        $('.WCOverButton').text("请再次确认您检验过的结果");
        wc_but_vec = $('.WCExamButton');
        wc_but_vec.removeClass("button gray").addClass("button green");
        //random display button
        Math.random();
        Math.random();
        for (var i = 1; i <= wc_but_vec.size(); i++) {
            if (Math.random() > (0.95 - 0.07 * i)) {
                wc_but_vec.get(i - 1).className = "WCExamButton";
                send_mouse_info(formInfo("NOT_SHOW", "result=" + (i - 1)));
            }
        }
        send_mouse_info(formInfo("OVER", "check_state=" + check_state));
    } else if (check_state == 3) {
        check_state = 4;//satisfy result
        $('.WCOverButton').text("请标记您认为有帮助的结果,至多3个");
        $('.WCExamButton').removeClass("button green").addClass("button orange");
        $('.WCExamButton').removeClass("button gray").addClass("button orange");
        $('.WCExamButton').text("有用");
    } else if (check_state == 4) {
        check_state = 5; //end
        $('.WCOverButton').text("完成任务!");
        $('.WCExamButton').removeClass("button orange");
        $('.bg.s_btn_wr').css('visibility', 'visible')
    } else if (check_state == 5) {
        nextQueryPage();
    }
}


function examining_message(exam_button_obj) {
    //exam_button_obj.disabled=true;
    var parent_obj = exam_button_obj.parentNode;
    while (parent_obj != null) {
        //alert(parent_obj.className);
        if (parent_obj.className == "WCResult") {
            var message = "check_state=" + check_state + "\tresult=" + parent_obj.id;
            send_mouse_info(formInfo("EXAMINE", message));
            break;
        }
        if (parent_obj.className == "WCAd") {
            var message = "check_state=" + check_state + "\tad=" + parent_obj.id;
            send_mouse_info(formInfo("EXAMINE", message));
            break;
        }
        parent_obj = parent_obj.parentNode;
    }
}

function base_link_message(link_obj, action_info, target_info) {
    var parent_obj = link_obj.parentNode;
    while (parent_obj != null) {
        if (parent_obj.className == "WCResult") {
            var message = "type=" + target_info + "\tresult=" + parent_obj.id;
            if (link_obj.href === undefined) {
                message = message + "\tsrc=" + link_obj.src;
            } else {
                message = message + "\tsrc=" + link_obj.href;
            }
            send_mouse_info(formInfo(action_info, message));
            break;
        }
        if (parent_obj.className == "WCAd") {
            var message = "type=" + target_info + "\tad=" + parent_obj.id;
            if (link_obj.href === undefined) {
                message = message + "\tsrc=" + link_obj.src;
            } else {
                message = message + "\tsrc=" + link_obj.href;
            }
            send_mouse_info(formInfo(action_info, message));
            break;
        }
        if (parent_obj.className == "WCRS") {
            var message = "type=" + target_info + "\trelevance_search";
            if (link_obj.href === undefined) {
                message = message + "\tsrc=" + link_obj.src;
            } else {
                message = message + "\tsrc=" + link_obj.href;
            }
            send_mouse_info(formInfo(action_info, message));
            break;
        }
        parent_obj = parent_obj.parentNode;
    }
}


//mouse tracking
function log_mouse_tracking(ev) {
    var new_time_stamp = (new Date()).getTime();
    var cur_pos = getMousePos(ev);
    var time_interval = new_time_stamp - mouse_tracking_time_stamp;
    var time_start = mouse_tracking_time_stamp - mouse_tracking_baseline_stamp;
    var time_end = new_time_stamp - mouse_tracking_baseline_stamp;
    var abs_pos_distance = Math.abs(cur_pos.x - mouse_tracking_pos_stamp.x) + Math.abs(cur_pos.y - mouse_tracking_pos_stamp.y);
    if (time_interval < mouse_tracking_least_move_interval || abs_pos_distance < mouse_tracking_least_move_distance) {
        return;
    }
    var info = "FROM\tx=" + mouse_tracking_pos_stamp.x + "\ty=" + mouse_tracking_pos_stamp.y + "\tTO\tx=" + cur_pos.x + "\ty=" + cur_pos.y + "\ttime=" + time_interval + "\tstart=" + time_start + "\tend=" + time_end;
    send_mouse_info(formInfo("MOUSE_MOVE", info));
    mouse_tracking_time_stamp = new_time_stamp;
    mouse_tracking_pos_stamp = cur_pos;
}

function time_info() {
    var new_time_stamp = (new Date()).getTime();
    var time_point = new_time_stamp - mouse_tracking_baseline_stamp;
    return time_point;
}

function send_mouse_info(info) {
    mouse_tracking_info = mouse_tracking_info + info;
    mouse_tracking_count++;
    if (mouse_tracking_count >= mouse_tracking_group_limit) {
        ajax_log_message(mouse_tracking_info);
        mouse_tracking_count = 0;
        mouse_tracking_info = "";
    }
}

function getMousePos(ev) {
    //alert("get mouse");
    var e = ev || window.event;
    var scrollX = document.documentElement.scrollLeft || document.body.scrollLeft;
    var scrollY = document.documentElement.scrollTop || document.body.scrollTop;
    var clientLeft = document.body.clientLeft;
    var clientTop = document.body.clientTop;
    var x = e.pageX || e.clientX + scrollX - clientLeft;
    //alert("x:" + x);
    var y = e.pageY || e.clientY + scrollY - clientTop;
    //alert('x: ' + x + '\ny: ' + y);
    return { 'x': x, 'y': y };
}

function formInfo(action_info, log_str) {
    var time_str = time_info();
    var info = "TIME=" + time_str + "\t" + "USER=" + studentID + "\t" + "QUERY=" + currentQueryID + "\t" + "ACTION=" + action_info + "\t" + "INFO:\t" + log_str + "\n";
    return info;
}

function ajax_log_message(log_str) {
    var encode_str = encodeURIComponent(log_str);
    //alert(encode_str + "\n");
    var log_url = "http://" + server_site + ":8080/PlusLogService";
    $.ajax({
        type: 'POST',
        url: log_url,
        data: {message: encode_str},
        complete: function (jqXHR, textStatus) {
            //alert(textStatus + "----" + jqXHR.status + "----" + jqXHR.readyState);
        }
    });
}

function do_search() {
    $("form").submit(function () {
        var tempInput = $('#kw').attr("value");
        if (tempInput != original_query) {
            send_mouse_info(formInfo("DO_SEARCH", ""));
            $('.bg.s_btn_wr').css('visibility', 'hidden');
        }
        else {
            //alert("两次输入一样");
            return false;
        }
    });
}