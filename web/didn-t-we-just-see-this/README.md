# Didn't We Just See This? - Writeup

## Category

Web

## Difficulty

Easy / Easy-Medium

---

## Challenge Overview

In this challenge we are given access to a developer portal called **DevHub**.

After registering an account, each user receives a private namespace:

```text
/c/<challenge_id>/
```

The portal contains several features:

- Dashboard
- Settings
- Support
- Inbox

The objective is to obtain the Support account API key, which contains the flag.

---

## Initial Reconnaissance

After creating an account and logging in, we can access our project settings page:

```text
/c/<challenge_id>/settings
```

The settings page contains an API key, but it is only a normal developer key.

The challenge description suggests that DevHub Support can investigate pages submitted through support tickets, so this functionality is worth examining.

---

## Investigating the Support System

The Support page allows us to submit a ticket containing a page URL.

After submitting a valid DevHub page, Support sends a reply such as:

```text
Thanks! I was able to open the page you provided and have forwarded it to engineering.
```

This confirms an important observation:

> The support system really opens pages that we provide.

---

## Inspecting HTTP Responses

Inspect static resources such as:

```text
/static/main.css
```

Observe the response headers:

```http
X-Cache-Status: MISS
```

and later:

```http
X-Cache-Status: HIT
```

This reveals that DevHub uses a caching layer.

---

## Investigating URL Routing

Compare:

```text
/c/<challenge_id>/settings
```

and

```text
/c/<challenge_id>/settings/test.css
```

Both return the settings page.

This indicates that the backend treats:

```text
/settings
/settings/test
/settings/test.css
```

as the same route.

---

## Understanding the Vulnerability

Two key observations:

1. URLs ending in `.css` can be cached.
2. The backend still serves the settings page when the URL ends in `.css`.

Example:

```text
/c/<challenge_id>/settings/test.css
```

This is a classic Web Cache Deception setup.

---

## Triggering the Support Bot

Create a fresh path that you have not visited yet:

```text
/c/<challenge_id>/settings/unique.css
```

Submit a support ticket containing that path.

Do not visit this path yourself before Support has processed the ticket.

The support bot will:

1. Log in as the Support account.
2. Visit the supplied URL.
3. Load the Support account settings page.

Because the URL ends in `.css`, the cache stores the response.

---

## Retrieving the Flag

After receiving the support reply, visit:

```text
/c/<challenge_id>/settings/unique.css
```

The cached Support settings page is returned.

Example:

```text
Project Settings

API Key:
PECAN{...}
```

The API key is the flag.

---

## Root Cause

The vulnerability exists because:

1. The cache classifies URLs by extension.
2. URLs ending in `.css` are cached.
3. The backend routes `/settings/<anything>` to the same authenticated page.
4. Support visits attacker-controlled URLs while authenticated.
5. The cached response becomes accessible to the attacker.

---

## Learning Objectives

- Identify caching behaviour using HTTP headers.
- Understand how routing inconsistencies create security issues.
- Learn how privileged users interacting with attacker-controlled URLs can introduce risk.
- Understand the fundamentals of Web Cache Deception.
