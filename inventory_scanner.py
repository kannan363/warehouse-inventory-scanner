import csv
import tkinter as tk
from tkinter import filedialog
from datetime import datetime

OUTPUT_CSV_FILE = "stock_status_report.csv"

def select_input_file():
    root = tk.Tk()
    root.withdraw()

    print("Opening file selection window...")
    file_path = filedialog.askopenfilename(
        title="Select Inventory CSV File",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )
    return file_path

def print_simulated_email(items, in_stock_count, low_count, critical_count):
    """Formats and prints the full stock status as a simulated email alert."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_restock = low_count + critical_count

    print("\n" + "=" * 102)
    print("                                     SIMULATED EMAIL ALERT                                     ")
    print("=" * 102)
    print("TO      : inventory-manager@warehouse.com")
    print("FROM    : system-alerts@warehouse-auto.com")
    print(f"SUBJECT : 🚨 ALERT: {total_restock} Items Require Restock ({critical_count} Critical)")
    print("-" * 102)
    print("Hello Procurement Team,\n")
    print(f"This is an automated inventory alert generated on {timestamp}.\n")
    print("Summary of current stock levels:")
    print(f"  - Total Scanned       : {len(items)}")
    print(f"  - Items In Stock      : {in_stock_count}")
    print(f"  - Low Priority Items  : {low_count}")
    print(f"  - CRITICAL Items      : {critical_count}\n")
    
    print("Full Inventory Status Report:\n")
    print(f"{'ITEM ID':<12}{'ITEM NAME':<40}{'CURRENT':<10}{'THRESHOLD':<12}{'STATUS':<18}{'PRIORITY'}")
    print("-" * 102)
    
    # (full report)
    for item in items:
        print(
            f"{item['item_id']:<12}"
            f"{item['item_name']:<40}"
            f"{item['current_quantity']:<10}"
            f"{item['reorder_threshold']:<12}"
            f"{item['status']:<18}"
            f"{item['priority']}"
        )

    print("\nFull breakdown has also been saved to 'stock_status_report.csv'.")
    print("\nRegards,\nAutomated Inventory System")
    print("=" * 102 + "\n")

def scan_inventory():
    input_file = select_input_file()

    if not input_file:
        print("No file selected. Operation canceled.")
        return

    try:
        items = []
        in_stock_count = 0
        low_priority_count = 0
        critical_priority_count = 0

        with open(input_file, mode="r", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            
            # Using enumerate to generate backup IDs (e.g., ITEM-001) if missing
            for idx, row in enumerate(reader, start=1):
                
                item_id = row.get("item_id")
                if not item_id:
                    item_id = f"ITEM-{idx:03d}"  

                item_name = row["item_name"]
                current_quantity = int(row["current_quantity"])
                reorder_threshold = int(row["reorder_threshold"])
                
                # Status & Priority Logic
                if current_quantity > reorder_threshold:
                    status = "IN STOCK"
                    priority = "GOOD"
                    in_stock_count += 1
                else:
                    status = "RESTOCK NEEDED"
                    critical_limit = reorder_threshold * 0.25
                    if current_quantity < critical_limit:
                        priority = "CRITICAL"
                        critical_priority_count += 1
                    else:
                        priority = "LOW"
                        low_priority_count += 1

                items.append({
                    "item_id": item_id,
                    "item_name": item_name,
                    "current_quantity": current_quantity,
                    "reorder_threshold": reorder_threshold,
                    "status": status,
                    "priority": priority
                })

        # 1. Output Full Simulated Email Alert to Terminal
        print_simulated_email(items, in_stock_count, low_priority_count, critical_priority_count)

        # 2. Export Output to CSV File (item_id remains in output)
        fieldnames = ["item_id", "item_name", "current_quantity", "reorder_threshold", "status", "priority"]
        
        with open(OUTPUT_CSV_FILE, mode="w", newline="", encoding="utf-8") as output_csv:
            writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
            writer.writeheader()
            for item in items:
                writer.writerow(item)

        print(f"Success! Report saved to CSV file: '{OUTPUT_CSV_FILE}'")

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except KeyError as e:
        print(f"Error: Missing required column in CSV - {e}")
    except ValueError as e:
        print(f"Error: Invalid numerical data in CSV - {e}")

if __name__ == "__main__":
    scan_inventory()
