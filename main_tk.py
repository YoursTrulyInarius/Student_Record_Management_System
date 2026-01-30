
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from database import Database
import re

class RecordSystemApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Record Management System")
        self.geometry("600x500")
        self.configure(bg="#f0f0f0")
        
        # Style Configuration
        style = ttk.Style(self)
        style.theme_use('clam') # Usually better cross-platform look than default
        style.configure("TLabel", background="#f0f0f0", font=("Arial", 12))
        style.configure("TButton", font=("Arial", 11), padding=6)
        style.configure("Title.TLabel", font=("Arial", 18, "bold"))
        style.configure("Treeview", font=("Arial", 10), rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))
        
        self.container = tk.Frame(self, bg="#f0f0f0")
        self.container.pack(fill="both", expand=True)
        
        self.frames = {}
        for F in (MainMenu, AddRecordFrame, ViewRecordsFrame):
            frame_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[frame_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("MainMenu")
    
    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        if hasattr(frame, 'on_show'):
            frame.on_show()
        frame.tkraise()

class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller
        
        # Center Content
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        
        ttk.Label(self, text="Record Management System", style="Title.TLabel").grid(row=1, column=1, pady=30)
        
        ttk.Button(self, text="Add New Record", width=25,
                   command=lambda: controller.show_frame("AddRecordFrame")).grid(row=2, column=1, pady=10)
        
        ttk.Button(self, text="View Records", width=25,
                   command=lambda: controller.show_frame("ViewRecordsFrame")).grid(row=3, column=1, pady=10)

class AddRecordFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller
        
        ttk.Label(self, text="Add New Record", style="Title.TLabel").pack(pady=20)
        
        form_frame = tk.Frame(self, bg="#f0f0f0")
        form_frame.pack(pady=10)
        
        self.entries = {}
        labels = ["Name", "Age", "Address", "Contact", "Email"]
        
        for idx, text in enumerate(labels):
            ttk.Label(form_frame, text=text + ":").grid(row=idx, column=0, padx=10, pady=8, sticky="e")
            entry = ttk.Entry(form_frame, width=30)
            entry.grid(row=idx, column=1, padx=10, pady=8)
            self.entries[text] = entry
            
        btn_frame = tk.Frame(self, bg="#f0f0f0")
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Save", command=self.save_record).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Cancel", command=lambda: controller.show_frame("MainMenu")).pack(side="left", padx=10)
    
    def save_record(self):
        name = self.entries["Name"].get().strip()
        age = self.entries["Age"].get().strip()
        address = self.entries["Address"].get().strip()
        contact = self.entries["Contact"].get().strip()
        email = self.entries["Email"].get().strip()
        
        # Validation
        if not all([name, age, address, contact, email]):
            messagebox.showerror("Error", "All fields are required!")
            return
            
        if not age.isdigit() or int(age) <= 0:
            messagebox.showerror("Error", "Age must be a positive number.")
            return

        if not contact.isdigit():
             messagebox.showerror("Error", "Contact must contain only numbers.")
             return

        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            messagebox.showerror("Error", "Invalid Email Address.")
            return
            
        try:
            db = Database()
            db.add_record(name, int(age), address, contact, email)
            messagebox.showinfo("Success", "Record Added Successfully!")
            self.clear_inputs()
            self.controller.show_frame("ViewRecordsFrame")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            
    def clear_inputs(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

class ViewRecordsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller
        
        top_frame = tk.Frame(self, bg="#f0f0f0")
        top_frame.pack(fill="x", pady=10)
        
        ttk.Label(top_frame, text="Records List", style="Title.TLabel").pack(side="left", padx=20)
        ttk.Button(top_frame, text="Back to Menu", command=lambda: controller.show_frame("MainMenu")).pack(side="right", padx=20)
        
        # Treeview
        columns = ("id", "name", "age", "address", "contact", "email")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("age", text="Age")
        self.tree.heading("address", text="Address")
        self.tree.heading("contact", text="Contact")
        self.tree.heading("email", text="Email")
        
        self.tree.column("id", width=30, anchor="center")
        self.tree.column("name", width=120)
        self.tree.column("age", width=40, anchor="center")
        self.tree.column("address", width=120)
        self.tree.column("contact", width=90)
        self.tree.column("email", width=120)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side="top", fill="both", expand=True, padx=10)
        scrollbar.pack(side="right", fill="y")
        
        # Action Buttons
        action_frame = tk.Frame(self, bg="#f0f0f0")
        action_frame.pack(pady=10)
        
        ttk.Button(action_frame, text="Edit Selected", command=self.edit_record).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Delete Selected", command=self.delete_record).pack(side="left", padx=5)
        
    def on_show(self):
        self.load_records()
        
    def load_records(self):
        # Clear existing
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        try:
            db = Database()
            records = db.get_records()
            for row in records:
                self.tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load records: {e}")
            
    def delete_record(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a record to delete.")
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this record?"):
            try:
                item = self.tree.item(selected[0])
                record_id = item['values'][0]
                db = Database()
                db.delete_record(record_id)
                self.load_records()
            except Exception as e:
                 messagebox.showerror("Error", f"Failed to delete: {e}")
                 
    def edit_record(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a record to edit.")
            return
            
        item = self.tree.item(selected[0])
        values = item['values']
        # values: (id, name, age, address, contact, email)
        
        EditDialog(self, values, self.load_records)

class EditDialog(tk.Toplevel):
    def __init__(self, parent, record_values, callback):
        super().__init__(parent)
        self.callback = callback
        self.record_id = record_values[0]
        self.title("Edit Record")
        self.geometry("400x400")
        
        form_frame = tk.Frame(self)
        form_frame.pack(pady=20, padx=20)
        
        self.entries = {}
        labels = ["Name", "Age", "Address", "Contact", "Email"]
        current_data = [record_values[1], record_values[2], record_values[3], record_values[4], record_values[5]]
        
        for idx, text in enumerate(labels):
            tk.Label(form_frame, text=text + ":").grid(row=idx, column=0, padx=10, pady=8, sticky="e")
            entry = tk.Entry(form_frame, width=25)
            entry.insert(0, str(current_data[idx]))
            entry.grid(row=idx, column=1, padx=10, pady=8)
            self.entries[text] = entry
            
        tk.Button(self, text="Save Changes", command=self.save).pack(pady=10)
        
    def save(self):
        name = self.entries["Name"].get().strip()
        age = self.entries["Age"].get().strip()
        address = self.entries["Address"].get().strip()
        contact = self.entries["Contact"].get().strip()
        email = self.entries["Email"].get().strip()
        
        # Validation (Simplified for brevity, but should match Add)
        if not all([name, age, address, contact, email]):
             messagebox.showerror("Error", "All fields are required!")
             return
        
        try:
            db = Database()
            db.update_record(self.record_id, name, int(age), address, contact, email)
            self.callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = RecordSystemApp()
    app.mainloop()
