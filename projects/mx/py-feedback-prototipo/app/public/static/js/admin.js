
var str_delete_user = '¿Está seguro que desea borrar al usuario?',
    str_delete_user_title = 'Confirmar eliminación de usuario',
    str_change_password = 'Al confirmar la operación, el usuario recibirá en su correo las instrucciones necesarias para realizar el cambio de la contraseña.',
    str_change_password_title = 'Confirmar cambio de contraseña de usuario',
    str_view_activity_title = 'Visualización de Actividad',
    str_register_allow = 'Al confirmar la operación, el usuario recibirá en su correo las instrucciones y datos necesarios para poder acceder al sistema.',
    str_register_allow_title = 'Confirmar activación de registro',
    str_register_deny = '¿Está seguro que desea eliminar el registro?',
    str_register_deny_title = 'Confirmar eliminación de registro',
    str_evaluation_send = '¿Está seguro que desea enviar la evaluación?',
    str_evaluation_send_title = 'Confirmar envío de evaluación',
    str_wait = 'Aguarde, por favor...';

var form_html_executives = '<form action="" method="post" id="{token}-executives"><fieldset><p>'
    + 'Seleccione las personas involucradas con el cliente:</p><hr>'
    + '{checkbox_list}</fieldset></form>';

var form_html_executives_list = '<div class="checkbox"><label>'
    + '<input type="checkbox" value="{id}" {checked}><strong>{first_name} {last_name}</strong>&nbsp;'
    + '<br><small>{email}</small>'
    + '<br><small class="text-muted"><span class="fa fa-briefcase"></span>&nbsp;{company}</small>&nbsp;&nbsp;'
    + '<small class="text-muted"><span class="fa fa-user"></span>&nbsp;{username}</small>&nbsp;&nbsp;'
    + '</label></div>';

var session_id = 'asi',
    services = {
        'change-status': {
            url: '/s/user/change/status',
            mode: 'ajax'
        },
        'change-level': {
            url: '/s/user/change/level',
            mode: 'ajax'
        },
        'change-dispatch': {
            url: '/s/user/change/dispatch',
            mode: 'ajax'
        },
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
        'list-executives': {
            url: '/s/user/list/executives',
            mode: 'ajax'
        },
        'change-executives': {
            url: '/s/user/change/executives',
            content: function(token){
                var executive, oid, ref, a, b, list = '';
                for(a = 0; a < window.users.length; a++) {
                    ref = window.users[a];
                    try {if(ref._id.$oid == token) break;} catch(e) {}
                }
                function check_relationship(value){
                    for(b = 0; b < ref.executives.length; b++) {
                        try {if(ref.executives[b] == value) {return 'checked';}} catch(e) {}
                    } return '';
                }
                for(a = 0; a < window.executives.length; a++) {
                    executive = window.executives[a];
                    oid = executive._id.$oid;
                    list += form_html_executives_list
                        .replace(/\{id\}/gi, oid)
                        .replace(/\{checked\}/gi, check_relationship(oid))
                        .replace(/\{first_name\}/gi, executive.first_name)
                        .replace(/\{last_name\}/gi, executive.last_name)
                        .replace(/\{company\}/gi, executive.company)
                        .replace(/\{username\}/gi, executive.username)
                        .replace(/\{email\}/gi, executive.email);
                }
                return form_html_executives
                    .replace('{checkbox_list}', list)
                    .replace('{token}', token);
            },
            validate: function(config){
                var a, item, result = [],
                    form = $("#"+config.token+"-executives"),
                    executives_list = form.find('input[type=checkbox]');
                for(a=0; a<executives_list.length; a++){
                    item = $(executives_list[a])
                    if(item.is(':checked')){
                        result.push(item.val())
                    }
                }
                return {executives: result};
            },
            mode: 'form',
            title: 'Asignación de ejecutivos'
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
        },
        'send-evaluation': {
            url: '/s/evaluation/send',
            mode: 'confirm',
            message: str_evaluation_send,
            title: str_evaluation_send_title
        }
    };

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

var change_dispatch_done = change_level_done;

