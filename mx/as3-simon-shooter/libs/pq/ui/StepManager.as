
package pq.ui {
	import pq.api.IStepManager;
	import pq.events.StepManagerEvent;

	import flash.display.FrameLabel;
	import flash.errors.IllegalOperationError;

	[Event(name="beforeChange", type="pq.events.StepManagerEvent")]
	[Event(name="afterChange", type="pq.events.StepManagerEvent")]
	[Event(name="introBegins", type="pq.events.StepManagerEvent")]
	[Event(name="introFinished", type="pq.events.StepManagerEvent")]
	[Event(name="outroBegins", type="pq.events.StepManagerEvent")]
	[Event(name="outroFinished", type="pq.events.StepManagerEvent")]

	public class StepManager extends UIComponent implements IStepManager {

		// Core.
		private var _index:uint;
		private var _indexMin:uint;
		private var _indexMax:uint;
		private var _offset:uint;
		private var _tween:Boolean;

		// Structure.
		private var _steps:Array;
		private var _intro:FrameLabel;
		private var _content:FrameLabel;
		private var _outro:FrameLabel;

		// Status.
		private var _available:Boolean;
		private var _showContentAfterIntro:Boolean;



		public function StepManager( scai:Boolean = true ) {

			super();

			this._showContentAfterIntro = scai;
			this._available = this.validate();

			if( ! this._available ){
				throw new IllegalOperationError( "No se definio corretamente la estructura de la linea de tiempo." );
			}

		}

		public function get label():String {
			if ( this._steps.length > 0 ) return null;
			return FrameLabel( this._steps[ this._index - 1 ] ).name;
		}

		public function set label( value:String ):void {
			if ( this._steps.length > 0 ) return;
			for ( var a:uint = 0; a < this._steps.length; a++ ) {
				if ( FrameLabel( this._steps[a] ).name == value ) {
					GoTo( a + 1 );
					break;
				}
			}
		}

		public function get index():uint {
			return this._index;
		}

		public function set index( value:uint ):void {
			GoTo( value );
		}

		public function get tween():Boolean {
			return this._tween;
		}

		public function set tween( value:Boolean ):void {
			this._tween = value;
		}

		public function get showContentAfterIntro():Boolean {
			return this._showContentAfterIntro;
		}

		public function set showContentAfterIntro(value:Boolean):void {
			this._showContentAfterIntro = value;
		}

		public function get offset():uint {
			return this._offset;
		}

		public function get size():uint {
			return this._indexMax;
		}

		public function get labelsSteps():Array {
			return ( this._steps || [] /*null*/ );
		}



		public function intro():* {
			if ( ! this.hasIntro() ) return this.content();
			this.gotoAndPlay( this._intro.frame );
			this.dispatchEvent( new StepManagerEvent( StepManagerEvent.INTRO_BEGINS ) );
		}

		public function content():void {
			if ( this._content == null ) return;
			this.firstStep();
		}

		public function outro():void {
			if ( ! this.hasOutro() ) return;
			this.gotoAndPlay( this._outro.frame );
			this.dispatchEvent( new StepManagerEvent( StepManagerEvent.OUTRO_BEGINS ) );
		}

		public function hasIntro():Boolean {
			return ( this._intro != null && this._available );
		}

		public function hasOutro():Boolean {
			return ( this._outro != null && this._available );
		}



		public function firstStep():uint {
			return this.GoTo( this._indexMin );
		}

		public function prevStep():uint {
			var i:uint = this._index;
			if( this.hasPrevStep() ){
				this._index --;
				i = this.GoTo( this._index );
			} return i;
		}

		public function nextStep():uint {
			var i:uint = this._index;
			if( this.hasNextStep() ){
				this._index ++;
				i = this.GoTo( this._index );
			} return i;
		}

		public function lastStep():uint {
			return this.GoTo( this._indexMax );
		}

		public function hasNextStep():Boolean {
			return Boolean( this._index < this._indexMax );
		}

		public function hasPrevStep():Boolean {
			return Boolean( this._index > this._indexMin );
		}



		public function addStepScript( frame:*, method:Function ):void {
			ResolveStepScript( frame, method );
		}

		public function removeStepScript( frame:* ):void {
			ResolveStepScript( frame );
		}



		public override function purge(...rest):void {
			this._index = undefined;
			this._indexMin = undefined;
			this._indexMax = undefined;
			this._offset = undefined;
			this._tween = undefined;
			this._available = undefined;
			this._showContentAfterIntro = undefined;
			this._content = null;
			this._intro = null;
			this._outro = null;
			this._steps = null;
			super.purge();
		}



		protected function validate():Boolean {

			this._steps = new Array();

			for ( var a:uint = 0; a < this.currentLabels.length; a++ ) {
				switch( this.currentLabels[a].name.toLowerCase() ) {
					case "intro":
					case "content":
					case "outro":
						this[ "_" + this.currentLabels[a].name ] = this.currentLabels[a];
						break;
					default:
						this._steps.push( this.currentLabels[a] );
				}
			}

			if( this._content != null ){

				this._tween = false;
				this._offset = this._content.frame - 1;
				this._indexMin = 1;

				if ( this._steps.length > 0 ) {
					this._indexMax = this._steps.length;
				} else if ( this._outro != null ) {
					this._indexMax = ( this._outro.frame - 1 ) - this._offset;
				}else {
					this._indexMax = this.totalFrames - this._offset;
				}

				if ( this._intro != null ) {
					this.addFrameScript( ( this._offset - 1 ), this.FinishedIntro );
				}

				if ( this._outro != null ) {
					this.addFrameScript( ( this.totalFrames - 1 ), this.FinishedOutro );
				}

				return true;

			}

			return false;

		}

		private function GoTo( value:uint ):uint {

			this.dispatchEvent( new StepManagerEvent( StepManagerEvent.BEFORE_CHANGE ) );

			this._index = uint( Math.min( this._indexMax, Math.max( this._indexMin, value ) ) );

			if ( this._steps.length > 0 ) {
				value = this._steps[ this._index - 1 ].frame;
			}else {
				value = this._index + this._offset;
			}

			if ( ! this.tween ) {
				this.gotoAndStop( value );
			}else {
				this.gotoAndPlay( value );
			}

			this.dispatchEvent( new StepManagerEvent( StepManagerEvent.AFTER_CHANGE ) );
			return this._index;

		}

		private function FinishedIntro():void {
			this.stop();
			this.dispatchEvent( new StepManagerEvent( StepManagerEvent.INTRO_FINISHED ) );
			if ( this._showContentAfterIntro ) {
				this.content();
			}
		}

		private function FinishedOutro():void {
			this.stop();
			this.dispatchEvent( new StepManagerEvent( StepManagerEvent.OUTRO_FINISHED ) );
		}

		private function ResolveStepScript( frame:*, method:Function = null ):void {

			if ( ! frame is Number && ! frame is String && frame < 1 && frame > this.totalFrames ) {
				return;
			} else if ( frame is String ) {
				for ( var a:uint = 0; a < this._steps.length; a++ ) {
					if ( this._steps[ a ].name == frame ) {
						frame = this._steps[ a ].frame;
					}
				}
			}

			this.addFrameScript( frame, method );

		}

	}

}