
package pq.core {
	
	import flash.errors.IllegalOperationError;
	
	public class CoreSingleton {
		
		public function CoreSingleton() {
			throw new IllegalOperationError( "Illegal instantiation attempted on class of singleton type." );
		}
		
	}
	
}