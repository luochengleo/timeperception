var resultList = [];
var checkList = [];
var clickList = [];
ex_result_vec = null;

interval = 12;

$(function () {
    wc_result_vec = $('.WCResult');
    wc_resultLayout_vec = $('.resultLayout');
    wc_buttonLayout_vec = $('.buttonLayout');
    //console.log(wc_resultLayout_vec);
    for (var i = 0; i < wc_result_vec.size(); i++) {
        height = wc_resultLayout_vec.get(i).offsetHeight + interval;
        newHeight = height + 'px'
        console.log(height);
        wc_result_vec.get(i).style.height = newHeight;
        wc_buttonLayout_vec.get(i).style.paddingTop = height * 0.28 + 'px';
    }
});

function ex_reveal() {
    $('#myModal_ex').reveal();
}


function randomSort(a, b) {
    Math.random();
    Math.random();
    return Math.random() - 0.5;
}

function ex_init(click_list) {
    clickList = click_list;
    console.log("click list:" + clickList);
    ex_reveal();
    if (resultList.length > 0) {
        resultList = [];
    }
    ex_result_vec = $('.WCResult');
    for (var i = 0; i < ex_result_vec.length; i++) {
        resultList.push(i);
    }
    resultList.sort(randomSort);
    resultDisplayList = resultList.join(",");
    resultList = resultList.reverse();
    checkList.push(resultList[resultList.length - 1]);
    $('#examineResult').html(ex_result_vec.get(resultList.pop()).cloneNode(true));
    return resultDisplayList;
}

function getCheckList() {
    return checkList;
}

function getResultID(exam_button_obj) {
    var child_obj = exam_button_obj.firstChild;//get first node
    var result_id = "";
    while (child_obj != null) {
        if (child_obj.className == "WCResult") {
            result_id = child_obj.id;
            break;
        }
        child_obj = child_boj.firstChild;

    }
    return result_id

}

function examining_message_ex(result_id, action_info) {
    var message = "check_state=1" + "\tresult=" + result_id;
    console.log(message);
    send_mouse_info(formInfo(action_info, message));
}

function examining_relevance_ex(result_id, score) {
    var message = "check_state=1" + "\tresult=" + result_id + '\tscore=' + score;
    console.log(message);
    send_mouse_info(formInfo("RELEVANCE", message));

}

function next_result() {
    checkList.push(resultList[resultList.length - 1]);
    $('#examineResult').html(ex_result_vec.get(resultList.pop()).cloneNode(true));
}

$(function () {
    $('.PanelExamButton').click(function () {
        if ($(this).attr('id') == 'examined') {
            if (resultList.length > 0) {
                tid = getResultID($('#examineResult').get(0));
                examining_message_ex(tid, "EXAMINE");
                $('#lzystardiv').css('visibility', 'visible');
                $('.PanelExamButton').css('visibility', 'hidden');
                $("#lzystar").raty({
                    number: 4,
                    click: function (score, evt) {
                        tid = getResultID($('#examineResult').get(0));
                        examining_relevance_ex(tid, score);
                        next_result()
                        $('#lzystardiv').css('visibility', 'hidden');
                        $('.PanelExamButton').css('visibility', 'visible');
                    }
                })

            }
            else {
                tid = getResultID($('#examineResult').get(0));
                examining_message_ex(tid, "EXAMINE");
                $('#lzystardiv').css('visibility', 'visible');
                $('.PanelExamButton').css('visibility', 'hidden');
                $("#lzystar").raty({
                    number: 4,
                    click: function (score, evt) {
                        examining_relevance_ex(tid, score);
                        $('#lzystardiv').css('visibility', 'hidden');
                        $('#myModal_ex').trigger('reveal:close');
                        $('#examineResult').empty();
                        display_examining_button();
                    }
                })

                console.log(clickList);
            }
        }

        if ($(this).attr('id') == 'notexamined') {
            checkList.pop();
            if (resultList.length > 0) {
                tid = getResultID($('#examineResult').get(0));
                if (clickList.indexOf(tid) >= 0) {
                    examining_message_ex(tid, "UNEXAMINE");
                    $('#lzystardiv').css('visibility', 'visible');
                    $('.PanelExamButton').css('visibility', 'hidden');
                    $("#lzystar").raty({
                        number: 4,
                        click: function (score, evt) {
                            examining_relevance_ex(tid, score);
                            next_result();
                            $('#lzystardiv').css('visibility', 'hidden');
                            $('.PanelExamButton').css('visibility', 'visible');
                        }
                    })
                }
                else {
                    next_result();
                }
            }
            else {
                tid = getResultID($('#examineResult').get(0));
                if (clickList.indexOf(tid) >= 0) {
                    examining_message_ex(tid, "UNEXAMINE");
                    $('#lzystardiv').css('visibility', 'visible');
                    $('.PanelExamButton').css('visibility', 'hidden');
                    $("#lzystar").raty({
                        number: 4,
                        click: function (score, evt) {
                            examining_relevance_ex(tid, score);
                        }
                    })
                }

                $('.PanelExamButton').css('visibility', 'hidden');
                $('#lzystardiv').css('visibility', 'hidden');
                $('#myModal_ex').trigger('reveal:close');
                $('#examineResult').empty();
                display_examining_button();


                console.log(clickList);
            }
        }


    });
});