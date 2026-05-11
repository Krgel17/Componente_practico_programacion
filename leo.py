import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import random

# ══════════════════════════════════════════════
#  PALETA DE COLORES — DARK LUXURY GOLD
# ══════════════════════════════════════════════
COLORS = {
    "bg_dark":      "#0D0D0F",   # fondo principal
    "bg_card":      "#16161A",   # tarjetas / paneles
    "bg_input":     "#1E1E24",   # inputs
    "bg_hover":     "#252530",   # hover inputs
    "accent":       "#C9A84C",   # dorado principal
    "accent_light": "#E8C97A",   # dorado claro
    "accent_dim":   "#6B5420",   # dorado apagado
    "text_primary": "#F0EDE4",   # texto principal
    "text_muted":   "#8A8590",   # texto secundario
    "text_hint":    "#4A4755",   # placeholder
    "border":       "#2A2A35",   # bordes sutiles
    "border_gold":  "#3D3020",   # borde dorado sutil
    "success":      "#2D6A4F",   # verde éxito
    "success_text": "#95D5B2",   # texto éxito
    "danger":       "#6B1F1F",   # rojo
    "danger_text":  "#F4ACAC",   # texto rojo
    "separator":    "#1F1F28",   # separadores
}

FONT_TITLE  = ("Georgia", 18, "bold")
FONT_LABEL  = ("Segoe UI", 9)
FONT_INPUT  = ("Segoe UI", 10)
FONT_BUTTON = ("Segoe UI", 9, "bold")
FONT_SMALL  = ("Segoe UI", 8)
FONT_LOGO   = ("Georgia", 14, "bold")
FONT_HIST   = ("Consolas", 9)


class StyledEntry(tk.Frame):
    """Entry con borde dorado al enfocar y placeholder."""

    def __init__(self, master, placeholder="", width=None, **kw):
        super().__init__(master, bg=COLORS["bg_card"], pady=2)
        self.placeholder = placeholder
        self.active = False

        self.border_frame = tk.Frame(self, bg=COLORS["border"], padx=1, pady=1)
        self.border_frame.pack(fill="x")

        self.entry = tk.Entry(
            self.border_frame,
            font=FONT_INPUT,
            bg=COLORS["bg_input"],
            fg=COLORS["text_hint"],
            insertbackground=COLORS["accent"],
            relief="flat",
            bd=4,
            width=width or 28,
        )
        self.entry.pack(fill="x")

        if placeholder:
            self.entry.insert(0, placeholder)

        self.entry.bind("<FocusIn>", self._on_focus_in)
        self.entry.bind("<FocusOut>", self._on_focus_out)

    def _on_focus_in(self, e):
        self.border_frame.config(bg=COLORS["accent"])
        if self.entry.get() == self.placeholder:
            self.entry.delete(0, "end")
            self.entry.config(fg=COLORS["text_primary"])

    def _on_focus_out(self, e):
        self.border_frame.config(bg=COLORS["border"])
        if not self.entry.get():
            self.entry.insert(0, self.placeholder)
            self.entry.config(fg=COLORS["text_hint"])

    def get(self):
        val = self.entry.get()
        return "" if val == self.placeholder else val

    def clear(self):
        self.entry.delete(0, "end")
        self.entry.insert(0, self.placeholder)
        self.entry.config(fg=COLORS["text_hint"])


class StyledCombo(tk.Frame):
    """Combobox con estilo dark gold."""

    def __init__(self, master, values=(), **kw):
        super().__init__(master, bg=COLORS["bg_card"], pady=2)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Gold.TCombobox",
            fieldbackground=COLORS["bg_input"],
            background=COLORS["bg_input"],
            foreground=COLORS["text_primary"],
            arrowcolor=COLORS["accent"],
            bordercolor=COLORS["border"],
            darkcolor=COLORS["bg_input"],
            lightcolor=COLORS["bg_input"],
            selectbackground=COLORS["accent_dim"],
            selectforeground=COLORS["accent_light"],
            padding=6,
        )
        style.map(
            "Gold.TCombobox",
            fieldbackground=[("readonly", COLORS["bg_input"])],
            background=[("active", COLORS["bg_hover"])],
            bordercolor=[("focus", COLORS["accent"])],
        )

        self.combo = ttk.Combobox(
            self,
            values=values,
            style="Gold.TCombobox",
            font=FONT_INPUT,
            state="readonly",
        )
        self.combo.pack(fill="x")

    def get(self):
        return self.combo.get()

    def set_values(self, values):
        self.combo["values"] = values

    def set(self, val):
        self.combo.set(val)


