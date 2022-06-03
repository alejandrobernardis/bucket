package activia.simon.shooter.core {
	import pq.log.Debugger;
	import pq.utils.StringUtil;

	import com.emc2zen.util.ClassUtil;

	import flash.display.MovieClip;
	import flash.events.Event;
	import flash.text.TextField;
	import flash.text.TextFormat;
	
	
	public class Localization extends MovieClip {
		
		private static var $data:XML = null;
		
		public function Localization() {
			super();
			this.visible = false;
			this.addEventListener( Event.ADDED_TO_STAGE, $config, false, 0, true );
		}
		
		public function get data():XMLList {
			return Localization.$data.child( ClassUtil.shortName( this ) ); 
		}
		
		public function labels():Array {
			var text:TextField;
			var result:Array = new Array();
			for ( var a:uint = 0; a < this.numChildren; a++ ) {
				if ( this.getChildAt( a ) is TextField ) {
					text = TextField( this.getChildAt( a ) );
					result.push( { label:text.name, value:text.htmlText } );
				}
			}
			return result;
		}
		
		/*Metodo util para localizacion con replace*/
		
		public function update():void {
			this.$config();
		}
		
		public function labelForce( label:String, value:String ):void {
			if ( this.getChildByName( label ) as TextField ) {
				TextField( this.getChildByName( label ) ).htmlText = value;
			}
		}
		
		private function $config( e:Event = null ):void {
			
			var text:TextField;	
			var id:String = ClassUtil.shortName( this );
			
			if ( Localization.$data.hasOwnProperty( id ) ) {
				
				var list:XMLList = Localization.$data.child( id );
				
				this.x = ( ! StringUtil.isEmpty( list.@x ) ) ? Number( list.@x ) : this.x;
				this.y = ( ! StringUtil.isEmpty( list.@y ) ) ? Number( list.@y ) : this.y;
				
				for ( var a:uint = 0; a < this.numChildren; a++ ) {
					if ( this.getChildAt( a ) is TextField ) {
						text = TextField( this.getChildAt( a ) );
						if ( ! StringUtil.isEmpty( text.name ) && ! StringUtil.hasWhiteSpace( text.name ) ) {
							Localization.localize( text, text.name, list );
						}
					}
				}
				
			}
			
			if ( e != null ) {
				this.removeEventListener( Event.ADDED_TO_STAGE, $config );
			}
			
			this.visible = true;
			
		}
		
		/**
		 * @Static
		 */
		
		public static function localize( text:TextField, label:String, node:XMLList = null ):void {
			
			if ( node == null && Localization.$data.hasOwnProperty( ClassUtil.shortName( text.parent ) ) ) {
				node = Localization.$data.child(ClassUtil.shortName( text.parent ));
			}
			
			if( node.hasOwnProperty( label ) ){
				
				text.text = "";
				
				var value:XMLList = node.child( label );
				var list:XMLList = value.attributes();
				var format:TextFormat = text.defaultTextFormat; 
				var caseType:String = new String();
				
				for ( var a:uint = 0; a < list.length(); a++ ) {
					if ( ! StringUtil.isEmpty( list[a] ) ) {
						var name:String = String( list[a].name() );
						if ( format.hasOwnProperty( name ) ) {
							format[ name ] = ResolveValue( list[a] );
						} else if ( text.hasOwnProperty( name ) ) {
							text[ name ] = ResolveValue( list[a] );
						} else if( name.toLowerCase() == "case" ) {
							caseType = list[a].toLowerCase();
						}
					}
				}
				
				
				text.htmlText = ResolveCase( 
					ResolveReplace( 
						value.text(), 
						node 
					), 
					caseType 
				);
				
				Debugger.INFO( text.parent, text.htmlText );				
				text.setTextFormat( format );
				
			}
			
		}
		
		public static function getNodeData( node:String ):XMLList {
			
			if ( ! Localization.$data.hasOwnProperty( node ) ) {
				return null;
			}
			
			return Localization.$data.child( node );
		}
		
		public static function data( value:XML ):void {
			$data = value;
			Debugger.DEBUG( Localization, value );
		}
		
		public static function purge( ...rest ):void {
			$data = null;
		} 
		
		private static function ResolveCase( value:String, caseType:String ):String {
			if( StringUtil.isEmpty( caseType ) ) return value;
            return ( caseType != "lower" ) ? value.toUpperCase() : value.toLowerCase();
		}
		
		private static function ResolveReplace( value:String, node:XMLList ):String {
			
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
					}					
				}				
			}
			
			return value;
			
		}
		
		private static function ResolveValue( value:String ):* {
			
			value = StringUtil.stripWhiteSpace( value );
			
			if ( value.search( /^(0x)([A-Fa-f0-9]{6})$/ ) > -1 ) {
				return parseInt( value, 16 );
			} else if ( value.search( /^([\-\+]?\d*[\.]?\d*|[\.]\d*)$/ ) > -1 ) {
				return Number( value );
			} else if ( value.search( /^(true|false)$/ ) > -1 ) {
				return ( value == "true" );
			} else if ( value.search( /^[a-z]*$/ ) > -1 ) {
				return value;
			}
			
			return null;
			
		}
		
	}
	
}
