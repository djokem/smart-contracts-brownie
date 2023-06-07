from brownie import accounts, LaganNFT, reverts, Wei

MAX_SUPPLY = 10
MAX_MINT_PER_WALLET = 2
PRICE = 2_000_000_000_000_000_000  # 1 ETH

def test_deploy():
    # Arrange
    factory_account = accounts[0]
    owner_account = accounts[1]

    payees = [factory_account, owner_account]
    shares = [5, 95]

    # Act
    lagannft = LaganNFT.deploy(
        "LaganNFT",
        "LAGAN",
        MAX_SUPPLY,
        MAX_MINT_PER_WALLET,
        PRICE,
        owner_account,
        payees,
        shares,
        {'from': factory_account}
    )
    # Assert
    assert lagannft.owner() == owner_account.address

    assert lagannft.shares(factory_account) == 5
    assert lagannft.shares(owner_account) == 95


def test_mint_token_ownership_and_max_supply_reached():
    factory_account = accounts[0]
    owner_account = accounts[1]

    payees = [factory_account, owner_account]
    shares = [5, 95]

    lagannft = LaganNFT.deploy(
        "LaganNFT",
        "LAGAN",
        MAX_SUPPLY,
        MAX_MINT_PER_WALLET,
        PRICE,
        owner_account,
        payees,
        shares,
        {'from': factory_account}
    )

    for i in range(MAX_SUPPLY):
        account = accounts.add()
        accounts[0].transfer(account, "2 ether")
        tx_receipt = lagannft.mint(account, {'from': account, 'value': PRICE})
        new_token_id = tx_receipt.return_value
        assert lagannft.ownerOf(new_token_id) == account

    assert lagannft.getNumberOfMinted() == MAX_SUPPLY;

    with reverts("The collection is minted out!"):
        lagannft.mint(accounts[2], {'from': accounts[2], 'value': PRICE})


def test_max_num_per_wallet_reached():

    factory_account = accounts[0]
    owner_account = accounts[1]

    payees = [factory_account, owner_account]
    shares = [5, 95]

    lagannft = LaganNFT.deploy(
        "LaganNFT",
        "LAGAN",
        MAX_SUPPLY,
        MAX_MINT_PER_WALLET,
        PRICE,
        owner_account,
        payees,
        shares,
        {'from': factory_account}
    )

    for i in range(MAX_MINT_PER_WALLET):
        lagannft.mint(accounts[2], {'from': accounts[2], 'value': PRICE})

    with reverts("Maximum number of minted tokens per wallet reached!"):
        lagannft.mint(accounts[2], {'from': accounts[2], 'value': PRICE})

def test_incorrect_price():

    factory_account = accounts[0]
    owner_account = accounts[1]

    payees = [factory_account, owner_account]
    shares = [5, 95]

    lagannft = LaganNFT.deploy(
        "LaganNFT",
        "LAGAN",
        MAX_SUPPLY,
        MAX_MINT_PER_WALLET,
        PRICE,
        owner_account,
        payees,
        shares,
        {'from': factory_account}
    )

    with reverts("Payment amount is incorrect"):
        lagannft.mint(accounts[2], {'from': accounts[2], 'value': PRICE + 1})


def test_payment_splitter_functionality():
    factory_account = accounts[0]
    owner_account = accounts[1]

    payees = [accounts[9], accounts[8]]
    shares = [50, 50]

    lagannft = LaganNFT.deploy(
        "LaganNFT",
        "LAGAN",
        MAX_SUPPLY,
        MAX_MINT_PER_WALLET,
        PRICE,
        owner_account,
        payees,
        shares,
        {'from': factory_account}
    )

    expected_balance_payee0 = payees[0].balance() + shares[0] * PRICE / 100
    expected_balance_payee1 = payees[1].balance() + shares[1] * PRICE / 100

    lagannft.mint(accounts[3], {'from': accounts[3], 'value': PRICE})
    assert payees[0].balance() == expected_balance_payee0
    assert payees[1].balance() == expected_balance_payee1
