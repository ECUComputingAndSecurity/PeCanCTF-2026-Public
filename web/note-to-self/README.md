## Challenge Description
*For participants*
We've made a handy new app you can keep all your reminders in! It's super secure and uses a unique JWT secret for each log-in session.

*For organisers*
This challenge is a two stage exploit that requires manipulation of a JWT `kid` value to forge a token using a known value, and then a simple value extraction from the associated Redis database to decrypt the provided key.

## Challenge Flag
Suggested flag: `pecan{o0ps!_a11_k3ys}`. Flag must be set using the `FLAG` environment variable when launching the Docker container.

## Files to Distribute
- `src.zip` — identical to `src/` except that the `ENV FLAG=...` line is stripped from the Dockerfile.

# Writeup: Note to Self

## Step 1 — Create an Account and Create a Note

A user must have an account to inject a known value into the Redis database. Once the participant has logged in they can create a note with a known value by which to sign a JWT with.

The note body is stored verbatim at `note:<note_id>:body`, and `/api/notes` returns the note id.

## Step 2 - Forge a JWT

The participant can then use the known value for authenticating with the JWT by setting the `kid` header of the forged JWT to `note:<note_id>:body`, which will select the known value for JWT validation during the authentication check. This allows the participant to forge a JWT for the admin user.

```python
forged = jwt.encode(
    {"sub": username, "role": "admin", "data": "x"},
    note_body,
    algorithm="HS256",
    headers={"kid": f"note:{note_id}:body"},
)
```

Setting that as the `token` cookie grants access to `/admin`.

## Step 3 - Extract the Encryption Key for the JWT

The JWT secret in use doubles as an encryption key for the flag data that is included in the original log-in JWT given to the participant for their created user. They can extract this key directly using the admin debug console, either grabbing the key name from their JWT or searching for it first using the `KEYS *` command.

```json
{"command": "get", "args": ["jwt_secrets:<sha256 from your real token's kid>"]}
```

## Step 4 - Decrypt the Flag Value

This is a simple AES decryption of the `data` value on the original JWT, using the extracted key. The claim is `iv || ciphertext`, AES-256-CBC with PKCS#7 padding:

```python
raw = bytes.fromhex(payload["data"])
iv, ct = raw[:16], raw[16:]
dec = Cipher(algorithms.AES(bytes.fromhex(secret)), modes.CBC(iv)).decryptor()
pt = dec.update(ct) + dec.finalize()
unpadder = PKCS7(128).unpadder()
print((unpadder.update(pt) + unpadder.finalize()).decode())
```

```flag
pecan{o0ps!_a11_k3ys}
```
