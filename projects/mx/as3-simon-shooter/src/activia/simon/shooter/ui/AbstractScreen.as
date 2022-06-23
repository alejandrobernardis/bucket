package activia.simon.shooter.ui {
	import pq.ui.BasicButton;
	import pq.ui.StepManager;

	import flash.errors.IllegalOperationError;
	import flash.events.Event;
	import flash.events.MouseEvent;
	
	
	public class AbstractScreen extends StepManager implements Screen {
		
		protected var _status:Boolean;
		
		public function AbstractScreen() {			
			super( false );			
			this.tween = true;
			this._status = false;			
			this.addEventListener( Event.ADDED_TO_STAGE, $config );			
		}
		
		public function init():void {			
			if ( this._status ) return;			
			this._status = true;
			this.intro();
		}        
		
		public function destroy():void {
			if ( ! this._status ) return; 
			this.RemoveActions(); // por las dudas!
		}
		
		public override function purge(...rest):void {
			this._status = undefined;
			this.RemoveActions();
			super.purge();
		}
		
		/* OVERRIDE */
		
		protected function $config( e:Event ):void{
			for ( var a:uint = 0; a < this.labelsSteps.length; a++ ) {
				this.addStepScript( this.labelsSteps[a].name, ApplyActions );
			}
			this.removeEventListener( Event.ADDED_TO_STAGE, $config );
		}
		
		protected function ApplyActions():void {
			for ( var a:uint = 0; a < this.numChildren; a++ ) {
				if( this.getChildAt(a) is BasicButton ) BasicButton( this.getChildAt( a ) ).addEventListener( MouseEvent.CLICK, ButtonsManager );
			}
		}
		
		protected function RemoveActions():void {
			for ( var a:uint = 0; a < this.numChildren; a++ ) {
				if( this.getChildAt(a) is BasicButton ) BasicButton( this.getChildAt( a ) ).removeEventListener( MouseEvent.CLICK, ButtonsManager );
			}
		}
		
		protected function ButtonsManager( e:MouseEvent ):void {
			throw new IllegalOperationError("Este metodo no fue aplicado.");
		}
		
	}
	
}