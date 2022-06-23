package org.oxcode.mail.smtp
{
	internal class DisconnectedConnectorState extends ConnectorState
	{
		public function DisconnectedConnectorState(smtpConnector:SMTPConnector):void
		{
			super(smtpConnector);
		}

		override public function connect():void
		{
			smtpConnector.socket.connect(smtpConnector.host, smtpConnector.port);

			smtpConnector.connectorState = smtpConnector.connectingConnectorState;
		}

		override public function get publicState():String
		{
			return SMTPConnector.STATE_DISCONNECTED;
		}
	}
}