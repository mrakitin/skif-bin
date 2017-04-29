#!/usr/bin/python
# encoding: utf-8

import os
import fnmatch
from optparse import OptionParser


#-------------------------------------------------------------------------------
# Options:

parser = OptionParser()

parser.add_option("-d", "--dir", dest="topdir", default=None,
                  help="Display calculations in the specified directory", metavar="DIR")
parser.add_option("-s", "--search", dest="mask", default=None,
                  help="Filter calculations by mask", metavar="MASK")

(options, args) = parser.parse_args()

#if not options.envdir:
#    parser.error('No environment dir specified.')

parser.destroy()

print 'options.topdir:', options.topdir


#------------------------------------------------------------------------------
# Find all *.dayfile files:

def dayfiles(dir):
    dir = os.path.abspath(dir)
    print 'Root dir:', dir

    matches = []
    for root, dirnames, filenames in os.walk(dir):
        for filename in fnmatch.filter(filenames, '*.dayfile'):
            matches.append(os.path.join(root, filename))

    return matches


#------------------------------------------------------------------------------
# Find directories to process:

#rootdir = '/home/max/calc/Fe53MeH/Fe53AlH'
rootdir = os.getcwd()
dayfiles_list = dayfiles(rootdir)


#-------------------------------------------------------------------------------
# Get running jobs and their attributes:

'''
NodeList
ExcNodeList
MinTmpDiskNode
Restarts
MinMemoryNode
Shared
EndTime
Network
QOS
SubmitTime
Gres
UserId
SecsPreSuspend
JobId
PreemptTime
Reason
TimeMin
ReqS:C:T
Reservation
NumCPUs
ReqNodeList
Account
WorkDir
Name
NumNodes
CPUs/Task
Partition
Dependency
Command
AllocNode:Sid
JobState
Requeue
MinCPUsNode
Priority
SuspendTime
Features
BatchFlag
EligibleTime
Contiguous
TimeLimit
StartTime
BatchHost
Licenses
RunTime
GroupId
ExitCode
'''


def scontrol_jobs(jobid = None):
    command = 'scontrol show job -o'
    if jobid is not None:
        command = command + ' ' + str(jobid)

    scontrol = os.popen(command).read().split('\n')
    scontrol_dict = {}

    for i in scontrol:
        attributes = i.split()
        for j in attributes:
            key   = j.split('=')[0]
            value = j.split('=')[1]
            scontrol_dict[key] = []
        break

    for i, attr_name in enumerate(scontrol_dict.keys()):
        values = []
        for j in scontrol:
            attributes = j.split()
            for k in attributes:
                if k.split('=')[0] == attr_name:
                    value = k.split('=')[1]
                    values.append(value)
        scontrol_dict[attr_name] = values

    return scontrol_dict



def dir2stat(dir):
    scontrol_dict = scontrol_jobs()

    status  = ''
    jobid   = '--'
    workdir = ''

    #---------------------------------------------------------------------------
    # Running job cases:

    if scontrol_dict != {}:
        # and os.path.abspath(dir) in scontrol_dict['WorkDir']:
        for i, name in enumerate(scontrol_dict['WorkDir']):
            if name.find(dir) >= 0 or dir.find(name) >= 0:
                status  = '*' + scontrol_dict['JobState'][i][0] + '*'
                jobid   = scontrol_dict['JobId'][i]
                workdir = scontrol_dict['WorkDir'][i]
                break


    #---------------------------------------------------------------------------
    # Non-running job cases:
    
    if jobid  == '--':
        basename = os.path.basename(dir)
        if os.path.exists(dir):
            os.chdir(dir)
            workdir = os.path.abspath(dir)
        else:
            print 'Error!!! Dir ' + dir + ' doesn\'t exist.'
            exit(1)

        dayfile = basename + '.dayfile'
        scffile = basename + '.scf'
        scfmini = scffile  + '_mini'
        logfile = ':log'

        f_dayfile = open(dayfile, 'rb')
        dayfile_content = f_dayfile.readlines()
        f_dayfile.close()

        stop_line = ''
        for i in dayfile_content:
            if i.find('>   stop') >= 0:
                stop_line = i.strip()
                break

        if stop_line == '>   stop':
            status = '-S-'
        elif stop_line == '>   stop error':
            status = '!E!'
        else:
            status = '?U?'

        #-----------------------------------------------------------------------

    return_dict = {
		    'status' : status,
		    'jobid'  : jobid,
		    'workdir': workdir
		  }
    return return_dict

a = [
     '/storage/home/max/calc/Fe53MeH/Fe53ZnH/optimized/Fe53ZnH_05/Fe53Zn_05_16.168600',
             '/home/max/calc/Fe53MeH/Fe53ZnH/optimized/Fe53ZnH_05/Fe53Zn_05_16.168600',
             '/home/max/calc/Fe53MeH/Fe53MnH/optimized/Fe53MnH_01/Fe53Mn_01_16.126500',
             '/home/max/calc/Fe53MeH/Fe53AlH/Fe53Al_0X/Fe53Al_01',
             '/home/max/calc/Fe53MeH/Fe53AlH/Fe53Al_0X/Fe53Al_05',
    ]

for i in a:
    status = dir2stat(i)
    print 'Status:', status


dict = scontrol_jobs()
for i in dict.keys():
    print i + ':', dict[i]


exit(9999)










for i in dayfiles_list:
    cur_dayfile = i
    cur_dir  = os.path.dirname(cur_dayfile)
    cur_basename = '.'.join(os.path.basename(cur_dayfile).split('.')[:-1])
    os.chdir(cur_dir)
    print os.getcwd()
    print cur_basename

    scf_file = cur_basename + '.scf'
    log_file = ':log'

    f_dayfile = open(cur_dayfile, 'rb')
    dayfile_content = f_dayfile.readlines()
    f_dayfile.close()

    stop_line = ''
    for j in dayfile_content:
        if j.find('>   stop') >= 0:
            #print j
            stop_line = j.strip()
            break


    print '===' + stop_line + '==='
    status = ''
    jobid  = None
    if stop_line == '>   stop':
        status = '-S-'
    elif stop_line == '>   stop error':
        status = '!E!'
    else:
        if jobid:
            status = '+R+'	
        else:
            status = '?U?'

    print 'Status:', status

    print
    os.chdir(rootdir)


