package org.oxcode.mail.smtp
{
	import org.oxcode.mail.Mail;

	internal class MAILTransactionState extends TransactionState
	{
		public function MAILTransactionState(mailTransaction:MailTransactionConnectorState,
											 smtpConnector:SMTPConnector):void
		{
			super(mailTransaction, smtpConnector);
		}

		override public function send(mail:Mail):void
		{
			// No mail being processed, ready for a new transaction
			if (!currentMail)
			{
				currentMail = mail;

				// TODO: Needs type checking for the contents of authors
				if (currentMail.from.length == 1 && currentMail.from[0])
				{
					smtpConnector.socket.writeUTFBytes("MAIL FROM: " +
													   currentMail.from[0].address + "\r\n");
				}
				else if (currentMail.sender)
				{
					smtpConnector.socket.writeUTFBytes("MAIL FROM: " +
													   currentMail.sender.address + "\r\n");
				}
				else
				{
					throw new Error("Multiple authors were specified, but the sender is undefined");
				}
	
				smtpConnector.socket.flush();
			}

			// Transaction is already in progress, send is not available
			else
			{
				super.send(mail);
			}
		}

		override public function get publicState():String
		{
			return SMTPConnector.STATE_MAIL_TRANSACTION_READY;
		}

		override public function dataListener(data:String):void
		{
			var replyCode:ReplyCode = new ReplyCode(data);

			if (replyCode.toArray()[0] == ReplyCode.POSITIVE_COMPLETION)
			{
				// Create a local reference to the current mail being processed, so
				// we can clear the currentMail reference before calling the process()
				// method on the next state.
				var mail:Mail = currentMail;

				currentMail = null;

				mailTransaction.transactionState = mailTransaction.rcptTransactionState;

				mailTransaction.transactionState.process(mail);
			}
			else
			{
				smtpConnector.dispatchEvent(new SMTPErrorEvent(SMTPErrorEvent.SMTP_ERROR,
														   false, false,
														   "The mail transaction was not accepted",
														    replyCode.toInt()));

				smtpConnector.reset();
			}
		}
	}
}