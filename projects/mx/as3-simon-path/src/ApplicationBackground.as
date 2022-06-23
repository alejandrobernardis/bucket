
package {
	import kc.api.IMap;
	import kc.core.KCComponent;
	import kc.core.KCDataLayer;
	import kc.logging.SimpleLog;

	import flash.display.Bitmap;

	/**
	 * @author @project.author@
	 */
	public class ApplicationBackground extends KCComponent {

		public function ApplicationBackground(data:XML = null, autorelease:Boolean = true) {
			super(data, autorelease);
		}
		
		public function change( value:String = "bgdefault" ):void {

			while(numChildren){
				removeChild(getChildAt(0));
			}

			var map:IMap = KCDataLayer.collection.value("backgrounds") as IMap;
			
			if(map.containsKey(value.toLowerCase())){
				addChild( map.value(value.toLowerCase()) as Bitmap);	
			}else{
				SimpleLog.print("ApplicationBackground-NotFound", value);
			}

		}
		
	}
	
}
