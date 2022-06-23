
package pq.core {
	
	import flash.errors.IllegalOperationError;
	
	public class CoreStatic {
		
		public function CoreStatic() {
			throw new IllegalOperationError( "Illegal instantiation attempted on class of static type." );
		}
		
	}
	
}