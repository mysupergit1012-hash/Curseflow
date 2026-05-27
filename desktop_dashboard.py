import subprocess
import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox


ROOT = Path(__file__).resolve().parent
ENGINE = ROOT / "curseflow.py"


class CurseflowDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Curseflow Desktop")
        self.geometry("520x360")
        self.minsize(460, 320)
        self.configure(bg="#f7f8f2")
        self.process = None

        self.protocol("WM_DELETE_WINDOW", self.close)
        self.create_widgets()

    def create_widgets(self):
        self.columnconfigure(0, weight=1)

        header = tk.Frame(self, bg="#f7f8f2")
        header.grid(row=0, column=0, sticky="ew", padx=24, pady=(24, 12))
        header.columnconfigure(0, weight=1)

        title = tk.Label(
            header,
            text="Curseflow Desktop",
            bg="#f7f8f2",
            fg="#171717",
            font=("Segoe UI", 22, "bold"),
            anchor="w",
        )
        title.grid(row=0, column=0, sticky="ew")

        self.status = tk.Label(
            header,
            text="Idle",
            bg="#d84f2a",
            fg="#ffffff",
            font=("Segoe UI", 10, "bold"),
            padx=14,
            pady=6,
        )
        self.status.grid(row=0, column=1, sticky="e")

        body = tk.Frame(self, bg="#ffffff", highlightthickness=1, highlightbackground="#d9ded6")
        body.grid(row=1, column=0, sticky="nsew", padx=24, pady=12)
        self.rowconfigure(1, weight=1)
        body.columnconfigure(0, weight=1)

        description = tk.Label(
            body,
            text=(
                "Activate starts the local webcam engine. Move the system cursor "
                "with your index finger, double blink for left click, and long "
                "blink for right click."
            ),
            bg="#ffffff",
            fg="#5f6460",
            font=("Segoe UI", 11),
            justify="left",
            wraplength=430,
            anchor="w",
        )
        description.grid(row=0, column=0, columnspan=2, sticky="ew", padx=18, pady=(18, 16))

        self.activate_button = tk.Button(
            body,
            text="Activate",
            command=self.activate,
            bg="#146c54",
            fg="#ffffff",
            activebackground="#0f5643",
            activeforeground="#ffffff",
            relief="flat",
            font=("Segoe UI", 12, "bold"),
            padx=18,
            pady=12,
        )
        self.activate_button.grid(row=1, column=0, sticky="ew", padx=(18, 8), pady=8)

        self.stop_button = tk.Button(
            body,
            text="Stop",
            command=self.stop,
            bg="#ffffff",
            fg="#171717",
            activebackground="#ecf3ed",
            activeforeground="#171717",
            relief="solid",
            borderwidth=1,
            font=("Segoe UI", 12, "bold"),
            padx=18,
            pady=12,
            state="disabled",
        )
        self.stop_button.grid(row=1, column=1, sticky="ew", padx=(8, 18), pady=8)

        self.log = tk.Label(
            body,
            text="Camera engine is stopped.",
            bg="#ecf3ed",
            fg="#5f6460",
            font=("Segoe UI", 10),
            justify="left",
            wraplength=430,
            anchor="nw",
            padx=12,
            pady=12,
        )
        self.log.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=18, pady=(14, 18))
        body.rowconfigure(2, weight=1)

        footer = tk.Label(
            self,
            text="The OpenCV preview window closes with q or Esc. This dashboard can also stop it.",
            bg="#f7f8f2",
            fg="#5f6460",
            font=("Segoe UI", 9),
            anchor="w",
        )
        footer.grid(row=2, column=0, sticky="ew", padx=24, pady=(0, 18))

    def activate(self):
        if self.process and self.process.poll() is None:
            return

        if not ENGINE.exists():
            messagebox.showerror("Curseflow", f"Missing engine file: {ENGINE}")
            return

        self.process = subprocess.Popen(
            [sys.executable, str(ENGINE)],
            cwd=str(ROOT),
            creationflags=getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0),
        )
        self.set_running()
        self.after(1000, self.watch_process)

    def stop(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
        self.process = None
        self.set_idle("Camera engine is stopped.")

    def watch_process(self):
        if not self.process:
            return
        exit_code = self.process.poll()
        if exit_code is None:
            self.after(1000, self.watch_process)
            return
        self.process = None
        self.set_idle(f"Camera engine exited with code {exit_code}.")

    def set_running(self):
        self.status.configure(text="Live", bg="#146c54")
        self.activate_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.log.configure(
            text=(
                "System-wide control is active. Keep your hand and face visible "
                "in the Curseflow preview window."
            )
        )

    def set_idle(self, message):
        self.status.configure(text="Idle", bg="#d84f2a")
        self.activate_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.log.configure(text=message)

    def close(self):
        self.stop()
        self.destroy()


if __name__ == "__main__":
    CurseflowDashboard().mainloop()
