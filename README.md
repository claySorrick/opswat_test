README

this is a test for opswat software engineer position

to run use:

python scan.py filename.txt

This program uses python3

and uses the following packages

-sys
-hashlib
-json
-os
-time
-requests


this program will create a hash (sha1) for a given file

the program will try to send a GET request to opswat with the given hash code

if the hash code is found on opswat,

  the results are printed

if the hash code is not found,

  the file will be uploaded to opswat via a POST request

  then the program will ping opswat for the status of the scan

  once the scan finishes the results are printed


Some of the code used was taken from documentation/stackoverflow and manipulated to fit the current needs


I use an external file, apiKey.txt, to hold the given api key.

If the file does not exist, the program uses a hardcoded api key which can be changed to the api key used to test this program on opswat's end