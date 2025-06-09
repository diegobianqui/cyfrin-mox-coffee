from src import coffee
from moccasin.config import get_active_network

def owithdraw():
    active_network = get_active_network()
    ncoffee= active_network.manifest_named("coffee")
    #ncoffee = active_network.get_latest_contract_unchecked("coffee") 
    print(f"Working with contract {ncoffee.address}")
    ncoffee.withdraw()

def moccasin_main():
    return owithdraw()

#0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512