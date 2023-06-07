// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/finance/PaymentSplitter.sol";

contract LaganNFT is ERC721, Ownable, PaymentSplitter {

    uint32 public _maxSupply;
    uint8 public _maxMintPerWallet;
    uint256 public _price;
    uint256 private _number_of_payees;

    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;

    constructor(
        string memory name, string memory symbol, uint32 maxSupply,
        uint8 maxMintPerWallet, uint256 price, address owner,
        address[] memory payees, uint256[] memory shares
    ) ERC721(name, symbol) PaymentSplitter(payees, shares) {
        _maxSupply = maxSupply;
        _maxMintPerWallet = maxMintPerWallet;
        _price = price;
        _number_of_payees = payees.length;
        transferOwnership(owner);
    }

    function mint(address to) public payable returns (uint256) {
        require(_tokenIds.current() < _maxSupply, "The collection is minted out!");
        require(balanceOf(to) < _maxMintPerWallet, "Maximum number of minted tokens per wallet reached!");
        require(msg.value == _price, "Payment amount is incorrect");

        uint256 totalBalance = address(this).balance;
        for (uint256 i = 0; i < _number_of_payees; i++) {
            address payable payee = payable(payee(i));
            uint256 paymentAmount = totalBalance * shares(payee) / 100;
            release(payee);
        }

        _tokenIds.increment();
        uint256 newTokenId = _tokenIds.current();

        _safeMint(to, newTokenId);
        return newTokenId;
    }

    function getNumberOfMinted() public view returns (uint256) {
        return _tokenIds.current();
    }
}
