
package pq.log.appenders {
	
	import com.emc2zen.util.ClassUtil;
	import flash.utils.describeType;
	import pq.api.IAppender;
	import pq.log.Appender;
	import pq.utils.StringUtil;
	import pq.utils.TypeUtil;
	
	public class OutputAppender implements IAppender {
		
		public function OutputAppender() {
			
		}
		
		public function send( value:Appender ):void {
			
			var pattern:String = "{1} [{2}] {3}: {4}";
			
			trace( 
				StringUtil.substitute ( 
					pattern,
					new Date(),
					value.level.label.toUpperCase(),
					ClassUtil.fullName( value.context ),
					serialize( value.message )
				)
			);
			
		}
		
		public function serialize( value:*, depth:uint = 0, ...rest ):String {
			
			var list:*;
			var maxdepth:uint = 255;
			var result:String = new String();
			var recursive:String = new String();
			
			var description:XML = describeType( value );
			var type:String = description.@name;
			
			if ( description.@base == "Function" ) {
				type = "Function";
			} else if ( type.search( /\:\:[A-Za-z]([\w_])*$/ ) > -1 ) {
				type = type.split("::").pop();
			}
			
			if ( TypeUtil.isLiteralPrimitive( type ) || value is Date ) {
				result += "\"" + value + "\"";
			}else if ( type.search( /^XML/ ) > -1 )  {
				result += "[" + type + "]\nBOX {\n" + value.toXMLString() + "\n} EOX\n";
			}else {	
				result += "[" + type + "]";
				if ( depth <= maxdepth ) {					
					if ( ! TypeUtil.isLiteralCollection( type ) ) {
						list = description..accessor.( @access != "writeonly" );
						for each ( var node:XML in list ) {							
							if ( node.@declaredBy == "flash.display::FrameLabel" /*node.@declaredBy.search(/^(flash\.display\:\:FrameLabel)$/) > -1*/ 
								|| node.@declaredBy.search(/^(flash)[\.](display|(text\:\:TextField)|(media\:\:Video))/) == -1 ) {
									recursive += template( node.@name, value, depth );
							}
						}
					}else {
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
		
		public function toString():String {
			return ClassUtil.shortName( this );
		}
		
		private function template( label:String, value:*, depth:uint ):String {
			
			try{
				value = value[ label ];
			}catch ( e:Error ) {
				value = "{Exception: " + e.message + "}";
			}			
			
			return new String( "\n" 
				+ StringUtil.multiply( "\t", ( depth + 1 ) ) 
				+ label + ": " 
				+ serialize( value, ( depth + 1 ) ) 
			);
			
		}
		
	}
	
}