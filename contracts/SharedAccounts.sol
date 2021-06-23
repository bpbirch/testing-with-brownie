pragma solidity ^0.8.0;

contract SharedAccounts {
    address contractOwner;

    constructor() {
        contractOwner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == contractOwner); // dev: Only contractOwner can call this function
        _;
    }

    struct User {
        string firstName;
        string lastName;
        uint weiBalance;
    }

    mapping (address => SharedAccounts.User) userBalances;

    function depositFunds() public payable {
        userBalances[msg.sender].weiBalance += msg.value;
    }
    
    function getContractBalance() public view returns(uint) {
        return address(this).balance;
    }
    
    function transferFunds(address payable to, uint amount) public payable {
        require(userBalances[msg.sender].weiBalance >= amount); // dev: not enough funds in sender account
        userBalances[to].weiBalance += amount;
        userBalances[msg.sender].weiBalance -= amount;
    }

    function withdrawFunds(uint amount) public payable {
        require(userBalances[msg.sender].weiBalance >= amount); // dev: not enough funds
        payable(msg.sender).transfer(amount);
        userBalances[msg.sender].weiBalance -= amount;
    }

    function getUserBalance() public view returns(uint) {
        return userBalances[msg.sender].weiBalance;
    }

    function changeFirstName(string memory first_name) public {
        userBalances[msg.sender].firstName = first_name;
    }

    function changeLastName(string memory last_name) public {
        userBalances[msg.sender].lastName = last_name;
    }

    function getUserFirstName(address userAddress) public view returns(string memory) {
        return userBalances[userAddress].firstName;
    }

    function getUserLastName(address userAddress) public view returns(string memory) {
        return userBalances[userAddress].lastName;
    }

    function removeUser(address payable userAddress) public onlyOwner {
        SharedAccounts.User memory blankUser;
        userAddress.transfer(userBalances[userAddress].weiBalance);
        userBalances[userAddress] = blankUser;
    }

}