from eth_utils import to_wei
import boa
from tests.conftest import SEND_VALUE

RANDOM_USER= boa.env.generate_address("non-owner")



def test_price_feed_correctness(coffee, eth_usd):
    """
    Test that the price feed returns the correct price.
    """    
    assert coffee.price_feed() == eth_usd.address

def test_starting_coffee(coffee,account):
    assert coffee.MINIMUM_USD() == to_wei(5, "ether")
    assert coffee.OWNER() == account.address

def test_funds_fail(coffee):
    with boa.reverts("You need to spend more ETH!"):
        coffee.fund()

def test_funds_success(coffee, account):
    # Arrange    
    boa.env.set_balance(account.address, SEND_VALUE)
    #Act
    coffee.fund(value=SEND_VALUE)
    # Assert
    funder = coffee.funders(0)
    assert funder == account.address
    assert coffee.address_to_amount_funded(funder) == SEND_VALUE

def test_non_owner_withdraw_fail(coffee_funded, account):
    #Arrange
    boa.env.set_balance(account.address, SEND_VALUE)
    coffee_funded.fund(value=SEND_VALUE)
    #Act & Assert    
    with boa.env.prank(RANDOM_USER):
        with boa.reverts("Not the contract owner"):
            coffee_funded.withdraw()

def test_owner_withdraw_success(coffee_funded, account):
    with boa.env.prank(coffee_funded.OWNER()):
        coffee_funded.withdraw()
    assert boa.env.get_balance(coffee_funded.address) == 0

def test_withdraw_from_multiple_funders(coffee_funded):
    number_of_funders = 10
    for i in range(number_of_funders):
        user = boa.env.generate_address(i)
        boa.env.set_balance(user, SEND_VALUE * 2)
        with boa.env.prank(user):
            coffee_funded.fund(value=SEND_VALUE)
    starting_fund_me_balance = boa.env.get_balance(coffee_funded.address)
    starting_owner_balance = boa.env.get_balance(coffee_funded.OWNER())

    with boa.env.prank(coffee_funded.OWNER()):
        coffee_funded.withdraw()

    assert boa.env.get_balance(coffee_funded.address) == 0
    assert starting_fund_me_balance + starting_owner_balance == boa.env.get_balance(
        coffee_funded.OWNER())
    
def test_get_rate(coffee):
    assert coffee.get_eth_to_usd_rate(SEND_VALUE) > 0