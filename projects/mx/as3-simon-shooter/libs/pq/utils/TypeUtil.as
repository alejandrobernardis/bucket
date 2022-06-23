
package pq.utils {
	
	import flash.external.ExternalInterface;
	import flash.system.Capabilities;
	import flash.utils.describeType;
	import pq.core.CoreStatic;
	
	public class TypeUtil extends CoreStatic {
		
		public function TypeUtil() {
			super();		
		}	
		
		public static function firebugAvailable():Boolean {
			if (  isBorwser() && ExternalInterface.available ){
				return ( ExternalInterface.call( "function(){ return typeof window.console == 'object' && typeof console.firebug == 'string'}" ) );
			}
			return false;
		}
		
		public static function isBorwser():Boolean {
			return ( Capabilities.playerType == "ActiveX" || Capabilities.playerType == "PlugIn" );
		}
		
		public static function isEmpty( value:* ):Boolean {
			
			if ( isSet( value ) ) {
				if ( value is Number ) {
					return isNaN( value );
				} else if ( value is Array || value is String ) {
					if ( value is String ) {
						value = StringUtil.stripWhiteSpace( value );
					} return ( value.length < 1 );
				} else if ( isLiteralCollection( describeType( value ).@name ) ) {
					for ( var a:String in value ) {
						return false;
					}
				}
			}
			
			return true;
			
		}
		
		public static function isSet( value:* ):Boolean {
			return ( value != null && value != undefined );
		}
		
		public static function isLiteralCollection( value:String ):Boolean {
			
			switch( value.toLowerCase() ){
				
				case "array":
				case "object":
				case "dictionary":
					return true;
				
				default:
					return false;
				
			}
			
		}
		
		public static function isLiteralPrimitive( value:String ):Boolean {
			
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
			
			switch( typeof( value ) ){
				
				case "string":
				case "boolean":
				case "number":
					return true;
					
				default:
					return false;
				
			}
			
		}
		
		public static function isBoolean( value:* ):Boolean {
			
			if( value is String ){
				value = value.toLowerCase();
			}
			
			switch( value ){
				
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

	}
	
}