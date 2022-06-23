package activia.simon.shooter.ui {
	import pq.api.IStepManager;
	
	
	public interface Screen extends IStepManager {
		
		function init():void;
		function destroy():void;
		
	}
	
}