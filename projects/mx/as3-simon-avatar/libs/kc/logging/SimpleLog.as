
package kc.logging {
	import kc.utils.NumberUtil;
	import kc.core.KCStatic;
	import kc.utils.StringUtil;
	import kc.utils.TypeUtil;

	import flash.utils.describeType;

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public class SimpleLog extends KCStatic {

		// @const

		private static const TEMPLATE_TRACE:String 	= "{1} [{2}]: {3}";
		private static const TEMPLATE_BREAK:String 	= "\n\n{1} ({2})\n{3}";
		private static const TEMPLATE_TIME:String 	= "{1}/{2}/{3} {4}:{5}:{6}";

		private static const NOT_FOUND:int = -1;
		
		public static var debuger:Boolean = true;  

		// @constructor

		public function SimpleLog() {
			super();
		}

		// @methods

		public static function breakpoint( title:String = "breakpoint" ):void {
			if(!debuger) 
				return;
			trace(
				StringUtil.substitute(
					TEMPLATE_BREAK,
					title.toUpperCase(),
					time(),
					StringUtil.multiply( "========", 8 )
				)
			);
		}

		public static function print(...rest):void {
			if(!debuger) 
				return;
			trace(
				StringUtil.substitute(
					TEMPLATE_TRACE,
					time(),
					"PRINT",
					rest.join(" ")
				)
			);
		}

		public static function tracking( ...rest ):void {
			trace(
				StringUtil.substitute(
					TEMPLATE_TRACE,
					time(),
					"TRACKING",
					rest.join(" ")
				)
			);
		}

		public static function log( level:String = "log", ...rest ):void {
			if(!debuger) 
				return;
			trace(
				StringUtil.substitute(
					TEMPLATE_TRACE,
					time(),
					level.toUpperCase(),
					serialize( rest )
				)
			);
		}

		public static function dump(...rest):void {
			if(!debuger) 
				return;
			SimpleLog.log.apply( null, new Array( "dump" ).concat( rest ) );
		}

		public static function string(...rest):String {
			return serialize( rest );
		}

		// @helpers

		private static function serialize( value:*, depth:uint = 0, ...rest ):String {

			var list:*;
			var maxdepth:uint = 255;
			var result:String = new String();
			var recursive:String = new String();

			var description:XML = describeType(value);
			var type:String = description.@name;

			if( description.@base == "Function" ){
				type = "Function";
			}else if( type.search( /\:\:[A-Za-z]([\w_])*$/ ) > NOT_FOUND ){
				type = type.split("::").pop();
			}

			if( TypeUtil.isPrimitiveString( type ) || value is Date ){
				result += "\"" + value + "\"";
			}else if( value is XML || value is XMLList ){
				result += "[" + type + "] =>\nBOX {\n" + value.toXMLString() + "\n} EOX\n";
			}else{
				result += "[" + type + "] => ";
				if ( depth <= maxdepth ) {
					if ( ! TypeUtil.isCollection( type ) ) {
						list = description..accessor.( @access == "readonly" );
						for each ( var node:XML in list ) {
							if ( node.@declaredBy == "flash.display::FrameLabel"
								|| node.@declaredBy.search(/^flash\.(display|text|media)/) == NOT_FOUND ) {
									recursive += template( node.@name.toString(), value, depth );
							}
						}
					}else{
						for ( var element:String in value ) {
							recursive += template( element, value, depth );
						}
					}
					if ( recursive.length > 0 ) {
						result += "{" + recursive + "\n" + StringUtil.multiply( "\t", depth ) + "}";
					}
				}
			}

			return result;

		}

		private static function template( label:String, value:*, depth:uint ):String {

			try{
				value = value[label];
			}catch(e:Error){
				value = "{Error #: " + String( e.message ).replace( /(\s+).*?/g, " " ) + "}";
			}

			return new String( "\n"
				+ StringUtil.multiply( "\t", ( depth + 1 ) )
				+ label + ": "
				+ serialize( value, ( depth + 1 ) )
			);

		}

		private static function time():String {

			var time:Date = new Date();

			return StringUtil.substitute(
				TEMPLATE_TIME,
				NumberUtil.addLeadingZero( time.getDate() ),
				NumberUtil.addLeadingZero( time.getMonth() + 1 ),
				time.getFullYear(),
				NumberUtil.addLeadingZero( time.getHours() ),
				NumberUtil.addLeadingZero( time.getMinutes() ),
				NumberUtil.addLeadingZero( time.getSeconds() )
				//time.getMilliseconds()
			);

		}

	}

}
