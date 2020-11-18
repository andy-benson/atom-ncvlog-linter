#-----------------------------------------------------------------------------
# run ncvlog and return data formatted for the providelinter function 
#
# Input: file to lint.
#
# Example Output ( from ncvlog) :
#   
#   ncvlog: *E,EXPCOM (lint_test.sv,21|8): expecting a comma [3.2.1][6.1(IEEE)].
#
# Example Output to providelinter:
#
# lint_test.sv:21:Error:expecting a comma [3.2.1][6.1(IEEE)].
#
#-----------------------------------------------------------------------------


from __future__ import print_function
import sys
import subprocess

import os
import re
import shutil
import glob


args = sys.argv
filelist=args[1:]
filelist[0] = os.path.abspath(filelist[0])
head_tail = os.path.split(filelist[0])
filepath = head_tail[0]

incdir_cmd = "+incdir+" + filepath

out = ""
#-----------------------------------------------------------------------------
# subroutine to extract data from the error line line provided from ncvlog
#-----------------------------------------------------------------------------

def process_line(msg_type,line):
    
    #print(msg_type)
    my_line = str(line)
    
    matches = re.search(r"\(([\w\.\/-]+),(\d*)\|\d*\):\s(.+\.$)", my_line)
    
    if (matches):
        file     = str(matches.group(1))
        line_num = str(matches.group(2))
        message  = str(matches.group(3))
    
        return file +":"+ line_num +":"+ msg_type +":"+ message + "\n\n"
    
    # if there no match something has gone wrong with the regex, put error on first line 
    else:    
        return str(filelist[0]) +":0:Error:"+ my_line + "\n\n" 



#-----------------------------------------------------------------------------
# run ncvlog on the current file
# logfile and worklib are send to /tmp and not required , so easy way of cleanup
#-----------------------------------------------------------------------------

ncvlog_output = subprocess.Popen(["ncvlog", incdir_cmd, "-sv", "-logfile", "/tmp/logfile", (filelist[0])], stdout=subprocess.PIPE, universal_newlines=True)


tmp = ncvlog_output.communicate()


lines = tmp[0]
lines = lines.split("\n")


#-----------------------------------------------------------------------------
# parse each of the lines looking for the ncvlog info / warning / error codes
#----------------------------------------------------------------------------

for line in lines:
    #print(line)
    if line.startswith("ncvlog: *E"):
            out += process_line("Error",line)

    if line.startswith("ncvlog: *W"):
            out += process_line("Warning",line)
            
    if line.startswith("ncvlog: *I"):
            out += process_line("Info",line)

    if line.startswith("ncvlog: *F"):
            out += process_line("Fatal",line)
            
#-----------------------------------------------------------------------------
# clean up temp files
# still got a weird issue of race condition *only* when this file is executed from 
# atom-ncvlog-linter. Deleting INCA_libs can cause an error with ncvlog and 
# it creates an err file.
# This is really weird as the subprocess.run should wait before continuing
# with the program execution ( i.e. deletion of the library)
# No problems when execute core_ncvlog.py directly.. 
#-----------------------------------------------------------------------------

dir_path = 'INCA_libs'
if os.path.exists(dir_path):
    shutil.rmtree(dir_path, ignore_errors=True)


err_files= glob.glob("*.err")
for err_file in err_files:
    os.remove(err_file)

    
#-----------------------------------------------------------------------------
# return formatted errors back to calling java script
#----------------------------------------------------------------------------

print(out)

#exit(0)
