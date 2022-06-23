package org.oxcode.mail.smtp
{
	import flash.events.StatusEvent;
	import org.oxcode.mail.Mail;

	internal class MailTransactionConnectorState extends ConnectorState
	{
		private var _mailTransactionState:ITransactionState;

		private var _rcptTransactionState:ITransactionState;

		private var _dataTransactionState:ITransactionState;

		private var _transactionState:ITransactionState;

		public function MailTransactionConnectorState(smtpConnector:SMTPConnector):void
		{
			super(smtpConnector);

			// Instantiate states
			_mailTransactionState = new MAILTransactionState(this, smtpConnector);
			_rcptTransactionState = new RCPTTransactionState(this, smtpConnector);
			_dataTransactionState = new DATATransactionState(this, smtpConnector);

			// Set default state
			_transactionState = mailTransactionState;
		}

		override public function send(mail:Mail):void
		{
			transactionState.send(mail);
		}

		override public function reset():void
		{
			transactionState.reset();
		}

		override public function close():void
		{
			smtpConnector.socket.writeUTFBytes("QUIT\r\n");
			smtpConnector.socket.flush();
			smtpConnector.socket.close();

			smtpConnector.connectorState = smtpConnector.disconnectedConnectorState;
		}

		override public function get publicState():String
		{
			return transactionState.publicState;
		}

		override public function dataListener(data:String):void
		{
			transactionState.dataListener(data);
		}

		public function get mailTransactionState():ITransactionState
		{
			return _mailTransactionState;
		}

		public function get rcptTransactionState():ITransactionState
		{
			return _rcptTransactionState;
		}

		public function get dataTransactionState():ITransactionState
		{
			return _dataTransactionState;
		}

		public function get transactionState():ITransactionState
		{
			return _transactionState;
		}

		public function set transactionState(value:ITransactionState):void
		{
			_transactionState = value;

			trace("Transaction state: " + _transactionState);

			smtpConnector.dispatchEvent(new StatusEvent(StatusEvent.STATUS));
		}
	}
}