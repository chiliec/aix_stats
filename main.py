import asyncio
from datetime import datetime, timedelta
import json
from web3 import Web3
from telegram import Bot
import psycopg2
from dotenv import dotenv_values


# Load variables from .env file into a dictionary
env_vars = dotenv_values(".env")

# Initialize Web3 with your preferred Ethereum provider
web3 = Web3(Web3.HTTPProvider(env_vars["WEB3_HTTP_PROVIDER"]))

# Initialize your Telegram bot
bot = Bot(token=env_vars["BOT_TOKEN"])

# Connect to your PostgreSQL database
conn = psycopg2.connect(env_vars["POSTGRES_DSN"])
cur = conn.cursor()

# Ethereum contract address and ABI
contract_address = "0xaBE235136562a5C2B02557E1CaE7E8c85F2a5da0"
contract_abi = json.loads(
    """[{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bool","name":"value","type":"bool"}],"name":"AnyoneCanDistributeSet","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token","type":"address"},{"indexed":true,"internalType":"address","name":"receiver","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Distributed","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint8","name":"version","type":"uint8"}],"name":"Initialized","type":"event"},{"anonymous":false,"inputs":[{"components":[{"internalType":"uint256","name":"share","type":"uint256"},{"internalType":"address","name":"receiver","type":"address"},{"internalType":"bool","name":"doCallback","type":"bool"}],"indexed":false,"internalType":"struct AIXTreasury.Receiver[]","name":"aixReceivers","type":"tuple[]"},{"components":[{"internalType":"uint256","name":"share","type":"uint256"},{"internalType":"address","name":"receiver","type":"address"},{"internalType":"bool","name":"doCallback","type":"bool"}],"indexed":false,"internalType":"struct AIXTreasury.Receiver[]","name":"ethReceivers","type":"tuple[]"}],"name":"ReceiversSet","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"previousAdminRole","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"newAdminRole","type":"bytes32"}],"name":"RoleAdminChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleGranted","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleRevoked","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"aixAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"ethAmount","type":"uint256"}],"name":"TokensSwapped","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"inputAixAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"distributedAixAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"swappedEthAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"distributedEthAmount","type":"uint256"}],"name":"TotalDistribution","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"TransferETH","type":"event"},{"inputs":[],"name":"DEFAULT_ADMIN_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"DENOMINATOR","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"DISTRIBUTOR_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"aix","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"aixReceivers","outputs":[{"internalType":"uint256","name":"share","type":"uint256"},{"internalType":"address","name":"receiver","type":"address"},{"internalType":"bool","name":"doCallback","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"anyoneCanDistribute","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"minETHPerAIXPrice","type":"uint256"}],"name":"distribute","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"ethReceivers","outputs":[{"internalType":"uint256","name":"share","type":"uint256"},{"internalType":"address","name":"receiver","type":"address"},{"internalType":"bool","name":"doCallback","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"}],"name":"getRoleAdmin","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"grantRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"hasRole","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract IERC20","name":"_aix","type":"address"},{"internalType":"address","name":"_uniswapRouter","type":"address"},{"internalType":"address","name":"_weth","type":"address"},{"components":[{"internalType":"uint256","name":"share","type":"uint256"},{"internalType":"address","name":"receiver","type":"address"},{"internalType":"bool","name":"doCallback","type":"bool"}],"internalType":"struct AIXTreasury.Receiver[]","name":"_aixReceivers","type":"tuple[]"},{"components":[{"internalType":"uint256","name":"share","type":"uint256"},{"internalType":"address","name":"receiver","type":"address"},{"internalType":"bool","name":"doCallback","type":"bool"}],"internalType":"struct AIXTreasury.Receiver[]","name":"_ethReceivers","type":"tuple[]"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"renounceRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"revokeRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"value","type":"bool"}],"name":"setAnyoneCanDistribute","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"uint256","name":"share","type":"uint256"},{"internalType":"address","name":"receiver","type":"address"},{"internalType":"bool","name":"doCallback","type":"bool"}],"internalType":"struct AIXTreasury.Receiver[]","name":"_aixReceivers","type":"tuple[]"},{"components":[{"internalType":"uint256","name":"share","type":"uint256"},{"internalType":"address","name":"receiver","type":"address"},{"internalType":"bool","name":"doCallback","type":"bool"}],"internalType":"struct AIXTreasury.Receiver[]","name":"_ethReceivers","type":"tuple[]"}],"name":"setReceivers","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalAixShares","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalEthShares","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"uniswapRouter","outputs":[{"internalType":"contract IUniswapV2Router02","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"weth","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"stateMutability":"payable","type":"receive"}]"""
)

# Initialize contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)


# Send message to Telegram
async def send_telegram_message(message):
    await bot.send_message(chat_id=env_vars["CHAT_ID"], text=message)


