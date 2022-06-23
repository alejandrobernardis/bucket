
var form_html_template = '<form action="" method="post" data-action="{token}-answer"><fieldset>'
    + '<h4>Comentario:</h4>'
    + '<p>{description}</p>'
    + '<p><small class="text-muted"><span class="fa fa-user"></span> {username}, {created}</small></p>'
    + '</fieldset><hr><fieldset><h5>{title}</h5>'
    + '<div class="form-group"><textarea id="{token}-arg-answer" class="form-control" required="1" name="answer" rows="5" onkeyup="check_form_chars(this);"></textarea>'
    + '<small id="form-answer-counter" class="help-block"></small>'
    + '<input id="{token}-arg-mode" type="hidden" name="mode" value="{mode}"/>'
    + '</div></fieldset></form>';

var answer_html_template = '<tr data-token="{token}-thread" class="warning">'
    + '<td class="text-center">&nbsp;</td><td class="text-center">'
    + '<p><span class="fa fa-2x {mode} text-default"></span></p>'
    + '<p><strong><a href="/a/evaluations?q={username}" class="answer-username">@{username}</a></strong></p>'
    + '<p class="items-list-date answer-date">{created}</p>'
    + '</td><td class="answer-description"><small>'
    + '<span class="fa fa-user">&nbsp;{full_name}</span>&nbsp;'
    + '</small><hr class="items-list-hr"><p>{description}</p></td></tr>';

var str_send_email_title = 'Responder vía email',
    str_call_user_title = 'Confirmar llamada telefónica con el cliente',
    str_wait = 'Aguarde, por favor...';

var session_id = 'asi',
    services = {
        'change-status': {url: '/s/evaluation/change/status', mode: 'ajax'},
        'send-email': {
            url: '/s/evaluation/answer/message',
            mode: 'form',
            content: set_form_content('Respuesta:', 1),
            validate: set_form_validate({mode: 1}),
            title: str_send_email_title
        },
        'call': {
            url: '/s/evaluation/answer/call',
            mode: 'form',
            content: set_form_content('Minuta de la charla:', 2),
            validate: set_form_validate({mode: 2}),
            title: str_call_user_title
        }
    };

function get_form_template(ref, token, title, mode) {
    return form_html_template
        .replace(/\{description\}/gi, ref.description.replace('\n', '</p><p>'))
        .replace(/\{username\}/gi, ref.client)
        .replace(/\{created\}/gi, new Date(ref.created.$date).toLocaleString())
        .replace(/\{title\}/gi, title)
        .replace(/\{mode\}/gi, mode)
        .replace(/\{token\}/gi, token);
}

function set_form_content(title, mode) {
    return function(token) {
        var a, ref;
        for(a=0; a < window.evaluations.length; a++) {
            ref = window.evaluations[a];
            try {
                if(ref._id.$oid == token){
                    return get_form_template(ref, token, title, mode);
                }
            } catch(e) {}
        } return false;
    }
}

function set_form_validate(args) {
    return function(config) {
        var error = {data: {error: {id: -1, message: false}}},
            answer = $("#"+config.token+"-arg-answer").val();
        if (answer.length < 10)
            error.data.error.message = 'Por favor, escriba un comentario más detallado.';
        else if (answer.length > 500)
            error.data.error.message = 'El comentarios ha superado el limite de 500 caracteres.';
        if(!error.data.error.message){
            try {args.answer = answer;} catch (e) {args = {answer: answer};}
            return args;
        }
        default_fail(error, {from: "top", align: "center"});
        return false;
    };
}

function check_form_chars(ref) {
    var _txt, _txt_tmpl, _txt_counter, _chars;
    _chars = ref.value.length;
    _txt_tmpl = '&nbsp; // &nbsp;<span class="fa fa-exclamation-triangle text-warning">&nbsp;{text}</span>'
    _txt_counter = 'Caracteres disponibles: ' + String(500 - _chars);
    if (_chars < 10)
        _txt = 'El mínimo requerido es de 10 caracteres.';
    else if (_chars > 500)
        _txt = 'Se ha exedido del límite de 500 caracteres.';
    else
        _txt = '';
    if (_txt.length)
        _txt = _txt_tmpl.replace('{text}', _txt);
    $('#form-answer-counter').html(_txt_counter + _txt);
}

function change_status_done(r) {
    var add_icon, remove_icon, add_style, remove_style;
    if (r.data.response.status) {
        add_icon = 'fa-check'; remove_icon = 'fa-times';
        add_style = 'btn-success'; remove_style = 'btn-danger';
        $('#'+ r.data.response.token+'-actions').show();
    } else {
        add_icon = 'fa-times'; remove_icon = 'fa-check';
        add_style = 'btn-danger'; remove_style = 'btn-success';
        $('#'+ r.data.response.token+'-actions').hide();
    }
    r.ref.children('span').removeClass(remove_icon).addClass(add_icon);
    r.ref.removeClass(remove_style).addClass(add_style);
    default_done(r);
}

function get_image_by_mode(mode){
    try {
        return {1: 'fa-envelope', 2: 'fa-phone'}[mode] || 'fa-question-circle';
    } catch (e){
        return 'fa-question-circle';
    }
}

function send_email_done(r) {
    var response = r.data.response,
        data = response.answer;
    var html = answer_html_template
        .replace(/\{token\}/gi, response.token)
        .replace(/\{mode\}/gi, get_image_by_mode(data.mode))
        .replace(/\{username\}/gi, data.username)
        .replace(/\{created\}/gi, data.created)
        .replace(/\{description\}/gi, remove_html_tags(data.description).replace(/\n/gi, '</p><p>'))
        .replace(/\{full_name\}/gi, data.full_name);
    $('#'+ response.token).after(html);
    $('#'+ response.token+'-actions').remove();
    r.ref.close();
    default_done(r);
}

var call_done = send_email_done;

function send_email_fail(r) {
    r.ref.enableButtons(true);
    r.ref.setClosable(true);
    r.ref.getModalBody().html('<p><span class="fa fa-exclamation-circle"></span>&nbsp;'+r.data.error.message+'</p>');
    default_fail(r);
}

var call_fail = send_email_fail;

$(function(){
    var engine = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('full_name'),
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        remote: '/a/users/autocomplete?q=%QUERY'
    });
    
    engine.initialize();
    
    $('#search-input .typeahead').typeahead({
            minLength: 3,
            highlight: false
        }, {
            name: 'search-input',
            displayKey: 'username', 
            source: engine.ttAdapter(),
            templates: {
                suggestion: Handlebars.compile(
                    '<p><strong>{{first_name}} {{last_name}}</strong>&nbsp;<br>'
                  + '<small class=""><span class="fa fa-briefcase"></span>&nbsp;{{company}}&nbsp;&nbsp;'
                  + '<span class="fa fa-user"></span>&nbsp;@{{username}}</small></p>')
            }
    });
    
    $('.js-button').bind('click', function(e) {
        session_available();
        var args, dialog, ref = $(this),
            settings = services[ref.attr('data-action')],
            config = {
                action: ref.attr('data-action'),
                token: ref.attr('data-token'),
                settings: settings
            };
        switch (settings.mode){
            case 'ajax':
                config.ladda = Ladda.create(this);
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
});