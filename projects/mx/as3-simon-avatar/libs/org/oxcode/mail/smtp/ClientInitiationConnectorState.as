package org.oxcode.mail.smtp{

	internal class ClientInitiationConnectorState extends ConnectorState
	{
		public function ClientInitiationConnectorState(smtpConnector:SMTPConnector):void
		{
			super(smtpConnector);
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
			return SMTPConnector.STATE_CLIENT_INITIATION;
		}

		override public function initiate():void
		{
			smtpConnector.socket.writeUTFBytes("EHLO " + smtpConnector.identity + "\r\n");
			smtpConnector.socket.flush();
		}

		override public function dataListener(data:String):void
		{
			var replyCode:ReplyCode = new ReplyCode(data);

			if (replyCode.toArray()[0] == ReplyCode.POSITIVE_COMPLETION)
			{
				// TODO: store the parameters returned in the response to EHLO

				smtpConnector.connectorState = smtpConnector.mailTransactionConnectorState;
			}
			else
			{
				smtpConnector.dispatchEvent(new SMTPErrorEvent(SMTPErrorEvent.SMTP_ERROR,
														   false, false,
														   "Client initiation failed",
														   replyCode.toInt()));

				close();
			}
		}
	}
}