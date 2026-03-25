import os
import sys
import tkinter as tk

crash_path = sys.argv[1] if len(sys.argv) > 1 else ""
summary = sys.argv[2] if len(sys.argv) > 2 else "Restart attempts exhausted. Diagnostics console standing by."

try:
    import ctypes
except Exception:
    ctypes = None


def rightmost_monitor_geometry():
    if ctypes is None:
        return None

    monitors = []
    user32 = ctypes.windll.user32

    class RECT(ctypes.Structure):
        _fields_ = [("left", ctypes.c_long), ("top", ctypes.c_long), ("right", ctypes.c_long), ("bottom", ctypes.c_long)]

    class MONITORINFO(ctypes.Structure):
        _fields_ = [
            ("cbSize", ctypes.c_ulong),
            ("rcMonitor", RECT),
            ("rcWork", RECT),
            ("dwFlags", ctypes.c_ulong),
        ]

    MONITORENUMPROC = ctypes.WINFUNCTYPE(
        ctypes.c_int,
        ctypes.c_ulong,
        ctypes.c_ulong,
        ctypes.POINTER(RECT),
        ctypes.c_double,
    )

    def callback(hMonitor, hdcMonitor, lprcMonitor, dwData):
        info = MONITORINFO()
        info.cbSize = ctypes.sizeof(MONITORINFO)
        user32.GetMonitorInfoW(hMonitor, ctypes.byref(info))
        monitors.append((info.rcWork.left, info.rcWork.top, info.rcWork.right, info.rcWork.bottom))
        return 1

    user32.EnumDisplayMonitors(0, 0, MONITORENUMPROC(callback), 0)
    if not monitors:
        return None
    return max(monitors, key=lambda m: m[2])


