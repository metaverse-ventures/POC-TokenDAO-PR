import logging
import os
import json
from eth_account import Account
from eth_account.messages import encode_defunct
from web3 import Web3

# TODO: Remove default values for safety
RPC_URLS = { 
        "vana": os.environ.get("VANA_RPC_URL","https://rpc.vana.org"),
        "ethereum": os.environ.get("ETH_RPC_URL", "https://mainnet.infura.io/v3/264791f816e24e5ca62747afee829c8c"),
        "base": os.environ.get("BASE_RPC_URL", "https://base-mainnet.infura.io/v3/264791f816e24e5ca62747afee829c8c"),
        "optimistic-ethereum": os.environ.get("OPTIMISM_RPC_URL", "https://optimism-mainnet.infura.io/v3/264791f816e24e5ca62747afee829c8c"),
        "binance-smart-chain": os.environ.get("BSC_RPC_URL", "https://bsc-mainnet.infura.io/v3/264791f816e24e5ca62747afee829c8c"),
        "polygon-pos": os.environ.get("POLYGON_RPC_URL", "https://polygon-mainnet.infura.io/v3/264791f816e24e5ca62747afee829c8c"),
        "opbnb": os.environ.get("OPBNB_RPC_URL", "https://opbnb-mainnet.infura.io/v3/264791f816e24e5ca62747afee829c8c"),
        "zksync": os.environ.get("ZK_RPC_URL", "https://zksync-mainnet.infura.io/v3/264791f816e24e5ca62747afee829c8c"),
        "mantle": os.environ.get("MANTLE_RPC_URL", "https://mantle-mainnet.infura.io/v3/264791f816e24e5ca62747afee829c8c"),
        "scroll": os.environ.get("SCROLL_RPC_URL", "https://scroll-mainnet.infura.io/v3/264791f816e24e5ca62747afee829c8c"),
        "arbitrum-one": os.environ.get("ARBITRUM_RPC_URL", "https://arbitrum-mainnet.infura.io/v3/264791f816e24e5ca62747afee829c8c"),
        "avalanche": os.environ.get("AVALANCHE_RPC_URL", "https://avalanche-mainnet.infura.io/v3/264791f816e24e5ca62747afee829c8c"),
        "linea": os.environ.get("LINEA_RPC_URL", "https://linea-mainnet.infura.io/v3/264791f816e24e5ca62747afee829c8c"),
        "blast": os.environ.get("BLAST_RPC_URL", "https://blast-mainnet.infura.io/v3/264791f816e24e5ca62747afee829c8c"),
        "solana": os.environ.get("SOLANA_RPC_URL", "https://solana-mainnet.g.alchemy.com/v2/PPZl-DY-c-w65nZwv6rTOikE9Aln0vn-"),
        "xdai": os.environ.get("GNOSIS_RPC_URL", "https://gnosis-mainnet.g.alchemy.com/v2/PPZl-DY-c-w65nZwv6rTOikE9Aln0vn-"),
        "fantom": os.environ.get("FANTOM_RPC_URL", "https://fantom-mainnet.g.alchemy.com/v2/PPZl-DY-c-w65nZwv6rTOikE9Aln0vn-"),
        "zklink-nova": os.environ.get("ZKLINK_RPC_URL"," https://rpc.zklink.io"),
        "tron": os.environ.get("TRON_RPC_URL", "https://api.trongrid.io/jsonrpc"),
        "kucoin-community-chain": os.environ.get("KCC_RPC_URL", "https://rpc-mainnet.kcc.network"),
        "manta-pacific": os.environ.get("MANTA_RPC_URL", "https://manta-pacific.drpc.org"),
        "x-layer": os.environ.get("XLAYER_RPC_URL", "https://gnosis-pokt.nodies.app"),
        "merlin-chain": os.environ.get("MERLIN_RPC_URL", "https://merlin.drpc.org"),
        "bitlayer": os.environ.get("BITLAYER_RPC_URL", "https://rpc-bitlayer.rockx.com"),
        "cronos": os.environ.get("CRONOS_RPC_URL", "https://cronos.drpc.org"),
    }

NON_EVM_CHAINS = {"solana", "tron", "zklink-nova"}

def check_token_ownership(chain: str, token_address: str, wallet_address: str) -> bool:
    """
    Checks if a wallet owns a given ERC-20 token by checking the balance.
    
    :param chain: The blockchain network to check.
    :param token_address: The contract address of the ERC-20 token.
    :param wallet_address: The wallet address to check ownership for.
    :return: True if the wallet owns the token (has a balance > 0), False otherwise. Returns 1 for non-EVM chains.
    """
    if chain in NON_EVM_CHAINS:
        return 1
    
    rpc_url = RPC_URLS.get(chain)
    if not rpc_url:
        raise ValueError(f"RPC URL not found for chain: {chain}")
    
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    if not w3.is_connected():
        raise ConnectionError("Failed to connect to RPC")
    
    wallet_address = Web3.to_checksum_address(wallet_address)
    token_address = Web3.to_checksum_address(token_address)
    
    erc20_abi = [
        {
            "constant": True,
            "inputs": [{"name": "_owner", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"name": "balance", "type": "uint256"}],
            "payable": False,
            "stateMutability": "view",
            "type": "function"
        }
    ]
    
    contract = w3.eth.contract(address=token_address, abi=erc20_abi)
    balance = contract.functions.balanceOf(wallet_address).call()
    
    return balance > 0
