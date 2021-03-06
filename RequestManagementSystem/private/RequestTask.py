########################################################################
# $HeadURL $
# File: RequestTask.py
# Author: Krzysztof.Ciba@NOSPAMgmail.com
# Date: 2013/03/13 12:42:45
########################################################################

""" :mod: RequestTask

    =================

    .. module: RequestTask

    :synopsis: request processing task

    .. moduleauthor:: Krzysztof.Ciba@NOSPAMgmail.com

    request processing task to be used inside ProcessTask created in RequesteExecutingAgent
"""
__RCSID__ = "$Id $"
# #
# @file RequestTask.py
# @author Krzysztof.Ciba@NOSPAMgmail.com
# @date 2013/03/13 12:42:54
# @brief Definition of RequestTask class.
# # imports
import os
import time
# # from DIRAC
from DIRAC import gLogger, S_OK, S_ERROR, gConfig
from DIRAC.FrameworkSystem.Client.MonitoringClient import gMonitor
from DIRAC.RequestManagementSystem.Client.ReqClient import ReqClient
from DIRAC.RequestManagementSystem.Client.Request import Request
from DIRAC.RequestManagementSystem.private.OperationHandlerBase import OperationHandlerBase
from DIRAC.FrameworkSystem.Client.ProxyManagerClient import gProxyManager
from DIRAC.ConfigurationSystem.Client.ConfigurationData import gConfigurationData
from DIRAC.ConfigurationSystem.Client.Helpers.Operations import Operations
from DIRAC.Core.DISET.RPCClient import RPCClient
from DIRAC.Core.Security import CS

########################################################################


