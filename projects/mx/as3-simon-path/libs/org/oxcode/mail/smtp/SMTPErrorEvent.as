package org.oxcode.mail.smtp
{
	import flash.events.ErrorEvent;

	/**
	 * An SMTPErrorEvent object is dispatched by the SMTPConnector when the SMTP service to which it is connected returns an error.
	 */
	public class SMTPErrorEvent extends ErrorEvent
	{
		/**
		 * An SMTPErrorEvent object dispatched by the SMTPConnector containing the reply code given by the SMTP service.
		 */
		public static const SMTP_ERROR:String = "smtpError";

		private var _replyCode:int;

		/**
		 * Creates a new SMTPErrorEvent object initialized with the specified type, description and reply code.
		 * @param type The type of the event, accessible in the type property. The SMTPErrorEvent defines one event type, the smtpError event, represented by the SMTPErrorEvent.SMTP_ERROR constant.
		 * @param bubbles Determines whether the event object participates in the bubbling stage of the event flow. The default value is false. 
		 * @param cancelable Determines whether the event object can be cancelled. The default value is false. 
		 * @param text Text to be displayed as an error message. Event listeners can access this information through the text property.
		 * @param replyCode The reply code as returned by the SMTP service.
		 */
		public function SMTPErrorEvent(type:String, bubbles:Boolean = false,
									   cancelable:Boolean = false, text:String = "",
									   replyCode:int = 0)
		{
			super(type, bubbles, cancelable, text);

			_replyCode = replyCode;
		}

		/**
		 * The reply code as returned by the SMTP service.
		 */
		public function get replyCode():int
		{
			return _replyCode;
		}
	}
}