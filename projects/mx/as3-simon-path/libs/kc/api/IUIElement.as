
package kc.api {
	import flash.geom.Rectangle;

	public interface IUIElement {
		
		function isUIElement():Boolean;
		function getUIRectangle():Rectangle;
		function setUIRectangle( ...rest ):void;		
		
	}
	
}
