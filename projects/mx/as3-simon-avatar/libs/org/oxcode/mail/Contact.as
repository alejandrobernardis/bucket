package org.oxcode.mail
{
	/**
	 * The Contact class represents the sender or recipient of a mail object.
	 * It holds the contact's mail address and optionally, a name.
	 */
	public class Contact
	{
		private var _address:String;
		private var _name:String;

		/**
		 * Creates a new Contact object initialized to the specified address and name.
		 * @param address The mail address of the contact.
		 * @param name The name of the contact.
		 */
		public function Contact(address:String, name:String = null):void
		{
			this.address = address;
			this.name = name;
		}

		/**
		 * The mail address of the contact.
		 */
		public function get address():String
		{
			return _address;
		}

		/**
		 * @private
		 */
		public function set address(value:String):void
		{
			_address = value;
		}

		/**
		 * The name of the contact.
		 */
		public function get name():String
		{
			return _name;
		}

		/**
		 * @private
		 */
		public function set name(value:String):void
		{
			_name = value;
		}

		/**
		 * Returns a string representation of the Contact object.
		 * Suitable for use in a mail transaction.
		 */
		public function toString():String
		{
			return name != null && name != "" ? name + " <" + address + ">" : address;
		}
	}
}