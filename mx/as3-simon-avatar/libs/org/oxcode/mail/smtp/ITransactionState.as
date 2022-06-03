package org.oxcode.mail.smtp
{
	import org.oxcode.mail.Mail;

	internal interface ITransactionState
	{
		function get publicState():String;

		function send(mail:Mail):void;

		function process(mail:Mail):void;

		function reset():void;

		function dataListener(data:String):void;
	}
}