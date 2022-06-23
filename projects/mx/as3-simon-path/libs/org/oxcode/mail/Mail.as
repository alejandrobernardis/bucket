package org.oxcode.mail
{
	/**
	 * The Mail class acts as both the envelope and contents of an internet message.
	 */
	public class Mail
	{
		private var _from:Array = [];

		private var _sender:Contact;

		private var _replyTo:Array = [];

		private var _to:Array = [];

		private var _cc:Array = [];

		private var _bcc:Array = [];

		private var _inReplyTo:Array = [];

		private var _subject:String;

		private var _plaintextContent:String;

		/**
		 * The authors of the mail in the form of Contact objects.
		 */
		public function get from():Array
		{
			return _from;
		}

		/**
		 * In case of multiple authors, the sender of the mail.
		 */
		public function get sender():Contact
		{
			return _sender;
		}

		/**
		 * @private
		 */
		public function set sender(value:Contact):void
		{
			_sender = value;
		}

		/**
		 * The contacts to which a reply to this mail should be sent.
		 */
		public function get replyTo():Array
		{
			return _replyTo;
		}

		/**
		 * The recipients of this mail in the form of Contact objects.
		 */
		public function get to():Array
		{
			return _to;
		}

		/**
		 * The CC recipients of this mail in the form of Contact objects.
		 */
		public function get cc():Array
		{
			return _cc;
		}

		/**
		 * The BCC recipients of this mail in the form of Contact objects.
		 */
		public function get bcc():Array
		{
			return _bcc;
		}

		/**
		 * The message ID's of the mails to which this mail is a reply.
		 */
		public function get inReplyTo():Array
		{
			return _inReplyTo;
		}

		/**
		 * The subject of this mail.
		 */
		public function get subject():String
		{
			return _subject;
		}

		/**
		 * @private
		 */
		public function set subject(value:String):void
		{
			_subject = value;
		}

		/**
		 * The plain text content of this mail.
		 */
		public function get plaintextContent():String
		{
			return _plaintextContent;
		}

		/**
		 * @private
		 */
		public function set plaintextContent(value:String):void
		{
			_plaintextContent = value;
		}
	}
}