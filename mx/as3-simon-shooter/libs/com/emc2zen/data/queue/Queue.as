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

package com.emc2zen.data.queue {

	/**
	* @import
	*/

	import com.emc2zen.core.CoreObject;
	import com.emc2zen.data.IQueue;
	import com.emc2zen.util.TypeUtil;

	/**
	* Modelo basico de una estrucutra de dato del tipo Queue.
	* @author	PollyJex
	*/
	public class Queue extends CoreObject implements IQueue {
		
		/**
		* Registro.
		*/
		private var _record:Array;
		
		/**
		* Tama&ntilde;o del registro.
		*/
		private var _capacity:int;
		
		
		
		/**
		* Constructor.
		* @param	capacity 	Tama&ntilde;o del Queue.
		* @return	Queue
		*/
		public function Queue( capacity:int = 0 ) {
			
			_capacity = capacity;
			clear();
			
		}
		
		
		
		/**
		* Retorna la capacidad disponible en el registro.
		* @param	void
		* @return	int
		*/
		public function availableCapacity():int {
			
			return new int( capacity() - size() );
			
		}
		
		/**
		* Retorna la capacidad del registro.
		* @param	void
		* @return	int
		*/
		public function capacity():int {
			
			return _capacity;
			
		}
		
		/**
		* Reinicia el registro.
		* @param	void
		* @return	void
		*/
		public function clear():void {
			
			_record = new Array();
			
		}
		
		/**
		* Verifica si existe el valor en el registro.
		* @param	value 	Valor a verificar.
		* @return	Boolean
		*/
		public function contains( value:* ):Boolean {
			
			return new Boolean( _record.indexOf( value ) != -1 );
			
		}
		
		/**
        * Remueve el primer elemnto del registro.
		* @param	void
		* @return	Boolean
        */
    	public function dequeue():Boolean {
			
			return new Boolean( ! TypeUtil.isNull( poll() ) );
			
		}
		
		/**
		* Retorna pero no remueve el primer elemento del registro.
		* @param	void
		* @return	*
		*/
		public function element():* {
			
			return _record[ 0 ];
			
		}
		
		/**
		* Inserta un valor en el registro de ser posible.
		* @param	value	Valor a insertar.
		* @return	Boolean
		*/
		public function enqueue( value:* ):Boolean {
			
			return ResolveEnqueue( value, true );
			
		}
		
		/**
		* Inserta un valor al inicio del registro de ser posible.
		* @param	value	Valor a insertar.
		* @return	Boolean
		*/
		public function enqueueFront( value:* ):Boolean {
			
			return ResolveEnqueue( value );
			
		}
		
		/**
		* Verifica si en registro se encuentra vacio.
		* @param	void
		* @return	Boolean
		*/
		public function isEmpty():Boolean {
			
			return new Boolean( size() < 1 );
			
		}
		
		/**
		* Retorna pero no remueve el primer elemento del registro, si el mismo se encuentra vacio retorna null.
		* @param	void
		* @return	*
		*/
		public function peek():* {
			
			return ResolvePeek( true );
			
		}
		
		/**
		* Retorna pero no remueve el ultimo elemento del registro, si el mismo se encuentra vacio retorna null.
		* @param	void
		* @return	*
		*/
		public function peekRear():* {
			
			return ResolvePeek();
			
		}
		
		/**
		* Retorna y remueve el primer elemento del registro, si el mismo se encuentra vacio retorna null.
		* @param	void
		* @return	*
		*/
		public function poll():* {
			
			return ResolvePoll( true );
			
		}
		
		/**
		* Retorna y remueve el ultimo elemento del registro, si el mismo se encuentra vacio retorna null.
		* @param	void
		* @return	*
		*/
		public function pollRear():* {
			
			return ResolvePoll();
			
		}
		
		/**
		* Retorna el tama&ntilde; del registro.
		* @param	void
		* @return	int
		*/
		public function size():int {
			
			return _record.length;
			
		}
		
		/**
		* Retorna una copia del registro para ser iterado.
		* @param	void
		* @return	Array
		*/
		public function toArray():Array {
			
			return _record.slice();
			
		}
		
		
		
		/**
		* Resuelve la insercion de un valor en el registro de ser posible.
		* @param	value		Valor a insertar.
		* @param	mode		Modo de la insercion. ENQUEUE:TRUE | ENQUEUEFRONT:FALSE
		* @return	Boolean
		*/
		protected function ResolveEnqueue( value:*, mode:Boolean = false ):Boolean {
			
			if( size() < capacity() && ! TypeUtil.isNull( value ) ){
				
				if( ! mode  ){
					_record.unshift( value );
				}else{
					_record.push( value );
				}
				
				
				return true;
				
			}
			
			return false;
			
		}
		
		/**
		* Resuelve la lectura de la posicion en el registro.
		* @param	value 	TRUE:FRONT | FALSE:REAR
		* @return	*
		*/
		protected function ResolvePeek( value:Boolean = false ):* {
			
			if( isEmpty() ){
				return null;
			}
			
			if( !value ){
				return element();
			}else{
				return _record[ size() - 1 ];
			}
			
		}
		
		/**
		* Resuelve la eliminacion de la posicion en el registro.
		* @param	value 	TRUE:FRONT | FALSE:REAR
		* @return	*
		*/
		protected function ResolvePoll( value:Boolean = false ):* {
			
			if( isEmpty() ){
				return null;
			}
			
			if( !value ){
				return _record.pop();
			}else{
				return _record.shift();
			}
			
		}
		
	}
	
}
