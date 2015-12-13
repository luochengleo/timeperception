var resultList = [];
var checkList = [];
ex_result_vec = null;

interval = 0;

$(function () {
    wc_result_vec = $('.WCResult');
    wc_resultLayout_vec = $('.resultLayout');
    wc_buttonLayout_vec = $('.buttonLayout');
    console.log(wc_resultLayout_vec);
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

function ex_init() {
    ex_reveal();
    if (resultList.length > 0) {
        resultList = [];
    }
    ex_result_vec = $('.WCResult');
    for (var i = 0; i < ex_result_vec.length; i++) {
        resultList.push(i);
    }
    resultList.sort(randomSort);
    resultDisplayList = resultList.join(" ");
    resultList = resultList.reverse();
    checkList.push(resultList[resultList.length - 1]);
    $('#examineResult').html(ex_result_vec.get(resultList.pop()).cloneNode(true));
    return resultDisplayList;
}

function getCheckList() {
    return checkList;
}

function examining_message_ex(exam_button_obj) {
    //exam_button_obj.disabled=true;
    var child_obj = exam_button_obj.firstChild;//get first node
    while (child_obj != null) {
        //alert(parent_obj.className);
        if (child_obj.className == "WCResult") {
            var message = "check_state=1" + "\tresult=" + child_obj.id;
            send_mouse_info(formInfo("EXAMINE", message));
            //alert(message);
            break;
        }
        child_obj = child_obj.firstChild;
    }
}

$(function () {
    $('.PanelExamButton').click(function () {
        if ($(this).attr('id') == 'examined') {
            if (resultList.length > 0) {
                examining_message_ex($('#examineResult').get(0));
                checkList.push(resultList[resultList.length - 1]);
                $('#examineResult').html(ex_result_vec.get(resultList.pop()).cloneNode(true));
            }
            else {
                examining_message_ex($('#examineResult').get(0));
                $('#myModal_ex').trigger('reveal:close');
                $('#examineResult').empty();
                display_examining_button();
            }
        }

        if ($(this).attr('id') == 'notexamined') {
            if (resultList.length > 0) {
                checkList.pop();
                checkList.push(resultList[resultList.length - 1]);
                $('#examineResult').html(ex_result_vec.get(resultList.pop()).cloneNode(true));
            }
            else {
                checkList.pop();
                $('#myModal_ex').trigger('reveal:close');
                $('#examineResult').empty();
                display_examining_button();
            }
        }


    });
});