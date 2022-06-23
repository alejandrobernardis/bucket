package org.oxcode.mail.smtp
{
	import org.oxcode.mail.Contact;
	import org.oxcode.mail.Mail;
	import org.oxcode.mail.RFC2822Date;

	internal class DATATransactionState extends TransactionState
	{
		public function DATATransactionState(mailTransaction:MailTransactionConnectorState,
											 smtpConnector:SMTPConnector):void
		{
			super(mailTransaction, smtpConnector);
		}

		override public function process(mail:Mail):void
		{
			if (!currentMail)
			{
				currentMail = mail;

				smtpConnector.socket.writeUTFBytes("DATA\r\n");
				smtpConnector.socket.flush();
			}
			else
			{
				// Date
				smtpConnector.socket.writeUTFBytes("Date: " + (new RFC2822Date()).dateTime + "\r\n");

				// From
				var fromString:String	= "From: ";
				var separator:String	= "";

				for each (var from:Contact in currentMail.from)
				{
					fromString += separator + from.toString();

					separator = ",";
				}

				smtpConnector.socket.writeUTFBytes(fromString + "\r\n");

				// Sender
				if (currentMail.sender)
					smtpConnector.socket.writeUTFBytes("Sender: " + currentMail.sender.toString() + "\r\n");
				else if (currentMail.from.length > 1)
					throw new Error("Multiple authors were specified, but the sender is undefined");

				// Reply to
				if (currentMail.replyTo.length > 0)
				{
					var replyToString:String	= "Reply-To: ";
						separator				= "";
	
					for each (var replyTo:Contact in currentMail.replyTo)
					{
						replyToString += separator + replyTo.toString();
	
						separator = ",";
					}
	
					smtpConnector.socket.writeUTFBytes(replyToString + "\r\n");
				}

				// To
				if (currentMail.to.length > 0)
				{
					var toString:String		= "To: ";
						separator			= "";
	
					for each (var to:Contact in currentMail.to)
					{
						toString += separator + to.toString();
	
						separator = ",";
					}
	
					smtpConnector.socket.writeUTFBytes(toString + "\r\n");
				}

				// CC
				if (currentMail.cc.length > 0)
				{
					var ccString:String		= "Cc: ";
						separator			= "";
	
					for each (var cc:Contact in currentMail.cc)
					{
						ccString += separator + cc.toString();
	
						separator = ",";
					}
	
					smtpConnector.socket.writeUTFBytes(ccString + "\r\n");
				}

				// In reply to
				if (currentMail.inReplyTo.length > 0)
				{
					var inReplyToString:String = "In-Reply-To: ";
						separator				= "";
	
					for each (var messageID:String in currentMail.inReplyTo)
					{
						inReplyToString += separator + messageID;
	
						separator = " ";
					}
	
					smtpConnector.socket.writeUTFBytes(inReplyToString + "\r\n");
				}

				// Subject
				if (currentMail.subject != null && currentMail.subject != "")
					smtpConnector.socket.writeUTFBytes("Subject: " + currentMail.subject + "\r\n");

				// Content type
				smtpConnector.socket.writeUTFBytes("Content-Type: text/plain; charset=utf-8\r\n");

				// Content
				smtpConnector.socket.writeUTFBytes("\r\n" + currentMail.plaintextContent + "\r\n");

				// Closing period
				smtpConnector.socket.writeUTFBytes(".\r\n");
				smtpConnector.socket.flush();
			}
		}

		override public function get publicState():String
		{
			return SMTPConnector.STATE_MAIL_TRANSACTION_BUSY;
		}

		override public function dataListener(data:String):void
		{
			var replyCode:ReplyCode = new ReplyCode(data);

			if (replyCode.toArray()[0] == ReplyCode.POSITIVE_INTERMEDIATE)
			{
				process(currentMail);
			}
			else if (replyCode.toArray()[0] == ReplyCode.POSITIVE_COMPLETION)
			{
				currentMail = null;

				mailTransaction.transactionState = mailTransaction.mailTransactionState;
			}
			else
			{
				smtpConnector.dispatchEvent(new SMTPErrorEvent(SMTPErrorEvent.SMTP_ERROR,
														   false, false,
														   "The data was not accepted",
														   replyCode.toInt()));

				smtpConnector.reset();
			}
		}
	}
}