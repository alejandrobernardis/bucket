
package kc.utils {
	import kc.core.KCStatic;

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public class PurgerUtil extends KCStatic {
		
		// @const
		
		private static const MAX_DEPTHS:uint = 255;

		// @constructor

		public function PurgerUtil() {
			super();
		}
		
		// @methods	
		
		public static function cleanCollection( value:*, depth:uint = 0 ):* {
			
			if( TypeUtil.isSet( value ) && depth < MAX_DEPTHS ) {
				
				if( value is Array ){
					for( var a:int = 0; a < value.length; a++ ){
						if( value[a] is Array ){
							cleanCollection( value[a], depth++ );	
						}else if( value[a] is Number || value[a] is Boolean ){
							value[a] = undefined;
						}else{
							value[a] = null;
						}
					}
				}else if( TypeUtil.isCollection( value ) ){
					for( var e:String in value ){
						if( value[e] is Array ){
							cleanCollection( value[a], depth++ );	
						}else if( value[e] is Number || value[e] is Boolean ){
							value[e] = undefined;
						}else{
							value[e] = null;
						}
					}
				}
				
				// TODO: Se podria implementar soporte para objetos complejos, o bien soporte para depuración.
					
			}
			
			return null;
			
		}
		
	}
	
}
