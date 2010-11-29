#!/usr/bin/env python
########################################################################
# $HeadURL$
########################################################################
__RCSID__   = "$Id$"

import pprint
import sys
from DIRAC import gLogger
from DIRAC.Core.Base import Script
from DIRAC.AccountingSystem.private.FileCoding import extractRequestFromFileId

Script.parseCommandLine()

fileIds = Script.getPositionalArgs()

for fileId in fileIds:
  result = extractRequestFromFileId( fileId )
  if not result[ 'OK' ]:
    gLogger.error( "Could not decode fileId","'%s', error was %s" % ( fileId, result[ 'Messaage' ] ) )
    sys.exit(1)
  gLogger.notice( "Decode for '%s' is:\n%s" % ( fileId, pprint.pformat( result[ 'Value' ] ) ) )

sys.exit(0)
