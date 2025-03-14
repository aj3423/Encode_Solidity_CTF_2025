// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

interface ILv0 {
    function solution() external returns (uint8);
}

interface ILv1 {
    function solution(
        uint256[2][3] calldata x,
        uint256[2][3] calldata y
    ) external pure returns (uint256[2][3] memory);
}

interface ILv2 {
    function solution(
        uint256[10] calldata unsortedArray
    ) external returns (uint256[10] memory sortedArray);
}

interface ILv3 {
    function solution(
        bytes memory packed
    ) external returns (uint16 a, bool b, bytes6 c);
}

interface ILv4 {
    function solution(uint256 number) external pure returns (uint256);
}

interface ILv5 {
    function solution(int256 a, int256 b) external pure returns (int256);
}
