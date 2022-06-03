package org.oxcode.mail.smtp{
	import org.oxcode.mail.Mail;

	internal class RCPTTransactionState extends TransactionState{

		private var recipients:Array;

		public function RCPTTransactionState(mailTransaction:MailTransactionConnectorState, smtpConnector:SMTPConnector):void{
			super(mailTransaction, smtpConnector);
		}

		override public function process(mail:Mail):void{
			if(!currentMail){
				currentMail = mail;

				// Create a local copy of the mail recipients
				recipients = [].concat(currentMail.to);
				recipients = recipients.concat(currentMail.cc);
				recipients = recipients.concat(currentMail.bcc);
			}

			smtpConnector.socket.writeUTFBytes("RCPT TO: " + recipients.shift().address + "\r\n");
			smtpConnector.socket.flush();
		}

		override public function get publicState():String{
			return SMTPConnector.STATE_MAIL_TRANSACTION_BUSY;
		}

		override public function dataListener(data:String):void{
			var replyCode:ReplyCode = new ReplyCode(data);

			if(replyCode.toArray()[0] == ReplyCode.POSITIVE_COMPLETION){
				// If we're all out of recipients, move on to the next state
				if(recipients.length == 0){
					// Create a local reference to the current mail being processed, so
					// we can clear the currentMail reference before calling the process()
					// method on the next state.
					var mail:Mail = currentMail;

					currentMail = null;

					mailTransaction.transactionState = mailTransaction.dataTransactionState;

					mailTransaction.transactionState.process(mail);
				}

				// Add another recipient 
				else{
					process(currentMail);
				}
			} else{
				smtpConnector.dispatchEvent(new SMTPErrorEvent(SMTPErrorEvent.SMTP_ERROR, false, false, "The recipient was not accepted", replyCode.toInt()));

				smtpConnector.reset();
			}
		}
	}
}