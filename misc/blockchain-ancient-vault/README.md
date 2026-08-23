## Solution

Going to the webpage when we get the link (exact values will differ) gets:

```text
AncientVault

Instructions
Any POST requests sent here will be forwarded to the blockchain network.
To reset your keys and deployed contract, clear your browser cookies and reload the page.
If you have solved the challenge, reload the page to reveal the flag (without clearing cookies).

Connection Details
Contract Address: 0x504E672f195Cb5376442C50BB28658d51AdEb047
Public Key: 0xaa26c104874A40C1393ad66b94B7030c78B37D93
Private Key: 67f747708e4b77ce6b4e3e627bbb63181fed66adf2831e39882a5bbfe837e4d5
Balance: 10

Flag
The flag is: Unknown
```

This tells the user that in order to make requests, they need to send post requests to the same link they got this info at, and then provides a contract address and a funded accoutn to interacte with it through.

Looking at the contract the user can download it is:

```sol
pragma solidity ^0.8.35;

contract AncientVault {
    event Solved(address who);

    bool public solved = false;

    uint256 private SACRED_NUMBER = 1337;

    function speak(uint256 number) external {
        require(number == SACRED_NUMBER, "The vault remains silent");
        solved = true;
        emit Solved(msg.sender);
    }

    function isSolved() external view returns (bool) {
        return solved;
    }
}
```

This is a very simple contract, where the user can call the 'speak' function, and if they passed in the value '1337', then the 'Solved' event is emmitted, therefore giving the user a very clear objective.

This is very easy to do, using `foundry` to do, it just requires a small `cast send`

the command is:

```bash
$ cast send 0x504E672f195Cb5376442C50BB28658d51AdEb047 "speak(uint256)" 1337 -r http://localhost:5000 --private-key 67f747708e4b77ce6b4e3e627bbb63181fed66adf2831e39882a5bbfe837e4d5

blockHash            0x19f4926938d81b6c410b1e492c1c5e2cacafc30d859bbb62398c54409f92e2d8
blockNumber          2
contractAddress      
cumulativeGasUsed    47162
effectiveGasPrice    877005835
from                 0xaa26c104874A40C1393ad66b94B7030c78B37D93
gasUsed              47162
logs                 [{"address":"0x504e672f195cb5376442c50bb28658d51adeb047","topics":["0x0bc74ec5d8b1557c26ff0939198ee528d125a4f4d198e1c680170389ec1389a2"],"data":"0x000000000000000000000000aa26c104874a40c1393ad66b94b7030c78b37d93","blockHash":"0x19f4926938d81b6c410b1e492c1c5e2cacafc30d859bbb62398c54409f92e2d8","blockNumber":"0x2","blockTimestamp":"0x6a47cf53","transactionHash":"0x6cdb83941029ed44ba4b564f4f59d710c862c4ca13eeca7483885491e966ca26","transactionIndex":"0x0","logIndex":"0x0","removed":false}]
logsBloom            0x00000000000000000000000000000000000000000000080000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000000000000000000
root                 
status               1 (success)
transactionHash      0x6cdb83941029ed44ba4b564f4f59d710c862c4ca13eeca7483885491e966ca26
transactionIndex     0
type                 2
blobGasPrice         1
blobGasUsed          
to                   0x504E672f195Cb5376442C50BB28658d51AdEb047
```

reloading the page now returns at the end:

```text
The flag is pecan{01d_v4u175_4r3_w3ird_bu7_1337}
```

getting the flag:

```flag
pecan{01d_v4u175_4r3_w3ird_bu7_1337}
```