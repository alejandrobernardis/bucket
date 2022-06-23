package org.oxcode.mail.smtp
{
	internal class ConnectingConnectorState extends ConnectorState
	{
		public function ConnectingConnectorState(smtpConnector:SMTPConnector):void
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
			return SMTPConnector.STATE_CONNECTING;
		}
	}
}