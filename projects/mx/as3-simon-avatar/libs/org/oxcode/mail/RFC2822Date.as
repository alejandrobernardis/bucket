package org.oxcode.mail
{
	/**
	 * The RFC2822Date provides a means to create dates formatted as specified in RFC 2822.
	 */
	public class RFC2822Date
	{
		private var localDate:Date = new Date();

		private var dayNames:Array = [ "Sun", "Mon", "Tue", "Wed", "Thu",
									  "Fri", "Sat" ];

		private var monthNames:Array = [ "Jan", "Feb", "Mar", "Apr",
										"May", "Jun", "Jul", "Aug",
										"Sep", "Oct", "Nov", "Dec" ];

		private var timezoneOffset:String;

		/**
		 * Creates a new RFC2822Date object.
		 */
		public function RFC2822Date():void
		{
			timezoneOffset = (localDate.timezoneOffset <= 0 ? "+" : "-") +
							 formatDoubleDigits(Math.floor(localDate.timezoneOffset / 60)) +
							 formatDoubleDigits(localDate.timezoneOffset % 60);
		}

		/**
		 * The local date and time including the time zone.
		 */
		public function get dateTime():String
		{
			return dayOfWeek + ", " + date + " " + time;
		}

		/**
		 * The name of the day of the week.
		 */
		public function get dayOfWeek():String
		{
			return dayNames[localDate.day];
		}

		/**
		 * The full date (day month year).
		 */
		public function get date():String
		{
			return day + " " + month + " " + year;
		}

		/**
		 * The year in four digits.
		 */
		public function get year():String
		{
			return String(localDate.fullYear);
		}

		/**
		 * The name of the month.
		 */
		public function get month():String
		{
			return monthNames[localDate.month];
		}

		/**
		 * The day of the month.
		 */
		public function get day():String
		{
			return String(localDate.date);
		}

		/**
		 * The local time including the time zone.
		 */
		public function get time():String
		{
			return hours + ":" + minutes + ":" + seconds + " " + zone;
		}

		/**
		 * The hour portion of the time.
		 */
		public function get hours():String
		{
			return String(localDate.hours);
		}

		/**
		 * The minutes portion of the time.
		 */
		public function get minutes():String
		{
			return formatDoubleDigits(localDate.minutes);
		}

		/**
		 * The seconds portion of the time.
		 */
		public function get seconds():String
		{
			return formatDoubleDigits(localDate.seconds);
		}

		/**
		 * The local time zone.
		 */
		public function get zone():String
		{
			return timezoneOffset;
		}

		/**
		 * Formats an integer to two digits for use in time representation.
		 */
		private function formatDoubleDigits(integer:int):String
		{
			var doubleDigits:String = "";

			if (integer < 0)
				integer = -integer;

			doubleDigits = String(integer);

			if (doubleDigits.length == 1)
				doubleDigits = "0" + doubleDigits;

			return doubleDigits;
		}
	}
}