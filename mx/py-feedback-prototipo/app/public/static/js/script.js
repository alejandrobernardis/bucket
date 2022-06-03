function session_cookies(key) {
    var value = document.cookie.match("\\b"+key+"=([^;]*)\\b");
    return value ? value[1] : undefined;
}

function session_available(not_redirect) {
    var status = (session_cookies(session_id) != undefined);
    if(! status && ! not_redirect){
        window.location.reload();
    } return status;
}

function get_handler_action(handler, action) {
    var fnc = window[
        '{action}_{handler}'
            .replace(/\{action\}/i, action.replace('-', '_'))
                .replace(/\{handler\}/i, handler.replace('-', '_'))
    ];
    if(!fnc) {
        throw new Error('El handler "' + handler + '" no esta definido para la acción "' + action + '"');
    } return fnc;
}

function remove_html_tags(value){
    return value.replace(/./g, function(chr, index){
        return chr.match(/[\w\d]/)
            ? chr : "&#"+chr.charCodeAt(0)+";" ;
    });
}

function default_done(r) {
    var message = (! r.data.error.message || r.data.error.message.toLowerCase() == 'success')
        ? 'El proceso finalizó correctamente.' : r.data.error.message;
    $.growl({
        message: message,
        title: ' ',
        icon: 'fa fa-bell'
    }, {
        type: 'success',
        position: {
            from: "bottom",
            align: "right"
        }
    });
}

function default_fail(r, position) {
	try{r.ref.close();}catch(e){}
    $.growl({
        message: r.data.error.message,
        title: ' ',
        icon: 'fa fa-bell'
    }, {
        type: 'danger',
        z_index: 2050,
        position: position || {
            from: "bottom",
            align: "right"
        }
    });
}

function simple_post(ref, config) {
    session_available();

    var args = config.args || {};
    args._xsrf = session_cookies('_xsrf');

    var ajax = $.ajax({
        url: config.settings.url + '/' + config.token,
        method: 'POST',
        data: $.param(args),
        beforeSend: function(xhr){
            try{config.ladda.start();}catch(e){}
        }
    });

    ajax.done(function(data){
        try{config.ladda.stop();}catch(e){}
        args = {ref: ref, data: data};
        try{
            if(data.error.id != 0) {throw new Error('');}
            return get_handler_action('done', config.action)(args);
        }catch(e){
            if(!args.data.error.message && e){args.data.error.message = e.toString()}
            try{return get_handler_action('fail', config.action)(args);}catch (e){default_fail(args);}
        }
    });

    ajax.fail(function(data){
        try{config.ladda.stop();}catch (e){}
        var args = {ref: ref, data: {error: {id: -1, message: data.statusText}}};
        try{
            return get_handler_action('fail', config.action)(args);
        }catch (e){
            default_fail(args);
        }
    });

}

$(function(){
    var offset = 220, duration = 500, back_to_top =  $('.back-to-top');

    $(window).scroll(function() {
        if ($(this).scrollTop() > offset) {
            back_to_top.fadeIn(duration);
        } else {
            back_to_top.fadeOut(duration);
        }
    });

    back_to_top.click(function(event) {
        event.preventDefault();
        $('html, body').animate({scrollTop: 0}, duration);
        return false;
    });

    if(window.paginator){
        var q = $('#q').val(), q_href = window.location.pathname + '?page={}' + (q.length ? '&q=' + q : '');
        $('.js-paginator').twbsPagination({
            first: 'Primero',
            prev: 'Anterior',
            next: 'Siguiente',
            last: 'Último',
            visiblePages: 5,
            startPage: parseInt(window.paginator.page_number),
            totalPages: parseInt(window.paginator.page_total),
            href: q_href,
            hrefVariable: '{}'
        });
    }
});