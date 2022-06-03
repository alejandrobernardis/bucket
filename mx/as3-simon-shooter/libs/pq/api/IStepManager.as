
package pq.api {
	
	public interface IStepManager extends IUIComponent {
		
		function get index():uint;		
		function set index( value:uint ):void;		
		function get tween():Boolean;		
		function set tween( value:Boolean ):void;		
		function get showContentAfterIntro():Boolean;		
		function set showContentAfterIntro( value:Boolean ):void;		
		function get offset():uint;	
		function get size():uint;
		function get labelsSteps():Array;
		
		function intro():*;		
		function content():void;		
		function outro():void;		
		function hasIntro():Boolean;		
		function hasOutro():Boolean;		
		
		function firstStep():uint;		
		function prevStep():uint;		
		function nextStep():uint;		
		function lastStep():uint;
		function hasNextStep():Boolean;		
		function hasPrevStep():Boolean;		
		function addStepScript( frame:*, method:Function ):void;
		function removeStepScript( frame:* ):void;
		
	}
	
}