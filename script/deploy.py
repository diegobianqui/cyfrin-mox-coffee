from moccasin.config import get_active_network
from src import coffee
from moccasin.boa_tools import VyperContract
from script.deploy_mocks import deploy_feed

def deploy_coffee(price_feed: VyperContract)-> VyperContract:
    ncoffee: VyperContract = coffee.deploy(price_feed)

    active_network = get_active_network()
    if active_network.has_explorer() and active_network.is_local_or_forked_network() is False:
        result = active_network.moccasin_verify(ncoffee)
        result.wait_for_verification()

    return ncoffee


def moccasin_main():
    active_network= get_active_network()
    price_feed: VyperContract=active_network.manifest_named("price_feed")
    print(f"Using price feed {price_feed.address} on {active_network.name}")
    return deploy_coffee(price_feed)
    '''
    ncoffee = coffee.deploy(price_feed)
    print(f"Deployed NCOFFEE contract at {ncoffee.address} on {active_network.name}")
    ncoffee.get_eth_to_usd_rate(1000)
    #deploy_coffee(price_feed)
    '''

if __name__ == "__main__":
    moccasin_main()