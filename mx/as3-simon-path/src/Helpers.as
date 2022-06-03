package{
	import kc.api.IBasicButton;
	import kc.api.IIterator;
	import kc.core.KCStatic;
	import kc.tda.SimpleIterator;
	import kc.utils.ArrayUtil;
	import kc.utils.ClassUtil;
	import kc.utils.ExceptionUtil;

	import flash.display.DisplayObjectContainer;
	import flash.display.SimpleButton;
	import flash.events.IEventDispatcher;
	import flash.events.MouseEvent;
	import flash.net.SharedObject;
	import flash.net.URLVariables;

	/**
	 * @author @project.author@
	 */
	public class Helpers extends KCStatic {

		public function Helpers(catchException:Boolean = false) {
			super(catchException);
		}		
		
		// !~
		
		public static function get SEX():Array {
			var r:Array=[{label: "--", item: 0}];
			r.push( {label: "Femenino", item: 1} );
			r.push( {label: "Masculino", item: 2} );
			return r;
		}
		
		public static function get SEX_MC():Array {
			return new Array("--","Femenino","Masculino");
		}
		
		public static function get DAYS():Array {
			var r:Array=[{label: "--", item: 0}];
			for(var a:int=1; a<32; a++){
				r.push( {label: a, item: a} );
			} return r;
		}
		
		public static function get DAYS_MC():Array {
			var r:Array=["DD"];
			for(var a:int=1; a<32; a++){
				r.push(a.toString());
			} return r;
		}

		public static function get MONTHS():Array {
			var r:Array=[{label: "--", item: 0}];
			for(var a:int=1; a<13; a++){
				r.push( {label: a, item: a} );
			} return r;
		}
		
		public static function get MONTHS_MC():Array {
			var r:Array=["MM"];
			for(var a:int=1; a<13; a++){
				r.push(a.toString());
			} return r;
		}

		public static function YEARS( e:int, i:int=1900 ):Array {
			var r:Array=[{label: "----", item: 0}];
			for(var a:int=e; a>i; a--){
				r.push( {label: a, item: a} );
			} return r;
		}
		
		public static function YEARS_MC( e:int, i:int=1900 ):Array {
			var r:Array=["AAAA"];
			for(var a:int=e; a>i; a--){
				r.push(a.toString());
			} return r;
		}
		
		public static function DATA_PROVIDER_STRING(value:String):Array {
			var r:Array=[{label: "----", item: 0}];
			var i:IIterator = new SimpleIterator(value.split("|"));
			while(i.hasNext()){
				i.next();
				r.push( 
					{
						label: i.value().replace(/:.+?$/i, ""), 
						item: i.value().replace(/^.+:/i, "")
					}
				);
			} return r;
		}
		
		public static function ageValidator(d:int,m:int,y:int,a:int=18,b:int=2010):Boolean {
			if( d > 0 && d < 32 ){
				if( m > 0 && m < 13 ){
					return ( ( b - y ) >= a && ( b - y ) <= 100 );
				}
			} return false;
		}

		// !~
		
		public static var COOKIE_NAME:String = "cookie-default";
		
		public static function getCookie( key:String ):* {
			var so:SharedObject = SharedObject.getLocal(COOKIE_NAME);
			return so.data[key];
		}

		public static function setCookie( key:String, value:* ):void {
			var so:SharedObject = SharedObject.getLocal(COOKIE_NAME);
			so.data[key] = value;
			try{
				so.flush(10000);
			}catch(e:Error){
				ExceptionUtil.ViewError(e, true);
			}
		}

		public static function removeCookie( key:String ):* {
			var so:SharedObject = SharedObject.getLocal(COOKIE_NAME);
			var v:* = so.data[key];
			delete so.data[key];
			return v;
		}
		
		// !~
		
		public static function Secure( value:*, list:Array = null ):void {
			if(!list){
				value.allowDomain("*");
			}else{
				var i:SimpleIterator = new SimpleIterator(ArrayUtil.discriminateArgument(list));
				while(i.hasNext()){
					value.allowDomain(i.next());
				}
			}
		}
		
		// !~
		
		public static function ResolveActions( scope:DisplayObjectContainer, handler:Function, remove:Boolean = false  ):void {
			
			var element:IEventDispatcher;

			var f:String = ( ! remove )
				? "addEventListener"
				: "removeEventListener";

			for ( var a:uint = 0; a < scope.numChildren; a++ ) {
				if( scope.getChildAt(a) is SimpleButton || scope.getChildAt(a) is  IBasicButton ){
					element = scope.getChildAt(a) as IEventDispatcher;
					element[f].apply(
						scope,
						[MouseEvent.CLICK, handler]
					);
				}
			}
			
		}
		
		// !~
		
		private static const encodingID:String = "I";
		private static const encodingKey:String = "9B3B6EDFBFC34F98B94A305D2ED7C308";

		public static function doit( s:String, k:String=null ):String {

			var theResult:String = "";
			var iKey:int = 0;
			var i:int;
			
			if(!k)
				k = encodingKey;

			for (i = 0; i < s.length; ++i ) {

				var theNumber:int = s.charCodeAt(i) ^ k.charCodeAt(iKey);
				var xored:String = theNumber.toString();

				if (theNumber < 10) {
					xored = "00" + xored;
				}else if (theNumber < 100){
					xored = "0" + xored;
				}

				theResult = theResult + xored;

				if(iKey == k.length-1){
					iKey = 0;
				}else{
					iKey++;
				}

			}

			return (encodingID + theResult);

		}

		public static function rdoit( s:String, k:String=null ):String {

			var iKey:int = 0;
			var coef:uint = 3;
			var str:String = s.substring( 1 );
			var result:String = new String("");
			
			if(!k)
				k = encodingKey;

			for ( var a:uint = 0; a < ( str.length / coef ); a++ ) {

				var pos:uint = a * coef;
				var xored:String = str.substring( pos, pos + coef );
				result = result + String.fromCharCode( int( xored ) ^ k.charCodeAt(iKey) );

				if(iKey == k.length-1){
					iKey = 0;
				}else{
					iKey++;
				}

			}

			return result;
		}
		
		public static function doitVars( variables:URLVariables, k:String=null ):URLVariables {
			var r:String = new String();
			for(var s:String in variables)
				r += s + "=" + encodeURIComponent(variables[s]) + "&";
			var vresult:URLVariables = new URLVariables();
			vresult.h = doit(r, k); 
			return vresult;
		}

		// !~

		public static function ResolveButtonName(target:*):String {
			return ( target is SimpleButton ) 
				? target.name 
				: ClassUtil.shortName(target);
		}
	}
}
