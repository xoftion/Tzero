import json
import os
from web3 import Web3
from django.conf import settings

class BlockchainService:
    """
    A service class to interact with the blockchain and the UltrokPayEscrow smart contract.
    """

    def __init__(self):
        # Initialize Web3 providers for Pi and Sidra chains
        self.pi_w3 = Web3(Web3.HTTPProvider(settings.PI_RPC_URL))
        self.sidra_w3 = Web3(Web3.HTTPProvider(settings.SIDRA_RPC_URL))

        # The ABI would be loaded from a JSON file generated after compiling the contract
        # For now, this is a placeholder path.
        abi_path = os.path.join(settings.BASE_DIR, 'escrow', 'artifacts', 'UltrokPayEscrow.json')

        try:
            with open(abi_path) as f:
                contract_interface = json.load(f)
            self.contract_abi = contract_interface['abi']
        except FileNotFoundError:
            # In a real scenario, this should not happen if deployment scripts are correct.
            # For now, we'll use an empty ABI as a placeholder to avoid crashing.
            self.contract_abi = []
            print("WARNING: Contract ABI file not found. BlockchainService will not be fully functional.")

        self.contract_address = settings.ESCROW_CONTRACT_ADDRESS

        # We need to decide which web3 instance to use based on the transaction.
        # This will be determined by the currency of the deal.
        # For now, let's assume a function will choose the correct w3 instance.

    def get_contract(self, currency):
        """
        Returns a web3 contract instance for the specified currency.
        """
        if currency.upper() == 'PI':
            w3 = self.pi_w3
        elif currency.upper() == 'SIDRA':
            w3 = self.sidra_w3
        else:
            raise ValueError("Unsupported currency")

        if not self.contract_abi:
            return None

        return w3.eth.contract(address=self.contract_address, abi=self.contract_abi)

    def create_deal(self, deal_id, buyer_address, seller_address, token_address, amount, currency):
        """
        Calls the createDeal function on the smart contract.

        NOTE: This is a placeholder implementation. The actual implementation would involve
        signing and sending a transaction from a backend wallet.
        """
        contract = self.get_contract(currency)
        if not contract:
            print("ERROR: Contract not initialized. Cannot create deal.")
            return None

        # In a real application, the platform would have its own wallet to pay for gas
        # and would call the contract functions.
        # tx_hash = contract.functions.createDeal(
        #     deal_id,
        #     buyer_address,
        #     seller_address,
        #     token_address,
        #     amount
        # ).transact({'from': settings.PLATFORM_WALLET_ADDRESS})

        print(f"--- MOCK BLOCKCHAIN INTERACTION ---")
        print(f"Creating deal {deal_id} on {currency} chain.")
        print(f"Buyer: {buyer_address}, Seller: {seller_address}, Amount: {amount}")
        print(f"--- END MOCK BLOCKCHAIN INTERACTION ---")

        # For now, we'll just return a mock transaction hash
        return f"0x_mock_tx_hash_{deal_id.hex()}"

    def get_deal_status(self, deal_id, currency):
        """
        Calls the 'deals' mapping on the smart contract to get the state of a deal.
        """
        contract = self.get_contract(currency)
        if not contract:
            print("ERROR: Contract not initialized. Cannot get deal status.")
            return None

        try:
            deal = contract.functions.deals(deal_id).call()
            # The state is an enum (uint8). We would map this back to the string representation.
            # e.g., 0: Created, 1: Funded, etc.
            deal_state_enum = deal[4]
            return deal_state_enum
        except Exception as e:
            print(f"Error fetching deal status: {e}")
            return None
