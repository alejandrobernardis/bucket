
package {

	import kc.core.KCStatic;
	import kc.logging.SimpleLog;
	import kc.utils.ExceptionUtil;
	import kc.utils.StringUtil;
	import kc.utils.TypeUtil;

	import flash.external.ExternalInterface;

	/**
	 * @author Alejandro M. Bernardis ( alejandro.bernardis@gmail.com )
	 */
	public class GoogleAnalytics extends KCStatic {

		public static var BlackList:Array = [];

		public function GoogleAnalytics() {
			super();
		}

		public static const FUNCTION_GA:String = "pageTracker._trackPageview('{1}')";

		public static var DATA:XML;
		public static var BASE_TAG:String;

		public static function initialize( data:XML, baseTag:String = "" ):void {
			SimpleLog.print("GATracking: Initialized.");
			DATA = data;
			BASE_TAG = baseTag;
		}

		public static function fhit( value:String ):Boolean {
			
			if( value.search(/^https?:/i) !=  -1 ) {
				value = value.replace(/https?:/, "link");
				value = value.replace(/\./g, "_");
				value = BASE_TAG + "/" + value;
			}

			value = value.replace(/\/+/g, "/" );
			SimpleLog.tracking(value);
			
			if( TypeUtil.isBrowser() ){
				try{
					
					try{
						//Facebook.getInstance().call("pageTracker._trackPageview", [value]);
						//return true;
						ExternalInterface.call('kctrack', value);
						return true;
					}catch(e:Error){
						SimpleLog.print("ga-catch",e);
						return ExternalInterface.call(
							StringUtil.substitute(
								FUNCTION_GA,
								value
							)
						);
					}finally {
						SimpleLog.print("ga-catch", "critico");
						return false;
					}
					
				}catch(e:Error){
					return false;				
				}
			}

			return false;

		}

		public static function hit( section:String, id:String = null ):Boolean {
			
			if( ! DATA )
				return ExceptionUtil.ViewError( "Object not initialized.", true );

			if( TypeUtil.isOR(section, BlackList) )
				return false;

			return fhit(ResolveHit(section, id));

		}

		private static function ResolveHit( section:String, id:String ):String {

			var list:XMLList = DATA.child(section).children();

			if( ! id )
				id = section;

			return ( list.( @id == id ) != undefined )
				? BASE_TAG + ( list.( @id == id ).text().toString() )
				: BASE_TAG + "/not-found/" + section + "/" + id;
		}
	}

}
