package org.oxcode.mail.smtp
{
	import flash.net.Socket;
	import flash.events.Event;
	import flash.events.EventDispatcher;
	import flash.events.IOErrorEvent;
	import flash.events.ProgressEvent;
	import flash.events.SecurityErrorEvent;
	import flash.events.StatusEvent;
	import org.oxcode.mail.Mail;

	/**
	 * The SMTPConnector class connects to a mail server and sends mail using the SMTP protocol.
	 */
	public class SMTPConnector extends EventDispatcher
	{
		/**
		 * The SMTPConnector is disconnected.
		 */
		public static const STATE_DISCONNECTED:String = "disconnected";

		/**
		 * The SMTPConnector is connecting to the specified host.
		 */
		public static const STATE_CONNECTING:String = "connecting";

		/**
		 * The SMTPConnector is connected to the specified host.
		 */
		public static const STATE_CONNECTED:String = "connected";

		/**
		 * The SMTPConnector is in the process of initiating a session with the SMTP service.
		 */
		public static const STATE_SESSION_INITIATION:String = "sessionInitiation";

		/**
		 * The SMTPConnector is in the process of identifying itself with the SMTP service.
		 */
		public static const STATE_CLIENT_INITIATION:String = "clientInitiation";

		/**
		 * The SMTPConnector is ready for a new mail transaction.
		 */
		public static const STATE_MAIL_TRANSACTION_READY:String = "mailTransactionReady";

		/**
		 * The SMTPConnector is busy performing a mail transaction.
		 */
		public static const STATE_MAIL_TRANSACTION_BUSY:String = "mailTransactionBusy";

		/**
		 * The SMTPConnector is resetting a mail transaction.
		 */
		public static const STATE_MAIL_TRANSACTION_RESET:String = "mailTransactionReset";

		private var _disconnectedConnectorState:IConnectorState;

		private var _connectingConnectorState:IConnectorState;

		private var _connectedConnectorState:IConnectorState;

		private var _sessionInitiationConnectorState:IConnectorState;

		private var _clientInitiationConnectorState:IConnectorState;

		private var _mailTransactionConnectorState:IConnectorState;

		private var _mailTransactionResetConnectorState:IConnectorState;

		private var _connectorState:IConnectorState;

		private var _host:String;

		private var _port:uint;

		private var _identity:String;

		private var _socket:Socket = new Socket();

		/**
		 * Creates a new SMTPConnector object initialized to the specified host and identity.
		 * @param host The IP address or hostname of the SMTP server to connect to.
		 * @param identity The identity by which this object identifies itself in the client initiation process.
		 * @param port The port number of the SMTP service on the host.
		 */
		public function SMTPConnector(host:String, identity:String, port:uint = 25):void
		{
			// Instantiate states
			_disconnectedConnectorState			= new DisconnectedConnectorState(this);
			_connectingConnectorState			= new ConnectingConnectorState(this);
			_connectedConnectorState			= new ConnectedConnectorState(this);
			_sessionInitiationConnectorState	= new SessionInitiationConnectorState(this);
			_clientInitiationConnectorState		= new ClientInitiationConnectorState(this);
			_mailTransactionConnectorState		= new MailTransactionConnectorState(this);
			_mailTransactionResetConnectorState	= new MailTransactionResetConnectorState(this);

			// Set default state
			_connectorState = disconnectedConnectorState;

			// Set connection parameters
			this.host		= host;
			this.identity	= identity;
			this.port		= port;

			// Set connection listeners
			socket.addEventListener(Event.CLOSE,socketCloseListener);
			socket.addEventListener(Event.CONNECT, socketConnectListener);
			socket.addEventListener(IOErrorEvent.IO_ERROR, socketIOErrorListener);
			socket.addEventListener(SecurityErrorEvent.SECURITY_ERROR, socketSecurityErrorListener);
			socket.addEventListener(ProgressEvent.SOCKET_DATA, socketDataListener);
		}

		/**
		 * Connect to the SMTP server.
		 */
		public function connect():void
		{
			connectorState.connect();
		}

		/**
		 * Send a mail.
		 * @param mail A Mail object.
		 */
		public function send(mail:Mail):void
		{
			connectorState.send(mail);
		}

		/**
		 * Reset a mail transaction.
		 */
		public function reset():void
		{
			connectorState.reset();
		}

		/**
		 * Close the connection to the SMTP server.
		 */
		public function close():void
		{
			connectorState.close();
		}

		/**
		 * Listener for a close event on the socket.
		 * @param event An event dispatched by the socket.
		 */
		private function socketCloseListener(event:Event):void
		{
			connectorState = disconnectedConnectorState;
		}

		/**
		 * Listener for the connect event on the socket.
		 * @param event An event dispatched by the socket.
		 */
		private function socketConnectListener(event:Event):void
		{
			connectorState = connectedConnectorState;
		}

		/**
		 * Listener for an IO error event on the socket.
		 * @param event An event dispatched by the socket.
		 */
		private function socketIOErrorListener(event:IOErrorEvent):void
		{
			connectorState = disconnectedConnectorState;
		}

		/**
		 * Listener for a security error event on the socket.
		 * @param event An event dispatched by the socket.
		 */
		private function socketSecurityErrorListener(event:SecurityErrorEvent):void
		{
			connectorState = disconnectedConnectorState;
		}

		/**
		 * Listener for a progress event on the socket.
		 * @param event An event dispatched by the socket.
		 */
		private function socketDataListener(event:ProgressEvent):void
		{
			var data:String = event.target.readUTFBytes(event.target.bytesAvailable);

			trace(data);

			connectorState.dataListener(data);
		}

		/**
		 * The state object used when the connector is disconnected.
		 * @private
		 */
		internal function get disconnectedConnectorState():IConnectorState
		{
			return _disconnectedConnectorState;
		}

		/**
		 * The state object used when the connector is connecting.
		 * @private
		 */
		internal function get connectingConnectorState():IConnectorState
		{
			return _connectingConnectorState;
		}

		/**
		 * The state object used when the connector is connected.
		 * @private
		 */
		internal function get connectedConnectorState():IConnectorState
		{
			return _connectedConnectorState;
		}

		/**
		 * The state object used when the connector is performing the session initiation.
		 * @private
		 */
		internal function get sessionInitiationConnectorState():IConnectorState
		{
			return _sessionInitiationConnectorState;
		}

		/**
		 * The state object used when the connector is performing the client initiation.
		 * @private
		 */
		internal function get clientInitiationConnectorState():IConnectorState
		{
			return _clientInitiationConnectorState;
		}

		/**
		 * The state object used when the connector is performing the mail transaction.
		 * @private
		 */
		internal function get mailTransactionConnectorState():IConnectorState
		{
			return _mailTransactionConnectorState;
		}

		/**
		 * The state object used when the connector is resetting a mail transaction.
		 * @private
		 */
		internal function get mailTransactionResetConnectorState():IConnectorState
		{
			return _mailTransactionResetConnectorState;
		}

		/**
		 * The current state of the SMTPConnector.
		 * @private
		 */
		internal function get connectorState():IConnectorState
		{
			return _connectorState;
		}

		/**
		 * @private
		 */
		internal function set connectorState(value:IConnectorState):void
		{
			_connectorState = value;

			trace("Connector state: " + _connectorState);

			dispatchEvent(new StatusEvent(StatusEvent.STATUS));
		}

		/**
		 * The IP address or hostname of the SMTP server to connect to.
		 */
		public function get host():String
		{
			return _host;
		}

		/**
		 * @private
		 */
		public function set host(value:String):void
		{
			_host = value;
		}

		/**
		 * The port number of the SMTP service on the host.
		 */
		public function get port():uint
		{
			return _port;
		}

		/**
		 * @private
		 */
		public function set port(value:uint):void
		{
			if (value > 65535)
				throw new ArgumentError("Port number out of range");

			_port = value;
		}

		/**
		 * The identity by which this object identifies itself in the client initiation process.
		 */
		public function get identity():String
		{
			return _identity;
		}

		/**
		 * @private
		 */
		public function set identity(value:String):void
		{
			_identity = value;
		}

		/**
		 * An internal reference to the socket opened by the SMTPConnector.
		 * @private
		 */
		internal function get socket():Socket
		{
			return _socket;
		}

		/**
		 * The current state of the SMTPConnector.
		 * @see #STATE_DISCONNECTED
		 * @see #STATE_CONNECTING
		 * @see #STATE_CONNECTED
		 * @see #STATE_SESSION_INITIATION
		 * @see #STATE_CLIENT_INITIATION
		 * @see #STATE_MAIL_TRANSACTION_READY
		 * @see #STATE_MAIL_TRANSACTION_BUSY
		 */
		public function get state():String
		{
			return connectorState.publicState;
		}
	}
}