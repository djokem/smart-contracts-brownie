// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract LaganProductNFT is ERC721, Ownable {

    // Mapping to store token ID to Product struct
    mapping(uint256 => Product) public products;

    // Event to log when a new product is tokenized
    event LaganProductTokenized(uint256 indexed tokenId, );


    constructor(string memory name, string memory symbol) ERC721(name, symbol) {}

    // Function to mint a new NFT for a product
    function mintProduct(
        uint256 _tokenId
    ) public onlyOwner {
        require(!products[_tokenId].isTokenized, "Product already tokenized");

        _mint(owner(), _tokenId);

        products[_tokenId] = Product({
            name: _name,
            description: _description,
            imageURL: _imageURL,
            price: _price,
            isTokenized: true
        });

        emit ProductTokenized(_tokenId, _name, _description, _imageURL, _price);
    }

    // Function to update a tokenized product's metadata
    function updateProductMetadata(
        uint256 _tokenId,
        string memory _name,
        string memory _description,
        string memory _imageURL,
        uint256 _price
    ) public onlyOwner {
        require(products[_tokenId].isTokenized, "Product not tokenized");

        products[_tokenId].name = _name;
        products[_tokenId].description = _description;
        products[_tokenId].imageURL = _imageURL;
        products[_tokenId].price = _price;
    }

    // Function to get a tokenized product's metadata
    function getProductMetadata(uint256 _tokenId)
        public
        view
        returns (
            string memory name,
            string memory description,
            string memory imageURL,
            uint256 price
        )
    {
        require(products[_tokenId].isTokenized, "Product not tokenized");

        name = products[_tokenId].name;
        description = products[_tokenId].description;
        imageURL = products[_tokenId].imageURL;
        price = products[_tokenId].price;
    }
}
