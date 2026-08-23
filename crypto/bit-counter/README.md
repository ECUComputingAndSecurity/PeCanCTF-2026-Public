# Bit Counter
**Author:** Raahguu
**Category:** Crypto

## Challenge Description
People always tell me to encrypt my data, so I did see? Finally putting my Kwikset key to good use!

## Challenge Flag
`pecan{D0n7_p057_y0ur_k3y5_0n71n3}`

## Files to Distribute
- `proof.png`

## Hints
1. What makes each physical key unique?
2. These are some interesting pictures: https://github.com/deviantollam/Key-and-Pin-Decoding/tree/master

# Bit Counter

This challenge provides an image of a key, with the text 'RC4:9b6ee79fd75874f7ec724b6f1bd57c321495bd37fcae2a6facafa4349f846464a1'

The description is: People always tell me to encrypt my data, so I did see? Finally putting my Kwikset key to good use!

## Solution

The description says that some data (likely the flag) was encrypted with a key, and specifies that it is a Kwikset key. With the challenge being called `Bit Counter`, that is likely a hint that you will need to count the `bits` of the key, which is the name for the parts of the key that change height making different keys different and providing the whole security aspect of a key, also called cuts.

If we get the keycode of the key then that value can be used as the RC4 password.

This action of getting the keycode from an image of a key is called 'Key Decoding', and a great resource for it is 'https://github.com/deviantollam/Key-and-Pin-Decoding/tree/master' from Deviant Ollam.

As the challenge specifies that the key is a 'Kwikset', that is likely a hint that the challenge wants the 'Kwikset' keycode following their standard sizes.

Downloading the image from the repo 'https://github.com/deviantollam/Key-and-Pin-Decoding/blob/master/Key%20Decoding/Decoding%20-%20Kwikset.png', and overlaying that with the key image, you can read the codes.

I used GIMP, but any image editing tool that supports layering two images will do.

The overlay is saved as `solution.png` in this folder, and it is clear that the key code is '24242'.

Then using Cyberchef with RC4, inputting the text on the image and the password for it as '24242' 'https://cyberchef.org/#recipe=RC4(%7B'option':'UTF8','string':'24242'%7D,'Hex','Latin1')&input=OWI2ZWU3OWZkNzU4NzRmN2VjNzI0YjZmMWJkNTdjMzIxNDk1YmQzN2ZjYWUyYTZmYWNhZmE0MzQ5Zjg0NjQ2NGEx'

Then we get the flag of 'pecan{D0n7_p057_y0ur_k3y5_0n71n3}'
