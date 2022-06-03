
var str_delete_user = '¿Está seguro que desea borrar al usuario?',
    str_delete_user_title = 'Confirmar la Eliminación de Usuario',
    str_change_password = 'Al confirmar la operación, el usuario recibirá en su correo las instrucciones necesarias para realizar el cambio de la contraseña.',
    str_change_password_title = 'Confirmar el Cambio de Contraseña de Usuario',
    str_view_activity_title = 'Visualización de Actividad',
    str_register_allow = 'Al confirmar la operación, el usuario recibirá en su correo las instrucciones y datos necesarios para poder acceder al sistema.',
    str_register_allow_title = 'Confirmar la Activación del Registro',
    str_register_deny = '¿Está seguro que desea eliminar el registro?',
    str_register_deny_title = 'Confirmar la Eliminación del Registro',
    str_wait = 'Aguarde, por favor...';


var session_id = 'asi',
    services = {
        'change-status': {url: '/s/user/change/status', mode: 'ajax'},
        'change-level': {url: '/s/user/change/level', mode: 'ajax'},
        'view-activity': {
            url: '/s/user/view/activity',
            mode: 'modal',
            title: str_view_activity_title
        },
        'change-password': {
            url: '/s/user/change/password',
            mode: 'confirm',
            message: str_change_password,
            title: str_change_password_title
        },
        'delete': {
            url: '/s/user/delete',
            mode: 'confirm',
            message: str_delete_user,
            title: str_delete_user_title
        },
        'register-allow': {
            url: '/s/register/allow',
            mode: 'confirm',
            message: str_register_allow,
            title: str_register_allow_title
        },
        'register-deny': {
            url: '/s/register/deny',
            mode: 'confirm',
            message: str_register_deny,
            title: str_register_deny_title
        }
    };

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
        throw new Error(
            'El handler "'+ handler + '" no esta definido para la acción "' + action + '"'
        );
    } return fnc;
}

// -----------------------------------------------------------------------------

function change_status_done(r) {
    var add_icon, remove_icon, add_style, remove_style;
    if (r.data.response.status) {
        add_icon = 'fa-check'; remove_icon = 'fa-times';
        add_style = 'btn-success'; remove_style = 'btn-danger';
    } else {
        add_icon = 'fa-times'; remove_icon = 'fa-check';
        add_style = 'btn-danger'; remove_style = 'btn-success';
    }
    r.ref.children('span').removeClass(remove_icon).addClass(add_icon);
    r.ref.removeClass(remove_style).addClass(add_style);
    default_done(r);
}

function change_level_done(r) {
    r.ref.closest('ul').children('.active').removeClass('active');
    r.ref.closest('li').addClass('active');
    r.ref.closest('.btn-group').find('[data-bind="label"]').text(r.ref.text());
    default_done(r);
}

function change_password_done(r) {
    r.ref.close();
    default_done(r);
}

