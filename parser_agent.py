# =====================================================================
# PROJECT 1: AI Invoice Auditor - Part 2 (The Parser Script)
# This script reads our text invoice, extracts key data, and saves to CSV (Excel).
# =====================================================================

import re
import csv
import os

def parse_invoice(file_path):
    print(f"Reading invoice: {file_path}...")
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # We use Regular Expressions (re) to find patterns.
    # Think of this like advanced 'Ctrl+F' in Excel!
    
    # 1. Extract Invoice Number (INV-XXXXX)
    inv_num_match = re.search(r"Invoice Number:\s*([^\n]+)", content)
    invoice_number = inv_num_match.group(1).strip() if inv_num_match else "Unknown"

    # 2. Extract Date
    date_match = re.search(r"Date:\s*([^\n]+)", content)
    invoice_date = date_match.group(1).strip() if date_match else "Unknown"

    # 3. Extract Vendor
    # We find the line after 'VENDOR DETAILS:'
    vendor_match = re.search(r"VENDOR DETAILS:\n([^\n]+)", content)
    vendor_name = vendor_match.group(1).strip() if vendor_match else "Unknown"

    # 4. Extract Total Due
    total_match = re.search(r"Total Due:\s*\$([0-9.]+)", content)
    total_due = float(total_match.group(1)) if total_match else 0.0

    print("\n--- Extracted Data ---")
    print(f"Vendor: {vendor_name}")
    print(f"Invoice Number: {invoice_number}")
    print(f"Date: {invoice_date}")
    print(f"Total Due: ${total_due}")

    # Now let's save this to a CSV file (which opens directly in Excel!)
    csv_file = "invoice_ledger.csv"
    file_exists = os.path.exists(csv_file)

    with open(csv_file, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        
        # If the file is new, write the headers first (just like Excel columns)
        if not file_exists:
            writer.writerow(["Vendor Name", "Invoice Number", "Invoice Date", "Total Amount Due"])
        
        # Write our extracted data row
        writer.writerow([vendor_name, invoice_number, invoice_date, total_due])

    print(f"\nSuccess! Saved to '{csv_file}' (Open this file in Excel!)")

# Run the parser on our sample invoice
if __name__ == "__main__":
    parse_invoice("sample_invoice.txt")
