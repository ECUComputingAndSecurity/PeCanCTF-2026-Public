# Aliens
**Author:** Raahguu
**Category:** Misc

## Challenge Description
We found this old conspiracy archive online. Had some weird stuff. There might be some useful info somewhere on there though.

## Challenge Flag
`pecan{alien_conspiracy_stuff_goes_weirdly_deep}`

## Deployment Instructions
- `src/`

## Hints
1. Maybe a program can be made to scrape the entire archive
2. There are only about 50 pages, you could just look by hand

## Solution

The challenger is supposed to `nc` into the port to find out what protocol the system is using, finding:

```bash
$ nc localhost 119
200 NNTP Service Ready (no posting)
```

This clearly states that the protocol used is NNTP, looking up about NNTP, the challenger can learn how to use NNTP to read any article they want:

```bash
$ nc localhost 119
200 NNTP Service Ready (no posting)
list
215 list follows
aliens.general 19 1 y
aliens.proof 38 20 y
aliens.random 51 39 y
.
groups aliens.general
500 Unknown command
group aliens.general
211 19 1 19 aliens.general
stat
223 1 <1@aliensare.real>
article
220 1 <1@aliensare.real> article follows
From: Paris@aliensare.real
Newsgroups: aliens.general
Subject: Welcome
Message-ID: <1@aliensare.real>
Date: Tue, 2 Jun 2015 12:00:03 +0000

Welcome to the group. 
Here is filled with fellow like minded people who know the truth.
That there are aliens who walk among us, hidden but there the very same.

If you want to reject this fact and live on pretending they aren't real, then leave.
But, know that some day you will come crawling back, one day, when you discover the truth...

 - Paris
.
next
223 2 <2@aliensare.real>
article
220 2 <2@aliensare.real> article follows
From: Paris@aliensare.real
Newsgroups: aliens.general
Subject: Message Board 101
Message-ID: <2@aliensare.real>
Date: Tue, 2 Jun 2015 12:03:57 +0000

In this message board:
    the 'general' group is used for us likeminded people to speek freely about the truth the government is hiding from us
    the 'random' group is for any off topic conversation
    the 'proof' group is for people to talk about  proof they have found could be shared with others to free this secret from being relegated to the shadows

 - Paris
.
quit
205 Goodbye
```

The challenger is then supposed to either look through all of the articles manually until they get the flag (not recommended unless they can't program), or to make a program which keeps querying the system to log every article.

Some code to do that is below:
```python
import subprocess

# list
# 215 list follows
# aliens.general 19 1 y
# aliens.proof 38 20 y
# aliens.random 51 39 y
GROUPS = {
    "aliens.general": [1, 19],
    "aliens.proof": [20, 38],
    "aliens.random": [39, 51]
}

for group in GROUPS:
    for i in range(GROUPS[group][0], GROUPS[group][1]):
        subprocess.run(f"echo 'group {group}\r\narticle {i}\r\nquit' | nc localhost 119 >> log.txt", shell=True)
```

The code can then be run getting a 600 line `log.txt` file, which can be `Ctrl + F`'d to find the flag in article number 31
```txt
200 NNTP Service Ready (no posting)
211 19 20 38 aliens.proof
220 34 <31@aliensare.real> article follows
From: Wayne@truthseekers.org
Newsgroups: aliens.proof
Subject: Re: Re: How Proving works
Message-ID: <31@aliensare.real>
Date: Fri, 5 Jun 2015 14:14:14 +0000

So the only way for us to trick the Greys, is for us to trick ourselves too, to have the proof and to post it without knowing we have the proof.

What if we hypnotise ourselves into believing we don't have any proof and become sleeper agents that position ourselves in ways to get more proof without knowing why or that we are doing it.
That way, even if they mind wipe us it doesn't matter as it is not something we remember but something we do instinctively.
The only thing they would need to do is broadcast some specific phrase like "pecan{alien_conspiracy_stuff_goes_weirdly_deep}" to activate everyone.
.
205 Goodbye
```

That gets the flag:
```flag
pecan{alien_conspiracy_stuff_goes_weirdly_deep}
```