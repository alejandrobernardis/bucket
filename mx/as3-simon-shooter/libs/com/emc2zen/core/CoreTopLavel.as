/**
* @private
* @license	GNU GPLv2
*
* Copyright (C) 2007  Polly Jex.
* 
* This program is free software; you can redistribute it and/or
* modify it under the terms of the GNU General Public License
* as published by the Free Software Foundation; either version 2
* of the License, or (at your option) any later version.
* 
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU General Public License for more details.
* 
* You should have received a copy of the GNU General Public License
* along with this program; if not, write to the Free Software
* Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, 
* MA  02110-1301, USA.
*
* @see	http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

package com.emc2zen.core {

	/**
	* @import
	*/

	import com.emc2zen.core.CoreInterface;
	import flash.display.DisplayObject;
	import flash.display.MovieClip;
	import flash.display.Stage;

	/**
	* Retine las referencias del STAGE y del ROOT para acceso global, es una alternativa al ser eliminadas _level0 y _root en AS3.
	* @author	PollyJex
	*/
	public class CoreTopLavel extends MovieClip implements CoreInterface {
		
		/**
		* Referencia del STAGE.
		*/
		public static var stage:Stage;
		
		/**
		* Referencia del ROOT.
		*/
		public static var root:DisplayObject;
		
		/**
		* Constructor.
		* @param	stage	Replica de la instancia del Stage.
		* @param	root	Replica de la instancia del Sprite.
		* @return	CoreTopLavel
		*/
		public function CoreTopLavel( stage:Stage, root:DisplayObject ) {
			
			super();
			
			CoreTopLavel.stage = stage;
			CoreTopLavel.root = root;
			
		}
		
	}
	
}
