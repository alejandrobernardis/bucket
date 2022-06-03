package activia.simon.shooter.ui.screens {
	import activia.simon.shooter.core.DataLayer;
	import activia.simon.shooter.core.Localization;
	import activia.simon.shooter.ui.AbstractScreen;

	import pq.log.Debugger;
	import pq.utils.Hasher;
	import pq.utils.StringUtil;

	import com.emc2zen.serverside.Conexion;
	import com.emc2zen.serverside.ConexionEvent;

	import flash.events.ErrorEvent;
	import flash.events.Event;
	import flash.events.IOErrorEvent;
	import flash.events.KeyboardEvent;
	import flash.events.MouseEvent;
	import flash.events.SecurityErrorEvent;
	import flash.text.TextField;
	import flash.ui.Keyboard;

	public class GScoreRegiste extends AbstractScreen {
		
		private var _cnx:Conexion;
		
		public function GScoreRegiste() {
			super();
		}
		
		protected override function ApplyActions():void {
			this.reset();			
			super.ApplyActions();
			this.stage.addEventListener( KeyboardEvent.KEY_UP, KeyboardManager );
		}
		
		protected override function RemoveActions():void {
			super.RemoveActions();
			this.stage.removeEventListener( KeyboardEvent.KEY_UP, KeyboardManager );
		}
		
		private function reset():void {
			
			var score_name:String = String( DataLayer.collection.value( "score_name" ) );
			
			this.scoreName.text = ( ! StringUtil.isEmpty( score_name ) && score_name != "@NN@" ) 
								? score_name
									: "" ;
			
			this.stage.focus = this.scoreName;			
			this.errorLabel.update();
			
		}
		
		private function get errorLabel():Localization {
			return Localization( this.getChildByName( "mcError" ) );
		}
		
		private function get scoreName():TextField {
			return TextField( this.getChildByName( "txScoreName" ) );
		}
		
		private function KeyboardManager( e:KeyboardEvent ):void {
			
			if ( KeyboardEvent( e ).keyCode != Keyboard.ENTER ) {
				return;
			}
			
			this.SendScore();
			
		}
		
		protected override function ButtonsManager( e:MouseEvent ):void {
			switch ( e.target.name ) {				
				case "btSend":
					this.SendScore();
					break;					
			}
		}
		
		private function SendScore():void {
			
			if ( StringUtil.isEmpty( this.scoreName.text ) ) {
				this.ResolveError( "validateName" );
				return;				
			}
			
			this.ResolveError( "sending" );
			
			var data:XMLList = DataLayer.CONFIG_GAME.serverSide.scoreregiste;			
			DataLayer.collection.update( "score_name", this.scoreName.text );
			Debugger.DEBUG( this, data );
			
			this._cnx = new Conexion();
			this._cnx.method = "POST";
			this._cnx.addEventListener( ConexionEvent.COMPLETE, CompleteHandler );			
			this._cnx.addEventListener( IOErrorEvent.IO_ERROR, ErrorHandler );
			this._cnx.addEventListener( SecurityErrorEvent.SECURITY_ERROR, ErrorHandler ); 
			
			var code:String = new String();
			var param:XMLList = data..param;
			
			Debugger.DEBUG( this, param );
			
			for each( var node:XML in param ) {				
				code += node.text().toString() + "=" + DataLayer.collection.value( node.@id.toString() ) + "&";
			}
			
			this._cnx.code = Hasher.encode( code );			
			this._cnx.send( DataLayer.CONFIG.dependency( data.url.text() ) );
			
			Debugger.INFO( this, DataLayer.CONFIG.dependency( data.url.text() ) );			
			Debugger.DEBUG( this, code, Hasher.encode( code ) );
			
		}
		
		private function ClearHandler( e:Event ):void {
			this._cnx.removeEventListener( ConexionEvent.COMPLETE, CompleteHandler );
			this._cnx.removeEventListener( IOErrorEvent.IO_ERROR, ErrorHandler );
			this._cnx.removeEventListener( SecurityErrorEvent.SECURITY_ERROR, ErrorHandler );
			this._cnx = null;
		}
		
		private function ErrorHandler( e:ErrorEvent ):void {
			this.dispatchEvent( new ErrorEvent( ErrorEvent.ERROR, false, false, e.text ) );	
			this.ClearHandler(e);
		}
		
		private function CompleteHandler( e:ConexionEvent ):void {
			
			Debugger.INFO( this, "ScoreRegiste", e.property );
			
			if ( e.property.search(/^\d+$/) > -1 ) {				
				ResolveError( Number( e.property ) );
				//this.dispatchEvent( new ErrorEvent( ErrorEvent.ERROR ) );
			}else {				
				this.RemoveActions();
				DataLayer.collection.update( "score_position", new XML( e.property ).children().( @id == "position" ).toString() );
				DataLayer.SCREEN.sRanking();				
				this.dispatchEvent( new Event( Event.COMPLETE ) );				
			}
			
			this.ClearHandler(e);
			
		}
		
		private function ResolveError( value:* = -1 ):void {
			
			if ( ! value is String && ! value is Number ) return;
			
			var error:String;
			
			if ( value is Number ) {
				switch( value ) {
					case 1:
					case 2:
						error = "error" + value;
						break;
					default:
						error = "uncontrolledError";
				}
			} else {
				error = value;
			}
			
			Debugger.INFO( this, value, errorLabel.data[ error ].text().toString() );
			errorLabel.labelForce( "label", errorLabel.data[ error ].text().toString() );
			
		}
		
	}
	
}