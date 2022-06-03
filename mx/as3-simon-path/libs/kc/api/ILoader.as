package kc.api {
	import flash.events.IEventDispatcher;
	import flash.net.URLVariables;
	import flash.system.LoaderContext;

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public interface ILoader extends IEventDispatcher, IPurger {
	
		// @properties (rw)

		function get url():String;
		function set url(value:String):void;
		function get method():String;
		function set method(value:String):void;
		function get variables():URLVariables;
		function set variables(value:URLVariables):void;
		function get headers():Array;
		function set headers(value:Array):void;
		function get contentType():String;
		function set contentType(value:String):void;
		function get context():LoaderContext;
		function set context(value:LoaderContext):void;
		function get type():String;
		function set type(value:String):void;
		function get dataFormat():String;
		function set dataFormat(value:String):void;
		function get catchExceptions():Boolean;
		function set catchExceptions(value:Boolean):void;
		function get antiCache():Boolean;
		function set antiCache(value:Boolean):void;
		
		// @properties (r)
		
		function get uid():String;		function get content():*;
		function get progress():uint;
		function get bytesLoaded():uint;
		function get bytesTotal():uint;

		// @methods
		
		function clear():void;
		function close():void;
		function isLoaded():Boolean;
		function load( url:String = null, method:String = null ):void;
		function send( url:String = null, method:String = null ):void;
		function sendAndLoad( url:String = null, method:String = null ):void;
		
	}
	
}
