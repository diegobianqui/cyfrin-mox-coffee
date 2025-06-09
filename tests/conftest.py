import pytest
from script.deploy import deploy_coffee
from script.deploy_mocks import deploy_feed
from moccasin.config import get_active_network
from eth_utils import to_wei
import boa


SEND_VALUE = to_wei(1, "ether")

@pytest.fixture(scope="session")
def account():
    return get_active_network().get_default_account()


@pytest.fixture(scope="session")
def eth_usd():
    return deploy_feed()

@pytest.fixture(scope="function")
def coffee(eth_usd):
    return deploy_coffee(eth_usd)

@pytest.fixture(scope="function")
def coffee_funded(coffee):
    boa.env.set_balance(coffee.OWNER(), SEND_VALUE * 2)
    with boa.env.prank(coffee.OWNER()):
        coffee.fund(value=SEND_VALUE)
    return coffee