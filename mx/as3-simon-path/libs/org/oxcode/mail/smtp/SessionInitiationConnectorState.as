package org.oxcode.mail.smtp
{
	internal class SessionInitiationConnectorState extends ConnectorState
	{
		public function SessionInitiationConnectorState(smtpConnector:SMTPConnector):void
		{
			super(smtpConnector);
		}

		override public function close():void
		{
			smtpConnector.socket.close();

			smtpConnector.connectorState = smtpConnector.disconnectedConnectorState;
		}

		override public function get publicState():String
		{
			return SMTPConnector.STATE_SESSION_INITIATION;
		}

		override public function dataListener(data:String):void
		{
			var replyCode:ReplyCode = new ReplyCode(data);

			if (replyCode.toArray()[0] == ReplyCode.POSITIVE_COMPLETION)
			{
				smtpConnector.connectorState = smtpConnector.clientInitiationConnectorState;

				smtpConnector.connectorState.initiate();
			}
			else
			{
				smtpConnector.dispatchEvent(new SMTPErrorEvent(SMTPErrorEvent.SMTP_ERROR,
														   false, false,
														   "Session initiation failed",
														   replyCode.toInt()));

				close();
			}
		}
	}
}