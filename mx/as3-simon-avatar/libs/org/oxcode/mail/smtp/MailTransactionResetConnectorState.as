package org.oxcode.mail.smtp{

	internal class MailTransactionResetConnectorState extends ConnectorState{

		public function MailTransactionResetConnectorState(smtpConnector:SMTPConnector):void{
			super(smtpConnector);
		}

		override public function close():void{
			smtpConnector.socket.writeUTFBytes("QUIT\r\n");
			smtpConnector.socket.flush();
			smtpConnector.socket.close();

			smtpConnector.connectorState = smtpConnector.disconnectedConnectorState;
		}

		override public function get publicState():String{
			return SMTPConnector.STATE_MAIL_TRANSACTION_RESET;
		}

		override public function initiate():void{
			smtpConnector.socket.writeUTFBytes("RSET\r\n");
			smtpConnector.socket.flush();
		}

		override public function dataListener(data:String):void{
			var replyCode:ReplyCode = new ReplyCode(data);

			if(replyCode.toArray()[0] == ReplyCode.POSITIVE_COMPLETION){
				smtpConnector.connectorState = smtpConnector.mailTransactionConnectorState;
			} else{
				close();
			}
		}
	}
}