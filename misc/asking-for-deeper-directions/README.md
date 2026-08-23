# Walkthrough
You are meant to use the command line to find the text within the file that has the flag, rather than manually searching each file! It has been hidden in a reduced version of rockyou.txt (to fit within file size restrictions), right below my name (Benjamin).

The easiest way to find it, in a single command, is to run the following command from the top-level "Files" folder:
grep -r "pecan" .

As we know that the flag starts with "pecan", we can use "grep", the command to search through text within files for "pecan". The flag "-r" indicates a recursive search, meaning it will search all files within a target directory, and our target directory is ".", which indicates the current directory the command is run from (in this case, "Files").

This will therefore reveal that the file is in the following file, revealing the flag:
./Downloads/rockyou.txt:pecan{sneaky\_sneaky\_flag}
