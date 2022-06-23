
package kc.utils {
	import kc.core.KCStatic;
	import kc.logging.SimpleLog;

	import flash.errors.IllegalOperationError;

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public class ExceptionUtil extends KCStatic {

		// @const
		
		private static const NOT_FOUND:int = -1;

		// @variables
		
		public static var CATCH_EXCEPTIONS:Boolean;

		// @constructor
		
		public function ExceptionUtil() {
			super();
		}
		
		// @mthods
		
		public static function ViewError( value:*, catchExceptions:Boolean = false ):* {
			
			var error:Object = new Object();
			
			if ( value is Error ) {
				error.id = value.errorID;
				error.name = value.name;
				error.message = value.message;
				error.stack = value.getStackTrace();
				value = error;
			}
			
			if( ! CATCH_EXCEPTIONS && ! catchExceptions ) {
				throw new Error( 
					SimpleLog.string( value )
					, 0 
				);
			}else{
				SimpleLog.log( "error", value );
			}
			
			return null;
			
		}
		
		// @eventsFilter
		
		public static function EventsFilterInclude( value:String, list:Array, enableEvents:Boolean = true ):Error {
			return EventsFilter( value, list, enableEvents, false );
		}
		
		public static function EventsFilterExclude( value:String, list:Array, enableEvents:Boolean = true ):Error {
			return EventsFilter( value, list, enableEvents, true );
		}
		
		private static function EventsFilter( value:String, list:Array, enableEvents:Boolean = true, exclude:Boolean = false ):Error {
			if( ! enableEvents )
				return new IllegalOperationError( "The events are not available." );
			if( ( exclude && list.indexOf( value ) != NOT_FOUND ) 
				|| ( ! exclude && list.indexOf( value ) == NOT_FOUND ) ) 
					return new IllegalOperationError( "The event \"" + value + "\" is not available." );
			return null;
		}
		
		// @methods
		
		public static function PropertyIsNotAvailable( value:String, access:int = -1, replace:String = null ):Error {
			var error:String = "The \"" + value + "\" property is not available.";
			if ( access == 0 )
				error = error.substr( 0, -1 ) + " for reading.";
			if ( access == 1 )
				error = error.substr( 0, -1 ) + " for writing.";
			if ( replace != null )
				error = error.substr( 0, -1 ) + ", use the \"" + replace + "\" property.";
			return new IllegalOperationError( error );
		}
		
		public static function MethodIsNotAvailable( value:String, replace:String = null ):Error {
			var error:String = "The \"" + value + "\" method is not available.";
			if ( replace != null )
				error = error.substr( 0, -1 ) + ", use the \"" + replace + "\" method.";
			return new IllegalOperationError( error );			
		}
		
	}
	
}
