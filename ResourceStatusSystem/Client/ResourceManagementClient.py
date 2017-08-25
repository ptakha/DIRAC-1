""" ResourceManagementClient

  Client to interact with the ResourceManagementDB.

"""

__RCSID__ = '$Id:  $'

from datetime import datetime, timedelta
from DIRAC.Core.DISET.RPCClient import RPCClient

# a method that makes the first letter uppercase only (and leaves the rest letters unaffected)
def uppercase_first_letter(key):
  return key[0].upper() + key[1:]

class ResourceManagementClient( object ):
  """
  The :class:`ResourceManagementClient` class exposes the :mod:`DIRAC.ResourceManagement`
  API. All functions you need are on this client.

  It has the 'direct-db-access' functions, the ones of the type:
   - insert
   - update
   - select
   - delete

  that return parts of the RSSConfiguration stored on the CS, and used everywhere
  on the RSS module. Finally, and probably more interesting, it exposes a set
  of functions, badly called 'boosters'. They are 'home made' functions using the
  basic database functions that are interesting enough to be exposed.

  The client will ALWAYS try to connect to the DB, and in case of failure, to the
  XML-RPC server ( namely :class:`ResourceManagementDB` and
  :class:`ResourceManagementHancler` ).

  You can use this client on this way

   >>> from DIRAC.ResourceManagementSystem.Client.ResourceManagementClient import ResourceManagementClient
   >>> rsClient = ResourceManagementClient()

  All functions calling methods exposed on the database or on the booster are
  making use of some syntactic sugar, in this case a decorator that simplifies
  the client considerably.
  """

  def __init__( self ):
    '''
    The client tries to connect to :class:ResourceManagementDB by default. If it
    fails, then tries to connect to the Service :class:ResourceManagementHandler.
    '''

    self.rmService = RPCClient( "ResourceStatus/ResourceManagement" )

  def _prepare(self, sendDict):

    # remove unnecessary key generated by locals()
    del sendDict['self']

    # make each key name uppercase to match database column names (case sensitive)
    for key, value in sendDict.items():
      del sendDict[key]

      # apply default values
      if key == 'tokenExpiration' and value is None:
        sendDict.update({uppercase_first_letter(key): datetime.utcnow() + timedelta(hours=24)})
      else:
        sendDict.update({uppercase_first_letter(key): value})

    return sendDict

  # AccountingCache Methods ....................................................

  def selectAccountingCache( self, name = None, plotType = None, plotName = None,
                             result = None, dateEffective = None, lastCheckTime = None, meta = None ):
    '''
    Gets from PolicyResult all rows that match the parameters given.

    :Parameters:
      **name** - `[, string, list]`
        name of an individual of the grid topology
      **plotType** - `[, string, list]`
        the plotType name (e.g. 'Pilot')
      **plotName** - `[, string, list]`
        the plot name
      **result** - `[, string, list]`
        command result
      **dateEffective** - `[, datetime, list]`
        time-stamp from which the result is effective
      **lastCheckTime** - `[, datetime, list]`
        time-stamp setting last time the result was checked
      **meta** - `dict`
        metadata for the mysql query. Currently it is being used only for column selection.
        For example: meta = { 'columns' : [ 'Name' ] } will return only the 'Name' column.

    :return: S_OK() || S_ERROR()
    '''

    return self.rmService.select( 'AccountingCache', self._prepare(locals()) )


  def addOrModifyAccountingCache( self, name = None, plotType = None, plotName = None,
                                  result = None, dateEffective = None, lastCheckTime = None ):
    '''
    Adds or updates-if-duplicated to AccountingCache. Using `name`, `plotType`
    and `plotName` to query the database, decides whether to insert or update the
    table.

    :Parameters:
      **name** - `string`
        name of an individual of the grid topology
      **plotType** - `string`
        the plotType name (e.g. 'Pilot')
      **plotName** - `string`
        the plot name
      **result** - `string`
        command result
      **dateEffective** - `datetime`
        time-stamp from which the result is effective
      **lastCheckTime** - `datetime`
        time-stamp setting last time the result was checked

    :return: S_OK() || S_ERROR()
    '''

    return self.rmService.addOrModify( 'AccountingCache', self._prepare(locals()) )



  def deleteAccountingCache( self, name = None, plotType = None, plotName = None,
                             result = None, dateEffective = None, lastCheckTime = None ):
    '''
    Deletes from AccountingCache all rows that match the parameters given.

    :Parameters:
      **name** - `string`
        name of an individual of the grid topology
      **plotType** - `string`
        the plotType name (e.g. 'Pilot')
      **plotName** - `string`
        the plot name
      **result** - `string`
        command result
      **dateEffective** - `datetime`
        time-stamp from which the result is effective
      **lastCheckTime** - `datetime`
        time-stamp setting last time the result was checked

    :return: S_OK() || S_ERROR()
    '''

    return self.rmService.delete( 'AccountingCache', self._prepare(locals()) )


  # GGUSTicketsCache Methods ...................................................

  def selectGGUSTicketsCache( self, gocSite = None, link = None, openTickets = None,
                              tickets = None, lastCheckTime = None, meta = None ):
    '''
    Gets from GGUSTicketsCache all rows that match the parameters given.

    :Parameters:
      **gocSite** - `string`
      **link** - `string`
        url to the details
      **openTickets** - `integer`
      **tickets** - `string`
      **lastCheckTime** - `datetime`
         time-stamp setting last time the result was checked
      **meta** - `dict`
        metadata for the mysql query. Currently it is being used only for column selection.
        For example: meta = { 'columns' : [ 'Name' ] } will return only the 'Name' column.

    :return: S_OK() || S_ERROR()
    '''

    return self.rmService.select( 'GGUSTicketsCache', self._prepare(locals()) )


  def deleteGGUSTicketsCache( self, gocSite = None, link = None, openTickets = None,
                              tickets = None, lastCheckTime = None ):
    '''
    Deletes from GGUSTicketsCache all rows that match the parameters given.

    :Parameters:
      **gocSite** - `string`
      **link** - `string`
        url to the details
      **openTickets** - `integer`
      **tickets** - `string`
      **lastCheckTime** - `datetime`
         time-stamp setting last time the result was checked

    :return: S_OK() || S_ERROR()
    '''

    return self.rmService.delete( 'GGUSTicketsCache', self._prepare(locals()) )


  def addOrModifyGGUSTicketsCache( self, gocSite = None, link = None, openTickets = None,
                                   tickets = None, lastCheckTime = None ):
    '''
    Adds or updates-if-duplicated to GGUSTicketsCache all rows that match the parameters given.

    :Parameters:
      **gocSite** - `string`
      **link** - `string`
        url to the details
      **openTickets** - `integer`
      **tickets** - `string`
      **lastCheckTime** - `datetime`
         time-stamp setting last time the result was checked

    :return: S_OK() || S_ERROR()
    '''

    return self.rmService.addOrModify( 'GGUSTicketsCache', self._prepare(locals()) )


  # DowntimeCache Methods ......................................................

  def selectDowntimeCache( self, downtimeID = None, element = None, name = None,
                           startDate = None, endDate = None, severity = None,
                           description = None, link = None, dateEffective = None,
                           lastCheckTime = None, gOCDBServiceType = None, meta = None ):
    '''
    Gets from DowntimeCache all rows that match the parameters given.

    :Parameters:
      **downtimeID** - [, `string`, `list`]
        unique id for the downtime
      **element** - [, `string`, `list`]
        valid element in the topology ( Site, Resource, Node )
      **name** - [, `string`, `list`]
        name of the element where the downtime applies
      **startDate** - [, `datetime`, `list`]
        starting time for the downtime
      **endDate** - [, `datetime`, `list`]
        ending time for the downtime
      **severity** - [, `string`, `list`]
        severity assigned by the gocdb
      **description** - [, `string`, `list`]
        brief description of the downtime
      **link** - [, `string`, `list`]
        url to the details
      **dateEffective** - [, `datetime`, `list`]
        time when the entry was created in this database
      **lastCheckTime** - [, `datetime`, `list`]
        time-stamp setting last time the result was checked
      **gOCDBServiceType** - `string`
        service type assigned by gocdb
      **meta** - `dict`
        metadata for the mysql query. Currently it is being used only for column selection.
        For example: meta = { 'columns' : [ 'Name' ] } will return only the 'Name' column.

    :return: S_OK() || S_ERROR()
    '''

    return self.rmService.select( 'DowntimeCache', self._prepare(locals()) )


  def deleteDowntimeCache( self, downtimeID = None, element = None, name = None,
                           startDate = None, endDate = None, severity = None,
                           description = None, link = None, dateEffective = None,
                           lastCheckTime = None, gOCDBServiceType = None ):
    '''
    Deletes from DowntimeCache all rows that match the parameters given.

    :Parameters:
      **downtimeID** - [, `string`, `list`]
        unique id for the downtime
      **element** - [, `string`, `list`]
        valid element in the topology ( Site, Resource, Node )
      **name** - [, `string`, `list`]
        name of the element where the downtime applies
      **startDate** - [, `datetime`, `list`]
        starting time for the downtime
      **endDate** - [, `datetime`, `list`]
        ending time for the downtime
      **severity** - [, `string`, `list`]
        severity assigned by the gocdb
      **description** - [, `string`, `list`]
        brief description of the downtime
      **link** - [, `string`, `list`]
        url to the details
      **dateEffective** - [, `datetime`, `list`]
        time when the entry was created in this database
      **lastCheckTime** - [, `datetime`, `list`]
        time-stamp setting last time the result was checked
      **gOCDBServiceType** - `string`
        service type assigned by gocdb

    :return: S_OK() || S_ERROR()
    '''

    return self.rmService.delete( 'DowntimeCache', self._prepare(locals()) )


  def addOrModifyDowntimeCache( self, downtimeID = None, element = None, name = None,
                                startDate = None, endDate = None, severity = None,
                                description = None, link = None, dateEffective = None,
                                lastCheckTime = None, gOCDBServiceType = None ):
    '''
    Adds or updates-if-duplicated to DowntimeCache. Using `downtimeID` to query
    the database, decides whether to insert or update the table.

    :Parameters:
      **downtimeID** - `string`
        unique id for the downtime
      **element** - `string`
        valid element in the topology ( Site, Resource, Node )
      **name** - `string`
        name of the element where the downtime applies
      **startDate** - `datetime`
        starting time for the downtime
      **endDate** - `datetime`
        ending time for the downtime
      **severity** - `string`
        severity assigned by the gocdb
      **description** - `string`
        brief description of the downtime
      **link** - `string`
        url to the details
      **dateEffective** - `datetime`
        time when the entry was created in this database
      **lastCheckTime** - `datetime`
        time-stamp setting last time the result was checked
      **gOCDBServiceType** - `string`
        service type assigned by gocdb

    :return: S_OK() || S_ERROR()
    '''

    return self.rmService.addOrModify( 'DowntimeCache', self._prepare(locals()) )


  # JobCache Methods ...........................................................

  def selectJobCache( self, site = None, maskStatus = None, efficiency = None,
                      status = None, lastCheckTime = None, meta = None ):
    '''
    Gets from JobCache all rows that match the parameters given.

    :Parameters:
      **site** - `[, string, list ]`
        name of the site element
      **maskStatus** - `[, string, list ]`
        maskStatus for the site
      **efficiency** - `[, float, list ]`
        job efficiency ( successful / total )
      **status** - `[, string, list ]`
        status for the site computed
      **lastCheckTime** - `[, datetime, list ]`
        time-stamp setting last time the result was checked
      **meta** - `dict`
        metadata for the mysql query. Currently it is being used only for column selection.
        For example: meta = { 'columns' : [ 'Name' ] } will return only the 'Name' column.

    :return: S_OK() || S_ERROR()
    '''

    return self.rmService.select( 'JobCache', self._prepare(locals()) )


  def deleteJobCache( self, site = None, maskStatus = None, efficiency = None,
                      status = None, lastCheckTime = None ):
    '''
    Deletes from JobCache all rows that match the parameters given.

    :Parameters:
      **site** - `[, string, list ]`
        name of the site element
      **maskStatus** - `[, string, list ]`
        maskStatus for the site
      **efficiency** - `[, float, list ]`
        job efficiency ( successful / total )
      **status** - `[, string, list ]`
        status for the site computed
      **lastCheckTime** - `[, datetime, list ]`
        time-stamp setting last time the result was checked

    :return: S_OK() || S_ERROR()
    '''

    return self.rmService.delete( 'JobCache', self._prepare(locals()) )


  def addOrModifyJobCache( self, site = None, maskStatus = None, efficiency = None,
                           status = None, lastCheckTime = None ):
    '''
    Adds or updates-if-duplicated to JobCache. Using `site` to query
    the database, decides whether to insert or update the table.

    :Parameters:
      **site** - `[, string, list ]`
        name of the site element
      **maskStatus** - `[, string, list ]`
        maskStatus for the site
      **efficiency** - `[, float, list ]`
        job efficiency ( successful / total )
      **status** - `[, string, list ]`
        status for the site computed
      **lastCheckTime** - `[, datetime, list ]`
        time-stamp setting last time the result was checked

    :return: S_OK() || S_ERROR()
    '''

    return self.rmService.addOrModify( 'JobCache', self._prepare(locals()) )


  # TransferCache Methods ......................................................

  def selectTransferCache( self, sourceName = None, destinationName = None, metric = None,
                           value = None, lastCheckTime = None, meta = None ):
    '''
     Gets from TransferCache all rows that match the parameters given.

     :Parameters:
       **elementName** - `[, string, list ]`
         name of the element
       **direction** - `[, string, list ]`
         the element taken as Source or Destination of the transfer
       **metric** - `[, string, list ]`
         measured quality of failed transfers
       **value** - `[, float, list ]`
         percentage
       **lastCheckTime** - `[, float, list ]`
         time-stamp setting last time the result was checked
      **meta** - `dict`
        metadata for the mysql query. Currently it is being used only for column selection.
        For example: meta = { 'columns' : [ 'Name' ] } will return only the 'Name' column.

     :return: S_OK() || S_ERROR()
    '''

    return self.rmService.select( 'TransferCache', self._prepare(locals()) )


  def deleteTransferCache( self, sourceName = None, destinationName = None, metric = None,
                           value = None, lastCheckTime = None ):
    '''
     Deletes from TransferCache all rows that match the parameters given.

     :Parameters:
       **elementName** - `[, string, list ]`
         name of the element
       **direction** - `[, string, list ]`
         the element taken as Source or Destination of the transfer
       **metric** - `[, string, list ]`
         measured quality of failed transfers
       **value** - `[, float, list ]`
         percentage
       **lastCheckTime** - `[, float, list ]`
         time-stamp setting last time the result was checked

     :return: S_OK() || S_ERROR()
    '''

    return self.rmService.delete( 'TransferCache', self._prepare(locals()) )


  def addOrModifyTransferCache( self, sourceName = None, destinationName = None, metric = None,
                                value = None, lastCheckTime = None ):
    '''
     Adds or updates-if-duplicated to TransferCache. Using `elementName`, `direction`
     and `metric` to query the database, decides whether to insert or update the table.

     :Parameters:
       **elementName** - `string`
         name of the element
       **direction** - `string`
         the element taken as Source or Destination of the transfer
       **metric** - `string`
         measured quality of failed transfers
       **value** - `float`
         percentage
       **lastCheckTime** - `datetime`
         time-stamp setting last time the result was checked

     :return: S_OK() || S_ERROR()
    '''

    return self.rmService.addOrModify( 'TransferCache', self._prepare(locals()) )


  # PilotCache Methods .........................................................

  def selectPilotCache( self, site = None, cE = None, pilotsPerJob = None,
                        pilotJobEff = None, status = None, lastCheckTime = None, meta = None ):
    '''
    Gets from TransferCache all rows that match the parameters given.

    :Parameters:
      **site** - `[, string, list ]`
        name of the site
      **cE** - `[, string, list ]`
        name of the CE of 'Multiple' if all site CEs are considered
      **pilotsPerJob** - `[, float, list ]`
        measure calculated
      **pilotJobEff** - `[, float, list ]`
        percentage
      **status** - `[, float, list ]`
        status of the CE / Site
      **lastCheckTime** - `[, datetime, list ]`
        measure calculated
      **meta** - `dict`
        metadata for the mysql query. Currently it is being used only for column selection.
        For example: meta = { 'columns' : [ 'Name' ] } will return only the 'Name' column.

    :return: S_OK() || S_ERROR()
    '''

    return self.rmService.select( 'PilotCache', self._prepare(locals()) )


  def deletePilotCache( self, site = None, cE = None, pilotsPerJob = None,
                        pilotJobEff = None, status = None, lastCheckTime = None ):
    '''
    Deletes from TransferCache all rows that match the parameters given.

    :Parameters:
      **site** - `[, string, list ]`
        name of the site
      **cE** - `[, string, list ]`
        name of the CE of 'Multiple' if all site CEs are considered
      **pilotsPerJob** - `[, float, list ]`
        measure calculated
      **pilotJobEff** - `[, float, list ]`
        percentage
      **status** - `[, float, list ]`
        status of the CE / Site
      **lastCheckTime** - `[, datetime, list ]`
        measure calculated

    :return: S_OK() || S_ERROR()    '''

    return self.rmService.delete( 'PilotCache', self._prepare(locals()) )


  def addOrModifyPilotCache( self, site = None, cE = None, pilotsPerJob = None,
                             pilotJobEff = None, status = None, lastCheckTime = None ):
    '''
    Adds or updates-if-duplicated to PilotCache. Using `site` and `cE`
    to query the database, decides whether to insert or update the table.

    :Parameters:
      **site** - `string`
        name of the site
      **cE** - `string`
        name of the CE of 'Multiple' if all site CEs are considered
      **pilotsPerJob** - `float`
        measure calculated
      **pilotJobEff** - `float`
        percentage
      **status** - `string`
        status of the CE / Site
      **lastCheckTime** - `datetime`
        measure calculated

    :return: S_OK() || S_ERROR()
    '''

    return self.rmService.addOrModify( 'PilotCache', self._prepare(locals()) )


  # PolicyResult Methods .......................................................

  def selectPolicyResult( self, element = None, name = None, policyName = None,
                          statusType = None, status = None, reason = None,
                          lastCheckTime = None, meta = None ):
    '''
    Gets from PolicyResult all rows that match the parameters given.

    :Parameters:
      **granularity** - `[, string, list]`
        it has to be a valid element ( ValidElement ), any of the defaults: `Site` \
        | `Service` | `Resource` | `StorageElement`
      **name** - `[, string, list]`
        name of the element
      **policyName** - `[, string, list]`
        name of the policy
      **statusType** - `[, string, list]`
        it has to be a valid status type for the given granularity
      **status** - `[, string, list]`
        it has to be a valid status, any of the defaults: `Active` | `Degraded` | \
        `Probing` | `Banned`
      **reason** - `[, string, list]`
        decision that triggered the assigned status
      **lastCheckTime** - `[, datetime, list]`
        time-stamp setting last time the policy result was checked
      **meta** - `dict`
        metadata for the mysql query. Currently it is being used only for column selection.
        For example: meta = { 'columns' : [ 'Name' ] } will return only the 'Name' column.

    :return: S_OK() || S_ERROR()
    '''

    return self.rmService.select( 'PolicyResult', self._prepare(locals()) )


  def deletePolicyResult( self, element = None, name = None, policyName = None,
                          statusType = None, status = None, reason = None,
                          dateEffective = True, lastCheckTime = None ):
    '''
    Deletes from PolicyResult all rows that match the parameters given.

    :Parameters:
      **granularity** - `[, string, list]`
        it has to be a valid element ( ValidElement ), any of the defaults: `Site` \
        | `Service` | `Resource` | `StorageElement`
      **name** - `[, string, list]`
        name of the element
      **policyName** - `[, string, list]`
        name of the policy
      **statusType** - `[, string, list]`
        it has to be a valid status type for the given granularity
      **status** - `[, string, list]`
        it has to be a valid status, any of the defaults: `Active` | `Degraded` | \
        `Probing` | `Banned`
      **reason** - `[, string, list]`
        decision that triggered the assigned status
      **dateEffective** - `datetime`
        time-stamp from which the policy result is effective
      **lastCheckTime** - `[, datetime, list]`
        time-stamp setting last time the policy result was checked

    :return: S_OK() || S_ERROR()
    '''

    return self.rmService.delete( 'PolicyResult', self._prepare(locals()) )


  def addOrModifyPolicyResult( self, element = None, name = None, policyName = None,
                               statusType = None, status = None, reason = None,
                               dateEffective = None, lastCheckTime = None ):
    '''
    Adds or updates-if-duplicated to PolicyResult. Using `name`, `policyName` and
    `statusType` to query the database, decides whether to insert or update the table.

    :Parameters:
      **element** - `string`
        it has to be a valid element ( ValidElement ), any of the defaults: `Site` \
        | `Service` | `Resource` | `StorageElement`
      **name** - `string`
        name of the element
      **policyName** - `string`
        name of the policy
      **statusType** - `string`
        it has to be a valid status type for the given element
      **status** - `string`
        it has to be a valid status, any of the defaults: `Active` | `Degraded` | \
        `Probing` | `Banned`
      **reason** - `string`
        decision that triggered the assigned status
      **dateEffective** - `datetime`
        time-stamp from which the policy result is effective
      **lastCheckTime** - `datetime`
        time-stamp setting last time the policy result was checked

    :return: S_OK() || S_ERROR()
    '''

    return self.rmService.addOrModify( 'PolicyResult', self._prepare(locals()) )


  # PolicyResultLog Methods ....................................................

  def selectPolicyResultLog( self, element = None, name = None, policyName = None,
                             statusType = None, status = None, reason = None,
                             lastCheckTime = None, meta = None ):
    '''
    Gets from PolicyResultLog all rows that match the parameters given.

    :Parameters:
      **element** - `[, string, list]`
        it has to be a valid element ( ValidRes ), any of the defaults: `Site` \
        | `Service` | `Resource` | `StorageElement`
      **name** - `[, string, list]`
        name of the element
      **policyName** - `[, string, list]`
        name of the policy
      **statusType** - `[, string, list]`
        it has to be a valid status type for the given element
      **status** - `[, string, list]`
        it has to be a valid status, any of the defaults: `Active` | `Degraded` | \
        `Probing` | `Banned`
      **reason** - `[, string, list]`
        decision that triggered the assigned status
      **lastCheckTime** - `[, datetime, list]`
        time-stamp setting last time the policy result was checked
      **meta** - `dict`
        metadata for the mysql query. Currently it is being used only for column selection.
        For example: meta = { 'columns' : [ 'Name' ] } will return only the 'Name' column.

    :return: S_OK() || S_ERROR()
    '''

    return self.rmService.select( 'PolicyResultLog', self._prepare(locals()) )


  def deletePolicyResultLog( self, element = None, name = None, policyName = None,
                             statusType = None, status = None, reason = None,
                             lastCheckTime = None ):
    '''
    Deletes from PolicyResult all rows that match the parameters given.

    :Parameters:
      **element** - `[, string, list]`
        it has to be a valid element ( ValidRes ), any of the defaults: `Site` \
        | `Service` | `Resource` | `StorageElement`
      **name** - `[, string, list]`
        name of the element
      **policyName** - `[, string, list]`
        name of the policy
      **statusType** - `[, string, list]`
        it has to be a valid status type for the given element
      **status** - `[, string, list]`
        it has to be a valid status, any of the defaults: `Active` | `Degraded` | \
        `Probing` | `Banned`
      **reason** - `[, string, list]`
        decision that triggered the assigned status
      **lastCheckTime** - `[, datetime, list]`
        time-stamp setting last time the policy result was checked

    :return: S_OK() || S_ERROR()
    '''

    return self.rmService.delete( 'PolicyResultLog', self._prepare(locals()) )


  def addOrModifyPolicyResultLog( self, element = None, name = None, policyName = None,
                                  statusType = None, status = None, reason = None,
                                  lastCheckTime = None ):
    '''
    Adds or updates-if-duplicated to PolicyResultLog. Using `name`, `policyName`,
    'statusType` to query the database, decides whether to insert or update the table.

    :Parameters:
      **element** - `string`
        it has to be a valid element ( ValidRes ), any of the defaults: `Site` \
        | `Service` | `Resource` | `StorageElement`
      **name** - `string`
        name of the element
      **policyName** - `string`
        name of the policy
      **statusType** - `string`
        it has to be a valid status type for the given element
      **status** - `string`
        it has to be a valid status, any of the defaults: `Active` | `Degraded` | \
        `Probing` | `Banned`
      **reason** - `string`
        decision that triggered the assigned status
      **lastCheckTime** - `datetime`
        time-stamp setting last time the policy result was checked

    :return: S_OK() || S_ERROR()
    '''

    return self.rmService.addOrModify( 'PolicyResultLog', self._prepare(locals()) )


  # SpaceTokenOccupancyCache Methods ...........................................

  def selectSpaceTokenOccupancyCache( self, endpoint = None, token = None,
                                      total = None, guaranteed = None, free = None,
                                      lastCheckTime = None, meta = None ):
    '''
    Gets from SpaceTokenOccupancyCache all rows that match the parameters given.

    :Parameters:
      **endpoint** - `[, string, list]`
        srm endpoint
      **token** - `[, string, list]`
        name of the token
      **total** - `[, integer, list]`
        total terabytes
      **guaranteed** - `[, integer, list]`
        guaranteed terabytes
      **free** - `[, integer, list]`
        free terabytes
      **lastCheckTime** - `[, datetime, list]`
        time-stamp from which the result is effective
      **meta** - `dict`
        metadata for the mysql query. Currently it is being used only for column selection.
        For example: meta = { 'columns' : [ 'Name' ] } will return only the 'Name' column.

    :return: S_OK() || S_ERROR()
    '''

    return self.rmService.select( 'SpaceTokenOccupancyCache', self._prepare(locals()) )


  def deleteSpaceTokenOccupancyCache( self, endpoint = None, token = None,
                                      total = None, guaranteed = None, free = None,
                                      lastCheckTime = None ):
    '''
    Deletes from SpaceTokenOccupancyCache all rows that match the parameters given.

    :Parameters:
      **endpoint** - `[, string, list]`
        srm endpoint
      **token** - `[, string, list]`
        name of the token
      **total** - `[, integer, list]`
        total terabytes
      **guaranteed** - `[, integer, list]`
        guaranteed terabytes
      **free** - `[, integer, list]`
        free terabytes
      **lastCheckTime** - `[, datetime, list]`
        time-stamp from which the result is effective

    :return: S_OK() || S_ERROR()
    '''

    return self.rmService.delete( 'SpaceTokenOccupancyCache', self._prepare(locals()) )


  def addOrModifySpaceTokenOccupancyCache( self, endpoint = None, token = None,
                                           total = None, guaranteed = None, free = None,
                                           lastCheckTime = None ):
    '''
    Adds or updates-if-duplicated to SpaceTokenOccupancyCache. Using `site` and `token`
    to query the database, decides whether to insert or update the table.

    :Parameters:
      **endpoint** - `[, string, list]`
        srm endpoint
      **token** - `string`
        name of the token
      **total** - `integer`
        total terabytes
      **guaranteed** - `integer`
        guaranteed terabytes
      **free** - `integer`
        free terabytes
      **lastCheckTime** - `datetime`
        time-stamp from which the result is effective

    :return: S_OK() || S_ERROR()
    '''

    return self.rmService.addOrModify( 'SpaceTokenOccupancyCache', self._prepare(locals()) )

#...............................................................................
#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF
