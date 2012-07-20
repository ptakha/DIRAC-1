# $HeadURL:  $
''' PEP

  Module used for enforcing policies. Its class is used for:
    1. invoke a PDP and collects results
    2. enforcing results by:
       a. saving result on a DB
       b. raising alarms
       c. other....
'''

from DIRAC                                                       import gLogger
from DIRAC.ResourceStatusSystem.Client.ResourceStatusClient      import ResourceStatusClient
from DIRAC.ResourceStatusSystem.Client.ResourceManagementClient  import ResourceManagementClient
#from DIRAC.ResourceStatusSystem.PolicySystem.Actions.EmptyAction import EmptyAction
from DIRAC.ResourceStatusSystem.PolicySystem.PDP                 import PDP
from DIRAC.ResourceStatusSystem.Utilities                        import Utils

__RCSID__  = '$Id:  $'

class PEP:

  def __init__( self, clients = None ):
   
    if clients is None:
      clients = {}
   
    if 'ResourceStatusClient' in clients:           
      self.rsClient = clients[ 'ResourceStatusClient' ]
    else:
      self.rsClient = ResourceStatusClient()
    if 'ResourceManagementClient' in clients:             
      self.rmClient = clients[ 'ResourceManagementClient' ]
    else: 
      self.rmClient = ResourceManagementClient()

    self.clients = clients
    self.pdp     = PDP( clients )   

  def enforce( self, decissionParams ):
    
    '''
      Enforce policies for given set of keyworkds. To be better explained.
    '''
  
    ##  real ban flag  #########################################################

#    realBan = False
#    if tokenOwner is not None:
#      if tokenOwner == 'rs_svc':
#        realBan = True
   
    ## policy decision point setup #############################################  
    
    self.pdp.setup( decissionParams )

    ## policy decision #########################################################

    resDecisions = self.pdp.takeDecision()
    if not resDecisions[ 'OK' ]:
      gLogger.error( 'Something went wrong, not enforcing policies for %s' % decissionParams )
      return resDecisions
    resDecisions = resDecisions[ 'Value' ]
    
    # We take from PDP the decision parameters used to find the policies
    decissionParams      = resDecisions[ 'decissionParams' ]
    policyCombinedResult = resDecisions[ 'policyCombinedResult' ]
    singlePolicyResults  = resDecisions[ 'singlePolicyResults' ]
    
    ## record all results before doing anything else    
    for resPolicy in singlePolicyResults:
      print ( decissionParams, resPolicy )
         
    for policyAction in policyCombinedResult[ 'PolicyAction' ]:
      
      print policyAction
      try:
        actionMod = Utils.voimport( 'DIRAC.ResourceStatusSystem.PolicySystem.Actions.%s' % policyAction )
      except ImportError:
        gLogger.error( 'Error importing %s action' % policyAction )
        
      if not hasattr( actionMod, policyAction ):
        gLogger.error( 'Error importing %s action class' % policyAction )
      
      action = getattr( actionMod, policyAction )( decissionParams, policyCombinedResult,
                                                   singlePolicyResults, self.clients )
      
      actionResult = action.run()
      if not actionResult[ 'OK' ]:
        gLogger.error( actionResult[ 'Message' ] )
        
      gLogger.debug( '> %s' % policyAction )     
        
#      
#      if not resP.has_key( 'OLD' ):       
#        self.clients[ "rmClient" ].insertPolicyResultLog( granularity, name,
#                                                          resP[ 'PolicyName' ], 
#                                                          statusType,
#                                                          resP[ 'Status' ], 
#                                                          resP[ 'Reason' ], now )
#        
#      else:
#        gLogger.warn( 'OLD: %s' % resP )
#        
#    res          = resDecisions[ 'PolicyCombinedResult' ] 
#    actionBaseMod = "DIRAC.ResourceStatusSystem.PolicySystem.Actions"
#
#    # Security mechanism in case there is no PolicyType returned
#    if res == {}:
#      EmptyAction(granularity, name, statusType, resDecisions).run()
#
#    else:
#      policyType   = res[ 'PolicyType' ]
#
#      if 'Resource_PolType' in policyType:
#        action = Utils.voimport( '%s.ResourceAction' % actionBaseMod )
#        action.ResourceAction(granularity, name, statusType, resDecisions,
#                         rsClient=self.rsClient,
#                         rmClient=self.rmClient).run()
#
#      if 'Alarm_PolType' in policyType:
#        action = Utils.voimport( '%s.AlarmAction' % actionBaseMod )
#        action.AlarmAction(granularity, name, statusType, resDecisions,
#                       Clients=self.clients,
#                       Params={"Granularity"  : granularity,
#                               "SiteType"     : siteType,
#                               "ServiceType"  : serviceType,
#                               "ResourceType" : resourceType}).run()
#
#      if 'RealBan_PolType' in policyType and realBan:
#        action = Utils.voimport( '%s.RealBanAction' % actionBaseMod )
#        action.RealBanAction(granularity, name, resDecisions).run()

    return resDecisions

################################################################################
#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF