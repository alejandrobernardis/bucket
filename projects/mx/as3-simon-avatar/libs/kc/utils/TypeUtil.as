
package kc.utils {
	import kc.core.KCStatic;

	import flash.external.ExternalInterface;
	import flash.system.Capabilities;

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public class TypeUtil extends KCStatic {

		// @constructor

		public function TypeUtil() {
			super();
		}
		
		// @methods
		
		public static function isBrowser():Boolean {
			return ExternalInterface.available && ( 
				Capabilities.playerType == "ActiveX" 
					|| Capabilities.playerType == "PlugIn" 
			);
		}
		
		public static function isExplorable( value:* ):Boolean {
			return ( ! ( value is Function ) && ! isEmpty( value ) );
		}
		
		public static function isEmpty( value:* ):Boolean {
			if ( isSet( value ) ) {
				if( typeof( value ) == "string" ){
					return StringUtil.isEmpty( value );
				}else if( value is Array ){
					return ( value.length == 0 );
				}else if( isCollection( value ) ){
					for ( var a:String in value ) {
						return a.length == 0;
					}
				}
			} return true;			
		}
		
		public static function isSet( value:* ):Boolean {
			return ( value is Number && ! isNaN( value ) ) 
				|| ( value != null && value != undefined );
		}
		
		public static function isCollection( value:* ):Boolean {
			if( typeof( value ) != "string" ) 
				value = ClassUtil.shortName( value ) as String;		
			switch( value.toLowerCase() ){				
				case "array":
				case "object":
				case "dictionary":
					return true;
				default:
					return false;
			}			
		}
		
		public static function isPrimitiveString( value:String ):Boolean {
			switch( value.toLowerCase() ){				
				case "string":
				case "boolean":
				case "number":
				case "uint":
				case "int":
				case "undefined":
				case "null":
					return true;				
				default:
					return false;
			}			
		}
		
		public static function isPrimitive( value:* ):Boolean {
			switch( typeof( value ) ) {				
				case "string":
				case "boolean":
				case "number":
					return true;					
				default:
					return false;				
			}			
		}
		
		public static function isBoolean( value:* ):Boolean {
			if( typeof( value ) == "string" )
				value = String( value ).toLowerCase();
			switch( value ) {				
				case 1:
				case "1":
				case true:
				case "true":
				case "ok":
				case "yes":
				case "si":
				case "oui":
				case "on":
				case "one":
				case "uno":
					return true;				
				default:
					return false;					
			}			
		}  
		
		public static function isOR( value:*, ...rest ):Boolean {
			
			rest = ArrayUtil.discriminateArgument(rest);
			
			if( rest.length ){
				while( rest.length ){
					if( value === rest.pop() ){
						return true;
					}
				}	
			}
			
			return false;
				
		}
		
	}
	
}
