# $Header: /tmp/libdirac/tmp.stZoy15380/dirac/DIRAC3/DIRAC/Core/DISET/private/Transports/PlainTransport.py,v 1.13 2008/10/14 13:54:22 acasajus Exp $
__RCSID__ = "$Id: PlainTransport.py,v 1.13 2008/10/14 13:54:22 acasajus Exp $"

import socket
from DIRAC.Core.DISET.private.Transports.BaseTransport import BaseTransport
from DIRAC.LoggingSystem.Client.Logger import gLogger
from DIRAC.Core.Utilities.ReturnValues import S_ERROR, S_OK

class PlainTransport( BaseTransport ):

  def initAsClient( self ):
    self.oSocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    self.oSocket.connect( self.stServerAddress )
    self.remoteAddress = self.oSocket.getpeername()
    return S_OK( self.oSocket )

  def initAsServer( self ):
    if not self.serverMode():
      raise RuntimeError( "Must be initialized as server mode" )
    self.oSocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    if self.bAllowReuseAddress:
      self.oSocket.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
    self.oSocket.bind( self.stServerAddress )
    self.oSocket.listen( self.iListenQueueSize )
    return S_OK( self.oSocket )

  def close( self ):
    gLogger.debug( "Closing socket" )
    try:
      self.oSocket.shutdown( socket.SHUT_RDWR )
    except:
      pass
    self.oSocket.close()

  def setClientSocket( self, oSocket ):
    if self.serverMode():
      raise RuntimeError( "Mustbe initialized as client mode" )
    self.oSocket = oSocket
    self.remoteAddress = self.oSocket.getpeername()

  def acceptConnection( self ):
    #HACK: Was = PlainTransport( self )
    oClientTransport = PlainTransport( self.stServerAddress )
    oClientSocket, stClientAddress = self.oSocket.accept()
    oClientTransport.setClientSocket( oClientSocket )
    return S_OK( oClientTransport )

def checkSanity( *args, **kwargs ):
  return S_OK()

def delegate( delegationRequest, kwargs ):
  """
  Check delegate!
  """
  return S_OK()