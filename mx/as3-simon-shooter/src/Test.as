
package  {
	
	import pq.log.Debugger;
	
	public class Test {
		
		public function Test() {
		
		}
		
		public static function active():void {
			Debugger.active(true);
			Debugger.appender("output");
			Debugger.level("all");
			Debugger.filter("*");
		}
		
	}
	
}