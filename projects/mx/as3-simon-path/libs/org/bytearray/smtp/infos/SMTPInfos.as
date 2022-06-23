package org.bytearray.smtp.infos
{
	public class SMTPInfos
	{
		public var code:int;
		public var message:String;
		
		public function SMTPInfos(code:int, message:String)
		{
			this.code = code;
			this.message = message;
		}

		public function get _code():int{
			return code;
		}

		public function get _message():String{
			return message;
		}
		
	}
}