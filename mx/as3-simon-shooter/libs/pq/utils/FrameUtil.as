
package pq.utils {
	
	import flash.display.FrameLabel;
	import flash.display.MovieClip;
	import flash.errors.IllegalOperationError;
	
	import pq.core.CoreStatic;

	public final class FrameUtil extends CoreStatic {
		
		public static function addScript( path:MovieClip, frame:*, handler:Function, EOL:Boolean = false ):void {
			
			if( frame is String ){
				path.addFrameScript( FrameUtil.resolveLabelAsNumber( path, frame, EOL ), handler );
			}else if( frame is uint ){
				path.addFrameScript( frame, handler );
			}else{
				throw new IllegalOperationError( "El parametro \"frame\", debe ser de tipo \"String\" o \"uint\", y mayor a cero en caso del utimo tipo." );			
			}
			
		}
		
		public static function resolveLabelAsNumber( path:MovieClip, label:String, EOL:Boolean = false ):uint {
			
			var a:uint;
			var list:Array = path.currentLabels;
			var fLabel:FrameLabel;
			var pLabel:Boolean = false;
			
			for( a = 0; a < list.length; a++ ){
				
				fLabel = list[a];
				
				if( EOL ){
					if( pLabel && fLabel.name != label ){
						return fLabel.frame - 1;
					}else if( fLabel.frame == path.totalFrames ){
						return fLabel.frame;
					}else if( fLabel.name == label ){
						pLabel = true;
					}
				}else if( fLabel.name == label ){
					return fLabel.frame;
				}
				
			}
			
			return 0;
			
		}
		
	}
	
}