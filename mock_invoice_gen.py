# =====================================================================
# PROJECT 1: AI Invoice Auditor - Part 1 (Sample Data Generator)
# This script generates a mock text-based invoice that we will parse.
# =====================================================================

invoice_content = """INVOICE
======================================
Invoice Number: INV-98724
Date: 2026-07-28
Due Date: 2026-08-28
======================================
VENDOR DETAILS:
Global Tech Solutions Ltd.
123 Cloud Avenue, Tech City
Email: billing@globaltech.com
======================================
BILL TO:
Acme Corporation
456 Enterprise Way, Suite 100
======================================
ITEMS:
1. Cloud Server Hosting - 1 Month: $800.00
2. Database Backup Service - 1 Month: $150.00
3. IT Consulting Hours - 5 Hours @ $100/hr: $500.00
======================================
FINANCIAL SUMMARY:
Subtotal: $1450.00
Tax (GST 18%): $261.00
Total Due: $1711.00
======================================
Thank you for your business!
"""

# Save the mock invoice text file
file_path = "sample_invoice.txt"
with open(file_path, "w", encoding="utf-8") as f:
    f.write(invoice_content)

print(f"Success! Mock invoice generated and saved to: {file_path}")
