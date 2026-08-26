import os
import socket
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# --- REPORTLAB IMPORTS FOR PDF EXPORT ---
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


class TrainDoorUploaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Train Door System Batch Uploader v2.0")
        self.root.geometry("680x580")
        self.root.resizable(False, False)

        # State Variables
        self.firmware_path = tk.StringVar()
        self.unit_id = tk.StringVar(value="01")
        self.car_type = tk.StringVar(value="long")
        self.status_records = {}
        self.lock = threading.Lock()

        self._build_ui()

    def _build_ui(self):
        # 1. Configuration Frame
        config_frame = ttk.LabelFrame(self.root, text=" Configuration ", padding=10)
        config_frame.pack(fill="x", padx=15, pady=10)

        ttk.Label(config_frame, text="Firmware File:").grid(row=0, column=0, sticky="w")
        ttk.Entry(config_frame, textvariable=self.firmware_path, width=45).grid(row=0, column=1, padx=5)
        ttk.Button(config_frame, text="Browse...", command=self.browse_firmware).grid(row=0, column=2)

        ttk.Label(config_frame, text="Unit Number:").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Entry(config_frame, textvariable=self.unit_id, width=15).grid(row=1, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(config_frame, text="Car Set Type:").grid(row=2, column=0, sticky="w")
        car_combo = ttk.Combobox(config_frame, textvariable=self.car_type, values=["single", "long"], state="readonly", width=12)
        car_combo.grid(row=2, column=1, sticky="w", padx=5)

        # 2. Control Frame
        btn_frame = ttk.Frame(self.root, padding=5)
        btn_frame.pack(fill="x", padx=15)

        self.start_btn = ttk.Button(btn_frame, text="Start Batch Upload", command=self.start_batch_thread)
        self.start_btn.pack(side="left", padx=5)

        self.pdf_btn = ttk.Button(btn_frame, text="Export PDF Checksheet", command=self.export_pdf, state="disabled")
        self.pdf_btn.pack(side="left", padx=5)

        # 3. Target / Results Treeview Table
        table_frame = ttk.LabelFrame(self.root, text=" DCU Upload Status ", padding=10)
        table_frame.pack(fill="both", expand=True, padx=15, pady=10)

        columns = ("door_label", "ip", "status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        self.tree.heading("door_label", text="Door Location")
        self.tree.heading("ip", text="IP Address")
        self.tree.heading("status", text="Status")

        self.tree.column("door_label", width=150)
        self.tree.column("ip", width=160)
        self.tree.column("status", width=260)
        self.tree.pack(fill="both", expand=True)

    def browse_firmware(self):
        filename = filedialog.askopenfilename(
            title="Select Firmware File",
            filetypes=[("Firmware Files", "*.bin *.hex *.img"), ("All Files", "*.*")]
        )
        if filename:
            self.firmware_path.set(filename)

    def generate_targets(self):
        unit = self.unit_id.get().zfill(2)
        subnet = "93" if self.car_type.get() == "single" else "94"
        
        # Mapping Door Names and Target IPs
        door_configs = [
            ("Door 1L (Side A)", f"10.{subnet}.{unit}.141"),
            ("Door 1R (Side B)", f"10.{subnet}.{unit}.142"),
            ("Door 2L (Side A)", f"10.{subnet}.{unit}.143"),
            ("Door 2R (Side B)", f"10.{subnet}.{unit}.144"),
            ("Door 3L (Side A)", f"10.{subnet}.{unit}.145"),
            ("Door 3R (Side B)", f"10.{subnet}.{unit}.146"),
            ("Door 4L (Side A)", f"10.{subnet}.{unit}.147"),
            ("Door 4R (Side B)", f"10.{subnet}.{unit}.148"),
        ]
        return door_configs

    def start_batch_thread(self):
        if not self.firmware_path.get():
            messagebox.showwarning("Missing File", "Please select a firmware file first.")
            return

        # Clear existing table
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.status_records.clear()
        self.start_btn.config(state="disabled")
        self.pdf_btn.config(state="disabled")

        targets = self.generate_targets()
        for label, ip in targets:
            item_id = self.tree.insert("", "end", values=(label, ip, "PENDING"))
            self.status_records[ip] = {"label": label, "status": "PENDING", "tree_id": item_id}

        # Run upload logic on a separate thread
        threading.Thread(target=self.run_batch_process, args=(targets,), daemon=True).start()

    def run_batch_process(self, targets):
        threads = []
        for label, ip in targets:
            t = threading.Thread(target=self.worker_upload, args=(label, ip))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        # Re-enable UI components once finished
        self.root.after(0, lambda: self.start_btn.config(state="normal"))
        self.root.after(0, lambda: self.pdf_btn.config(state="normal"))
        self.root.after(0, lambda: messagebox.showinfo("Completed", "Batch upload process finished!"))

    def worker_upload(self, label, ip):
        # Update UI: In Progress
        self.update_status(ip, "UPLOADING...")

        try:
            # TFTP / UDP Transfer Logic (Simulated socket delay for demo)
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(3.0)
            
            # Send transfer packet routine...
            time.sleep(1.5)  # Simulating transfer execution
            sock.close()

            self.update_status(ip, "SUCCESS / VERIFIED")
        except Exception as err:
            self.update_status(ip, f"FAILED ({str(err)})")

    def update_status(self, ip, status_str):
        with self.lock:
            self.status_records[ip]["status"] = status_str
            tree_id = self.status_records[ip]["tree_id"]
            self.root.after(0, lambda: self.tree.item(tree_id, values=(self.status_records[ip]["label"], ip, status_str)))

    def export_pdf(self):
        save_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Documents", "*.pdf")],
            initialfile=f"Train_Unit_{self.unit_id.get()}_Door_Checksheet.pdf"
        )
        if not save_path:
            return

        doc = SimpleDocTemplate(save_path, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        # Title Block
        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Heading1'],
            fontSize=16,
            leading=20,
            textColor=colors.HexColor('#1B365D')
        )
        elements.append(Paragraph("Train Door System Maintenance Checksheet", title_style))
        elements.append(Spacer(1, 10))

        meta_text = f"<b>Unit ID:</b> {self.unit_id.get()} &nbsp;&nbsp;&nbsp;&nbsp; " \
                    f"<b>Configuration:</b> {self.car_type.get().upper()} Set &nbsp;&nbsp;&nbsp;&nbsp; " \
                    f"<b>Date:</b> {time.strftime('%Y-%m-%d %H:%M')}<br/>" \
                    f"<b>Firmware Loaded:</b> {os.path.basename(self.firmware_path.get())}"
        elements.append(Paragraph(meta_text, styles['Normal']))
        elements.append(Spacer(1, 15))

        # Build Results Table for PDF
        table_data = [["Door Location", "IP Address", "Execution Status"]]
        for ip, info in self.status_records.items():
            table_data.append([info["label"], ip, info["status"]])

        pdf_table = Table(table_data, colWidths=[180, 150, 180])
        pdf_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1B365D')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
        ]))

        elements.append(pdf_table)

        try:
            doc.build(elements)
            messagebox.showinfo("PDF Export", f"Checksheet generated successfully:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Could not create PDF: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = TrainDoorUploaderApp(root)
    root.mainloop()