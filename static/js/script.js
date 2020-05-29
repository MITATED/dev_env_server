$(function () {
    // get_list();
    sortable();
    $("#run").submit(submit);
    $("#log").on('click', log_sensor);

    $('.xpathes li').on('click', function () {
        var xpath = $(this).attr('data-xpath');
        $(active_li).find('input').val(xpath);
    });
    $('#search_click').on('click', send_click);
    $('#search_hover').on('click', send_hover);
    $('#search_several').on('click', send_several);

    $('label:has(#clear_cpanel)').on('click', clear_cpanel);
    $('label:has(#send_cpanel)').on('click', send_cpanel);
    $('label:has(#copy_cpanel)').on('click', copy_cpanel);

    $('.lpanel .list-group-item').on('click', add_to_sortable);

    $('#find_xpath').on('click', function () {
        find_xpath($('#xpath_active').val())
    });
    setTimeout(5000, get_po);

});