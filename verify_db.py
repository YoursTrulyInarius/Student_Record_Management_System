
from database import Database
import os

def test_database():
    print("Testing Database Operations...")
    
    # Remove existing db to start fresh
    if os.path.exists("records.db"):
        os.remove("records.db")

    db = Database()
    
    # 1. Test Add Record
    print("\n1. Testing Add Record...")
    db.add_record("John Doe", 30, "123 Main St", "555-0100", "john@example.com")
    records = db.get_records()
    if len(records) == 1 and records[0][1] == "John Doe":
        print("PASS: Record added successfully.")
    else:
        print(f"FAIL: Expected 1 record, got {len(records)}")

    # 2. Test Get Record By ID
    print("\n2. Testing Get Record By ID...")
    record = db.get_record_by_id(1)
    if record and record[1] == "John Doe":
        print("PASS: Record retrieval successful.")
    else:
        print("FAIL: Record not found.")

    # 3. Test Update Record
    print("\n3. Testing Update Record...")
    db.update_record(1, "John Smith", 31, "456 Oak Ave", "555-0101", "john.smith@example.com")
    record = db.get_record_by_id(1)
    if record and record[1] == "John Smith" and record[2] == 31:
        print("PASS: Record updated successfully.")
    else:
        print(f"FAIL: Record update failed. Got {record}")

    # 4. Test Delete Record
    print("\n4. Testing Delete Record...")
    db.delete_record(1)
    records = db.get_records()
    if len(records) == 0:
        print("PASS: Record deleted successfully.")
    else:
        print(f"FAIL: Record not deleted. Count: {len(records)}")

if __name__ == "__main__":
    test_database()
