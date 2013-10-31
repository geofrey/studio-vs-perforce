# studio-vs-perforce

Guidewire Studio doesn't work right with Perforce. This is my quest to fix it.

...That's pretty much it. Studio out of the box has problems, so I originally wrote a quick script to trap p4 commands and try to figure out what was wrong with them.

## Features
- p4.exe doesn't like the username and password specified on its command line. Extract these and set their valuas as environment variables P4USER and P4PASSWD
- 'p4 print' by default prints the depot path of the file being listed. Studio doesn't know to disable this with the -q flag. Add the flag to command lines whose operation is 'print'
- Studio's settings ask for Perforce user name and password, but Studio is unable to log in to Perforce when an active ticket does not already exist. Invoke 'p4 login' when 'p4 tickets' gives no results.

## Known Bugs Remaining
- The initial command line starting with 'p4shim.cmd' is printed in the contents of the source file when invoking diff from Studio's Source Control menu. I don't know where this is coming from, but suppressing it with @ in the shell causes the first line of the file to also be omitted; this makes the first line of the target file (usually a 'package' directive) appear to be added in target.
- p4shim logging could be nicer. Currently using a simple text file, but Studio appears to use several or many worker threads at startup to p4 fstat all its resources; this doesn't seem to be a problem so far but there could be open() errors getting the log file if another process is in the middle of logging its own work.
- ???
