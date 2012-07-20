# $HeadURL:  $
''' BaseAction
  
  Base class for Actions.
  
'''

from DIRAC import gLogger

__RCSID__  = '$Id:  $'

class BaseAction( object ):
  
  def __init__( self, decissionParams, enforcementResult, singlePolicyResults, clients ):

    # enforcementResult supposed to look like:
    # { 
    #   'Status'        : <str>,
    #   'Reason'        : <str>, 
    #   'PolicyActions' : <list>,
    #   [ 'EndDate' : <str> ]
    # } 

    # decissionParams supposed to look like:
    # {
    #   'element'     : None,
    #   'name'        : None,
    #   'elementType' : None,
    #   'statusType'  : None,
    #   'status'      : None,
    #   'reason'      : None,
    #   'tokenOwner'  : None
    # }

    self.actionName          = 'BaseAction'
    self.decissionParams     = decissionParams
    self.enforcementResult   = enforcementResult
    self.singlePolicyResults = singlePolicyResults
    self.clients             = clients

  def run( self ):
    
    gLogger.info( '%s: you may want to overwrite this method' % self.actionName )

################################################################################
#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF