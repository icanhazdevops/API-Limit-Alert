#!/usr/bin/env python
# Copyright 2013 Rackspace

# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import os
import sys
import pyrax
import argparse

def main(argv):
  parser = argparse.ArgumentParser(description='get percent of api limit of ram used')
  parser.add_argument('-u','--username', help='Rackspace Username', required=True)
  parser.add_argument('-a','--apikey', help='Rackspace API Key', required=True)
  parser.add_argument('-m','--maxthreshold', help='API Percent Used Threshold, integer between 1-99', required=True)
  args = parser.parse_args()

  pyrax.set_setting("identity_type", "rackspace")
  pyrax.set_credentials(args.username, args.apikey)
  
  
  getlimit(args.maxthreshold)

def getlimit(maxthreshold):
  cs = pyrax.cloudservers
  cslimits = cs.limits.get()
  # Convert the generator to a list
  cslimits_list = [rate for rate in cslimits.absolute]
  # Pull out max_ram api limit and total used ram from list
  max_ram = [x.value for x in cslimits_list if x.name == "maxTotalRAMSize"][0]
  total_ram = [x.value for x in cslimits_list if x.name == "totalRAMUsed"][0]
  #Get the percent ram used and round it up for clean output
  percent_ram = (float(total_ram) / float(max_ram)) * 100
  percent_ram_used = round(float(("%.2f" % percent_ram)))

  ######If this is anything other then Cloud Monitoring custom agent plugin
  ######just print nicely to the terminal.  Comment out section if using as a CM Agent Plugin.
  print "Current RAM Usage: %sMB" % total_ram
  print "Max RAM API Limit: %sMB" % max_ram
  if percent_ram_used >= float(maxthreshold):
    print "WARNING: Percent of API Limit Used: %s" % percent_ram_used + "%"
  else:
    print "OK: Percent of API Limit Used: %s" % percent_ram_used + "%"

  ######If this is for Cloud Monitoring Agent Plugin uncomment this section
  #test percent ram used against threshold
  #Print status and metric lines that Cloud Monitoring Agent Plugin needs
  #if percent_ram_used < float(maxthreshold):
  #	print "status ok Percent RAM Used", percent_ram_used
  #	print "metric percent_ram_used float", percent_ram_used
  #else:
  #	print "status err Percent RAM Used", percent_ram_used
  #	print "metric percent_ram_used float", percent_ram_used

if __name__ == "__main__":
   main(sys.argv[1:])