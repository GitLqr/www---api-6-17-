import logging
import logging.config

class TcpHandler(logging.handlers.SocketHandler):
    """
    A handler class which writes logging records, in pickle format, to
    a datagram socket.  The pickle which is sent is that of the LogRecord's
    attribute dictionary (__dict__), so that the receiver does not need to
    have the logging module installed in order to process the logging event.

    To unpickle the record at the receiving end into a LogRecord, use the
    makeLogRecord function.

    """
    def __init__(self, host, port):
        """
        Initializes the handler with a specific host address and port.
        """
        logging.handlers.SocketHandler.__init__(self, host, port)

    def emit(self, record):
        """
        Emit a record.

        Pickles the record and writes it to the socket in binary format.
        If there is an error with the socket, silently drop the packet.
        If there was a problem with the socket, re-establishes the
        socket.
        """
        try:
            msg = record.levelname+':'+self.format(record)
            msg_len = '%04d' % len(msg)
            self.send(msg_len+':'+msg)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

class UdpHandler(logging.handlers.DatagramHandler):
    """
    A handler class which writes logging records, in pickle format, to
    a datagram socket.  The pickle which is sent is that of the LogRecord's
    attribute dictionary (__dict__), so that the receiver does not need to
    have the logging module installed in order to process the logging event.

    To unpickle the record at the receiving end into a LogRecord, use the
    makeLogRecord function.

    """
    def __init__(self, host, port):
        """
        Initializes the handler with a specific host address and port.
        """
        logging.handlers.DatagramHandler.__init__(self, host, port)

    def emit(self, record):
        """
        Emit a record.

        Pickles the record and writes it to the socket in binary format.
        If there is an error with the socket, silently drop the packet.
        If there was a problem with the socket, re-establishes the
        socket.
        """
        try:
            msg = record.levelname+':'+self.format(record)
            msg_len = '%04d' % len(msg)
            self.send(msg_len+':'+msg)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