function change_password_done(r) {
    r.ref.close();
    default_done(r);
}

function send_evaluation_done(r) {
    default_done(r);
    var tmpl = '<p>El identificador de la evaluci&oacute;n es <strong class="label label-default">{key}</strong> y expira el <strong class="label label-default">{expires}</strong></p>'
             + '<hr><p><a href="/p/evaluation/verify/{url}" target="_blank" class="btn btn-block btn-danger"><span class="fa fa-exclamation-triangle"></span>&nbsp;VERIFICACI&Oacute;N DE URL, NO REALIZAR LA EVALUACI&Oacute;N</a></p>';
    r.ref.enableButtons(true);
    r.ref.setClosable(true);
    r.ref.setTitle('Datos de la evaluación');
    r.ref.getModalFooter().hide();
    r.ref.getModalBody().html(
        tmpl.replace('{key}', r.data.response.key)
            .replace('{expires}', r.data.response.expires)
            .replace(/\{url\}/gi, r.data.response.public)
    );
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
    r.ref.getModalBody().html('<pre style="font-size: 11px;">'+lines+'</pre>');
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

function list_executives_done(r){
    window.executives = r.data.response;
    var ref = $(r.ref[0]);
    ref.attr('data-action', 'change-executives');
    ref.trigger('click');
    ref.attr('data-action', 'list-executives');
    default_done(r);
}

function change_executives_done(r){
    var ref, a, token = r.data.response.token, list = r.data.response.executives;
    for(a = 0; a < window.users.length; a++) {
        ref = window.users[a];
        try {
            if(ref._id.$oid == token){ ref.executives = list; break; }
        } catch(e) {}
    }
    r.ref.close();
    default_done(r);
}

function delete_fail(r) {
    r.ref.enableButtons(true);
    r.ref.setClosable(true);
    r.ref.getModalBody().html('<p><span class="fa fa-exclamation-circle"></span>&nbsp;'+r.data.error.message+'</p>');
    default_fail(r);
}

var view_activity_fail = delete_fail;
var register_allow_fail = delete_fail;
var register_deny_fail = delete_fail;
var change_password_fail = delete_fail;
var change_executives_fail = delete_fail;

$(function(){
    $('.js-button').bind('click', function(e) {
        e.preventDefault();
        session_available();
        var dialog, args, ref = $(this),
            settings = services[ref.attr('data-action')],
            config = {
                action: ref.attr('data-action'),
                token: ref.attr('data-token'),
                settings: settings
            };
        switch (settings.mode){
            case 'ajax':
                if(config.action == 'change-level' || config.action == 'change-dispatch'){
                    if(ref.parent().hasClass('active')){
                        return;
                    }else{
                        config.ladda = Ladda.create(
                            this.parentNode.parentNode.parentNode.querySelector('.js-button-drop')
                        );
                        config.args = {level: ref.text().toLowerCase()};
                    }
                }else{
                    config.ladda = Ladda.create(this);
                }
                return simple_post(ref, config);
            case 'form':
                dialog = new BootstrapDialog({
                    title: settings.title || 'Formulario',
                    message: $(settings.content(config.token)),
                    closable: true,
                    buttons: [{
                        icon: 'fa fa-check',
                        label: ' Enviar',
                        cssClass: 'btn-primary',
                        action: function(dref){
                            args = settings.validate(config);
                            if(args) {
                                dref.enableButtons(false);
                                dref.setClosable(false);
                                dref.getModalBody().html(str_wait);
                                config.args = args;
                                simple_post(dref, config);
                            }
                        }
                    }, {
                        label: 'Cancelar',
                        action: function(dref){
                            dref.close();
                        }
                    }]
                });
                dialog.realize();
                return dialog.open();
            case 'modal':
                if(config.action == 'view-activity'){
                    config.args = {username: ref.attr('data-username')};
                }
                dialog = new BootstrapDialog({
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
                    type: BootstrapDialog.TYPE_DANGER,
                    buttons: [{
                        icon: 'fa fa-check',
                        label: 'Confirmar',
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
});