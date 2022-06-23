package org.oxcode.mail.smtp
{
	import org.oxcode.mail.Mail;

	internal class ConnectorState implements IConnectorState
	{
		protected var smtpConnector:SMTPConnector;

		public function ConnectorState(smtpConnector:SMTPConnector):void
		{
			this.smtpConnector = smtpConnector;
		}

		public function connect():void
		{
			trace("connect() is not available in the current state");
		}

		public function send(mail:Mail):void
		{
			trace("send() is not available in the current state");
		}

		public function reset():void
		{
			trace("reset() is not available in the current state");
		}

		public function close():void
		{
			trace("close() is not available in the current state");
		}

		public function get publicState():String
		{
			trace("publicState is not available in the current state");

			return null;
		}

		public function initiate():void
		{
			trace("initiate() is not available in the current state");
		}

		public function dataListener(data:String):void
		{
			trace("dataListener() is not available in the current state");
		}
	}
}