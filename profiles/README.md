# profiles manual

profiles describes to app how each esc/pos (based) printers works with different commands

## command format

commands defenied in the profile must follow these rules:
1. command must contain only **ASCII** chars
2. each parameter must be separated by space
3. make sure you used correct char case

each number in command will be parsed **as number**, not as the  ASCII charater! 

supported command basics (not case-sensetive):

`ESC`, `GS`, `DLE`, `EOT`, `ENQ`, `SP`, `LF`, `FF`, `CR`

### examples

command: **ESC c0 SP n**

if it stored incorrectly like:

`ESC C0 sp 0`

it will be parsed as:

`1B 43 30 20 00` 

which is equivalent to **ESC C 31 SP 0**

in this example rules **2** and **3** not followed: you dont separated `0` from `C` and uses incorrect `c` case

but if you store this command in correct way like:

`ESC c 0 sp 0`

it will be parsed as:

`1B 63 00 20 00` 

which is equivalent to **ESC c0 SP 0** (our command)