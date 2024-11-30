# utils/evm_wallet_derivation.py
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes

def derive_evm_wallet(seed_phrase: str, num_addresses: int):
    seed = Bip39SeedGenerator(seed_phrase).Generate()
    bip44_wallet = Bip44.FromSeed(seed, Bip44Coins.ETHEREUM)
    wallets = []
    for i in range(num_addresses):
        account = (
            bip44_wallet
            .Purpose()
            .Coin()
            .Account(0)
            .Change(Bip44Changes.CHAIN_EXT)
            .AddressIndex(i)
        )
        wallets.append({
            "address": account.PublicKey().ToAddress(),
            "private_key": account.PrivateKey().Raw().ToHex()
        })
    return wallets
