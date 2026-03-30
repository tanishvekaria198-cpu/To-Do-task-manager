import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class TodoApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("My Todo List")
        self.root.geometry("600x700")
        self.root.configure(bg="#f0f0f0")
        
        self.tasks = []
        self.load_tasks()
        
        self.create_widgets()
        self.refresh_list()
    
    def create_widgets(self):
        # Title
        title = tk.Label(self.root, text="📋 My Todo List", font=("Arial", 24, "bold"), 
                        bg="#f0f0f0", fg="#333")
        title.pack(pady=20)
        
        # Input Frame
        input_frame = tk.Frame(self.root, bg="#f0f0f0")
        input_frame.pack(pady=10, fill="x", padx=20)
        
        self.task_entry = tk.Entry(input_frame, font=("Arial", 12), width=40)
        self.task_entry.pack(side="left", padx=(0, 10), ipady=8)
        self.task_entry.bind("<Return>", lambda e: self.add_task())
        
        add_btn = tk.Button(input_frame, text="Add Task", font=("Arial", 11, "bold"),
                           bg="#4CAF50", fg="white", command=self.add_task)
        add_btn.pack(side="left")
        
        # Task List
        list_frame = tk.Frame(self.root)
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.task_list = tk.Listbox(list_frame, font=("Arial", 12), height=18,
                                   selectmode="single", bg="white")
        self.task_list.pack(fill="both", expand=True, side="left")
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        self.task_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.task_list.yview)
        
        # Buttons Frame
        btn_frame = tk.Frame(self.root, bg="#f0f0f0")
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="✅ Complete", bg="#2196F3", fg="white", 
                 font=("Arial", 10, "bold"), width=12, command=self.complete_task).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="🗑 Delete", bg="#f44336", fg="white", 
                 font=("Arial", 10, "bold"), width=12, command=self.delete_task).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="Clear All", bg="#9E9E9E", fg="white", 
                 font=("Arial", 10, "bold"), width=12, command=self.clear_all).pack(side="left", padx=5)
        
        # Status
        self.status_label = tk.Label(self.root, text="", font=("Arial", 10), bg="#f0f0f0")
        self.status_label.pack(pady=10)
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def add_task(self):
        task_text = self.task_entry.get().strip()
        if not task_text:
            messagebox.showwarning("Empty", "Please enter a task!")
            return
        
        task = {
            "text": task_text,
            "completed": False,
            "time": datetime.now().strftime("%H:%M")
        }
        
        self.tasks.append(task)
        self.save_tasks()
        self.refresh_list()
        self.task_entry.delete(0, tk.END)
        self.status_label.config(text=f"Task added: {task_text[:30]}...", fg="green")
    
    def complete_task(self):
        try:
            selected = self.task_list.curselection()[0]
            self.tasks[selected]["completed"] = not self.tasks[selected]["completed"]
            self.save_tasks()
            self.refresh_list()
        except:
            messagebox.showwarning("Select", "Please select a task to complete!")
    
    def delete_task(self):
        try:
            selected = self.task_list.curselection()[0]
            deleted_task = self.tasks.pop(selected)
            self.save_tasks()
            self.refresh_list()
            self.status_label.config(text=f"Deleted: {deleted_task['text'][:30]}...", fg="red")
        except:
            messagebox.showwarning("Select", "Please select a task to delete!")
    
    def clear_all(self):
        if messagebox.askyesno("Clear All", "Delete all tasks?"):
            self.tasks.clear()
            self.save_tasks()
            self.refresh_list()
    
    def refresh_list(self):
        self.task_list.delete(0, tk.END)
        for i, task in enumerate(self.tasks):
            prefix = "✅ " if task["completed"] else "⬜ "
            text = f"{prefix}{task['time']} - {task['text']}"
            self.task_list.insert(tk.END, text)
            
            if task["completed"]:
                self.task_list.itemconfig(i, fg="gray")
    
    def save_tasks(self):
        try:
            with open("tasks.json", "w") as f:
                json.dump(self.tasks, f, indent=4)
        except:
            pass
    
    def load_tasks(self):
        if os.path.exists("tasks.json"):
            try:
                with open("tasks.json", "r") as f:
                    self.tasks = json.load(f)
            except:
                self.tasks = []
    
    def on_closing(self):
        self.save_tasks()
        self.root.destroy()

if __name__ == "__main__":
    app = TodoApp()
    app.root.mainloop()