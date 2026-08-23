There is no password recovery involved.
ZipCrypto is vulnerable to known-plaintext attacks.
Description says flag is added to the end of template, which means the beginnings of the zipped file and the template are the same.

Solution:
`bkcrack -C archive.zip -c README.md -p README_template.md` will give key "e20f06e3 57cae001 1cd01b05"
`bkcrack -C archive.zip -c README.md -k e20f06e3 57cae001 1cd01b05 -D unlocked.zip`
`unlocked.zip` has no password, so just `unzip unlocked.zip` and get the flag.