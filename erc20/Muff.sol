// contracts/GLDToken.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import {ERC20} from "./oppenzeppelin/ERC20.sol";

contract MUFFToken is ERC20 {
    constructor(uint256 initialSupply) ERC20("MoveUFF", "MUFF") {
        _mint(msg.sender, initialSupply);
    }
}
