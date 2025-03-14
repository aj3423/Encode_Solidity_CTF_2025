// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import {Test, console} from "forge-std/Test.sol";
import "foundry-huff/HuffDeployer.sol";
import "../src/CTF.sol";
import "./interface.sol";

contract MyTest is Test {
    CTF ctf;
    ILv0 lv0;
    ILv1 lv1;
    ILv2 lv2;
    ILv3 lv3;
    ILv4 lv4;
    ILv5 lv5;

    address constant MY_WALLET =
        address(...);

    function setUp() public {
        vm.createSelectFork("https://rpc.ankr.com/eth_sepolia", 7847347);
        // vm.createSelectFork("https://rpc.ankr.com/eth_sepolia");

        ctf = CTF(0x47bF301bB9B5Ec3fFb84448a95b3573b305456Db);
        lv0 = ILv0(HuffDeployer.deploy("Lv0"));
        lv1 = ILv1(HuffDeployer.deploy("Lv1"));
        lv2 = ILv2(HuffDeployer.deploy("Lv2"));
        lv3 = ILv3(HuffDeployer.deploy("Lv3"));
        lv4 = ILv4(HuffDeployer.deploy("Lv4"));
        lv5 = ILv5(HuffDeployer.deploy("Lv5"));
    }

    function test_all_levels() public view {
        console.log("lvl0", ctf.levels(0));
        console.log("lvl1", ctf.levels(1));
        console.log("lvl2", ctf.levels(2));
        console.log("lvl3", ctf.levels(3));
        console.log("lvl4", ctf.levels(4));
        console.log("lvl5", ctf.levels(5));

        console.log("lvl6", ctf.levels(6)); // 0, deleted by `removeLevel()`...
        console.log("lvl7", ctf.levels(7)); // 0, deleted by `removeLevel()`...
    }

    function simulate(uint8 level, address lvl) public {
        address addr = address(lvl);
        vm.prank(MY_WALLET);

        ctf.submitSolution(level, addr);
    }

    function test_lv0() public {
        simulate(0, address(lv0));
        assertEq(lv0.solution(), 42);
    }

    function test_lv1() public {
        simulate(1, address(lv1));

        uint[2][3] memory a = [[uint(1), 2], [uint(3), 4], [uint(5), 6]];
        uint[2][3] memory b = [[uint(11), 12], [uint(13), 14], [uint(15), 16]];

        uint[2][3] memory c = lv1.solution(a, b);
        assertEq(c[0][0], 12);
        assertEq(c[1][0], 16);
        assertEq(c[2][0], 20);
        assertEq(c[0][1], 14);
        assertEq(c[1][1], 18);
        assertEq(c[2][1], 22);
    }

    function try_lv2(uint[10] memory input, uint[10] memory goal) private {
        uint[10] memory result = lv2.solution(input);

        for (uint i = 0; i < 10; i++) {
            assertEq(result[i], goal[i]);
        }
    }

    function test_lv2() public {
        simulate(2, address(lv2));

        try_lv2(
            [uint(99), 4, 8, 1, 33, 22, 2, 4, 5, 9],
            [uint(1), 2, 4, 4, 5, 8, 9, 22, 33, 99]
        );
        try_lv2(
            [uint(5), 10, 3, 4, 6, 1, 7, 8, 9, 2],
            [uint(1), 2, 3, 4, 5, 6, 7, 8, 9, 10]
        );
        try_lv2(
            [uint(7), 4, 8, 1, 47, 66, 2, 2, 2, 9],
            [uint(1), 2, 2, 2, 4, 7, 8, 9, 47, 66]
        );
    }

    function test_lv3() public {
        simulate(3, address(lv3));

        uint16 a = 0x1234;
        bool b = true;
        bytes6 c = bytes6("abcdef");

        bytes memory input = abi.encodePacked(a, b, c);

        (uint16 x, bool y, bytes6 z) = lv3.solution(input);

        assertEq(a, x);
        assertEq(b, y);
        assertEq(c, z);
    }

    function test_lv4() public {
        lv4.solution(10);
        simulate(4, address(lv4));

        assertEq(lv4.solution(1), 0x1);
        assertEq(lv4.solution(10), 0x8);
        assertEq(lv4.solution(21), 0x10);
        assertEq(lv4.solution(31), 0x10);
        assertEq(lv4.solution(2048), 0x800);
        assertEq(lv4.solution(0x8000000000000000), 0x8000000000000000);
        assertEq(lv4.solution(0xffffffff), 0x80000000);
        assertEq(lv4.solution(511), 256);
        assertEq(lv4.solution(512), 512);
        assertEq(lv4.solution(65536), 65536);
        assertEq(lv4.solution(65537), 65536);
        assertEq(lv4.solution(1 << 32), 1 << 32);
        assertEq(lv4.solution((1 << 32) - 1), 1 << 31);
        assertEq(lv4.solution(1 << 128), 1 << 128);
        assertEq(lv4.solution((1 << 128) + 1), 1 << 128);
        assertEq(lv4.solution(1 << 255), 1 << 255);
        assertEq(lv4.solution(type(uint).max), 1 << 255);
    }

    function test_lv5() public {
        simulate(5, address(lv5));

        assertEq(lv5.solution(1, 2), 2);
        assertEq(lv5.solution(10, 20), 15);
        assertEq(lv5.solution(-2, -5), -3);
        assertEq(lv5.solution(-3, 3), 0);
        assertEq(lv5.solution(2, 5), lv5.solution(5, 2));
        int max = type(int).max;
        assertEq(lv5.solution(max, max), max);
        assertEq(lv5.solution(max, max - 1), max);
    }
}
