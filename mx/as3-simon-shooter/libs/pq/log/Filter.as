
package pq.log {
	
	import com.emc2zen.util.ClassUtil;
	import flash.errors.IllegalOperationError;
	import pq.utils.StringUtil;
	
	public class Filter extends Layout {
		
		public static const DEFAULT_SEPARATOR:String	= "|";
		public static const DEFAULT_WILDCARD:String 	= "*";
		
		private var _filters:Array;
		private var _levels:Array;
		private var _separator:String;
		
		public function Filter() {
			super();
		}
		
		public function getLevels():Array {
			return ( this._levels || [ Level.ALL ] );
		}
		
		public function getFilters():Array {
			return ( this._filters || [ Filter.DEFAULT_WILDCARD ] );
		}
		
		public function set levels( value:String ):void {
			
			if ( StringUtil.isEmpty( value ) ) return;
			
			var level:Level;
			var result:Array = new Array();
			var list:Array = value.toLowerCase().split( this._separator || Filter.DEFAULT_SEPARATOR );
			
			for ( var a:uint = 0; a < list.length; a++ ) {
				level = Level.isLevel( list[a] );
				if ( level == Level.ALL ) {
					return;
				}else if ( level != null ) {
					result.push( level );
				}				
			}
			
			if ( result.length > 0 ) {
				this._levels = result;
			}
			
		}
		
		public function set filters( value:String ):void {
			
			if ( StringUtil.isEmpty( value ) ) return;
			
			var classes:String;
			var result:Array = new Array();
			var list:Array = value.split( this.separator || Filter.DEFAULT_SEPARATOR );
			
			for ( var a:uint = 0; a < list.length; a++ ) {
				classes = String( list[a] )
				if ( classes.search( /^([a-zA-Z]([\w_])*|[\*])([\.][a-zA-Z]([\w_])*)*((\.\*)|(\:\:[a-zA-Z]([\w_])*))?$/ ) > -1 ) {
					if ( classes == Filter.DEFAULT_WILDCARD ) {
						return;
					}else {
						result.push( list[a] );
					}
				}
			}
			
			if ( result.length > 0 ) {
				this._filters = result;
			}
			
		}		
		
		public function get separator():String {
			return this._separator;
		}
		
		public function set separator( value:String ):void {
			
			if ( StringUtil.isEmpty( value ) ) return;
			
			if ( value.search( /[\w\-\_\.\:]+/g ) > -1 ) {
				throw new IllegalOperationError( "No se puede utilizar cualquiera de estos carcateres como separador: 'A-Za-z0-9-_.:' " );
			}
			
			this._separator = value.substr( 0, 1 );
			
		}
		
		protected function validate():Boolean {
			
			if ( this._levels == null && this._filters == null ) return true;
			
			var a:uint;
			var level:Boolean =  false;
			var filter:Boolean =  false;
			var context:String = ClassUtil.fullName( this.context );
			
			if ( this._levels != null ) {
				if( this._levels.length > 1 ) {
					for ( a = 0; a < this._levels.length; a++ ) {
						if ( this._levels[ a ] == this.level ) {
							level = true;
							break;
						}
					}
				} else if( this.level.gequals( this._levels[ 0 ] ) ) {
					level = true;
				}
			}else {
				level = true;
			}
			
			if ( this._filters != null ) {
				for ( a = 0; a < this._filters.length; a++ ) {
					filter = validateContext( context, this._filters[ a ] );
					if ( filter ) break;						
				}
			}else {
				filter = true;
			}
			
			return new Boolean( level && filter );
			
		}
		
		protected function validateContext( value:String, filter:String ):Boolean {
			
			var flags:String = new String();
			
			if ( value.search( /^(pq\.log\:\:)(Logger|Debugger)$/ ) > -1 ) {
				filter = "^pq.log";
			}else if ( filter.search( /\.\*/ ) > -1 ) {
				filter = "^" + filter.replace( /\.\*/, "" );
			}else {
				filter = "^" + filter + "$";
			}
			
			return new Boolean( value.search( new RegExp( filter ) ) > -1 );
			
		}
		
	}
	
}