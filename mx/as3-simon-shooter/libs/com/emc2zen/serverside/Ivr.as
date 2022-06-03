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

package com.emc2zen.serverside {
	
	/**
	 * @import
	 */
	
	import com.emc2zen.core.CoreSingleton;
	import com.emc2zen.serverside.Conexion;
	import com.emc2zen.serverside.ConexionEvent;
	import com.emc2zen.util.TypeUtil;
	import flash.events.Event;
	import flash.events.EventDispatcher;
	import flash.events.IEventDispatcher;
	import flash.events.TimerEvent;
	import flash.utils.Timer;
	
	/**
	 * Conexion con el IVR.
	 * @author	PollyJex
	 */
	public class Ivr extends CoreSingleton implements IEventDispatcher {
		
		/**
		 * Instacia singleton.
		 */
		private static var $singleton:Ivr;
		
		/**
		 * Controlador de eventos.
		 */
		private var _dispatcher:EventDispatcher;
		
		/**
		 * Controlador del tiempo.
		 */
		private var _timer:Timer;
		
		/**
		 * Conexion contra el servidor.
		 */
		private var _cnx:Conexion;
		
		/**
		 * Timepo de espera para finalizar la operacion.
		 */
		public static const TIME_OUT:uint = 100000;
		
		/**
		 * Conteo del listener.
		 */
		private static var TIME_COUNT:uint = 0;
		
		/**
		 * Diferencia entre escucha y escucha.
		 */
		private static var TIME_DELAY:uint = 5000;
		
		/**
		 * Codigo del IVR
		 */
		private var IVR_CODE:String;
		
		/**
		 * Path del handler.
		 */
		private static const PATH_HANDLER:String = '../_serverside/registroViral.php';
		//private static const PATH_HANDLER:String = 'http://190.210.039.213/_serverside/registroViral.php';
		
		/**
		 * Constructor.
		 * @param	access	Acceso publico.
		 * @return	Ivr
		 */
		public function Ivr( access:SingletonPublic = null ){			
			
			if( ! TypeUtil.isNull( access ) ){
				
				this._dispatcher = new EventDispatcher( this );
				
			}else{
				
				super( this );
				
			}
			
		}		
		
		public static function getInstance():Ivr {
			
			if( TypeUtil.isNull( $singleton ) ){
				
				$singleton = new Ivr( new SingletonPublic() );
				
			}
			
			return $singleton;
			
		}
		
		public static function destroy():void {
			
			$singleton = null;
			
		}
		
		public function getCode( guid:String = null ):void {
			
			this._cnx = new Conexion();
			this._cnx.url = PATH_HANDLER;
			this._cnx.method = 'POST';
			this._cnx.action = 'IVR_GET_CODE';
			this._cnx.guid = guid;
			this._cnx.addEventListener( ConexionEvent.COMPLETE, getCodeComplete );
			this._cnx.send();
			
		}
		
		private function getCodeComplete( event:ConexionEvent ):void {
			
			var type:String = ( event.property != 'ERROR' ) ? IvrEvent.COMPLETE : IvrEvent.ERROR;
			this._dispatcher.dispatchEvent( new IvrEvent( type, event.property ) );
			
		}
		
		private var _verify:Boolean = false;
		
		public function CancelVerify():void {
			
			if( StopVerify() ){				
				if ( ! TypeUtil.isNull( this._cnx ) ){
					this._cnx.removeEventListener( ConexionEvent.COMPLETE, StatusVerifyComplete );
					this._cnx = null;				
				}
				this._dispatcher.dispatchEvent( new IvrEvent( IvrEvent.CANCEL ) );				
			}		
			
		}
		
		public function InitializeVerify( value:String ):void {
			
			if( ! this._verify ){
				this.IVR_CODE = value;
				TIME_COUNT = 0;
				this.StatusVerify();
				this._verify = true;
			}
			
		}
		
		private function StopVerify():Boolean {
			
			if( this._verify ){
				if ( ! TypeUtil.isNull( this._timer ) ){
					this._timer.stop();
					this._timer.removeEventListener( TimerEvent.TIMER_COMPLETE, StatusVerify );
					this._timer = null;				
				}
				this._verify = false;
				return true;
			}
			
			return false;
			
		}
		
		public function StatusVerify( event:TimerEvent = null ):void {	
			
			trace( new Date(), 'VERIFICAR IVR...' );
			
			if( ! TypeUtil.isNull( this._timer ) ){
				this._timer.removeEventListener( TimerEvent.TIMER_COMPLETE, StatusVerify );
				this._timer = null;				
			}
			
			this._cnx = new Conexion();
			this._cnx.url = PATH_HANDLER;
			this._cnx.method = 'POST';
			this._cnx.action = 'IVR_VERIFY';
			this._cnx.ivrcode = this.IVR_CODE;
			this._cnx.addEventListener( ConexionEvent.COMPLETE, StatusVerifyComplete );
			this._cnx.send();
			
		}
		
		private function StatusVerifyComplete( event:ConexionEvent = null ):void {
			
			if( event.property == 'OK' ){
				
				StopVerify();
				this._dispatcher.dispatchEvent( new IvrEvent( IvrEvent.COMPLETE, event.property ) );
				
				
			}else if( event.property == 'WAIT' && TIME_COUNT < TIME_OUT ){
				
				this._timer = new Timer( TIME_DELAY, 1 );
				this._timer.addEventListener( TimerEvent.TIMER_COMPLETE, StatusVerify );
				this._timer.start();
				
				TIME_COUNT += TIME_DELAY				
				
			}else{
				
				StopVerify();
				this._dispatcher.dispatchEvent( new IvrEvent( IvrEvent.COMPLETE, 'ERROR' ) );
				
			}
			
			this._cnx = null;
			
		}
		
		/* ### EVENTS ### */
		
		public function addEventListener( type:String, listener:Function, useCapture:Boolean = false, priority:int = 0, useWeakReference:Boolean = false ):void {
			
			this._dispatcher.addEventListener( type, listener, useCapture, priority, useWeakReference );
			
		}
		
		public function dispatchEvent( event:Event ):Boolean {
			
			return this._dispatcher.dispatchEvent( event );
			
		}
		
		public function hasEventListener( type:String ):Boolean {
			
			return this._dispatcher.hasEventListener( type );
			
		}
		
		public function removeEventListener( type:String, listener:Function, useCapture:Boolean = false ):void {
			
			this._dispatcher.removeEventListener( type, listener, useCapture );
			
		}
		
		public function willTrigger( type:String ):Boolean {
			
			return this._dispatcher.willTrigger( type );
			
		}
		
	}
	
}

final class SingletonPublic {}