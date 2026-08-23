# RSA and the Probably Private Primes
**Author:** Pritchard, Chelsea (cmpritch@our.ecu.edu.au)
**Category:** Crypto

## Challenge Description
*For participants*
We've intercepted a secure channel between two hackers! They're using RSA to secure their communications but we've managed to compromise their key generation. Can you crack the code and read the secret messages?

*For organisers*
Participants will attempt to crack two private RSA keys to read the messages in the provided transcript. The keys have a vulnerability in that their modulus shares a prime. For participants with experience in cryptography and RSA this should be a fairly straightforward challenge, and those that don't have the opportunity to learn about asymmetric cryptography and RSA key generation. `generate_transcript.py` can be used to create a new transcript with updated messages.

## Challenge Flag
`pecan{r3us1ng_pr1m3s_i5_b4d}`

## Files to Distribute
- `intercepted_messages.txt`
