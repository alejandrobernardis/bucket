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
	
	import com.emc2zen.util.ClassUtil;
	import com.emc2zen.util.TypeUtil;
	
	/**
	 * Modelo basico y abstracto de un objeto statico.
	 * @author	PollyJex 
	 * @example
	 * 
	 * <listing version="3.0" >
	 * // CLASS
	 * 
	 * package com.emc2zen.util {
	 * 	
	 * 	import com.emc2zen.com.CoreAbstractStatic;
	 * 
	 * 	public class StringUtil extends CoreAbstractStatic {
	 * 
	 * 		public static function remove( source:String, value:String ):String {
	 * 			return new String( "ACTIONS!" );
	 * 		}
	 * 
	 * 	}
	 * 
	 * }
	 * 
	 * 
	 * // BAD USAGE:
	 * 
	 * var a:StringUtil = new StringUtil();
	 * a.remove( "My name is PJX", "PJX" );
	 * 
	 * // trace output: 
	 * Illegal instantiation attempted on class of static type: StringUtil in Sprite. 
	 * 
	 * 
	 * // GOOD USAGE:
	 * 
	 * StringUtil.remove( "My name is PJX", "PJX" );
	 * </listing>
	 */
	public class CoreStatic {
		
		
		/**
		 * Mensaje de error de tipo STATIC.
		 */
		private static const MESSAGE_ERROR:String = "Illegal instantiation attempted on class of static type: ";
		
		
		
		/**
		 * Constructor.
		 * @param	value		Instancia de una clase.
		 * @param	message		Mensaje alternativo.
		 * @return	CoreStatic 
		 */
		public function CoreStatic( value:* = null, message:String = null ) {
			
			if( TypeUtil.isNull( value ) ){
				value = this;
			}
			
			if( TypeUtil.isNull( message ) ){
				message = MESSAGE_ERROR;
			}
			
			var exception:Error = new Error();
			
			exception.message = message + 
									// class static (super)
									ClassUtil.shortName( value ) + " in " +
										// class execute (child)
										exception.getStackTrace().split("at ").pop().toString().split("$")[0];
			
            throw exception;
			
		}
		
	}
	
}
