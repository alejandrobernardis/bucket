(function(){
	// window
	// ======

	var root = this;

	// underscore
	// ==========

	var _ = root._;
	if(!_) {throw new Error('require underscore');}

	// jQuery
	// ======

	var $ = root.$;
	if(!$) {throw new Error('require jQuery');}

	// Young
	// =====

	var Young = root.Young = {};
	Young.VERSION = 'v1.0.0-Beta';

	// Alert (bootstrap)
	// =================

	Young.Alert = function(args){
		this.init.apply(this, args || {});
	}

	_.extend(Young.Alert.prototype, {
		init: function(){},

		_element_name: '.js-alert',
		_element: function(){
			return $(this._element_name) || null;
		},

		_template: function(){
			var tmpl = '<div class="alert alert-block alert-{type}">'
				 	 + '<a class="close" data-dismiss="alert">×</a>'
				 	 + '<h4 class="alert-heading">{title}</h4>'
				 	 + '<p>{message}</p>'
				 	 + '</div>';
			return tmpl;
		},

		add: function(type, title, message){
			var el = this.remove();
			if(el){
				var errors = [title, message];
				for(var a in errors){
					var msn = '';
					var ref = errors[a];
					if(ref){
						if(typeof ref == 'object'){
							for(var b in ref){
								msn += '<strong>'
									+  $(".js_"+b).find('label').html()
									+  ':</strong> ' + ref[b] + '-  ';
							}
						}else{
							msn = ref;
						}
					} errors[a] = msn;
				} var msn = this._template()
							  	.replace('{type}', type||'error')
							  	.replace('{title}', errors[0])
							  	.replace('{message}', errors[1]);
				el.append(msn).show();
				if(type == 'success'){
					el.delay(1500).fadeOut(400);
				}
			}
		},

		add_warn: function(title, message){
			this.add('warn', title || 'WARNING!', message);
		},

		add_error: function(title, message){
			this.add('error', title || 'ERROR!', message);
		},

		add_success: function(title, message){
			this.add('success', title || 'SUCCESS!', message);
		},

		add_info: function(title, message){
			this.add('info', title || 'INFORMATION!', message);
		},

		remove: function(){
			try{
				var el = this._element();
				el.empty();
				el.hide();
				return el;
			}catch(e){
				return null;
			}
		},
	});

	// Server
	// ======

	Young.Server = function(args){
		this.init.apply(this, args || {});
	}

	_.extend(Young.Server.prototype, {
		init: function(){},

		get_cookie: function(value){
			var result = document.cookie.match('\\b' + value + '=([^;]*)\\b');
			return result ? result[1] : undefined;
		},

		simple_get: function(url, args, callback){
			args = args || {};
			$.ajax({
				url: url,
				data: $.param(args),
				dataType: 'text',
				type: 'GET',
				success: function(response){
					if(response){
						var json = eval('('+response+')');
						if(json.error.id == 0){
							if(typeof callback == 'function'){
								callback(json);
							}else{
								var url = new String('');
								try{
									url = json.response.next;
								}catch(e){
									url = $.url().param('next');
								}if(url.match(/.+/ig)){
									location.href = unescape(url);
								}
							}
						}else{
							alert(json.error.message);
						}
					}else{}
				}, error: function(response){}
			});
		},

		simple_post: function(url, args, callback){
			args = args || {};
			args._xsrf = this.get_cookie('_xsrf');
			$.ajax({
				url: url,
				data: $.param(args),
				dataType: 'text',
				type: 'POST',
				success: function(response){
					if(response){
						var json = eval('('+response+')');
						if(json.error.id == 0){
							if(typeof callback == 'function'){
								callback(json);
							}else{
								var url = new String('');
								try{
									url = json.response.next;
								}catch(e){
									url = $.url().param('next');
								}if(url.match(/.+/ig)){
									location.href = unescape(url);
								}
							}
						}else{
							alert(json.error.message);
						}
					}else{
						alert("Se produjo un error no controlado.");
					}
				}, error: function(response){
					alert("Se produjo un error no controlado.");
				}
			});
		},

		post: function(url, args, callback){
			var alert = new Young.Alert();
			alert.add_info('Please, wait...');
			args = args || {};
			args._xsrf = this.get_cookie('_xsrf');
			$.ajax({
				url: url,
				data: $.param(args),
				dataType: 'text',
				type: 'POST',
				success: function(response){
					if(response){
						alert.remove();
						var json = eval('('+response+')');
						if(json.error.id == 0){
							if(typeof callback == 'function'){
								callback(json);
							}else{
								var url = new String('');
								try{
									url = json.response.next;
								}catch(e){url = $.url().param('next');}
								if(url.length && url.match(/.+/ig)){
									location.href = unescape(url);
								}
							} alert.add_success(undefined, json.error.message);
						}else{
							alert.add_error(undefined, json.error.message);
						}
					}else{
						alert.add_error('CRITICAL');
					}
				},
				error: function(response){
					alert.add_error('FATAL');
				}
			});
		},

	});

}).call(this);