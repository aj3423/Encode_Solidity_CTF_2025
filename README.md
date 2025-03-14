# The solutions for Encode advanced solidity bootcamp CTF 2025 (https://www.solidityctf.xyz/)


## Level 0 - Return 42 (tutorial)
This level is really simple. Use the interface below to write a smart contract. Your contract should contain a function called solution that returns a uint8. In this case the function body logic is very simply as the answer is always 42.
```solidity
interface Isolution {
    function solution() external pure returns (uint8);
}
```


## Level 1 - Matrix Addition
Write a function that adds two matrices returns the result. To keep things simple the array sizes will be fixed sizes of 2x3 (uint256[2][3]). Take a look at Wikipedia if you need help understanding matrix addition. Your solution should implement the following interface:
```solidity
interface Isolution1 {
    function solution(
        uint256[2][3] calldata x, 
        uint256[2][3] calldata y
    ) external pure returns (
        uint256[2][3] memory
    );
}
```


## Level 2 - Sorting an Array
Write a function that sorts an array in ascending order and returns the result. The array will be a fixed of 10 but the contents random. Your solution should implement the following interface:
```solidity
interface Isolution2 {
  function solution(uint256[10] calldata unsortedArray) external returns (uint256[10] memory sortedArray);
}
```


## Level 3 - abi.encodePacked
Using the Isolution3 interface write a function that unpacks our data that was packed using abi.encodePacked(a, b, c). Where a is type uint16, b is type bool and c is type bytes6.
```solidity
interface Isolution3 {
    function solution(bytes memory packed) external returns (uint16 a, bool b, bytes6 c);
}
```


## Level 4 - Powers of 2
Using the Isolution4 interface write a function that takes a uint256 value and returns the greatest power of 2, (2 ^ n) that is less than or equal to the input value. The input value is a number between 2^0 and 2^256 -1

// stdin: 1                     stdout: 1 or 2**0
// stdin: 10                    stdout: 8 or 2**3
// stdin: 21                    stdout: 16 or 2**4
// stdin: 2048                  stdout: 2048 or 2**11
// stdin: 9223372036854775808   stdout: 9223372036854775808 or 2**63
// stdin: 0xffffffff            stdout: 2147483648 or 0x80000000 or 2**31
```solidity
interface Isolution {
    function solution(uint256 number) external pure returns (uint256);
}
```


## Level 5 - Overflow-free Average, Rounded up
Using the Isolution5 interface calculate the average of two values int256 a and int256 b.

You will need to write an overflow-free method that will round up the average of (a + b) / 2. Keep in mind that we are rounding up (ceil) and NOT rounding down (floor). Floor = rounding towards zero while Ceil = rounding away from zero see examples on wikipedia
```solidity
interface Isolution5 {
    function solution(int256 a, int256 b) external pure returns (int256);
}
```
