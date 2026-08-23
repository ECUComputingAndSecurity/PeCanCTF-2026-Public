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