let answer;
let date_mod = 0;
let c;
let active_li;
let c_list = [];
let el;
let uniq;
let refreshIntervalId = false;


let send = function (type_event) {
    active_li = $(this).closest('li');
    $('.loader').removeClass('hidden');
    $('.xpathes>*[data-xpath]').remove();
    $.ajax({
        url: 'http://localhost:5001/' + type_event,
        type: 'GET',
        contentType: 'application/json',
        success: function (data) {
            answer = JSON.parse(data);
            console.log(answer);
            for (let i in answer) {
                c = $('.xpathes .hidden').clone(true).removeClass('hidden');
                c.attr('data-xpath', answer[i]);
                c.find('.select').text(answer[i]);
                c.appendTo('.xpathes');
                c.on('click', function () {
                    let xpath = $(this).attr('data-xpath');
                    $('#xpath_active').val(xpath);
                });
            }
        },
        complete: function () {
            $('.loader').addClass('hidden');
        }
    });
};

let clear_cpanel = function () {
    $("#sortable").empty();
};
let copy_cpanel = function () {
    copyToClipboard($("#po").text());
};

let send_cpanel = function () {
    let data_send = [];
    $("#sortable>form").each(function (index) {
        data_send[index] = [$(this).attr('data-click'), $(this).serialize()];
    });
    console.log(data_send);
    $.ajax({
        url: '/po',
        type: 'POST',
        data: JSON.stringify(data_send),
        contentType: 'application/json',
        success: function (data) {
            let po = $("#po");
            po.html(data);
            $('#po').each(function (i, block) {
                hljs.highlightBlock(block);
            });
        }
    });
};

let send_click = function () {
    send('click')
};
let send_hover = function () {
    send('hover')
};
let send_several = function () {
    send('several')
};

let down_properties = function (id) {
    el = $('.cpanel *[data-id="' + id + '"]');
    get_from_db(el);
    let panel_body = el.find('.panel-body');
    let xpath = el.find('.xpath-input');

    let dropdown = el.find('.btn-dropdown');
    dropdown.off('click').on('click', function (event) {
        event.preventDefault();
        panel_body.toggleClass('hidden');
    });

    let clone = el.find('.btn-clone');
    clone.off('click').on('click', function (event) {
        event.preventDefault();
        uniq = 'id' + (new Date()).getTime();
        li = $(this).closest('#sortable>*');
        li.after(li.clone(true, true).attr('data-id', uniq));
        down_properties(uniq);
    });
    let search = el.find('.btn-search');
    search.off('click').on('click', function (event) {
        event.preventDefault();
        find_xpath(xpath.val())
    });
    let pointer = el.find('.btn-pointer');
    pointer.off('click').on('click', function (event) {
        event.preventDefault();
        xpath.val($('#xpath_active').val());
    });
    let database = el.find('.btn-database');
    database.off('click').on('click', function (event) {
        event.preventDefault();
        li = $(this).closest('#sortable>*');
        get_from_db(li);
    });
    let trash = el.find('.btn-trash');
    trash.off('click').on('click', function (event) {
        event.preventDefault();
        $(this).closest('#sortable>*').remove();
    });
};

let get_from_db = function (li) {
    $.ajax({
        url: 'http://localhost:5001/find_by_type/' + li.attr('data-click'),
        type: 'GET',
        contentType: 'application/json',
        success: function (data) {
            console.log(data);
            answer = JSON.parse(data);
            li.find('input[name="xpath"]').val(answer['xpath']);
            for (let key in answer['param']) {
                li.find('*[name=' + key + ']').val(answer['param'][key])
            }
        }
    });
};

let sortable = function () {
    $("#sortable").sortable({
        revert: true
    });
    $(".lpanel>*").draggable({
        connectToSortable: "#sortable",
        helper: function () {
            uniq = 'id' + (new Date()).getTime();
            c_list.push(uniq);
            return $(this).clone(true, true).attr('data-id', uniq);
        },
        revert: "invalid",
        stop: function () {
            down_properties(uniq);
        }
    });
};

let get_list = function () {
    $.ajax({
        url: '/list',
        type: 'GET',
        contentType: 'application/json',
        success: function (data) {
            answer = JSON.parse(data);
            console.log(answer);
            for (let i in answer) {
                c = $('*[data-click="' + answer[i] + '"]').clone(true, true).removeClass('hidden');
                if (c.length === 0) {
                    c = $('*[data-click="other"]').clone(true, true).removeClass('hidden');
                    c = c.removeClass('hidden');
                    c.attr('data-click', answer[i]);
                    c.find('.c-hidden, .btn-name').text(answer[i]);
                }
                c.appendTo('.lpanel');
            }
            sortable();
        }
    });
};

let get_log = function () {
    $.ajax({
        url: '/log/' + date_mod,
        type: 'GET',
        contentType: 'application/json',
        success: function (data) {
            answer = JSON.parse(data);
            date_mod = answer['date'];
            // console.log(answer);
            if (answer['log'] !== 0) {
                log = $("#log");
                log.html(function () {
                    return answer['log'];
                });
                log.scrollTop(log.prop('scrollHeight'));
            }
        }
    });
};

let submit = function (e) {
    let form = $('#run');
    e.preventDefault(); // avoid to execute the actual submit of the form.
    console.log(form.serialize());
    var url = "/"; // the script where you handle the form input.
    $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(), // serializes the form's elements.
        success: function (data) {
            console.log(data);
            // show response from the php script.
        }
    });

};

let log_sensor = function () {
    if (refreshIntervalId) {
        clearInterval(refreshIntervalId);
        refreshIntervalId = false;
        $('#log_sensor').css('background-color', 'red');
    } else {
        refreshIntervalId = setInterval(get_log, 1500);
        $('#log_sensor').css('background-color', 'green');
    }
};

let get_po = function () {
    let data = [];
    $('.cpanel>*[data-click]').each(function () {
        alert($(this));
    })
};

let add_to_sortable = function () {
    uniq = 'id' + (new Date()).getTime();
    c_list.push(uniq);
    $(this).clone().attr('data-id', uniq).appendTo('#sortable');
    down_properties(uniq);
};

let find_xpath = function (xpath) {
    $.ajax({
        type: "POST",
        url: 'http://localhost:5001/find_xpath',
        contentType: 'application/json',
        data: JSON.stringify({"xpath": xpath}), // serializes the form's elements.
        success: function (data) {
            console.log(data);
            // show response from the php script.
        }
    });
};