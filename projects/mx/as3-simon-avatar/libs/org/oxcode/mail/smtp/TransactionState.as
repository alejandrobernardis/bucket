package org.oxcode.mail.smtp
{
	import org.oxcode.mail.Mail;

	internal class TransactionState implements ITransactionState
	{
		protected var mailTransaction:MailTransactionConnectorState;

		protected var smtpConnector:SMTPConnector;

		protected var currentMail:Mail;

		public function TransactionState(mailTransaction:MailTransactionConnectorState,
										 smtpConnector:SMTPConnector):void
		{
			this.mailTransaction	= mailTransaction;
			this.smtpConnector		= smtpConnector;
		}

		public function send(mail:Mail):void
		{
			trace("send() is not available in the current state");
		}

		public function process(mail:Mail):void
		{
			trace("process() is not available in the current state");
		}

		public function reset():void
		{
			currentMail = null;

			smtpConnector.connectorState = smtpConnector.mailTransactionResetConnectorState;

			smtpConnector.connectorState.initiate();
		}

		public function get publicState():String
		{
			trace("publicState is not available in the current state");

			return null;
		}

		public function dataListener(data:String):void
		{
			trace("dataListener() is not available in the current state");
		}
	}
}