def format_time_difference(timestamp):
    # Convert timestamp to datetime object
    timestamp = datetime.fromtimestamp(timestamp)

    # Get the current time
    now = datetime.now()

    # Calculate the time difference
    time_diff = now - timestamp

    # Extract hours and minutes
    hours = int(time_diff.total_seconds() / 3600)
    minutes = int((time_diff.total_seconds() % 3600) / 60)

    # Format the output
    if hours > 0:
        return f"{hours}h{minutes}m ago"
    else:
        return f"{minutes}m ago"


def format_token_value(value: int, decimal_places=2, unit="ether"):
    return "{:,.{}f}".format(web3.from_wei(value, unit), decimal_places)


async def generate_report():
    print("Generate report started")

    # Get the block number of 24 hours ago
    block_number_24h_ago = (
        web3.eth.get_block("latest").number - 5760
    )  # Assuming 15 seconds per block

    # Get all logs for the contract's events in the last 24 hours
    logs = web3.eth.get_logs(
        {
            "address": contract_address,
            "fromBlock": block_number_24h_ago,
            "toBlock": "latest",
            "topics": [
                # HEX of TotalDistribution()
                "0xe689c8111f40a171596b9d81ac47c6fe406d2297392957c5126c2f7448c58694",
            ],
        }
    )

    # Summing up all the values of events
    aix_input = 0
    aix_distributed = 0
    eth_swapped = 0
    eth_distributed = 0
    for log in logs:
        print(log, "\n")
        event = contract.events.TotalDistribution().process_log(log)
        args = event["args"]
        aix_input += args["inputAixAmount"]
        aix_distributed += args["distributedAixAmount"]
        eth_swapped += args["swappedEthAmount"]
        eth_distributed += args["distributedEthAmount"]

    first_block_tx, last_block_tx = logs[0]["blockNumber"], logs[-1]["blockNumber"]
    first_tx_timestamp = web3.eth.get_block(first_block_tx).timestamp
    first_tx_time = format_time_difference(first_tx_timestamp)
    last_tx_timestamp = web3.eth.get_block(last_block_tx).timestamp
    last_tx_time = format_time_difference(last_tx_timestamp)
    last_tx_hash = logs[-1]["transactionHash"]
    last_tx = web3.eth.get_transaction(last_tx_hash)
    distributor = last_tx["from"]
    # Raw balance value
    distributor_balance = web3.eth.get_balance(distributor)

    # Generate report based on the contract data
    report = """Daily $AIX Stats:
        - First TX: {}
        - Last TX: {}
        - AIX processed: {}
        - AIX distributed: {}
        - ETH bought: {}
        - ETH distributed: {}
        
        Distributor wallet: {}
        Distributor balance: {} ETH
    """.format(
        first_tx_time,
        last_tx_time,
        format_token_value(aix_input),
        format_token_value(aix_distributed),
        format_token_value(eth_swapped),
        format_token_value(eth_distributed),
        distributor,
        format_token_value(distributor_balance, 1),
    )

    # Send report to Telegram
    await send_telegram_message(report)

    # Save report date to PostgreSQL
    cur.execute(
        """INSERT INTO report_info (report_date,first_tx_time,last_tx_time,aix_input,
            aix_distributed,eth_swapped,eth_distributed,distributor,distributor_balance) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        (
            datetime.now(),
            first_tx_timestamp,
            last_tx_timestamp,
            aix_input,
            aix_distributed,
            eth_swapped,
            eth_distributed,
            distributor,
            distributor_balance,
        ),
    )
    conn.commit()


def fetch_last_report_date() -> datetime:
    # Fetch the date of the last report from PostgreSQL
    cur.execute("SELECT report_date FROM report_info ORDER BY id DESC LIMIT 1")
    try:
        last_report_date = cur.fetchone()[0]
    except:
        # fallback to epoch
        last_report_date = datetime.fromtimestamp(0)
    return last_report_date


async def main():
    # Define the table schema
    create_table_query = """
        CREATE TABLE IF NOT EXISTS report_info (
            id SERIAL PRIMARY KEY,
            report_date TIMESTAMP NOT NULL,
            first_tx_time NUMERIC NOT NULL,
            last_tx_time NUMERIC NOT NULL,
            aix_input NUMERIC NOT NULL,
            aix_distributed NUMERIC NOT NULL,
            eth_swapped NUMERIC NOT NULL,
            eth_distributed NUMERIC NOT NULL,
            distributor VARCHAR(42) NOT NULL,
            distributor_balance NUMERIC NOT NULL
        )
    """
    # Execute the query to create the table
    cur.execute(create_table_query)
    # Commit the transaction
    conn.commit()
    # Report every n seconds
    report_every = timedelta(seconds=int(env_vars["INTERVAL_SECONDS"]))
    # Fetch the date of the last report when the script starts
    last_report_date = fetch_last_report_date()
    next_report_date = last_report_date + report_every
    if datetime.now() < next_report_date:
        wait = (next_report_date - datetime.now()).total_seconds()
        print("Wait {} seconds before next report".format(wait))
        await asyncio.sleep(wait)
    while True:
        await generate_report()
        # Waiting before sending the next message
        await asyncio.sleep(report_every.total_seconds())


asyncio.run(main())
# Close the cursor and connection
cur.close()
conn.close()
