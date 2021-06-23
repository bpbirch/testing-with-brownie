import pytest
import brownie
from brownie import accounts

# this fixture, scoped to 'module', ensures that we deploy and return an instance of SharedAccounts contract
# in each test that employs it. 
# to utilize this fixture, we pass it as a parameter to our tests (see 'shared' being passed to test functions below)
# brownie provides access to accounts from ganache when we run tests
# by specifying {'from': accounts[0]}, we tell brownie to deploy our contract from accounts[0]
@pytest.fixture(scope='module')
def shared(SharedAccounts, accounts):
    return SharedAccounts.deploy({'from': accounts[0]})

# fn_isolation fixture tells brownie that the blockchain state should be snapshot and reverted at each test function call
@pytest.fixture(autouse=True)
def revert_chain(fn_isolation):
    pass

# the following fixture will auto distribute 5 eth to everyone's account
@pytest.fixture(autouse=True)
def auto_distribute(shared):
    for i in range(10):
        shared.depositFunds({'from':accounts[i], 'value':5e18})


def test_reverts_because_withdrawing_too_much(shared):
    with brownie.reverts("dev: not enough funds"):
        amount = 10e18
        shared.withdrawFunds(amount, {'from':accounts[0]})

def test_reverts_transfer_not_enough_funds(shared):
    with brownie.reverts("dev: not enough funds in sender account"):
        amount = 10e18
        shared.transferFunds(accounts[1], amount, {'from':accounts[0]})

def test_remove_user_from_non_contractowner(shared):
    with brownie.reverts("dev: Only contractOwner can call this function"):
        shared.removeUser(accounts[3], {'from':accounts[1]})