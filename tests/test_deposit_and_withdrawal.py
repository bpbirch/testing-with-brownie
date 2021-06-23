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
# this first test is really just checking to make sure our auto_distribute is working
def test_auto_distribute(shared):
    assert shared.getUserBalance({'from':accounts[1]}) == 5e18

def test_deposit(shared):
    userBalance = shared.getUserBalance({'from':accounts[1]})
    contractBalance = shared.getContractBalance({'from':accounts[1]})
    amount = 2e18
    shared.depositFunds({'from':accounts[1], 'value':amount})
    assert shared.getUserBalance({'from':accounts[1]}) == userBalance + amount, "amount was not added to user balance"
    assert shared.getContractBalance({'from':accounts[1]}) == contractBalance + amount, "amount was not added to contract balance"

def test_withdrawal(shared):
    outerBalance = accounts[1].balance()
    innerBalance = shared.getUserBalance({'from':accounts[1]})
    amount = 3e18
    shared.withdrawFunds(amount, {'from':accounts[1]})
    assert shared.getUserBalance({'from':accounts[1]}) == innerBalance - amount, "amount was not subtracted from user's account balance"
    assert accounts[1].balance() == outerBalance + amount, "amount was not refunded back to user's wallet"

def test_transfer(shared):
    oneBalance = shared.getUserBalance({'from':accounts[1]})
    twoBalance = shared.getUserBalance({'from':accounts[2]})
    contractBalance = shared.getContractBalance({'from':accounts[1]})
    amount = 3e18
    shared.transferFunds(accounts[2], amount, {'from':accounts[1]})
    assert shared.getUserBalance({'from':accounts[1]}) == oneBalance - amount, "amount was not subtracted from user1 balance"
    assert shared.getUserBalance({'from':accounts[2]}) == twoBalance + amount, "amount was not added to user2 balance"
    assert shared.getContractBalance({'from':accounts[1]}) == contractBalance, "contract balance was altered but should not have been"



# function withdrawFunds(address payable to) public payable {
#     require(userBalances[msg.sender].weiBalance >= msg.value);
#     require(msg.sender == to);
#     to.transfer(msg.value);
#     userBalances[msg.sender].weiBalance -= msg.value;
# }