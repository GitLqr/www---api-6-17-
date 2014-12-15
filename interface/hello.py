import web
import logging
import logging.config
import conf

logger = logging.getLogger() 
logger_info = logging.getLogger( 'info' )
        
class hello:        
    def __init__ ( self ):
        web.header( 'Content-Type', 'text/html;charset=utf-8' )
        pass

    def GET(self, *args):
        inPars = web.input()
        logger.debug( '%s', str(inPars) )
        logger_info.info( '%s', 'info logger test' )
        return "hello"
