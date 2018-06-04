# studio-vs-perforce

Guidewire Studio V7 didn't work right with Perforce. This was my quest to fix it.

...That's pretty much it. Studio out of the box has problems, so I originally wrote a quick script to trap p4 commands and try to figure out what was wrong with them.

## Features
### Command-line Fixups
- p4.exe doesn't like the username and password specified on its command line. Extract these and set their valuas as environment variables P4USER and P4PASSWD
- 'p4 print' by default prints the depot path of the file being listed. Studio doesn't know to disable this with the -q flag. Add the flag to command lines whose operation is 'print'

### Session
- Studio's settings ask for Perforce user name and password, but Studio is unable to log in to Perforce when an active ticket does not already exist. Check 'p4 login -s' and create a new session when needed.
