import pytest
from brownie import LaganNFTFactory, LaganNFT, accounts


@pytest.fixture
def factory():
    return LaganNFTFactory.deploy({'from': accounts[0]})


def test_create_lagan_nft(factory):
    name = "My NFT"
    symbol = "MNFT"
    max_supply = 100
    max_mint_per_wallet = 2
    price = 1

    tx = factory.createLaganNFT(name, symbol, max_supply, max_mint_per_wallet, price, {'from': accounts[1]})
    nft_address = tx.return_value

    assert nft_address is not None

    nft = LaganNFT.at(nft_address)

    assert nft.name() == name
    assert nft.symbol() == symbol
    assert nft._maxMintPerWallet() == max_mint_per_wallet
    assert nft._price() == price

    assert nft.owner() == accounts[1]
    assert nft.payee(0) == accounts[1]
    assert nft.payee(1) == factory.address
    assert nft.shares(accounts[1]) == 95
    assert nft.shares(factory.address) == 5

    assert tx.events['LaganNFTCreated']['creator'] == accounts[1]
    assert tx.events['LaganNFTCreated']['nftContract'] == nft_address
