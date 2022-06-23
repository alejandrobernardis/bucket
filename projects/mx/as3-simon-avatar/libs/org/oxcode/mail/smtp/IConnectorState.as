package org.oxcode.mail.smtp
{
	import org.oxcode.mail.Mail;

	internal interface IConnectorState
	{
		function connect():void;

		function send(mail:Mail):void;

		function reset():void;

		function close():void;

		function get publicState():String;

		function initiate():void;

		function dataListener(data:String):void;
	}
}