class RequestTask(object):
  """
  .. class:: RequestTask

  request's processing task
  """

  def __init__(
          self,
          requestJSON,
          handlersDict,
          csPath,
          agentName,
          standalone=False,
          requestClient=None):
    """c'tor

    :param self: self reference
    :param str requestJSON: request serialized to JSON
    :param dict opHandlers: operation handlers
    """
    self.request = Request(requestJSON)
    # # csPath
    self.csPath = csPath
    # # agent name
    self.agentName = agentName
    # # standalone flag
    self.standalone = standalone
    # # handlers dict
    self.handlersDict = handlersDict
    # # handlers class def
    self.handlers = {}
    # # own sublogger
    self.log = gLogger.getSubLogger("pid_%s/%s" % (os.getpid(), self.request.RequestName))
    # # get shifters info
    self.__managersDict = {}
    shifterProxies = self.__setupManagerProxies()
    if not shifterProxies["OK"]:
      self.log.error(shifterProxies["Message"])

    # # initialize gMonitor
    gMonitor.setComponentType(gMonitor.COMPONENT_AGENT)
    gMonitor.setComponentName(self.agentName)
    gMonitor.initialize()

    # # own gMonitor activities
    gMonitor.registerActivity("RequestAtt", "Requests processed",
                              "RequestExecutingAgent", "Requests/min", gMonitor.OP_SUM)
    gMonitor.registerActivity("RequestFail", "Requests failed",
                              "RequestExecutingAgent", "Requests/min", gMonitor.OP_SUM)
    gMonitor.registerActivity("RequestOK", "Requests done",
                              "RequestExecutingAgent", "Requests/min", gMonitor.OP_SUM)

    if requestClient is None:
      self.requestClient = ReqClient()
    else:
      self.requestClient = requestClient

  def __setupManagerProxies(self):
    """ setup grid proxy for all defined managers """
    oHelper = Operations()
    shifters = oHelper.getSections("Shifter")
    if not shifters["OK"]:
      self.log.error(shifters["Message"])
      return shifters
    shifters = shifters["Value"]
    for shifter in shifters:
      shifterDict = oHelper.getOptionsDict("Shifter/%s" % shifter)
      if not shifterDict["OK"]:
        self.log.error(shifterDict["Message"])
        continue
      userName = shifterDict["Value"].get("User", "")
      userGroup = shifterDict["Value"].get("Group", "")

      userDN = CS.getDNForUsername(userName)
      if not userDN["OK"]:
        self.log.error(userDN["Message"])
        continue
      userDN = userDN["Value"][0]
      vomsAttr = CS.getVOMSAttributeForGroup(userGroup)
      if vomsAttr:
        self.log.debug("getting VOMS [%s] proxy for shifter %s@%s (%s)" % (vomsAttr, userName,
                                                                           userGroup, userDN))
        getProxy = gProxyManager.downloadVOMSProxyToFile(userDN, userGroup,
                                                         requiredTimeLeft=1200,
                                                         cacheTime=4 * 43200)
      else:
        self.log.debug("getting proxy for shifter %s@%s (%s)" % (userName, userGroup, userDN))
        getProxy = gProxyManager.downloadProxyToFile(userDN, userGroup,
                                                     requiredTimeLeft=1200,
                                                     cacheTime=4 * 43200)
      if not getProxy["OK"]:
        self.log.error(getProxy["Message"])
        return S_ERROR("unable to setup shifter proxy for %s: %s" % (shifter, getProxy["Message"]))
      chain = getProxy["chain"]
      fileName = getProxy["Value"]
      self.log.debug("got %s: %s %s" % (shifter, userName, userGroup))
      self.__managersDict[shifter] = {"ShifterDN": userDN,
                                      "ShifterName": userName,
                                      "ShifterGroup": userGroup,
                                      "Chain": chain,
                                      "ProxyFile": fileName}
    return S_OK()

  def setupProxy(self):
    """ download and dump request owner proxy to file and env

    :return: S_OK with name of newly created owner proxy file and shifter name if any
    """
    self.__managersDict = {}
    shifterProxies = self.__setupManagerProxies()
    if not shifterProxies["OK"]:
      self.log.error(shifterProxies["Message"])

    ownerDN = self.request.OwnerDN
    ownerGroup = self.request.OwnerGroup
    isShifter = []
    for shifter, creds in self.__managersDict.items():
      if creds["ShifterDN"] == ownerDN and creds["ShifterGroup"] == ownerGroup:
        isShifter.append(shifter)
    if isShifter:
      proxyFile = self.__managersDict[isShifter[0]]["ProxyFile"]
      os.environ["X509_USER_PROXY"] = proxyFile
      return S_OK({"Shifter": isShifter, "ProxyFile": proxyFile})

    # # if we're here owner is not a shifter at all
    ownerProxyFile = gProxyManager.downloadVOMSProxyToFile(ownerDN, ownerGroup)
    if not ownerProxyFile["OK"] or not ownerProxyFile["Value"]:
      reason = ownerProxyFile.get("Message", "No valid proxy found in ProxyManager.")
      return S_ERROR("Change proxy error for '%s'@'%s': %s" % (ownerDN, ownerGroup, reason))

    ownerProxyFile = ownerProxyFile["Value"]
    os.environ["X509_USER_PROXY"] = ownerProxyFile
    return S_OK({"Shifter": isShifter, "ProxyFile": ownerProxyFile})

  @staticmethod
  def getPluginName(pluginPath):
    if not pluginPath:
      return ''
    if "/" in pluginPath:
      pluginPath = ".".join([chunk for chunk in pluginPath.split("/") if chunk])
    return pluginPath.split(".")[-1]

  @staticmethod
  def loadHandler(pluginPath):
    """ Create an instance of requested plugin class, loading and importing it when needed.
    This function could raise ImportError when plugin cannot be find or TypeError when
    loaded class object isn't inherited from BaseOperation class.

    :param str pluginName: dotted path to plugin, specified as in import statement, i.e.
        "DIRAC.CheesShopSystem.private.Cheddar" or alternatively in 'normal' path format
        "DIRAC/CheesShopSystem/private/Cheddar"

    :return: object instance

    This function try to load and instantiate an object from given path. It is assumed that:

      * `pluginPath` is pointing to module directory "importable" by python interpreter, i.e.: it's
        package's top level directory is in $PYTHONPATH env variable,
      * the module should consist a class definition following module name,
      *  the class itself is inherited from DIRAC.RequestManagementSystem.private.BaseOperation.BaseOperation

    If above conditions aren't meet, function is throwing exceptions:

    :raises ImportError: when class cannot be imported
    :raises TypeError: when class isn't inherited from OperationHandlerBase
    """
    if "/" in pluginPath:
      pluginPath = ".".join([chunk for chunk in pluginPath.split("/") if chunk])
    pluginName = pluginPath.split(".")[-1]
    if pluginName not in globals():
      mod = __import__(pluginPath, globals(), fromlist=[pluginName])
      pluginClassObj = getattr(mod, pluginName)
    else:
      pluginClassObj = globals()[pluginName]
    if not issubclass(pluginClassObj, OperationHandlerBase):
      raise TypeError(
          "operation handler '%s' isn't inherited from OperationHandlerBase class" %
          pluginName)
    for key, status in (("Att", "Attempted"), ("OK", "Successful"), ("Fail", "Failed")):
      gMonitor.registerActivity(
          "%s%s" %
          (pluginName, key), "%s operations %s" %
          (pluginName, status), "RequestExecutingAgent", "Operations/min", gMonitor.OP_SUM)
    # # return an instance
    return pluginClassObj

  def getHandler(self, operation):
    """ return instance of a handler for a given operation type on demand
        all created handlers are kept in self.handlers dict for further use

    :param ~Operation.Operation operation: Operation instance
    """
    if operation.Type not in self.handlersDict:
      return S_ERROR("handler for operation '%s' not set" % operation.Type)
    handler = self.handlers.get(operation.Type, None)
    if not handler:
      try:
        handlerCls = self.loadHandler(self.handlersDict[operation.Type])
        self.handlers[operation.Type] = handlerCls(
            csPath="%s/OperationHandlers/%s" % (self.csPath, operation.Type))
        handler = self.handlers[operation.Type]
      except (ImportError, TypeError) as error:
        self.log.exception("getHandler: %s" % str(error), lException=error)
        return S_ERROR(str(error))
    # # set operation for this handler
    handler.setOperation(operation)
    # # and return
    return S_OK(handler)

  def updateRequest(self):
    """ put back request to the RequestDB """
    updateRequest = self.requestClient.putRequest(
        self.request, useFailoverProxy=False, retryMainService=2)
    if not updateRequest["OK"]:
      self.log.error(updateRequest["Message"])
    return updateRequest

  def __call__(self):
    """ request processing """

    self.log.debug("about to execute request")
    gMonitor.addMark("RequestAtt", 1)

    # # setup proxy for request owner
    setupProxy = self.setupProxy()
    if not setupProxy["OK"]:
      self.request.Error = setupProxy["Message"]
      if 'has no proxy registered' in setupProxy["Message"]:
        self.log.error('Request set to Failed:', setupProxy["Message"])
        # If user is no longer registered, fail the request
        for operation in self.request:
          for opFile in operation:
            opFile.Status = 'Failed'
          operation.Status = 'Failed'
      else:
        self.log.error(setupProxy["Message"])
      return S_OK(self.request)
    shifter = setupProxy["Value"]["Shifter"]
    proxyFile = setupProxy["Value"]["ProxyFile"]

    error = None
    while self.request.Status == "Waiting":

      # # get waiting operation
      operation = self.request.getWaiting()
      if not operation["OK"]:
        self.log.error(operation["Message"])
        return operation
      operation = operation["Value"]
      self.log.info("executing operation #%s '%s'" % (operation.Order, operation.Type))

      # # and handler for it
      handler = self.getHandler(operation)
      if not handler["OK"]:
        self.log.error("unable to process operation %s: %s" % (operation.Type, handler["Message"]))
        # gMonitor.addMark( "%s%s" % ( operation.Type, "Fail" ), 1 )
        operation.Error = handler["Message"]
        break

      handler = handler["Value"]
      # # set shifters list in the handler
      handler.shifter = shifter
      # # and execute
      pluginName = self.getPluginName(self.handlersDict.get(operation.Type))
      if self.standalone:
        useServerCertificate = gConfig.useServerCertificate()
      else:
        # Always use server certificates if executed within an agent
        useServerCertificate = True
      try:
        if pluginName:
          gMonitor.addMark("%s%s" % (pluginName, "Att"), 1)
        # Always use request owner proxy
        if useServerCertificate:
          gConfigurationData.setOptionInCFG('/DIRAC/Security/UseServerCertificate', 'false')
        exe = handler()
        if useServerCertificate:
          gConfigurationData.setOptionInCFG('/DIRAC/Security/UseServerCertificate', 'true')
        if not exe["OK"]:
          self.log.error("unable to process operation %s: %s" % (operation.Type, exe["Message"]))
          if pluginName:
            gMonitor.addMark("%s%s" % (pluginName, "Fail"), 1)
          gMonitor.addMark("RequestFail", 1)
          if self.request.JobID:
            # Check if the job exists
            monitorServer = RPCClient("WorkloadManagement/JobMonitoring", useCertificates=True)
            res = monitorServer.getJobPrimarySummary(int(self.request.JobID))
            if not res["OK"]:
              self.log.error("RequestTask: Failed to get job %d status" % self.request.JobID)
            elif not res['Value']:
              self.log.warn(
                  "RequestTask: job %d does not exist (anymore): failed request" %
                  self.request.JobID)
              for opFile in operation:
                opFile.Status = 'Failed'
              if operation.Status != 'Failed':
                operation.Status = 'Failed'
              self.request.Error = 'Job no longer exists'
      except Exception as error:
        self.log.exception("hit by exception: %s" % str(error))
        if pluginName:
          gMonitor.addMark("%s%s" % (pluginName, "Fail"), 1)
        gMonitor.addMark("RequestFail", 1)
        if useServerCertificate:
          gConfigurationData.setOptionInCFG('/DIRAC/Security/UseServerCertificate', 'true')
        break

      # # operation status check
      if operation.Status == "Done" and pluginName:
        gMonitor.addMark("%s%s" % (pluginName, "OK"), 1)
      elif operation.Status == "Failed" and pluginName:
        gMonitor.addMark("%s%s" % (pluginName, "Fail"), 1)
      elif operation.Status in ("Waiting", "Scheduled"):
        # # no update for waiting or all files scheduled
        break

    gMonitor.flush()

    if error:
      return S_ERROR(error)

    # # request done?
    if self.request.Status == "Done":
      # # update request to the RequestDB
      self.log.info('updating request with status %s' % self.request.Status)
      update = self.updateRequest()
      if not update["OK"]:
        self.log.error(update["Message"])
        return update
      self.log.info("request '%s' is done" % self.request.RequestName)
      gMonitor.addMark("RequestOK", 1)
      # # and there is a job waiting for it? finalize!
      if self.request.JobID:
        attempts = 0
        while True:
          finalizeRequest = self.requestClient.finalizeRequest(
              self.request.RequestID, self.request.JobID)  # pylint: disable=no-member
          if not finalizeRequest["OK"]:
            if not attempts:
              self.log.error(
                  "unable to finalize request %s: %s, will retry" %
                  (self.request.RequestName, finalizeRequest["Message"]))
            self.log.verbose("Waiting 10 seconds")
            attempts += 1
            if attempts == 10:
              self.log.error("giving up finalize request after %d attempts" % attempts)
              return S_ERROR('Could not finalize request')

            time.sleep(10)

          else:
            self.log.info(
                "request '%s' is finalized%s" %
                (self.request.RequestName,
                 (' after %d attempts' %
                  attempts) if attempts else ''))
            break

    # Request will be updated by the callBack method
    self.log.verbose("RequestTasks exiting, request %s" % self.request.Status)
    return S_OK(self.request)
