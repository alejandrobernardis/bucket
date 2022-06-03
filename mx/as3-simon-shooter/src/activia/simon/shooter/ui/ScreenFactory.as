/* TODO: Modificar la logica y que funcione como contenedor. */
package activia.simon.shooter.ui {
	import activia.simon.shooter.core.DataLayer;
	import activia.simon.shooter.core.FacebookUtil;
	import activia.simon.shooter.events.ScreenFactoryEvent;
	import activia.simon.shooter.ui.assets.Header;

	import pq.log.Debugger;
	import pq.ui.Position;
	import pq.ui.UIComponent;
	import pq.utils.ClassUtil;

	import flash.display.MovieClip;
	import flash.external.ExternalInterface;
	import flash.net.URLRequest;
	import flash.net.navigateToURL;
	import flash.utils.describeType;
	
	
	[Event(name="add", type="activia.simon.shooter.events.ScreenFactoryEvent")]
	[Event(name="remove", type="activia.simon.shooter.events.ScreenFactoryEvent")]
	[Event(name="replace", type="activia.simon.shooter.events.ScreenFactoryEvent")]
	
	public class ScreenFactory extends UIComponent implements IScreenFactory {
		
		public static const ADD_VALUE:int = 1;
		public static const REMOVE_VALUE:int = -1;
		public static const REPLACE_VALUE:int = 0;
		
		private var _screens:ScreensStack;
		private var _screenX:Number;
		private var _screenY:Number;
		private var _isPlaying:Boolean;
		
		public function ScreenFactory() {
			
			super();
			
			if( DataLayer.CONFIG_GAME != null  ) {
				var axis:Position = new Position( DataLayer.CONFIG_GAME..config.canvas.axis.text() );
				this._screenX = axis.x;
				this._screenY = axis.y;	
			} 
			
			this._screens = new ScreensStack( 2 );
			
		}
		
		/*
		 * Api
		 */
		
		public function add( value:String ):void {	
			
			Debugger.DEBUG( this, "Add", this._screens.isEmpty(), this._screens.toArray() );
			
			if ( this._screens.availableCapacity() == 0 ) {
				remove();
			}
			
			this._screens.push( ResolveController( value ) );
			ResolveAdd( ScreenFactory.ADD_VALUE );
			
		}
		
		public function remove():void {
			
			if ( this._screens.isEmpty() ) return;
			
			Debugger.DEBUG( this, "RemoveBefore", this._screens.toArray() );
			
			this.dispatchEvent( new ScreenFactoryEvent( ScreenFactoryEvent.REMOVE_SCREEN ) );
			
			var screen:Screen = this._screens.pop() as Screen;
			screen.destroy();
			
			DataLayer.SCOPE.removeChild( MovieClip( screen ) );			
			screen = null;
			
			Debugger.DEBUG( this, "RemoveAfter", this._screens.toArray() );
			
		}
		
		public function replace( value:String ):void {
			
			Debugger.DEBUG( this, "Replace", this._screens.isEmpty(), this._screens.toArray() );
			
			remove();
			
			this._screens.push( ResolveController( value ) );
			ResolveAdd( ScreenFactory.REPLACE_VALUE );
			
		}
		
		/*
		 * Helpers 
		 */
		
		public function get content():Screen {
			return this._screens.top() as Screen;
		}
		
		public function get screens():ScreensStack {
			return this._screens;
		}
		
		public function get quantity():uint {
			return this._screens.size();
		}
		
		public function get isPlaying():Boolean {
			return this._isPlaying;
		}
		
		/*
		 * Secciones disponible, no se pueden agregar desde el XML.
		 * -1:	Remove
		 *  0: 	Add
		 *  1:	Replace
		 */	
		
		public function sHome( action:int = 0 ):void {
			this.ResolveSection( DataLayer.CONFIG_GAME..screens.screen.( @id == "home" ).@controller, action );
		}
		
		public function sInstructions( action:int = 0 ):void {
			this.ResolveSection( DataLayer.CONFIG_GAME..screens.screen.( @id == "instructions" ).@controller, action );
		}
		
		public function sGame( action:int = 0 ):void {
			this.ResolveSection( DataLayer.CONFIG_GAME..screens.screen.( @id == "game" ).@controller, action );
		}
		
		public function sGameOver( action:int = 0 ):void {
			this.ResolveSection( DataLayer.CONFIG_GAME..screens.screen.( @id == "gameover" ).@controller, action );
		}
		
		public function sGameExit( action:int = 0 ):void {
			this.ResolveSection( DataLayer.CONFIG_GAME..screens.screen.( @id == "gameexit" ).@controller, action );
		}
		
		public function sScoreRegiste( action:int = 0 ):void {
			this.ResolveSection( DataLayer.CONFIG_GAME..screens.screen.( @id == "scoreregiste" ).@controller, action );
		}
		
		public function sRanking( action:int = 0 ):void {
			this.ResolveSection( DataLayer.CONFIG_GAME..screens.screen.( @id == "ranking" ).@controller, action );
		}
		
		public override function purge( ...rest ):void {
			while ( this._screens.isEmpty() ) remove();
			this._screens.clear();
			this._screens = null;
			this._screenX = undefined;
			this._screenY = undefined;
			super.purge();
		}
		
		public function exit():void {
			if ( ! DataLayer.isFacebook() ) {
				this.resolveExternal( XML( DataLayer.CONFIG_GAME.exit.action.( @id == "standalone" ) ) );
			} else {
				FacebookUtil.getInstance().resolveXML( XML( DataLayer.CONFIG_GAME.exit.action.( @id == "facebook" ) ) );
			}
		}
		
		public function resolveExternal( value:XML ):void {
			
			Debugger.INFO( this, "external", value );
			
			if ( value.text().toString().search( /^js\:\/\// ) > -1 ) {
				
				var js:String = value.text().toString().replace( /^js\:\/\//, "" );
				ExternalInterface.call( js );
				Debugger.DEBUG( this, "js-external:", value, js );
				
			} else {
				
				navigateToURL( 
					new URLRequest( value.text().toString() ),
					value.@target
				);
				
				Debugger.DEBUG( this, "http-external:", value );
				
			}
		}
		
		/*
		 * @Helpers
		 */
		
		private function ResolveSection( controller:String, action:int ):void {
			switch ( action ) {
				case ScreenFactory.REMOVE_VALUE:
					if( ResolveRemove( controller ) ) remove();
					break;
				case ScreenFactory.ADD_VALUE:
					add( controller );
					break;
				case ScreenFactory.REPLACE_VALUE:
				default:
					if ( controller != DataLayer.CONFIG_GAME..screens.screen.( @id == "game" ).@controller ) {
						this._isPlaying = false;
					} else {
						this._isPlaying = true;
					}
					ResolveHeader( controller );
					replace( controller );
			}
		}
		
		private function ResolveHeader( controller:String ):void {
			
			var header:Header = Header( DataLayer.SCOPE.getChildByName("mcHeader") ); 
			
			if ( controller == DataLayer.CONFIG_GAME..screens.screen.( @id == "game" ).@controller ) {
				header.index = 2;
			} else if ( controller == DataLayer.CONFIG_GAME..screens.screen.( @id == "gameover" ).@controller 
							|| controller == DataLayer.CONFIG_GAME..screens.screen.( @id == "scoreregiste" ).@controller ) {
				header.index = 3;
			} else if ( controller == DataLayer.CONFIG_GAME..screens.screen.( @id == "ranking" ).@controller ) {
				header.index = 4;
			} else {
				header.index = 1;
			}
			
		}
		
		private function ResolveController( controller:String ):Screen {
			return ClassUtil.create( ResolveClass( controller ) ) as Screen;
		}
		
		private function ResolveClass( value:* ):String {
			if ( value is String ) {
				return ( value.search( /^(activia\.simon\.shooter\.ui\.screens\:\:)([A-Za-z]([\w])*)$/ ) < 0 )
					? "activia.simon.shooter.ui.screens::" + value 
						: value;
			}
			return describeType( value ).@name;
		}
		
		private function ResolveRemove( controller:String ):Boolean {
			if ( this._screens.isEmpty() ) return false;
			return ( ResolveClass( controller ) == ResolveClass( this._screens.top() as Screen ) );
		}
		
		private function ResolveAdd( value:uint = 0 ):void{
			
			Debugger.DEBUG( this, "ResolveAdd", this._screens.isEmpty(), this._screens.toArray() );
			
			var screen:Screen = this._screens.top() as Screen;
			screen.align( this._screenX, this._screenY );
			screen.init();
			
			DataLayer.SCOPE.addChild( MovieClip( screen ) );
			
			var type:String = ( value == ScreenFactory.REPLACE_VALUE ) ? ScreenFactoryEvent.REPLACE_SCREEN : ScreenFactoryEvent.ADD_SCREEN;
			this.dispatchEvent( new ScreenFactoryEvent( type ) );
			
		}
		
	}
	
}