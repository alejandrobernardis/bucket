
package kc.api {

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public interface IKCComponentSteps extends IKCComponent {
		
		// @properties (rw)
		
		function get label():String;
		function set label( value:String ):void;
		function get index():uint;
		function set index( value:uint ):void;
		function get tweening():Boolean;
		function set tweening( value:Boolean ):void;
		function get showContentAfterIntro():Boolean;
		function set showContentAfterIntro( value:Boolean ):void;
		function get ignoreCase():Boolean;
		function set ignoreCase( value:Boolean ):void;

		// @properties (r)
		
		function get available():Boolean;
		function get offset():uint;
		function get steps():uint;
		function get labels():Array;
		function get history():IHistory;
		
		// @methods
		
		function intro():void;
		function content():void;
		function outro():void;
		function firstStep():uint;
		function prevStep():uint;
		function nextStep():uint;
		function lastStep():uint;
		
		// @has
		
		function hasIntro():Boolean;
		function hasOutro():Boolean;
		function hasPrevStep():Boolean;
		function hasNextStep():Boolean;
		function hasLabel( value:String, ignoreCase:Boolean = true ):Boolean;

		// @history
		
		function back():void;
		function forward():void;

		// @scripts
		
		function addStepScript( frame:*, method:Function ):void;			
		function removeStepScript( frame:* ):void; 
		
	}
	
}