class JarvisDiagnostics(tk.Tk):
    BG = "#06111a"
    PANEL = "#0b1d2b"
    PANEL_ALT = "#0e2435"
    EDGE = "#2dd4ff"
    TEXT = "#c7f6ff"
    TEXT_DIM = "#79bed0"
    WARN = "#7ee7ff"
    FAIL = "#6fd7ff"
    ACCENT = "#1aa8d8"
    BUTTON_BG = "#071925"
    BUTTON_ACTIVE = "#0f2b3f"

    def __init__(self):
        super().__init__()
        self.configure(bg=self.BG)
        self.overrideredirect(True)
        self.geometry("980x690")
        self.minsize(860, 620)
        self._drag_start = None
        self._place_on_right_monitor()
        self._build_ui()

    def _place_on_right_monitor(self):
        g = rightmost_monitor_geometry()
        if not g:
            return
        left, top, right, bottom = g
        w, h = 980, 690
        x = left + max(20, (right - left - w) // 2)
        y = top + max(20, (bottom - top - h) // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _build_ui(self):
        shell = tk.Frame(self, bg=self.BG, highlightbackground=self.EDGE, highlightthickness=1)
        shell.pack(fill="both", expand=True, padx=14, pady=14)

        titlebar = tk.Frame(shell, bg="#04101a", height=34, highlightbackground=self.ACCENT, highlightthickness=1)
        titlebar.pack(fill="x", padx=18, pady=(14, 8))
        titlebar.pack_propagate(False)
        for widget in (titlebar,):
            widget.bind("<ButtonPress-1>", self._start_drag)
            widget.bind("<B1-Motion>", self._drag_window)

        title_left = tk.Frame(titlebar, bg="#04101a")
        title_left.pack(side="left", fill="y")
        title_left.bind("<ButtonPress-1>", self._start_drag)
        title_left.bind("<B1-Motion>", self._drag_window)
        tk.Label(title_left, text="J.A.R.V.I.S. // DIAGNOSTICS", bg="#04101a", fg=self.TEXT_DIM, font=("Consolas", 10, "bold")).pack(side="left", padx=10)

        close_btn = tk.Button(
            titlebar,
            text="✕",
            command=self.destroy,
            bg="#04101a",
            fg=self.EDGE,
            activebackground="#102334",
            activeforeground="#d8fbff",
            relief="flat",
            borderwidth=0,
            font=("Segoe UI Symbol", 11),
            cursor="hand2",
            padx=10,
        )
        close_btn.pack(side="right", pady=2, padx=4)

        header = tk.Frame(shell, bg=self.BG, height=54)
        header.pack(fill="x", padx=18, pady=(2, 8))

        tk.Label(
            header,
            text="J.A.R.V.I.S. // RECOVERY DIAGNOSTICS",
            bg=self.BG,
            fg=self.EDGE,
            font=("Segoe UI Semibold", 18),
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Desktop engine failure detected // autonomous recovery unavailable",
            bg=self.BG,
            fg=self.TEXT_DIM,
            font=("Consolas", 10),
        ).pack(anchor="w", pady=(3, 0))

        divider = tk.Frame(shell, bg=self.EDGE, height=1)
        divider.pack(fill="x", padx=18, pady=(0, 12))

        grid = tk.Frame(shell, bg=self.BG)
        grid.pack(fill="both", expand=True, padx=18, pady=(0, 12))
        grid.grid_columnconfigure(0, weight=3)
        grid.grid_columnconfigure(1, weight=2)
        grid.grid_rowconfigure(1, weight=1)

        status_panel = tk.Frame(grid, bg=self.PANEL, highlightbackground=self.ACCENT, highlightthickness=1)
        status_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=(0, 10))

        tk.Label(status_panel, text="SYSTEM STATUS", bg=self.PANEL, fg=self.EDGE, font=("Consolas", 11, "bold")).pack(anchor="w", padx=14, pady=(12, 4))
        tk.Label(status_panel, text="STATE: CRITICAL", bg=self.PANEL, fg=self.FAIL, font=("Consolas", 16, "bold")).pack(anchor="w", padx=14)
        tk.Label(status_panel, text=summary, bg=self.PANEL, fg=self.TEXT, font=("Segoe UI", 11), wraplength=560, justify="left").pack(anchor="w", padx=14, pady=(8, 12))

        meta_panel = tk.Frame(grid, bg=self.PANEL_ALT, highlightbackground=self.ACCENT, highlightthickness=1)
        meta_panel.grid(row=0, column=1, sticky="nsew", pady=(0, 10))

        tk.Label(meta_panel, text="RECOVERY TELEMETRY", bg=self.PANEL_ALT, fg=self.EDGE, font=("Consolas", 11, "bold")).pack(anchor="w", padx=14, pady=(12, 10))
        self._kv(meta_panel, "Crash file", crash_path if crash_path else "Unavailable")
        self._kv(meta_panel, "Recovery", "Retries exhausted")
        self._kv(meta_panel, "Console", "Manual intervention required")

        log_panel = tk.Frame(grid, bg=self.PANEL, highlightbackground=self.ACCENT, highlightthickness=1)
        log_panel.grid(row=1, column=0, sticky="nsew", padx=(0, 10))

        tk.Label(log_panel, text="CRASH LOG STREAM", bg=self.PANEL, fg=self.EDGE, font=("Consolas", 11, "bold")).pack(anchor="w", padx=14, pady=(12, 8))

        text_wrap = tk.Frame(log_panel, bg=self.PANEL)
        text_wrap.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        scrollbar = tk.Scrollbar(text_wrap)
        scrollbar.pack(side="right", fill="y")

        self.text = tk.Text(
            text_wrap,
            bg="#04101a",
            fg=self.TEXT,
            insertbackground=self.EDGE,
            selectbackground="#144a63",
            selectforeground=self.TEXT,
            relief="flat",
            borderwidth=0,
            wrap="word",
            yscrollcommand=scrollbar.set,
            font=("Consolas", 10),
            padx=10,
            pady=10,
        )
        self.text.pack(fill="both", expand=True)
        scrollbar.config(command=self.text.yview)

        details = "No crash file available."
        if crash_path and os.path.exists(crash_path):
            with open(crash_path, "r", encoding="utf-8") as f:
                details = f.read()
        self.text.insert("1.0", details)
        self.text.config(state="disabled")

        control_panel = tk.Frame(grid, bg=self.PANEL_ALT, highlightbackground=self.ACCENT, highlightthickness=1)
        control_panel.grid(row=1, column=1, sticky="nsew")

        tk.Label(control_panel, text="RECOVERY ACTIONS", bg=self.PANEL_ALT, fg=self.EDGE, font=("Consolas", 11, "bold")).pack(anchor="w", padx=14, pady=(12, 8))
        tk.Label(
            control_panel,
            text="Recovery automation has failed. Use the controls below to inspect the crash artifacts or dismiss the diagnostics shell.",
            bg=self.PANEL_ALT,
            fg=self.TEXT,
            wraplength=280,
            justify="left",
            font=("Segoe UI", 10),
        ).pack(anchor="w", padx=14, pady=(0, 12))

        self.feedback = tk.Label(control_panel, text="Operator controls online.", bg=self.PANEL_ALT, fg=self.TEXT_DIM, font=("Consolas", 10))
        self.feedback.pack(anchor="w", padx=14, pady=(0, 12))

        button_row = tk.Frame(control_panel, bg=self.PANEL_ALT)
        button_row.pack(fill="x", padx=14, pady=(0, 12))

        self._button(button_row, "OPEN CRASH FOLDER", self.open_folder).pack(fill="x", pady=(0, 10))
        self._button(button_row, "DISMISS DIAGNOSTICS", self.destroy).pack(fill="x")

        footer = tk.Frame(shell, bg=self.BG)
        footer.pack(fill="x", padx=18, pady=(0, 14))
        tk.Label(footer, text="JARVIS fallback console // styled recovery shell", bg=self.BG, fg=self.TEXT_DIM, font=("Consolas", 9)).pack(anchor="e")

    def _kv(self, parent, key, value):
        row = tk.Frame(parent, bg=parent["bg"])
        row.pack(fill="x", padx=14, pady=2)
        tk.Label(row, text=f"{key}:", width=14, anchor="w", bg=parent["bg"], fg=self.TEXT_DIM, font=("Consolas", 10)).pack(side="left")
        tk.Label(row, text=value, anchor="w", justify="left", bg=parent["bg"], fg=self.TEXT, wraplength=260, font=("Consolas", 10)).pack(side="left", fill="x", expand=True)

    def _button(self, parent, text, command):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=self.BUTTON_BG,
            fg=self.EDGE,
            activebackground=self.BUTTON_ACTIVE,
            activeforeground="#d8fbff",
            relief="flat",
            borderwidth=0,
            highlightbackground=self.EDGE,
            highlightthickness=1,
            font=("Consolas", 10, "bold"),
            padx=10,
            pady=10,
            cursor="hand2",
        )

    def _start_drag(self, event):
        self._drag_start = (event.x_root, event.y_root)

    def _drag_window(self, event):
        if not self._drag_start:
            return
        start_x, start_y = self._drag_start
        dx = event.x_root - start_x
        dy = event.y_root - start_y
        x = self.winfo_x() + dx
        y = self.winfo_y() + dy
        self.geometry(f"+{x}+{y}")
        self._drag_start = (event.x_root, event.y_root)

    def open_folder(self):
        if crash_path and os.path.exists(crash_path):
            self.feedback.config(text="Opening crash folder...", fg=self.WARN)
            os.startfile(os.path.dirname(crash_path))
        else:
            self.feedback.config(text="Crash folder unavailable.", fg=self.FAIL)


if __name__ == "__main__":
    app = JarvisDiagnostics()
    app.mainloop()
