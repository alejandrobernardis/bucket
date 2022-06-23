
package pq.log.appenders {
	
	import com.emc2zen.util.ClassUtil;
	import flash.errors.IllegalOperationError;
	import flash.external.ExternalInterface;
	import flash.utils.describeType;
	import pq.api.IAppender;
	import pq.log.Appender;
	import pq.log.Level;
	import pq.utils.StringUtil;
	import pq.utils.TypeUtil;
	
	public class FirebugAppender implements IAppender {
		
		private var _appender:Appender;
		private var _console:String;
		private var _method:String = "function(message){try{console.{1}(message);}catch(e){}}";
		
		public function FirebugAppender() {
		
		}
		
		public function send( value:Appender ):void {
			
			this._appender = value;
			this._console = getMethod( value.level );
			
			if ( TypeUtil.firebugAvailable() ) {
				this.group( this.template( "" ) );
				serialize( this._appender.message );
				this.group();
			} else {
				trace( 
					this.template( 
						"Firebug is not avaible.", 
						Level.FATAL, 
						this 
					) 
				);
			}
			
			this._appender = null;
			this._console = null;
			
		}
		
		public function serialize( value:*, depth:uint = 0, ...rest ):String {
			
			if ( this._appender == null ) {
				return null;
			}
			
			var maxdepth:uint = 255;
			
			if ( depth <= maxdepth ) {
				
				var list:XMLList;
				var pattern:String = "[{1}] {2}\"{3}\"";
				var id:String = ( rest[0] != null ) ? ( rest[0] + " = " ) : "";
				
				var description:XML = describeType( value );
				var type:String = description.@name;
				
				if ( TypeUtil.isLiteralPrimitive( type ) || value is Date ) {
					ExternalInterface.call (
						this._console,
						StringUtil.substitute( pattern, type, id, value )
					);
				}else if ( type.search( /^XML/ ) > -1 )  {
					ExternalInterface.call (
						this._console,
						this._appender.message.toString()
					);
				} else if ( TypeUtil.isLiteralCollection( type ) ) {
					this.group( type );
					for ( var element:String in value ) {
						this.ResolveValue( element, value, depth );
					}
					this.group();
				} else {
					this.group( type );
					list = describeType(value)..accessor.( @access != "writeonly" );					
					for each ( var node:XML in list ) {
						if ( node.@declaredBy.search( /^(flash)[\.](display|(text\:\:TextField)|(media\:\:Video))/ ) == -1 ) {
							this.ResolveValue( node.@name, value, depth );
						}
					}
					this.group();
				}
				
			}
			
			return "Output in Firebug.";
			
		}
		
		public function toString():String {
			
			return ClassUtil.shortName( this ); 
			
		}
		
		private function template( message:String, level:Level = null, context:* = null ):String {
			
			var pattern:String = "{1} [{2}] {3} {4}";
			
			if ( level == null ) {
				level = this._appender.level;
			}
			
			if ( context == null ) {
				context = this._appender.context;
			}
			
			return StringUtil.substitute(
				pattern,
				new Date(),
				level.label.toUpperCase(),
				ClassUtil.fullName( context ),
				message
			);
			
		}
		
		private function ResolveValue( element:*, value:*, depth:uint ):void {
			
			try {
				value = value[ element ];
			}catch (e:Error){
				value = "{Exception: " + e.message + "}";
			}
			
			serialize( value, ( depth + 1 ), element );
			
		}
		
		private function group( value:* = null ):void {			
			if ( value != null ) {
				ExternalInterface.call( "console.group", value );		
			} else {				
				ExternalInterface.call( "console.groupEnd" );	
			}
		}
		
		private function getMethod( value:Level ):String {
			
			switch( value ) {
				
				case Level.ALL:
					return StringUtil.substitute( this._method, "log" );
				
				case Level.DEBUG: 
				case Level.INFO:
				case Level.WARN:
					return StringUtil.substitute( this._method, value.label );
				
				case Level.ERROR:
				case Level.CRITICAL:
				case Level.FATAL:
					return StringUtil.substitute( this._method, Level.ERROR.label );
				
				case Level.OFF: 
				default:
					return new String();
				
			}
			
		}
		
	}
	
}