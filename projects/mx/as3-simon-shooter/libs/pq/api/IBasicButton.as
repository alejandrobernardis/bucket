package pq.api {
	
	public interface IBasicButton extends IUIComponent {
		
		function get label():String;
		function set label( value:String ):void;
		function get frameTransition():Boolean;
		function set frameTransition( value:Boolean ):void;
		
	}
	
}