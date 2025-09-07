// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract UltrokPayEscrow is Ownable, ReentrancyGuard {

    enum DealState { Created, Funded, Released, Refunded, InDispute }

    struct Deal {
        address payable seller;
        address payable buyer;
        address token;
        uint256 amount;
        DealState state;
    }

    mapping(bytes32 => Deal) public deals;
    mapping(address => bool) public whitelistedTokens;

    event DealCreated(bytes32 indexed dealId, address indexed buyer, address indexed seller, address token, uint256 amount);
    event DealFunded(bytes32 indexed dealId);
    event DealFundsReleased(bytes32 indexed dealId);
    event DealRefunded(bytes32 indexed dealId);
    event DealInDispute(bytes32 indexed dealId);
    event DisputeResolved(bytes32 indexed dealId, address indexed resolver, address winner);

    modifier onlyBuyer(bytes32 dealId) {
        require(msg.sender == deals[dealId].buyer, "Only the buyer can call this function");
        _;
    }

    modifier onlySeller(bytes32 dealId) {
        require(msg.sender == deals[dealId].seller, "Only the seller can call this function");
        _;
    }

    modifier inState(bytes32 dealId, DealState state) {
        require(deals[dealId].state == state, "Deal is not in the required state");
        _;
    }

    constructor() Ownable(msg.sender) {}

    function addWhitelistedToken(address token) public onlyOwner {
        whitelistedTokens[token] = true;
    }

    function removeWhitelistedToken(address token) public onlyOwner {
        whitelistedTokens[token] = false;
    }

    function createDeal(bytes32 dealId, address payable buyer, address payable seller, address token, uint256 amount) public {
        require(deals[dealId].amount == 0, "Deal already exists");
        require(whitelistedTokens[token], "Token is not whitelisted");
        require(amount > 0, "Amount must be greater than zero");

        deals[dealId] = Deal({
            buyer: buyer,
            seller: seller,
            token: token,
            amount: amount,
            state: DealState.Created
        });

        emit DealCreated(dealId, buyer, seller, token, amount);
    }

    function fundDeal(bytes32 dealId) public onlyBuyer(dealId) inState(dealId, DealState.Created) nonReentrant {
        Deal storage deal = deals[dealId];
        IERC20 tokenContract = IERC20(deal.token);

        uint256 allowance = tokenContract.allowance(msg.sender, address(this));
        require(allowance >= deal.amount, "Check token allowance");

        bool success = tokenContract.transferFrom(msg.sender, address(this), deal.amount);
        require(success, "Token transfer failed");

        deal.state = DealState.Funded;
        emit DealFunded(dealId);
    }

    function releaseFunds(bytes32 dealId) public onlyBuyer(dealId) inState(dealId, DealState.Funded) nonReentrant {
        Deal storage deal = deals[dealId];
        deal.state = DealState.Released;

        IERC20(deal.token).transfer(deal.seller, deal.amount);

        emit DealFundsReleased(dealId);
    }

    function raiseDispute(bytes32 dealId) public inState(dealId, DealState.Funded) {
        require(msg.sender == deals[dealId].buyer || msg.sender == deals[dealId].seller, "Only buyer or seller can raise a dispute");
        deals[dealId].state = DealState.InDispute;
        emit DealInDispute(dealId);
    }

    function resolveDispute(bytes32 dealId, bool releaseToSeller) public onlyOwner inState(dealId, DealState.InDispute) nonReentrant {
        Deal storage deal = deals[dealId];
        address winner;

        if (releaseToSeller) {
            deal.state = DealState.Released;
            winner = deal.seller;
            IERC20(deal.token).transfer(deal.seller, deal.amount);
            emit DealFundsReleased(dealId);
        } else {
            deal.state = DealState.Refunded;
            winner = deal.buyer;
            IERC20(deal.token).transfer(deal.buyer, deal.amount);
            emit DealRefunded(dealId);
        }

        emit DisputeResolved(dealId, msg.sender, winner);
    }
}
