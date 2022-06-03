package activia.simon.shooter.ui.screens {
	import activia.simon.shooter.core.DataLayer;
	import activia.simon.shooter.core.FacebookUtil;
	import activia.simon.shooter.core.Localization;
	import activia.simon.shooter.ui.AbstractScreen;
	import activia.simon.shooter.ui.assets.RankingCell;

	import pq.log.Debugger;
	import pq.ui.BasicButton;
	import pq.utils.StringUtil;

	import com.emc2zen.serverside.Conexion;
	import com.emc2zen.serverside.ConexionEvent;

	import flash.events.ErrorEvent;
	import flash.events.Event;
	import flash.events.IOErrorEvent;
	import flash.events.MouseEvent;
	import flash.events.SecurityErrorEvent;
	import flash.net.URLRequest;
	import flash.net.navigateToURL;

	public class GRanking extends AbstractScreen {

		private var _cnx:Conexion;

		public function GRanking() {
			super();
		}

		public override function init():void {

			if ( this._status ) return;
			super.init();

		}

		private function get errorLabel():Localization {
			if ( this.index > 1 ) return null;
			return Localization( this.getChildByName( "mcError" ) );
		}

		protected override function ApplyActions():void {

			if ( this.index == this.size ) {

				this.CreateRanking();

				if ( DataLayer.isFacebook() ) {
					BasicButton(this.getChildByName("btFacebookShare")).visible = true;
					BasicButton(this.getChildByName("btFacebookWall")).visible = true;
				} else {
					BasicButton(this.getChildByName("btFacebook")).visible = true;
					BasicButton(this.getChildByName("btTwitter")).visible = true;
				}

			} else {
				this.GetRankingXML();
			}

			super.ApplyActions();

		}

		protected override function ButtonsManager( e:MouseEvent ):void {

			var name:String = e.target.name;

			switch ( name ) {

				case "btFacebook":
				case "btTwitter":
					this.ResolveSocialNetworks( name.substring( 2 ) );
					break;

				case "btFacebookShare":
					FacebookUtil.getInstance().resolveXML( XML( DataLayer.CONFIG_GAME.facebook.share ) );
					break;

				case "btFacebookWall":
					FacebookUtil.getInstance().resolveXML( XML( DataLayer.CONFIG_GAME.facebook.wall ) );
					break;

			}

		}

		private function GetRankingXML():void {

			var data:XMLList = DataLayer.CONFIG_GAME.serverSide.ranking;
			Debugger.DEBUG( this, this.index, this.label, data );

			this._cnx = new Conexion();
			this._cnx.method = "POST";
			this._cnx.addEventListener( ConexionEvent.COMPLETE, CompleteHandler );
			this._cnx.addEventListener( IOErrorEvent.IO_ERROR, ErrorHandler );
			this._cnx.addEventListener( SecurityErrorEvent.SECURITY_ERROR, ErrorHandler );
			this._cnx.send( DataLayer.CONFIG.dependency( data.url.text() ) );
			Debugger.INFO( this, DataLayer.CONFIG.dependency( data.url.text() ) );

			errorLabel.update();

		}

		private function CreateRanking():void{

			var mypos:uint 		= uint( DataLayer.collection.value( "score_position" ) );
			var myname:String 	= String( DataLayer.collection.value( "score_name" ) );
			var myscore:uint 	= uint( DataLayer.collection.value( "score_value" ) );

			var pattern:String = DataLayer.CONFIG_GAME.serverSide.ranking.pattern.text();

			if ( mypos > 6 ) {
				this.data.ranking.replace(
					this.data.ranking.record.length() - 1,
					new XML(
						StringUtil.substitute(
							pattern,
							mypos,
							myscore,
							myname
						)
					)
				);
				mypos = this.data.ranking.record.length();
			}

			mypos--;

			var cell:RankingCell = RankingCell( this.getChildByName( "mcCell" ) );
			var x:Number = cell.x;
			var y:Number = cell.y;
			this.removeChild( cell );

			var node:XML;
			var pos:XMLList = this.data.ranking..record;

			Debugger.DEBUG( this, mypos, pos );

			for ( var a:uint = 0; a < pos.length(); a++ ) {

				node = pos[a];

				cell = new RankingCell();
				cell.data = XML( Localization.getNodeData( "lbGRankingCell" ).toString() );
				cell.positionNumber = node.@id;
				cell.positionName = node.text();
				cell.positionScore = node.@score;
				cell.align( x, y + ( ( cell.height + Number( cell.data.@offset ) ) * a ) );

				if ( a == mypos ) cell.myPosition();

				this.addChild( cell );

			}

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

			Debugger.INFO( this, "Ranking", e.property );

			if ( e.property.search(/^\d+$/) > -1 ) {

				ResolveError( Number( e.property ) );
				//this.dispatchEvent( new ErrorEvent( ErrorEvent.ERROR ) );

			}else {

				this.data = new XML( e.property );
				Debugger.DEBUG( this, this.data );

				this.nextStep();
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

		private function ResolveSocialNetworks( value:String ):void{

			var node:XMLList = DataLayer.CONFIG_GAME.socialNetworks[ value.toLowerCase() ];
			
			Debugger.INFO( 
				this, 
				node, 
				node.message.text().toString(), 
				DataLayer.CONFIG.dependency( node.message.text().toString() ),
				this.ResolveReplace( DataLayer.CONFIG.dependency( node.message.text().toString() ), node )
			);			
			
			var message:String = DataLayer.CONFIG.dependency( node.message.text().toString() );
			
			if ( value.toLowerCase() != "facebook" ) {
				message = encodeURIComponent( message ).replace( /(\%40)/g, "@" );
			}
			
			navigateToURL(
				new URLRequest(
					this.ResolveReplace(
						message,
						node
					)
				),
				node.@target.toString()
			);

		}

		private function ResolveReplace( value:String, node:XMLList ):String {

			var rexp:RegExp = /\@[A-Za-z]([\w]*)([\_\-]?([\w]*))*\@/g;
			
			if ( value.search( rexp ) > -1 ) {
				var key:String;
				var property:String;
				var list:Array = value.match( rexp );
				for ( var a:uint = 0; a < list.length; a++ ) {
					property = list[a];
					key = node..replace.( @id == property );
					if ( DataLayer.collection.contain( key ) ) {
						value = value.replace( property, DataLayer.collection.value( key ) );
					}else {
						value = value.replace( property, key );
					}
				}
			}

			return value;

		}

	}

}