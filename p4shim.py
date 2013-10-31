import datetime
import io
import os
import re
import subprocess
import sys
import time

args = sys.argv[1:]

log = open(r'c:\dev\tools\studio-vs-perforce\p4shim.txt', 'a')
stamp = datetime.datetime.now()

def extricate(flag, envname):
	global args
	if flag in args:
		p_at = args.index(flag)
		value = args[p_at+1]
		args[p_at:p_at+2] = []
		os.putenv(envname, value)

# It may be peculiar to my setup, but p4 is ignoring the username and password options and only responds to the corresponding environment variables.
to_env = [('-u', 'P4USER'), ('-P', 'P4PASSWD')]
list(map(lambda params: extricate(*params), to_env)) # list() to force evaluation - map is lazy

# if there's no active ticket, log in before proceeding
tickets = subprocess.Popen(['p4', 'tickets'], stdout=subprocess.PIPE, stderr=log).communicate()[0].split()
if len(tickets) == 0:
	log.write('[Log in.]\n')
	thepass = r'C:\dev\tools\studio-vs-perforce\p4shim.password'
	status = subprocess.call('p4 login', stdin=open(thepass), stdout=open(os.devnull), stderr=log)
	if status != 0:
		log.write('[Login error]\n')
		# maybe quit here?
def tokenize_args(args):
	args2 = args[:]
	while args2:
		if args2[0].startswith('-'):
			yield args2[:2]
			args2[:2] = []
		else:
			yield args2[:1]
			args2[:1] = []

if ['print'] in tokenize_args(args):
	# 'p4 print' mentions its file path on stdout, which is silly
	args[-1:-1] = ['-q'] # so we tell it to stick to business

for i in range(len(args)):
	if ' ' in args[i]:
		args[i] = '"{}"'.format(args[i]) # re-quote arguments that need 'em. doesn't handle escapes.

#p4 = r'"C:\Program Files\Perforce\p4"'
p4 = 'p4'
commandline = ' '.join([p4]+args)

log.write('{}\t{} {}\n'.format(stamp, p4, ' '.join(args)))

log.flush()
log.close()

# not redirecting anything here to try to stay transparent for Studio
exit(subprocess.call(commandline))

#
