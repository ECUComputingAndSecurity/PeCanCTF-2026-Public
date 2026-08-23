*For organisers*
Participants are provided a URL to a web app for moving through directories and displaying text files. The directory selection is vulnerable to one level of path traversal.

## Solution
This challenge is a basic path traversal exploit. Once the URL parameter `path` has been identified, participants can use the value `/..` to view the application base directory and find the `flag.txt` file. They can click this file to open it and view the flag.

```flag
pecan{d4nger0us_un5an7ised_p4th5}
```
