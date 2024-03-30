from web3 import Web3
from datetime import datetime, timedelta

# Connect to the Ethereum node
w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"))

# Contract address
contract_address = "0xaBE235136562a5C2B02557E1CaE7E8c85F2a5da0"

# ABI (Application Binary Interface) of the contract
abi = [
    # Define your contract's ABI here
    # Example:
    # {
    #     "anonymous": false,
    #     "inputs": [
    #         {
    #             "indexed": false,
    #             "internalType": "uint256",
    #             "name": "value",
    #             "type": "uint256"
    #         }
    #     ],
    #     "name": "TotalDistribution",
    #     "type": "event"
    # }
]

# Create a contract instance
contract = w3.eth.contract(address=contract_address, abi=abi)

# Get the block number of 24 hours ago
block_number_24h_ago = (
    w3.eth.getBlock("latest").number - 5760
)  # Assuming 15 seconds per block

# Get all logs for the contract's events in the last 24 hours
logs = w3.eth.getLogs(
    {
        "address": contract_address,
        "fromBlock": block_number_24h_ago,
        "toBlock": "latest",
        "topics": [Web3.sha3(text="TotalDistribution()").hex()],
    }
)

# Parse hexadecimal data to array
values_array = []
for log in logs:
    event = contract.events.TotalDistribution().processLog(log)
    value_hex = event["args"]["value"].hex()
    # Convert hexadecimal string to array of decimal values
    values_array.extend(
        [int(value_hex[i : i + 2], 16) for i in range(0, len(value_hex), 2)]
    )

print("Values array:", values_array)