function view_activity_done(r) {
    var item, line, session, activity, message, lines = '';
    for(data_item in r.data.response){
        item = eval('(' + r.data.response[data_item] + ')');
        if(!session || session != item.session) {
            session = item.session;
            lines += '\n<strong class="text-primary">Session: {sid}</strong>\n'
                     .replace('{sid}', item.session);
        }
        line  = '<span class="">[{date}] {ip} </span>'
              + '<span class="text-success">{activity}</span> '
              + '<span class="text-warning">{message}</span>\n';
        activity = item.activity;
        activity = (activity.match(/^\/$/g)) ? 'search' : activity.replace(/^\//, '').replace(/\//g, ' ');
        message = item.message.replace(/./g,function(chr, index){return chr.match(/[\w\d]/) ? chr : "&#"+chr.charCodeAt(0)+";" ;});
        lines += line.replace('{date}', new Date(item.created.$date))
                .replace('{ip}', item.remote_ip)
                .replace('{activity}', activity)
                .replace('{message}', message);
    }
    r.ref.enableButtons(true);
    r.ref.setClosable(true);
    r.ref.getModalBody().html('<pre style="font-size:11px;">'+lines+'</pre>');
    r.ref.getModalDialog().css('width', '90%');
    default_done(r);
}

function delete_done(r) {
    r.ref.close();
    default_done(r);
    setTimeout(function(){window.location.reload();}, 500);
}

var register_allow_done = delete_done;
var register_deny_done = delete_done;

function delete_fail(r) {
    r.ref.enableButtons(true);
    r.ref.setClosable(true);
    r.ref.getModalBody().html('<p><span class="fa fa-exclamation-circle"></span>&nbsp;'+r.data.error.message+'</p>');
    default_fail(r);
}

var change_password_fail = delete_fail;
var view_activity_fail = delete_fail;
var register_allow_fail = delete_fail;
var register_deny_fail = delete_fail;

// -----------------------------------------------------------------------------

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

function default_fail(r) {
    $.growl({
        message: r.data.error.message,
        title: ' ',
        icon: 'fa fa-bell'
    }, {
        type: 'danger',
        position: {
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
            if(data.error.id != 0) {
                throw new Error('');
            }
            return get_handler_action('done', config.action)(args);
        }catch(e){
            if(!args.data.error.message && e){
                args.data.error.message = e.toString()
            }
            try{
                return get_handler_action('fail', config.action)(args);
            }catch (e){
                default_fail(args);
            }
        }
    });

    ajax.fail(function(data){
        try{config.ladda.stop();}catch (e){}
        var args = {
            ref: ref, data: {
                error: {
                    id: -1,
                    message: data.statusText
                }
            }
        };
        try{
            return get_handler_action('fail', config.action)(args);
        }catch (e){
            default_fail(args);
        }
    });

}

$(function(){
    $('.js-button').bind('click', function(e) {
        session_available();
        var ref = $(this),
            settings = services[ref.attr('data-action')],
            config = {
                action: ref.attr('data-action'),
                token: ref.attr('data-token'),
                settings: settings
            };
        switch (settings.mode){
            case 'ajax':
                if(config.action == 'change-level'){
                    if(ref.parent().hasClass('active')){
                        return;
                    }else{
                        config.ladda = Ladda.create(this.parentNode.parentNode.parentNode.querySelector('.js-button-drop'));
                        config.args = {level: ref.text().toLowerCase()};
                    }
                }else{
                    config.ladda = Ladda.create(this);
                }
                return simple_post(ref, config);
            case 'modal':
                if(config.action == 'view-activity'){
                    config.args = {username: ref.attr('data-username')};
                }
                var dialog = new BootstrapDialog({
                    title: settings.title || 'Visualización',
                    message: str_wait,
                    closable: false
                });
                dialog.realize();
                dialog.getModalFooter().hide();
                dialog.open();
                return simple_post(dialog, config);
            case 'confirm':
                return BootstrapDialog.show({
                    title: settings.title || 'Confirmar Operación',
                    message: settings.message,
                    type: BootstrapDialog.TYPE_WARNING,
                    buttons: [{
                        icon: 'fa fa-check',
                        label: ' Confirmar',
                        cssClass: 'btn-danger',
                        action: function(dref){
                            dref.enableButtons(false);
                            dref.setClosable(false);
                            dref.getModalBody().html(str_wait);
                            simple_post(dref, config);
                        }
                    }, {
                        label: 'Cancelar',
                        action: function(dref){
                            dref.close();
                        }
                    }]
                });
        }
    });
    if(window.paginator){
        $('.js-paginator').twbsPagination({
            first: 'Primero',
            prev: 'Anterior',
            next: 'Siguiente',
            last: 'Último',
            visiblePages: 5,
            startPage: parseInt(window.paginator.page_number),
            totalPages: parseInt(window.paginator.page_total),
            href: '/a/users?page={}',
            hrefVariable: '{}'
        });
    }
});