class GoldButton(tk.Frame):
    """Botón con fondo dorado y efecto hover."""

    def __init__(self, master, text, command=None, variant="primary", **kw):
        super().__init__(master, bg=COLORS["bg_card"])

        if variant == "primary":
            bg, fg, hover = COLORS["accent"], COLORS["bg_dark"], COLORS["accent_light"]
        else:
            bg, fg, hover = COLORS["bg_input"], COLORS["accent"], COLORS["bg_hover"]

        self.btn = tk.Label(
            self,
            text=text,
            font=FONT_BUTTON,
            bg=bg,
            fg=fg,
            pady=8,
            padx=16,
            cursor="hand2",
        )
        self.btn.pack(fill="x", ipadx=4)

        self._bg, self._hover, self._cmd = bg, hover, command

        self.btn.bind("<Enter>",  lambda e: self.btn.config(bg=self._hover))
        self.btn.bind("<Leave>",  lambda e: self.btn.config(bg=self._bg))
        self.btn.bind("<Button-1>", lambda e: command() if command else None)


def separator(parent, padx=0, pady=(6, 6)):
    line = tk.Frame(parent, height=1, bg=COLORS["border"])
    line.pack(fill="x", padx=padx, pady=pady)


class SistemaFJ(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Sistema FJ  —  Reservas")
        self.geometry("420x720")
        self.resizable(False, False)
        self.config(bg=COLORS["bg_dark"])

        self.clientes = {}       # nombre → edad
        self.reservas = []

        self._build_ui()

    # ─────────────────────── CONSTRUCCIÓN DE UI ───────────────────────

    def _build_ui(self):
        # ── Cabecera logo ──────────────────────────────────────────────
        header = tk.Frame(self, bg=COLORS["bg_card"], pady=0)
        header.pack(fill="x")

        accent_bar = tk.Frame(header, bg=COLORS["accent"], height=3)
        accent_bar.pack(fill="x")

        inner_h = tk.Frame(header, bg=COLORS["bg_card"], padx=24, pady=16)
        inner_h.pack(fill="x")

        tk.Label(
            inner_h,
            text="✦ FJ",
            font=FONT_LOGO,
            bg=COLORS["bg_card"],
            fg=COLORS["accent"],
        ).pack(side="left")

        tk.Label(
            inner_h,
            text="S I S T E M A  D E  R E S E R V A S",
            font=("Segoe UI", 7, "bold"),
            bg=COLORS["bg_card"],
            fg=COLORS["text_muted"],
        ).pack(side="left", padx=(8, 0), pady=(5, 0))

        now = datetime.now().strftime("%d %b %Y")
        tk.Label(
            inner_h,
            text=now,
            font=FONT_SMALL,
            bg=COLORS["bg_card"],
            fg=COLORS["text_hint"],
        ).pack(side="right")

        # ── Cuerpo principal (scroll) ──────────────────────────────────
        canvas = tk.Canvas(self, bg=COLORS["bg_dark"], highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self.body = tk.Frame(canvas, bg=COLORS["bg_dark"])
        win_id = canvas.create_window((0, 0), window=self.body, anchor="nw")

        def _on_resize(e):
            canvas.itemconfig(win_id, width=e.width)
        canvas.bind("<Configure>", _on_resize)

        def _update_scroll(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
        self.body.bind("<Configure>", _update_scroll)

        self._build_section_cliente()
        separator(self.body, padx=24, pady=(0, 0))
        self._build_section_reserva()
        separator(self.body, padx=24, pady=(0, 0))
        self._build_section_historial()

    def _card(self, parent, title, icon="◈"):
        """Crea un card con título dorado."""
        outer = tk.Frame(parent, bg=COLORS["bg_dark"], padx=16, pady=12)
        outer.pack(fill="x")

        card = tk.Frame(outer, bg=COLORS["bg_card"], padx=20, pady=18)
        card.pack(fill="x")

        # borde izquierdo dorado
        accent_line = tk.Frame(card, bg=COLORS["accent"], width=3)
        accent_line.pack(side="left", fill="y", padx=(0, 14))

        content = tk.Frame(card, bg=COLORS["bg_card"])
        content.pack(side="left", fill="both", expand=True)

        title_row = tk.Frame(content, bg=COLORS["bg_card"])
        title_row.pack(fill="x", pady=(0, 12))

        tk.Label(
            title_row,
            text=f"{icon}  {title}",
            font=("Segoe UI", 10, "bold"),
            bg=COLORS["bg_card"],
            fg=COLORS["accent"],
        ).pack(side="left")

        return content

    def _label(self, parent, text):
        tk.Label(
            parent,
            text=text.upper(),
            font=("Segoe UI", 7, "bold"),
            bg=COLORS["bg_card"],
            fg=COLORS["text_muted"],
            pady=2,
        ).pack(anchor="w")

    # ─────────────────────── SECCIÓN CLIENTES ─────────────────────────

    def _build_section_cliente(self):
        content = self._card(self.body, "Nuevo Cliente", "◈")

        self._label(content, "Nombre")
        self.entry_nombre = StyledEntry(content, placeholder="ej. María García")
        self.entry_nombre.pack(fill="x", pady=(0, 10))

        self._label(content, "Edad")
        self.entry_edad = StyledEntry(content, placeholder="ej. 28", width=10)
        self.entry_edad.pack(anchor="w", pady=(0, 14))

        GoldButton(content, "＋  Registrar Cliente", command=self._crear_cliente).pack(fill="x")

        # badge contador
        self.lbl_count = tk.Label(
            content,
            text="0 clientes registrados",
            font=FONT_SMALL,
            bg=COLORS["bg_card"],
            fg=COLORS["text_hint"],
            pady=4,
        )
        self.lbl_count.pack(anchor="e")

    # ─────────────────────── SECCIÓN RESERVAS ─────────────────────────

    def _build_section_reserva(self):
        content = self._card(self.body, "Crear Reserva", "◇")

        self._label(content, "Seleccionar Cliente")
        self.combo_cliente = StyledCombo(content)
        self.combo_cliente.pack(fill="x", pady=(0, 10))

        self._label(content, "Hora de la reserva")
        self.entry_hora = StyledEntry(content, placeholder="ej. 14:30")
        self.entry_hora.pack(fill="x", pady=(0, 10))

        self._label(content, "Servicio")
        self.combo_servicio = StyledCombo(content, values=[
            "💆  Masaje Relajante",
            "✂️  Corte & Estilo",
            "💅  Manicure Premium",
            "🧖  Tratamiento Facial",
            "💇  Peinado & Brushing",
            "🪒  Afeitado Clásico",
        ])
        self.combo_servicio.pack(fill="x", pady=(0, 14))

        GoldButton(content, "✦  Confirmar Reserva", command=self._crear_reserva).pack(fill="x")

    # ─────────────────────── SECCIÓN HISTORIAL ────────────────────────

    def _build_section_historial(self):
        content = self._card(self.body, "Historial de Reservas", "▣")

        toolbar = tk.Frame(content, bg=COLORS["bg_card"])
        toolbar.pack(fill="x", pady=(0, 8))

        GoldButton(toolbar, "↺ Actualizar", command=self._refresh_historial, variant="secondary").pack(side="left")
        GoldButton(toolbar, "✕ Cancelar",   command=self._cancelar_reserva,  variant="secondary").pack(side="left", padx=(6, 0))
        GoldButton(toolbar, "✎ Modificar",  command=self._modificar_reserva, variant="secondary").pack(side="left", padx=(6, 0))

        self.lbl_total = tk.Label(
            toolbar,
            text="",
            font=FONT_SMALL,
            bg=COLORS["bg_card"],
            fg=COLORS["accent_dim"],
        )
        self.lbl_total.pack(side="right", padx=4)

        # Lista
        list_frame = tk.Frame(content, bg=COLORS["bg_input"], padx=2, pady=2)
        list_frame.pack(fill="both", expand=True)

        self.listbox = tk.Listbox(
            list_frame,
            font=FONT_HIST,
            bg=COLORS["bg_input"],
            fg=COLORS["text_primary"],
            selectbackground=COLORS["accent_dim"],
            selectforeground=COLORS["accent_light"],
            activestyle="none",
            relief="flat",
            bd=0,
            height=8,
        )
        sb = tk.Scrollbar(list_frame, orient="vertical", command=self.listbox.yview)
        self.listbox.config(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.listbox.pack(fill="both", expand=True, padx=4, pady=4)

        # Mensaje vacío
        self.lbl_empty = tk.Label(
            content,
            text="Sin reservas aún. ¡Crea la primera!",
            font=FONT_SMALL,
            bg=COLORS["bg_card"],
            fg=COLORS["text_hint"],
            pady=6,
        )
        self.lbl_empty.pack()

    # ─────────────────────── LÓGICA ───────────────────────────────────

    def _crear_cliente(self):
        nombre = self.entry_nombre.get().strip()
        edad   = self.entry_edad.get().strip()

        if not nombre:
            self._toast("⚠  El nombre no puede estar vacío.", error=True)
            return
        if nombre in self.clientes:
            self._toast(f"⚠  «{nombre}» ya está registrado.", error=True)
            return
        if not edad.isdigit() or not (1 <= int(edad) <= 120):
            self._toast("⚠  Ingresa una edad válida (1‑120).", error=True)
            return

        self.clientes[nombre] = int(edad)
        lista = sorted(self.clientes.keys())
        self.combo_cliente.set_values(lista)
        self.combo_cliente.set(nombre)

        self.lbl_count.config(
            text=f"{len(self.clientes)} cliente{'s' if len(self.clientes)!=1 else ''} registrado{'s' if len(self.clientes)!=1 else ''}",
            fg=COLORS["accent_dim"],
        )
        self.entry_nombre.clear()
        self.entry_edad.clear()
        self._toast(f"✓  Cliente «{nombre}» registrado correctamente.")

    def _crear_reserva(self):
        cliente  = self.combo_cliente.get()
        hora     = self.entry_hora.get().strip()
        servicio = self.combo_servicio.get()

        if not cliente:
            self._toast("⚠  Selecciona un cliente.", error=True)
            return
        if not hora:
            self._toast("⚠  Ingresa la hora de la reserva.", error=True)
            return
        if not servicio:
            self._toast("⚠  Selecciona un servicio.", error=True)
            return

        edad = self.clientes.get(cliente, "—")
        fecha = datetime.now().strftime("%d/%m/%Y")
        codigo = f"#{random.randint(1000,9999)}"

        registro = {
            "codigo": codigo,
            "cliente": cliente,
            "edad": edad,
            "hora": hora,
            "servicio": servicio,
            "fecha": fecha,
        }
        self.reservas.append(registro)
        self._refresh_historial()
        self._toast(f"✓  Reserva {codigo} confirmada para {cliente}.")

    def _refresh_historial(self):
        self.listbox.delete(0, "end")

        if not self.reservas:
            self.lbl_empty.pack()
            self.lbl_total.config(text="")
            return

        self.lbl_empty.pack_forget()
        self.lbl_total.config(text=f"{len(self.reservas)} reserva(s)")

        for i, r in enumerate(reversed(self.reservas)):
            svc = r["servicio"].split("  ")[-1] if "  " in r["servicio"] else r["servicio"]
            line = f"  {r['codigo']}  {r['fecha']} {r['hora']}  │  {r['cliente']} ({r['edad']}a)  │  {svc}"
            self.listbox.insert("end", line)
            if i % 2 == 0:
                self.listbox.itemconfig(i, bg=COLORS["bg_input"])
            else:
                self.listbox.itemconfig(i, bg=COLORS["bg_hover"])

    def _cancelar_reserva(self):
        sel = self.listbox.curselection()
        if not sel:
            self._toast("⚠  Selecciona una reserva del historial.", error=True)
            return

        idx = len(self.reservas) - 1 - sel[0]   # lista está invertida
        r   = self.reservas[idx]

        ventana = tk.Toplevel(self)
        ventana.title("Cancelar Reserva")
        ventana.geometry("340x180")
        ventana.resizable(False, False)
        ventana.config(bg=COLORS["bg_card"])
        ventana.grab_set()

        tk.Frame(ventana, bg=COLORS["danger"], height=3).pack(fill="x")

        tk.Label(
            ventana,
            text="¿Cancelar esta reserva?",
            font=("Segoe UI", 11, "bold"),
            bg=COLORS["bg_card"],
            fg=COLORS["danger_text"],
            pady=14,
        ).pack()

        svc = r["servicio"].split("  ")[-1] if "  " in r["servicio"] else r["servicio"]
        tk.Label(
            ventana,
            text=f"{r['codigo']}  •  {r['cliente']}  •  {svc}\n{r['fecha']} a las {r['hora']}",
            font=FONT_SMALL,
            bg=COLORS["bg_card"],
            fg=COLORS["text_muted"],
        ).pack(pady=(0, 14))

        btn_row = tk.Frame(ventana, bg=COLORS["bg_card"])
        btn_row.pack(fill="x", padx=20)

        def confirmar():
            self.reservas.pop(idx)
            self._refresh_historial()
            ventana.destroy()
            self._toast(f"✓  Reserva {r['codigo']} cancelada.")

        GoldButton(btn_row, "Sí, cancelar", command=confirmar).pack(side="left", fill="x", expand=True)
        tk.Frame(btn_row, width=8, bg=COLORS["bg_card"]).pack(side="left")
        GoldButton(btn_row, "Volver", command=ventana.destroy, variant="secondary").pack(side="left", fill="x", expand=True)

    def _modificar_reserva(self):
        sel = self.listbox.curselection()
        if not sel:
            self._toast("⚠  Selecciona una reserva del historial.", error=True)
            return

        idx = len(self.reservas) - 1 - sel[0]
        r   = self.reservas[idx]

        ventana = tk.Toplevel(self)
        ventana.title("Modificar Reserva")
        ventana.geometry("360x310")
        ventana.resizable(False, False)
        ventana.config(bg=COLORS["bg_card"])
        ventana.grab_set()

        tk.Frame(ventana, bg=COLORS["accent"], height=3).pack(fill="x")

        tk.Label(
            ventana,
            text=f"✎  Modificar  {r['codigo']}",
            font=("Segoe UI", 11, "bold"),
            bg=COLORS["bg_card"],
            fg=COLORS["accent"],
            pady=12,
        ).pack()

        body = tk.Frame(ventana, bg=COLORS["bg_card"], padx=20)
        body.pack(fill="x")

        # Cliente
        tk.Label(body, text="CLIENTE", font=("Segoe UI", 7, "bold"),
                 bg=COLORS["bg_card"], fg=COLORS["text_muted"]).pack(anchor="w")
        combo_cli = StyledCombo(body, values=sorted(self.clientes.keys()))
        combo_cli.set(r["cliente"])
        combo_cli.pack(fill="x", pady=(0, 8))

        # Hora
        tk.Label(body, text="HORA", font=("Segoe UI", 7, "bold"),
                 bg=COLORS["bg_card"], fg=COLORS["text_muted"]).pack(anchor="w")
        entry_hora = StyledEntry(body, placeholder=r["hora"])
        entry_hora.entry.delete(0, "end")
        entry_hora.entry.insert(0, r["hora"])
        entry_hora.entry.config(fg=COLORS["text_primary"])
        entry_hora.pack(fill="x", pady=(0, 8))

        # Servicio
        tk.Label(body, text="SERVICIO", font=("Segoe UI", 7, "bold"),
                 bg=COLORS["bg_card"], fg=COLORS["text_muted"]).pack(anchor="w")
        combo_svc = StyledCombo(body, values=[
            "💆  Masaje Relajante", "✂️  Corte & Estilo", "💅  Manicure Premium",
            "🧖  Tratamiento Facial", "💇  Peinado & Brushing", "🪒  Afeitado Clásico",
        ])
        combo_svc.set(r["servicio"])
        combo_svc.pack(fill="x", pady=(0, 14))

        def guardar():
            nueva_hora = entry_hora.entry.get().strip()
            nuevo_cli  = combo_cli.get()
            nuevo_svc  = combo_svc.get()

            if not nueva_hora:
                self._toast("⚠  La hora no puede estar vacía.", error=True)
                return
            if not nuevo_cli:
                self._toast("⚠  Selecciona un cliente.", error=True)
                return

            self.reservas[idx]["cliente"]  = nuevo_cli
            self.reservas[idx]["edad"]     = self.clientes.get(nuevo_cli, "—")
            self.reservas[idx]["hora"]     = nueva_hora
            self.reservas[idx]["servicio"] = nuevo_svc
            self._refresh_historial()
            ventana.destroy()
            self._toast(f"✓  Reserva {r['codigo']} actualizada.")

        GoldButton(body, "✦  Guardar cambios", command=guardar).pack(fill="x")

    # ─────────────────────── TOAST NOTIFICATION ───────────────────────

    def _toast(self, msg, error=False):
        bg  = COLORS["danger"]       if error else COLORS["success"]
        fg  = COLORS["danger_text"]  if error else COLORS["success_text"]

        toast = tk.Toplevel(self)
        toast.overrideredirect(True)
        toast.attributes("-topmost", True)

        lbl = tk.Label(
            toast,
            text=msg,
            font=("Segoe UI", 9),
            bg=bg,
            fg=fg,
            padx=16,
            pady=10,
        )
        lbl.pack()

        # posicionar en la esquina inferior derecha de la ventana
        self.update_idletasks()
        x = self.winfo_x() + self.winfo_width()  - 320
        y = self.winfo_y() + self.winfo_height() - 60
        toast.geometry(f"300x40+{x}+{y}")

        toast.after(2600, toast.destroy)


if __name__ == "__main__":
    app = SistemaFJ()
    app.mainloop()
