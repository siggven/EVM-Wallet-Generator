# gui.py
import tkinter as tk
from tkinter import messagebox, ttk
from utils.seed_phrase import generate_seed_phrase, validate_seed_phrase
from utils.evm_wallet_derivation import derive_evm_wallet

class EvmWalletManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("EVM Wallet Manager")
        self.seed_phrases = []
        self.wallets_data = []
        self.create_widgets()

    def create_widgets(self):
        # Security Warning
        security_warning = tk.Label(
            self.root,
            text="Warning: Keep your seed phrases and private keys secure!",
            fg="red"
        )
        security_warning.pack(pady=5)

        # Seed Phrase Options Frame
        seed_frame = tk.LabelFrame(self.root, text="Seed Phrase Options")
        seed_frame.pack(padx=10, pady=10, fill="x")

        # Seed Phrase Length
        seed_length_label = tk.Label(seed_frame, text="Seed Phrase Length:")
        seed_length_label.grid(row=0, column=0, sticky="w")
        self.seed_length_var = tk.IntVar(value=12)  # Default to 12 words
        seed_length_options = [12, 24]
        self.seed_length_combo = ttk.Combobox(
            seed_frame,
            textvariable=self.seed_length_var,
            values=seed_length_options,
            state='readonly',
            width=5
        )
        self.seed_length_combo.grid(row=0, column=1, sticky="w")

        # Number of Seed Phrases to Generate
        num_seed_phrases_label = tk.Label(seed_frame, text="Number of Seed Phrases:")
        num_seed_phrases_label.grid(row=1, column=0, sticky="w")
        self.num_seed_phrases_entry = tk.Entry(seed_frame, width=10)
        self.num_seed_phrases_entry.insert(0, "1")  # Default to 1
        self.num_seed_phrases_entry.grid(row=1, column=1, sticky="w")

        # Number of Addresses per Seed Phrase
        num_addresses_label = tk.Label(seed_frame, text="Addresses per Seed Phrase:")
        num_addresses_label.grid(row=2, column=0, sticky="w")
        self.num_addresses_entry = tk.Entry(seed_frame, width=10)
        self.num_addresses_entry.insert(0, "1")  # Default to 1
        self.num_addresses_entry.grid(row=2, column=1, sticky="w")

        # Include Private Keys
        self.include_private_keys_var = tk.BooleanVar(value=True)  # Default to include
        include_private_keys_checkbox = tk.Checkbutton(
            seed_frame,
            text="Include Private Keys",
            variable=self.include_private_keys_var
        )
        include_private_keys_checkbox.grid(row=3, column=0, columnspan=2, sticky="w")

        # Output Format
        output_format_label = tk.Label(seed_frame, text="Output Format:")
        output_format_label.grid(row=4, column=0, sticky="w")
        self.output_format_var = tk.StringVar(value="csv")  # Default to CSV
        output_format_options = ['csv', 'json']
        self.output_format_combo = ttk.Combobox(
            seed_frame,
            textvariable=self.output_format_var,
            values=output_format_options,
            state='readonly',
            width=10
        )
        self.output_format_combo.grid(row=4, column=1, sticky="w")

        # Output File Name
        output_file_label = tk.Label(seed_frame, text="Output File Name:")
        output_file_label.grid(row=5, column=0, sticky="w")
        self.output_file_entry = tk.Entry(seed_frame, width=20)
        self.output_file_entry.insert(0, "wallets")  # Default file name
        self.output_file_entry.grid(row=5, column=1, sticky="w")

        # Generate Wallets Button
        self.generate_wallets_btn = tk.Button(
            self.root,
            text="Generate Wallets",
            command=self.generate_wallets
        )
        self.generate_wallets_btn.pack(pady=10)

        # Tooltip Label (optional, can be removed if not used)
        # self.tooltip_label = tk.Label(self.root, text="", fg="blue")
        # self.tooltip_label.pack(pady=5)

    def generate_wallets(self):
        # Get user inputs with validation
        try:
            num_seed_phrases = int(self.num_seed_phrases_entry.get())
            if num_seed_phrases <= 0:
                raise ValueError("Number of seed phrases must be a positive integer.")
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            return

        try:
            num_addresses = int(self.num_addresses_entry.get())
            if num_addresses <= 0:
                raise ValueError("Number of addresses must be a positive integer.")
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            return

        seed_length = self.seed_length_var.get()
        if seed_length not in [12, 24]:
            messagebox.showerror(
                "Input Error",
                "Seed phrase length must be one of the following: 12, 15, 18, 21, or 24."
            )
            return

        include_private_keys = self.include_private_keys_var.get()
        output_format = self.output_format_var.get()
        output_file_name = self.output_file_entry.get().strip()

        if not output_file_name:
            messagebox.showerror("Input Error", "Please enter a valid output file name.")
            return

        # Generate seed phrases
        seed_phrases = []
        for _ in range(num_seed_phrases):
            seed_phrase = generate_seed_phrase(num_words=seed_length)
            seed_phrases.append(seed_phrase)

        # Generate wallets
        self.wallets_data = []

        for seed_phrase in seed_phrases:
            try:
                wallets = derive_evm_wallet(seed_phrase, num_addresses)
            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"Failed to derive wallets for seed phrase:\n{seed_phrase}\n\nError: {str(e)}"
                )
                continue
            self.wallets_data.append({
                "seed_phrase": seed_phrase if include_private_keys else "Excluded",
                "wallets": wallets
            })

        # Save the output automatically
        self.save_output(output_file_name, output_format, include_private_keys)

        messagebox.showinfo(
            "Success",
            f"Generated {num_addresses} addresses per seed phrase for {len(seed_phrases)} seed phrases.\nOutput saved to {output_file_name}.{output_format}"
        )

    def save_output(self, filename, output_format, include_private_keys):
        filepath = f"{filename}.{output_format}"
        if output_format == 'csv':
            self.save_as_csv(self.wallets_data, filepath, include_private_keys)
        elif output_format == 'json':
            self.save_as_json(self.wallets_data, filepath, include_private_keys)
        else:
            messagebox.showerror("Error", "Unsupported file format.")

    def save_as_csv(self, data, filepath, include_private_keys):
        import csv
        headers = ["Seed Phrase", "Address"]
        if include_private_keys:
            headers.append("Private Key")
        with open(filepath, mode="w", newline='', encoding='utf-8') as file:
            writer = csv.writer(file, quoting=csv.QUOTE_ALL)
            writer.writerow(headers)
            for entry in data:
                seed_phrase = entry.get("seed_phrase", "")
                wallets = entry.get("wallets", [])
                for wallet in wallets:
                    address = wallet.get("address", "")
                    row = [seed_phrase, address]
                    if include_private_keys:
                        private_key = wallet.get("private_key", "")
                        row.append(private_key)
                    writer.writerow(row)

    def save_as_json(self, data, filepath, include_private_keys):
        import json
        data_to_save = []
        for entry in data:
            seed_phrase_entry = {
                "seed_phrase": entry["seed_phrase"],
                "wallets": []
            }
            for wallet in entry["wallets"]:
                wallet_entry = {"address": wallet["address"]}
                if include_private_keys:
                    wallet_entry["private_key"] = wallet["private_key"]
                seed_phrase_entry["wallets"].append(wallet_entry)
            data_to_save.append(seed_phrase_entry)
        with open(filepath, mode="w", encoding='utf-8') as file:
            json.dump(data_to_save, file, indent=4)

if __name__ == '__main__':
    root = tk.Tk()
    app = EvmWalletManagerGUI(root)
    root.mainloop()
