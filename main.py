# main.py
import argparse
import os
from utils.seed_phrase import generate_seed_phrase, validate_seed_phrase
from utils.evm_wallet_derivation import derive_evm_wallet
from utils.file_handler import write_output, read_seed_file
from colorama import Fore, Style, init

def main():
    init(autoreset=True)  # Initialize colorama for colored output

    parser = argparse.ArgumentParser(description='EVM Wallet Manager')
    parser.add_argument('--generate', action='store_true', help='Generate a new seed phrase')
    parser.add_argument('--num-words', type=int, choices=[12, 24], default=12, help='Number of words in seed phrase (12 or 24)')
    parser.add_argument('--file', type=str, help='File path to read seed phrases from')
    parser.add_argument('--num-addresses', type=int, default=1, help='Number of addresses to derive per seed phrase')
    parser.add_argument('--output-format', type=str, choices=['csv', 'json', 'txt'], default='csv', help='Output file format')
    parser.add_argument('--output-file', type=str, help='Output file path')
    parser.add_argument('--exclude-private-keys', action='store_true', help='Exclude private keys from output')
    parser.add_argument('--interactive', action='store_true', help='Run in interactive mode')
    args = parser.parse_args()

    seed_phrases = []

    # Check if interactive mode is enabled or no sufficient arguments are provided
    if args.interactive or (not args.generate and not args.file):
        print(Fore.CYAN + "Interactive Mode:" + Style.RESET_ALL)

        # Seed Phrase Generation or Input
        while True:
            generate_new_seed = input("Do you want to generate a new seed phrase? (y/n): ").strip().lower()
            if generate_new_seed == 'y':
                # Choose number of words for the seed phrase
                while True:
                    num_words_input = input("Enter number of words for seed phrase (12 or 24): ").strip()
                    if num_words_input in ['12', '24']:
                        num_words = int(num_words_input)
                        break
                    else:
                        print(Fore.RED + "Invalid input. Please enter 12 or 24." + Style.RESET_ALL)
                seed_phrase = generate_seed_phrase(num_words=num_words)
                print(f"Generated Seed Phrase: {Fore.GREEN}{seed_phrase}{Style.RESET_ALL}")
                seed_phrases.append(seed_phrase)
            else:
                # Input seed phrase manually
                seed_phrase_input = input("Enter your seed phrase: ").strip()
                if validate_seed_phrase(seed_phrase_input):
                    seed_phrases.append(seed_phrase_input)
                else:
                    print(Fore.RED + "Invalid seed phrase." + Style.RESET_ALL)
            # Ask if the user wants to add another seed phrase
            add_another = input("Do you want to add another seed phrase? (y/n): ").strip().lower()
            if add_another != 'y':
                break

        # Number of Addresses
        while True:
            num_addresses_input = input("Enter the number of addresses to generate: ").strip()
            if num_addresses_input.isdigit() and int(num_addresses_input) > 0:
                args.num_addresses = int(num_addresses_input)
                break
            else:
                print(Fore.RED + "Invalid input. Please enter a positive integer." + Style.RESET_ALL)

        # Output Format
        output_format_input = input("Save output as CSV, JSON, or TXT? (default: CSV): ").strip().lower()
        if output_format_input in ['csv', 'json', 'txt', '']:
            args.output_format = output_format_input if output_format_input else 'csv'
        else:
            print(Fore.RED + "Invalid input. Defaulting to CSV." + Style.RESET_ALL)
            args.output_format = 'csv'

        # Exclude Private Keys
        exclude_private_keys_input = input("Do you want to exclude private keys from the output? (y/n): ").strip().lower()
        args.exclude_private_keys = (exclude_private_keys_input == 'y')

        # Output File Path
        default_output_file = f"output.{args.output_format}"
        output_file_input = input(f"Enter output file path (default: {default_output_file}): ").strip()
        args.output_file = output_file_input if output_file_input else default_output_file

    else:
        # Non-interactive mode
        if args.generate:
            seed_phrase = generate_seed_phrase(num_words=args.num_words)
            print(f"Generated Seed Phrase: {Fore.GREEN}{seed_phrase}{Style.RESET_ALL}")
            seed_phrases.append(seed_phrase)
        elif args.file:
            if os.path.isfile(args.file):
                seed_phrases = read_seed_file(args.file)
            else:
                print(Fore.RED + f"File not found: {args.file}" + Style.RESET_ALL)
                return
        else:
            print(Fore.RED + "No seed phrase provided. Use --generate, --file, or --interactive." + Style.RESET_ALL)
            parser.print_help()
            return

        # Set default output file if not provided
        if not args.output_file:
            args.output_file = f"output.{args.output_format}"

    # Security Warning
    print(Fore.YELLOW + "Warning: Private keys are sensitive information. Keep them secure." + Style.RESET_ALL)
    if args.exclude_private_keys:
        print(Fore.YELLOW + "Private keys will be excluded from the output." + Style.RESET_ALL)

    data = []
    for seed_phrase in seed_phrases:
        if not validate_seed_phrase(seed_phrase):
            print(Fore.RED + f"Invalid seed phrase: {seed_phrase}" + Style.RESET_ALL)
            continue
        wallets = derive_evm_wallet(seed_phrase, args.num_addresses)
        data.append({
            "seed_phrase": seed_phrase if not args.exclude_private_keys else "Excluded",
            "wallets": wallets
        })

    # Write Output
    write_output(data, args.output_file, args.output_format, args.exclude_private_keys)
    print(Fore.GREEN + f"Output written to {args.output_file}" + Style.RESET_ALL)

if __name__ == '__main__':
    main()
