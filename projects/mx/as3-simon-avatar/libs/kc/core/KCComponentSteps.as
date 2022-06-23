
package kc.core {
	import kc.api.IHistory;
	import kc.api.IKCComponentSteps;
	import kc.events.KCComponentStepsEvent;
	import kc.tda.SimpleHistory;
	import kc.utils.ExceptionUtil;
	import kc.utils.PurgerUtil;

	import flash.display.FrameLabel;
	import flash.events.Event;

	[Event(name="beforeChange", type="kc.events.KCComponentStepsEvent")]	
	[Event(name="afterChange", type="kc.events.KCComponentStepsEvent")]
	[Event(name="introBegins", type="kc.events.KCComponentStepsEvent")]
	[Event(name="introFinished", type="kc.events.KCComponentStepsEvent")]
	[Event(name="outroBegins", type="kc.events.KCComponentStepsEvent")]
	[Event(name="outroFinished", type="kc.events.KCComponentStepsEvent")] 	[Event(name="available", type="kc.events.KCComponentStepsEvent")] 

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public class KCComponentSteps extends KCComponent implements IKCComponentSteps {
		
		// @const
		
		public static const ERROR_NOT_DEFINED_CONTENT:String = "The structure is not well defined, there is no \"content\" label.";		public static const ERROR_DEFINED_CONTENT_ON_FIRST_FRAME:String = "The structure is not well defined, the label \"content\" is on the first frame.";
		public static const ERROR_NOT_SUPPORT_LABELS:String = "The structure is not defined to support labels.";
		
		public static const DEFAULT_LABEL_INTRO:String 		= "intro";		public static const DEFAULT_LABEL_CONTENT:String 	= "content";		public static const DEFAULT_LABEL_OUTRO:String 		= "outro";
		
		private static const NOT_FOUND:int = -1;
		
		// @variables
	
		// Core.
		protected var _index:int;
		protected var _indexMin:uint;
		protected var _indexMax:uint;
		protected var _offset:uint;
		protected var _tweening:Boolean;
		protected var _ignoreCase:Boolean;
		
		// Structure.
		protected var _steps:Array;
		protected var _intro:FrameLabel;
		protected var _content:FrameLabel;
		protected var _outro:FrameLabel;
		
		// Status.
		protected var _available:Boolean;
		protected var _showContentAfterIntro:Boolean;
		
		// History
		protected var _history:IHistory; 
		
		// @constructor
		
		public function KCComponentSteps(data:XML = null, autorelease:Boolean = true) {
			super( data, autorelease );
		}
		
		// @override
		
		override public function purge(...rest:*):void {
			PurgerUtil.cleanCollection( this._steps );
			this._history.purge();
			this._index = undefined;
			this._indexMin = undefined;
			this._indexMax = undefined;
			this._offset = undefined;
			this._tweening = undefined;
			this._ignoreCase = undefined;
			this._available = undefined;
			this._showContentAfterIntro = undefined;
			this._steps = null;
			this._intro = null;
			this._content = null;
			this._outro = null;
			this._history = null;
			super.purge();
		}

		override protected function $config(e:Event):void {
			
			super.$config( e );
			
			this._history = new SimpleHistory( 50 );
						
			this._ignoreCase = true;
			this._showContentAfterIntro = true;
			
			Validate();
			
		}
		
		protected function Validate():void {
			
			var frame:FrameLabel;
			var frameName:String;
			
			this._steps = new Array();
			
			for( var a:int=0; a < this.currentLabels.length; a++ ){
				frame = this.currentLabels[a] as FrameLabel;
				frameName = frame.name.toLowerCase();
				switch( frameName ){
					case DEFAULT_LABEL_INTRO:
					case DEFAULT_LABEL_CONTENT:
					case DEFAULT_LABEL_OUTRO:
						this["_"+frameName] = frame;
						break;
					default:
						this._steps.push( frame );
				}
			}
			
			if( ! this._content )
				ExceptionUtil.ViewError( ERROR_NOT_DEFINED_CONTENT );
				
			if( this._content.frame == 1 )
				ExceptionUtil.ViewError( ERROR_DEFINED_CONTENT_ON_FIRST_FRAME );
				
			this._available = true;
			this._offset = this._content.frame - 1;
			this._indexMin = 1;
			
			if( this._steps.length ){
				this._indexMax = this._steps.length;
			}else if( this._outro != null ){
				this._indexMax = ( this._outro.frame - 1 ) - this._offset;
			} else {
				this._indexMax = this.totalFrames - this._offset;
			}
			
			if ( this._intro != null ) {
				ResolveStepScript( 
					( this._offset - 1 ), 
					FinishedIntro 
				);
			}
			
			if ( this._outro != null ) {
				ResolveStepScript( 
					( this.totalFrames - 1 ), 
					FinishedOutro 
				);
			}
			
			this.dispatchEvent( 
				new KCComponentStepsEvent( 
					KCComponentStepsEvent.AVAILABLE
				) 
			);		
			
		}
		
		protected function FinishedIntro():void {
			this.stop();			
			this.dispatchEvent( 
				new KCComponentStepsEvent( 
					KCComponentStepsEvent.INTRO_FINISHED 
				) 
			);			
			if ( this._showContentAfterIntro ) {
				this.content();
			}			
		}
		
		protected function FinishedOutro():void {
			this.stop();
			this.dispatchEvent( 
				new KCComponentStepsEvent( 
					KCComponentStepsEvent.OUTRO_FINISHED 
				) 
			);
		}
		
		// @properties (rw)
		
		public function get label():String {
			ThrowNotSupportLabels();
			return ( this._steps && this._index > 0 ) 
				? FrameLabel( this._steps[ this._index - 1 ] ).name
				: null;
		}
		
		public function set label( value:String ):void {
			ThrowNotSupportLabels();
			var i:int = ResolveStepLabel( value, this._ignoreCase );
			if( i != NOT_FOUND )
				GoTo( i + 1 );
		}
		
		public function get index():uint {
			return this._index;
		}
		
		public function set index( value:uint ):void {
			GoTo( value );
		}
		
		public function get tweening():Boolean {
			return this._tweening;
		}
		
		public function set tweening( value:Boolean ):void {
			this._tweening = value;
		}
		
		public function get showContentAfterIntro():Boolean {
			return this._showContentAfterIntro;
		}
		
		public function set showContentAfterIntro( value:Boolean ):void {
			this._showContentAfterIntro = value;
		}
		
		public function get ignoreCase():Boolean {
			return this._ignoreCase;
		}
		
		public function set ignoreCase( value:Boolean ):void {
			this._ignoreCase = value;
		}
		
		// @properties (r)
		
		public function get available():Boolean {
			return this._available;
		}
		
		public function get offset():uint {
			return this._offset;		
		}
		
		public function get steps():uint {
			return this._indexMax;
		}
		
		public function get labels():Array {
			ThrowNotSupportLabels();
			return this._steps;
		}
		
		public function get history():IHistory {
			return this._history;
		}
		
		// @methods
		
		public function intro():void {
			if ( ! this.hasIntro() ) {
				this.content();
				return;
			}
			this._index = 0;
			this.gotoAndPlay( this._intro.frame );
			this.dispatchEvent( 
				new KCComponentStepsEvent( 
					KCComponentStepsEvent.INTRO_BEGINS 
				) 
			);
		}
		
		public function content():void {
			if ( this._content == null ) return;
			this.firstStep();
		}
		
		public function outro():void {
			if ( ! this.hasOutro() ) return;
			this._index = 0;
			this.gotoAndPlay( this._outro.frame );
			this.dispatchEvent( 
				new KCComponentStepsEvent( 
					KCComponentStepsEvent.OUTRO_BEGINS 
				) 
			);
		}
		
		public function firstStep():uint {
			return GoTo( this._indexMin );
		}
		
		public function prevStep():uint {
			var i:uint = this._index;
			if( this.hasPrevStep() ){
				this._index --;
				i = GoTo( this._index );
			} return i;
		}
		
		public function nextStep():uint {
			var i:uint = this._index;
			if( this.hasNextStep() ){
				this._index ++;
				i = GoTo( this._index );
			} return i;
		}
		
		public function lastStep():uint {
			return GoTo( this._indexMax );
		} 
		
		protected function GoTo( value:uint, ignoreHistory:Boolean = false ):uint {
			
			this.dispatchEvent( 
				new KCComponentStepsEvent( 
					KCComponentStepsEvent.BEFORE_CHANGE 
				) 
			);
			
			this._index = uint( 
				Math.min( 
					this._indexMax, 
					Math.max( 
						this._indexMin, 
						value 
					) 
				) 
			);
			
			if( ! ignoreHistory ) {
				this._history.add( this._index );
			} 
			
			if ( this._steps.length ) {
				value = this._steps[this._index - 1].frame;
			}else {
				value = this._index + this._offset;
			}
			
			if ( ! this._tweening ) {
				this.gotoAndStop( value );
			}else {
				this.gotoAndPlay( value );
			}
			
			this.dispatchEvent( 
				new KCComponentStepsEvent( 
					KCComponentStepsEvent.AFTER_CHANGE 
				) 
			); 
			
			return this._index;
			
		}
		
		// @has
		
		public function hasIntro():Boolean {
			return ( this._intro != null && this._available );
		}
		
		public function hasOutro():Boolean {
			return ( this._outro != null && this._available );
		} 
		
		public function hasPrevStep():Boolean {
			return ( this._index > this._indexMin );
		}
		
		public function hasNextStep():Boolean {
			return ( this._index < this._indexMax );
		}  
		
		public function hasLabel( value:String, ignoreCase:Boolean = true ):Boolean {
			return ( ResolveStepLabel( value, ignoreCase ) > NOT_FOUND );
		}
		
		// @history
		
		public function back():void {
			GoTo( this._history.back(), true );
		}
		
		public function forward():void {
			GoTo( this._history.forward(), true );
		}
		
		// @scripts
		
		public function addStepScript( frame:*, method:Function ):void {			
			ResolveStepScript( frame, method );			
		}
		
		public function removeStepScript( frame:* ):void {			
			ResolveStepScript( frame );			
		} 
		
		protected function ResolveStepScript( frame:*, method:Function = null ):void {
			
			if ( ! frame is Number && ! frame is String 
				|| ( frame is Number && ( frame < 1 || frame > this.totalFrames ) ) ) 
			{ 
				return;
			} else if ( frame is String ) {
				var a:int = ResolveStepLabel( frame, this._ignoreCase );
				if( a != NOT_FOUND ) {
					frame = this._steps[a].frame;
				}else{
					 return;
				}
			}
			
			this.addFrameScript( frame, method );
			
		}
		
		protected function ResolveStepLabel( value:String, ignoreCase:Boolean = true ):int {
			var label:String;
			for( var a:int = 0; a < this._steps.length; a++ ){
				label = FrameLabel( this._steps[a] ).name;
				if( ( ignoreCase && value.toLowerCase() == label.toLowerCase() ) 
					|| ( ! ignoreCase && value == label ) ) 
				{
					return a;
				}
			} return NOT_FOUND;
		}
		
		// @helper
		
		protected function ThrowNotSupportLabels():void {
			if( ! this._steps ) {
				ExceptionUtil.ViewError( ERROR_NOT_SUPPORT_LABELS );
			}
		}
		
	}
	
}
