package org.oxcode.mail.smtp
{
	internal class ReplyCode
	{
		public static const POSITIVE_PRELIMINARY:int = 1;

		public static const POSITIVE_COMPLETION:int = 2;

		public static const POSITIVE_INTERMEDIATE:int = 3;

		public static const TRANSIENT_NEGATIVE_COMPLETION:int = 4;

		public static const PERMANENT_NEGATIVE_COMPLETION:int = 5;

		public static const SYNTAX:int = 0;

		public static const INFORMATION:int = 1;

		public static const CONNECTION:int = 2;

		public static const MAIL_SYSTEM:int = 5;

		private var _replyCode:int;

		private var _replyCodeDigits:Array;

		public function ReplyCode(reply:String):void
		{
			var replyCode:String = reply.substring(0, 3);

			_replyCode			= int(replyCode);
			_replyCodeDigits	= replyCode.split("");
		}

		public function toInt():int
		{
			return _replyCode;
		}

		public function toArray():Array
		{
			return _replyCodeDigits;
		}
	}
}