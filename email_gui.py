import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from send_email import send_email

class EmailGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Sender")
        self.root.geometry("600x500")
        
        # Create main frame with padding
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Recipient
        ttk.Label(main_frame, text="To:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.recipient = ttk.Entry(main_frame, width=50)
        self.recipient.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Subject
        ttk.Label(main_frame, text="Subject:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.subject = ttk.Entry(main_frame, width=50)
        self.subject.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Message body
        ttk.Label(main_frame, text="Message:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.body = tk.Text(main_frame, width=50, height=15)
        self.body.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Attachments
        self.attachments = []
        ttk.Label(main_frame, text="Attachments:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.attachment_label = ttk.Label(main_frame, text="No files selected")
        self.attachment_label.grid(row=3, column=1, sticky=tk.W, pady=5)
        ttk.Button(main_frame, text="Add Files", command=self.add_attachments).grid(row=3, column=2, sticky=tk.E, pady=5)
        
        # Send button
        ttk.Button(main_frame, text="Send Email", command=self.send_email_click).grid(row=4, column=1, pady=20)
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
    def add_attachments(self):
        files = filedialog.askopenfilenames(
            title="Choose files",
            filetypes=[("All files", "*.*")]
        )
        if files:
            self.attachments.extend(files)
            self.attachment_label.config(text=f"{len(self.attachments)} files selected")
    
    def send_email_click(self):
        recipient = self.recipient.get().strip()
        subject = self.subject.get().strip()
        body = self.body.get("1.0", tk.END).strip()
        
        if not recipient or not subject or not body:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        try:
            attachments = self.attachments if self.attachments else None
            send_email(recipient, subject, body, attachments)
            messagebox.showinfo("Success", "Email sent successfully!")
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send email: {str(e)}")
    
    def clear_fields(self):
        self.recipient.delete(0, tk.END)
        self.subject.delete(0, tk.END)
        self.body.delete("1.0", tk.END)
        self.attachments = []
        self.attachment_label.config(text="No files selected")

if __name__ == "__main__":
    root = tk.Tk()
    app = EmailGUI(root)
    root.mainloop()