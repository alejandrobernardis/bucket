
package pq.log.appenders {
	
	import com.emc2zen.util.ClassUtil;
	import flash.errors.IllegalOperationError;
	import flash.utils.describeType;
	import pq.api.IAppender;
	import pq.log.Appender;
	import pq.utils.StringUtil;
	import pq.utils.TypeUtil;
	
	public class SimpleAppender implements IAppender {
		
		public function SimpleAppender() {
			
		}
		
		public function send( value:Appender ):void {
			
			var pattern:String = "{1} [{2}] {3}: {4}";
			
			trace( 
				StringUtil.substitute ( 
					pattern,
					new Date(),
					value.level.label.toUpperCase(),
					ClassUtil.fullName( value.context ),
					ResolveMessage( value.message )
				)
			);
			
		}
		
		public function serialize( value:*, depth:uint = 0, ...rest ):String {
			throw new IllegalOperationError("Esta operación no se encuetra disponible.");
		}
		
		public function toString():String {
			return ClassUtil.shortName( this );
		}
		
		private function ResolveMessage( value:* ):String {
			if ( TypeUtil.isLiteralPrimitive( describeType( value ).@name ) ) {
				return String( value );
			} else {
				return value.toString();
			}
		}
		
	}
	
}