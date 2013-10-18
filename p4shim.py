import datetime
import os
import re
import subprocess
import sys

args = sys.argv[1:]

def extricate(flag, envname):
	global args
	p_at = args.index(flag)
	value = args[p_at+1]
	args[p_at:p_at+2] = []
	os.putenv(envname, value)

#extricate('-u', 'P4USER')
#extricate('-P', 'P4PASSWD')

to_env = [('-u', 'P4USER'), ('-P', 'P4PASSWD')]
list(map(lambda params: extricate(*params), to_env)) # list() to force evaluation - map is lazy?

for i in range(len(args)):
	if ' ' in args[i]:
		args[i] = '"{}"'.format(args[i]) # re-quote arguments that need 'em. doesn't handle escapes.
commandline = ' '.join(['p4']+args)

log = open(r'c:\dev\tools\p4shim.txt', 'a')
stamp = datetime.datetime.now()
log.write('{}\t{} {}\n'.format(stamp, sys.argv[0], ' '.join(args)))
log.flush()
subprocess.call(commandline, shell=True, stderr=log)

log.close()

#