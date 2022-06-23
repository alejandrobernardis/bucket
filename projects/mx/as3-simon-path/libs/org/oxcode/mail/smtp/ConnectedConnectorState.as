package org.oxcode.mail.smtp
{
	internal class ConnectedConnectorState extends ConnectorState
	{
		public function ConnectedConnectorState(smtpConnector:SMTPConnector):void
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
			return SMTPConnector.STATE_CONNECTED;
		}

		override public function dataListener(data:String):void
		{
			smtpConnector.connectorState = smtpConnector.sessionInitiationConnectorState;

			smtpConnector.connectorState.dataListener(data);
		}
	}
}