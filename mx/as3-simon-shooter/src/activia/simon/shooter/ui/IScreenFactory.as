package activia.simon.shooter.ui {
	import pq.api.IUIComponent;
	
	
	public interface IScreenFactory extends IUIComponent {
		
		function add( value:String ):void;
		function remove():void;
		function replace( value:String ):void;
		
		function get content():Screen;
		function get screens():ScreensStack;
		function get quantity():uint;
		function get isPlaying():Boolean;
		
		function sHome( action:int = 0 ):void;
		function sInstructions( action:int = 0 ):void;
		function sGame( action:int = 0 ):void;
		function sGameOver( action:int = 0 ):void;
		function sScoreRegiste( action:int = 0 ):void;
		function sRanking( action:int = 0 ):void;
		
	}
	
}