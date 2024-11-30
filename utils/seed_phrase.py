# utils/seed_phrase.py
from bip_utils import Bip39MnemonicGenerator, Bip39SeedGenerator

def generate_seed_phrase(num_words: int = 12):
    mnemonic = Bip39MnemonicGenerator().FromWordsNumber(num_words)
    return mnemonic.ToStr()

def validate_seed_phrase(seed_phrase: str):
    try:
        Bip39SeedGenerator(seed_phrase).Generate()
        return True
    except Exception:
        return False
