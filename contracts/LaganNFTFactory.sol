// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import "./LaganNFT.sol";

contract LaganNFTFactory is Ownable {

    event LaganNFTCreated(address indexed creator, address indexed nftContract);

    function createLaganNFT(
        string memory name, string memory symbol, uint32 maxSupply,
        uint8 maxMintPerWallet, uint256 price
    ) public returns (address) {
        address[] memory payees = new address[](2);
        uint256[] memory shares = new uint256[](2);

        payees[0] = msg.sender;
        shares[0] = 95;

        payees[1] = address(this);
        shares[1] = 5;

        LaganNFT lagan_nft = new LaganNFT(name, symbol, maxSupply, maxMintPerWallet, price, msg.sender, payees, shares);
        emit LaganNFTCreated(msg.sender, address(lagan_nft));
        return address(lagan_nft);
    }
}
