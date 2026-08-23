from flask import Flask, request, Response, render_template, make_response
import subprocess
import requests
from eth_account import Account
from  decimal import Decimal

app = Flask(__name__)
ANVIL_URL = "http://127.0.0.1:8545"

# Things to change between challenges
SCRIPT = "AncientVault.sol:AncientVault"
FLAG = "pecan{01d_v4u175_4r3_w3ird_bu7_1337}"

from web3 import Web3
w3 = Web3(Web3.HTTPProvider(ANVIL_URL))
assert w3.is_connected()

def get_keys():
    account = Account.create()
    w3.provider.make_request(
        "anvil_setBalance", 
        [
            account.address,
            hex(w3.to_wei(10, "ether"))
        ]
    )
    return account.address, account.key.hex()

def get_balance(address):
    return w3.from_wei(w3.eth.get_balance(address), "ether")

def deploy_contract():
    addresses = [0, 0]
    addresses[0], addresses[1] = get_keys()

    output = subprocess.run(f"forge create {SCRIPT} --private-key {addresses[1]} --broadcast", shell=True, capture_output=True, text=True)
    if output.stderr != "":
        return output.stderr
    else:
        out = output.stdout.split()
        i = out.index("to:")
        return out[i + 1]

# technically just returns if the contract has emmitted an event
def get_solved(address):
    logs = w3.eth.get_logs({
        "address": address,
        "fromBlock": 0,
        "toBlock": "latest",
    })

    print(logs)

    if len(logs) >= 1:
        return True
    
    return False
        

@app.route('/', methods=["GET"])
def index():

    # Check if the cookie already exists
    addresses = [request.cookies.get(name) for name in ["pub", "priv", "addr"]]
    # If not, create one
    new_cookie = False
    if None in addresses:
        addresses[0], addresses[1] = get_keys()
        # addresses[1] = get_priv(account_number)
        addresses[2] = deploy_contract()
        new_cookie = True

    balance = get_balance(addresses[0])

    flag = FLAG if get_solved(addresses[2]) else "Unknown"

    # Build the response using the cookie value
    response = make_response(render_template(
        "index.html",
        title=SCRIPT.split(":", 1)[1],
        conaddr=addresses[2],
        pubk=addresses[0],
        privk=addresses[1],
        bal=balance,
        flag=flag
    ))

    # Set the cookie only if it was missing
    if new_cookie:
        response.set_cookie("pub", addresses[0])
        response.set_cookie("priv", addresses[1])
        response.set_cookie("addr", addresses[2])

    return response

@app.route('/', methods=["POST"])
def rpc():
    # Check to make sure anvil control commands aren't being used
    if request.json["method"].startswith("anvil_"):
        return {"error": "Method not allowed"}, 403

    r = requests.post(
        ANVIL_URL,
        data=request.data,
        headers={
            k: v
            for k, v in request.headers.items()
            if k.lower() != "host"
        },
    )

    return Response(
        r.content,
        status=r.status_code,
        content_type=r.headers.get("Content-Type"),
    )

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)