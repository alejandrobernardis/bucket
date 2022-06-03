package activia.simon.shooter.ui.actors {
	import pq.api.IUIComponent;
	
	
	public interface Actor extends IUIComponent {
		
		function get type():String;
		function set type( value:String ):void;
		function get points():String;
		function set points(value:String):void;
		function set wildcard(value:Boolean):void;
		function get actorTween():ActorTween;
		
		function init():void;
		function destroy():void;
		
		function startMotion():void;		
		function pauseMotion():void;
		function resumeMotion():void;
		function stopMotion():void;
		
		function get duration():Number;
		function set duration(seconds:Number):void;
		
		function get speedX():Number;
		function set speedX(value:Number):void;
		function get speedY():Number;
		function set speedY(value:Number):void;
		function get desacX():Number;
		function set desacX(value:Number):void;
		function get desacY():Number;
		function set desacY(value:Number):void;
		function get angle():Number;
		function set angle(value:Number):void;
		function get range():Number;
		function set range(value:Number):void;
		function get delta():Number;
		function set delta(value:Number):void;		
		function get sound():String;
		function set sound(value:String):void;
		
	}
	
}