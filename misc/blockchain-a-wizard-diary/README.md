## Solution

Going to the webpage when we get the link (exact values will differ) gets:

```text
WizardDiary

Instructions
Any POST requests sent here will be forwarded to the blockchain network.
To reset your keys and deployed contract, clear your browser cookies and reload the page.
If you have solved the challenge, reload the page to reveal the flag.

Connection Details
Contract Address
0x504E672f195Cb5376442C50BB28658d51AdEb047
Public Key
0xcfAe97B73B65d509E89AC29dd2931549f169900a
Private Key
fa5f9393fff6fe20123e8afdab93a709b41372c7997f10f89914dfc145b2724f
Balance
10

Flag
The Flag is
Unknown
```

This tells the user that in order to make requests, they need to send post requests to the same link they got this info at, and then provides a contract address and a funded accoutn to interacte with it through.

Looking at the contract the user can download it is:

```sol
pragma solidity ^0.8.35;

contract WizardDiary {
    event Solved(address who);

    bool public solved = false;

    bytes32 private diaryEntry;

    constructor(bytes32 entry) {
        diaryEntry = entry;
    }

    function read(bytes32 entry) external {
        require(entry == diaryEntry, "That wasn't it sorry.");
        solved = true;
        emit Solved(msg.sender);
    }

    function isSolved() external view returns (bool) {
        return solved;
    }
}
```

This is a very simple contract, where the user needs to call the 'read' function passing in the value to the private variable 'diaryEntry' to solve the challenge.

In order to get the value of 'diaryEntry', it is also very simple, as this is a contract on the blockchain, its 'storage' which is where the ocntract stores all the values of its variables can be directly read.

This storage is split into slots, 'solved' is located in slot '0', and 'diaryEntry' is located in slot '1'.

So reading slot one gets it very easily:

```bash
$ cast storage 0x504E672f195Cb5376442C50BB28658d51AdEb047 1 -r http://localhost:5000
0x000000000000000000000000000000000000000000000000000000deadbeef37
```

So `diaryEntry` is:
```text
0x000000000000000000000000000000000000000000000000000000deadbeef37
```

Calling the `read` function passing in this then solves the challenge:
```bash
$ cast send 0x504E672f195Cb5376442C50BB28658d51AdEb047 "read(bytes32)" 0x000000000000000000000000000000000000000000000000000000deadbeef37 -r http://localhost:5000 --private-key fa5f9393fff6fe20123e8afdab93a709b41372c7997f10f89914dfc145b2724f

blockHash            0x3a5365b4d23b493a009d51d44f4809723c13eb0e7bfc0bfc7cf336621c5705e6
blockNumber          2
contractAddress      
cumulativeGasUsed    47154
effectiveGasPrice    877026543
from                 0xcfAe97B73B65d509E89AC29dd2931549f169900a
gasUsed              47154
logs                 [{"address":"0x504e672f195cb5376442c50bb28658d51adeb047","topics":["0x0bc74ec5d8b1557c26ff0939198ee528d125a4f4d198e1c680170389ec1389a2"],"data":"0x000000000000000000000000cfae97b73b65d509e89ac29dd2931549f169900a","blockHash":"0x3a5365b4d23b493a009d51d44f4809723c13eb0e7bfc0bfc7cf336621c5705e6","blockNumber":"0x2","blockTimestamp":"0x6a47d5f7","transactionHash":"0x0067fd7c12286c4a97299f40c1a20ccca50156c917c4072ed6c0f27e36428d57","transactionIndex":"0x0","logIndex":"0x0","removed":false}]
logsBloom            0x00000000000000000000000000000000000000000000080000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000000000000000000
root                 
status               1 (success)
transactionHash      0x0067fd7c12286c4a97299f40c1a20ccca50156c917c4072ed6c0f27e36428d57
transactionIndex     0
type                 2
blobGasPrice         1
blobGasUsed          
to                   0x504E672f195Cb5376442C50BB28658d51AdEb047
```

Then reloading the index page at `http://localhost:5000` updates the end to say:

```text
The Flag is pecan{pr1v473_isnt_pr1v473?}
```

Getting the flag:
```flag
pecan{pr1v473_isnt_pr1v473?}
```