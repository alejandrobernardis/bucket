
package {
	import kc.core.KCComponent;
	import kc.core.KCDataLayer;

	import flash.events.Event;
	import flash.events.MouseEvent;

	/**
	 * @author @project.author@
	 */
	public class ApplicationFooter extends KCComponent {

		public function ApplicationFooter(data:XML = null, autorelease:Boolean = true) {
			super(data, autorelease);
		}
		
		override protected function $config(e:Event):void {
			super.$config(e);
			var xml:XML = KCDataLayer.collection.value("application") as XML;
			_data = new XML(xml.child("externalLink").toXMLString());
			Helpers.ResolveActions(this, ButtonsManager);
		}

		override public function purge(...rest):void {
			super.purge(rest);
			Helpers.ResolveActions(this, ButtonsManager, true);						
		}

		protected function ButtonsManager( e:MouseEvent ):void {
			var name:String = Helpers.ResolveButtonName(e.target);
			GoogleAnalytics.hit("common", name);
		}
		
	}
	
}
