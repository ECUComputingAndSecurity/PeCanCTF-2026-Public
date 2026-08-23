# Walkthrough
You are meant to use the command line to find the filename that has the flag, rather than manually searching each directory!

The easiest way to find it, in a single command, is to run the following command from the top-level "Files" folder:
find . -name "pecan\*"

As we know that the flag starts with "pecan", we can use a wildcard search to find it at the start of a filename. The dot "." indicates that we are searching from our current directory (Files).

This will therefore reveal that the file is in the following directory, revealing the flag:
./Documents/Important/pecan{wow_you_did_it!}.txt