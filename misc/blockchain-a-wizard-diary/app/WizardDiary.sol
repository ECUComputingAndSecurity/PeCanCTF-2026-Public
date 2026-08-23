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