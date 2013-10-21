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

# It may be peculiar to my setup, but p4 is ignoring the username and password options and only responds to the corresponding environment variables.
to_env = [('-u', 'P4USER'), ('-P', 'P4PASSWD')]
list(map(lambda params: extricate(*params), to_env)) # list() to force evaluation - map is lazy

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

log = open(r'c:\dev\tools\studio-vs-perforce\p4shim.txt', 'a')
stamp = datetime.datetime.now()
log.write('{}\t{} {}\n'.format(stamp, p4, ' '.join(args)))
log.flush()
sys.stdout.flush()
subprocess.call(commandline, shell=True, stderr=log)

log.close()

#