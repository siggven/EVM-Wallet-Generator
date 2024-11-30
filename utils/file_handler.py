# utils/file_handler.py
import csv
import json

def read_seed_file(file_path: str):
    with open(file_path, 'r') as file:
        seed_phrases = [line.strip() for line in file if line.strip()]
    return seed_phrases

def write_output(data: list, file_path: str, format: str = "csv", exclude_private_keys: bool = False):
    if format == "csv":
        with open(file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            headers = ["Seed Phrase", "Address"]
            if not exclude_private_keys:
                headers.append("Private Key")
            writer.writerow(headers)
            for entry in data:
                seed_phrase = entry["seed_phrase"]
                for wallet in entry["wallets"]:
                    row = [seed_phrase, wallet["address"]]
                    if not exclude_private_keys:
                        row.append(wallet["private_key"])
                    writer.writerow(row)
    elif format == "json":
        if exclude_private_keys:
            # Remove private keys from wallets
            for entry in data:
                for wallet in entry["wallets"]:
                    wallet.pop("private_key", None)
        with open(file_path, mode="w") as file:
            json.dump(data, file, indent=4)
    elif format == "txt":
        with open(file_path, mode="w") as file:
            for entry in data:
                seed_phrase = entry["seed_phrase"]
                file.write(f"Seed Phrase: {seed_phrase}\n")
                for wallet in entry["wallets"]:
                    file.write(f"Address: {wallet['address']}\n")
                    if not exclude_private_keys:
                        file.write(f"Private Key: {wallet['private_key']}\n")
                file.write("\n")
