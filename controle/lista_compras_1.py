import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime, timedelta

# Paleta
BG       = "#F7F6F3"
SURFACE  = "#FFFFFF"
BORDER   = "#E8E6E1"
ACCENT   = "#2D7DD2"
TEXT     = "#1A1916"
TEXT_SUB = "#8A8680"
DANGER   = "#E05A4E"
GREEN    = "#2E9E5B"

SAVE_FILE   = os.path.join(os.path.dirname(__file__), "lista_compras.json")
STATUS_OPTS = ["Nao comprado", "Comprado"]


def load_items():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_items(items):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

def fmt_price(value):
    try:
        v = float(value)
        # Format: R$ 1.234,56
        s = f"{v:,.2f}"          # 1,234.56
        s = s.replace(",", "X").replace(".", ",").replace("X", ".")
        return f"R$ {s}"
    except (ValueError, TypeError):
        return ""


class ListaCompras(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lista de Compras")
        self.geometry("800x580")
        self.minsize(640, 440)
        self.configure(bg=BG)
        self.resizable(True, True)

        self.items = load_items()
        self._editing_index = None
        self._sort_col = None
        self._sort_rev = False

        self._apply_styles()
        self._build_ui()
        self._refresh_table()

    def _apply_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview",
            background=SURFACE, fieldbackground=SURFACE,
            foreground=TEXT, rowheight=36,
            font=("Helvetica", 11), borderwidth=0)
        style.configure("Treeview.Heading",
            background=BG, foreground=TEXT_SUB,
            font=("Helvetica", 10, "bold"), relief="flat", borderwidth=0)
        style.map("Treeview",
            background=[("selected", "#E8F0FB")],
            foreground=[("selected", TEXT)])
        style.map("Treeview.Heading", background=[("active", BORDER)])
        style.configure("TCombobox",
            fieldbackground=SURFACE, background=SURFACE,
            foreground=TEXT, arrowcolor=ACCENT,
            bordercolor=BORDER, lightcolor=BORDER, darkcolor=BORDER, relief="flat")
        style.map("TCombobox",
            fieldbackground=[("readonly", SURFACE)],
            bordercolor=[("focus", ACCENT)])
        style.configure("TEntry",
            fieldbackground=SURFACE, foreground=TEXT,
            bordercolor=BORDER, lightcolor=BORDER, darkcolor=BORDER, relief="flat", padding=6)
        style.map("TEntry", bordercolor=[("focus", ACCENT)])

    def _build_ui(self):
        # Cabecalho
        hdr = tk.Frame(self, bg=SURFACE, pady=16)
        hdr.pack(fill="x")
        tk.Label(hdr, text="Lista de Compras", bg=SURFACE,
                 fg=TEXT, font=("Helvetica", 18, "bold"), padx=20).pack(side="left")
        self.summary_lbl = tk.Label(hdr, text="", bg=SURFACE,
                                    fg=TEXT_SUB, font=("Helvetica", 11), padx=20)
        self.summary_lbl.pack(side="right", anchor="s", pady=4)
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")

        # Formulario
        form_outer = tk.Frame(self, bg=SURFACE,
                              highlightbackground=BORDER, highlightthickness=1)
        form_outer.pack(fill="x", padx=16, pady=12)
        form = tk.Frame(form_outer, bg=SURFACE, padx=16, pady=14)
        form.pack(fill="x")

        for col, label in enumerate(["Nome do item", "Data", "Preco (R$)", "Status"]):
            tk.Label(form, text=label, bg=SURFACE, fg=TEXT_SUB,
                     font=("Helvetica", 9, "bold")).grid(
                row=0, column=col, sticky="w", padx=(0, 10))

        # Nome
        self.entry_nome = ttk.Entry(form, font=("Helvetica", 11), width=20)
        self.entry_nome.grid(row=1, column=0, sticky="ew", padx=(0, 10), ipady=4)
        self.entry_nome.bind("<Return>", lambda e: self._add_or_save())

        # Data
        today = datetime.today()
        date_opts = [(today + timedelta(days=i)).strftime("%d/%m/%Y") for i in range(7)]
        self.combo_data = ttk.Combobox(form, values=date_opts,
                                       font=("Helvetica", 11), width=12, state="normal")
        self.combo_data.set(today.strftime("%d/%m/%Y"))
        self.combo_data.grid(row=1, column=1, sticky="ew", padx=(0, 10), ipady=4)

        # Preco
        vcmd = (self.register(self._validate_price), "%P")
        self.entry_preco = ttk.Entry(form, font=("Helvetica", 11), width=10,
                                     validate="key", validatecommand=vcmd)
        self.entry_preco.grid(row=1, column=2, sticky="ew", padx=(0, 10), ipady=4)
        self.entry_preco.bind("<Return>", lambda e: self._add_or_save())

        # Status
        self.combo_status = ttk.Combobox(form, values=STATUS_OPTS,
                                         font=("Helvetica", 11), width=14, state="readonly")
        self.combo_status.set("Nao comprado")
        self.combo_status.grid(row=1, column=3, sticky="ew", padx=(0, 10), ipady=4)

        # Botao Adicionar
        self.btn_add = tk.Label(form, text="+ Adicionar", bg=ACCENT, fg="white",
                                font=("Helvetica", 10, "bold"), padx=12, pady=6, cursor="hand2")
        self.btn_add.grid(row=1, column=4, padx=(4, 0))
        self.btn_add.bind("<Enter>", lambda e: self.btn_add.config(bg="#1A5EA8"))
        self.btn_add.bind("<Leave>", lambda e: self.btn_add.config(bg=ACCENT))
        self.btn_add.bind("<Button-1>", lambda e: self._add_or_save())

        # Botao Cancelar
        self.btn_cancel = tk.Label(form, text="Cancelar", bg=BORDER, fg=TEXT,
                                   font=("Helvetica", 10), padx=12, pady=6, cursor="hand2")
        self.btn_cancel.grid(row=1, column=5, padx=(6, 0))
        self.btn_cancel.bind("<Button-1>", lambda e: self._cancel_edit())
        self.btn_cancel.grid_remove()

        form.columnconfigure(0, weight=3)
        form.columnconfigure(1, weight=2)
        form.columnconfigure(2, weight=1)
        form.columnconfigure(3, weight=2)

        # Filtro
        filter_bar = tk.Frame(self, bg=BG, pady=4)
        filter_bar.pack(fill="x", padx=16)
        tk.Label(filter_bar, text="Mostrar:", bg=BG, fg=TEXT_SUB,
                 font=("Helvetica", 9)).pack(side="left", padx=(0, 6))
        self._filter_var = tk.StringVar(value="Todos")
        for opt in ["Todos", "Nao comprado", "Comprado"]:
            rb = tk.Radiobutton(filter_bar, text=opt, variable=self._filter_var, value=opt,
                                bg=BG, fg=TEXT, activebackground=BG, selectcolor=BG,
                                font=("Helvetica", 10), command=self._refresh_table)
            rb.pack(side="left", padx=6)

        # Tabela
        table_frame = tk.Frame(self, bg=SURFACE,
                               highlightbackground=BORDER, highlightthickness=1)
        table_frame.pack(fill="both", expand=True, padx=16, pady=(4, 8))

        cols = ("nome", "data", "preco", "status")
        self.tree = ttk.Treeview(table_frame, columns=cols,
                                  show="headings", selectmode="browse")

        self.tree.heading("nome",   text="Nome do item",  command=lambda: self._sort("nome"))
        self.tree.heading("data",   text="Data",          command=lambda: self._sort("data"))
        self.tree.heading("preco",  text="Preco (R$)",    command=lambda: self._sort_price())
        self.tree.heading("status", text="Status",        command=lambda: self._sort("status"))

        self.tree.column("nome",   width=220, anchor="w")
        self.tree.column("data",   width=110, anchor="center")
        self.tree.column("preco",  width=120, anchor="center")
        self.tree.column("status", width=130, anchor="center")

        sb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        self.tree.tag_configure("comprado",     foreground=GREEN,  background="#F0FFF4")
        self.tree.tag_configure("nao_comprado", foreground=DANGER, background="#FFF5F5")

        self.tree.bind("<Double-1>", self._on_double_click)
        self.tree.bind("<Delete>",   self._delete_selected)

        # Rodape
        footer = tk.Frame(self, bg=BG)
        footer.pack(fill="x", padx=16, pady=(0, 10))
        tk.Label(footer, text="Duplo clique para editar  |  Delete para remover",
                 bg=BG, fg=TEXT_SUB, font=("Helvetica", 9)).pack(side="left")
        del_btn = tk.Label(footer, text="Remover selecionado",
                           bg=BG, fg=DANGER, font=("Helvetica", 9), cursor="hand2")
        del_btn.pack(side="right")
        del_btn.bind("<Button-1>", lambda e: self._delete_selected())
        self.total_lbl = tk.Label(footer, text="", bg=BG,
                                   fg=TEXT, font=("Helvetica", 9, "bold"))
        self.total_lbl.pack(side="right", padx=20)

    def _validate_price(self, value):
        if value == "":
            return True
        v = value.replace(",", ".")
        try:
            float(v)
            return True
        except ValueError:
            return v.endswith(".")

    def _add_or_save(self):
        nome      = self.entry_nome.get().strip()
        data      = self.combo_data.get().strip()
        status    = self.combo_status.get()
        preco_raw = self.entry_preco.get().strip().replace(",", ".")

        if not nome:
            self.entry_nome.focus_set()
            messagebox.showwarning("Atencao", "Informe o nome do item.")
            return
        if not data:
            data = datetime.today().strftime("%d/%m/%Y")
        try:
            preco = float(preco_raw) if preco_raw else None
        except ValueError:
            messagebox.showwarning("Atencao", "Preco invalido.")
            return

        record = {"nome": nome, "data": data, "preco": preco, "status": status}

        if self._editing_index is not None:
            self.items[self._editing_index] = record
            self._editing_index = None
            self.btn_add.config(text="+ Adicionar")
            self.btn_cancel.grid_remove()
        else:
            self.items.append(record)

        save_items(self.items)
        self.entry_nome.delete(0, "end")
        self.entry_preco.delete(0, "end")
        self.combo_data.set(datetime.today().strftime("%d/%m/%Y"))
        self.combo_status.set("Nao comprado")
        self._refresh_table()
        self.entry_nome.focus_set()

    def _cancel_edit(self):
        self._editing_index = None
        self.btn_add.config(text="+ Adicionar")
        self.btn_cancel.grid_remove()
        self.entry_nome.delete(0, "end")
        self.entry_preco.delete(0, "end")
        self.combo_data.set(datetime.today().strftime("%d/%m/%Y"))
        self.combo_status.set("Nao comprado")

    def _on_double_click(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        idx  = self.tree.index(sel[0])
        filt = self._filter_var.get()
        visible  = [i for i, it in enumerate(self.items)
                    if filt == "Todos" or it["status"] == filt]
        real_idx = visible[idx]
        item     = self.items[real_idx]
        self._editing_index = real_idx

        self.entry_nome.delete(0, "end")
        self.entry_nome.insert(0, item["nome"])
        self.combo_data.set(item["data"])
        self.entry_preco.delete(0, "end")
        if item.get("preco") is not None:
            self.entry_preco.insert(0, str(item["preco"]).replace(".", ","))
        self.combo_status.set(item["status"])
        self.btn_add.config(text="Salvar")
        self.btn_cancel.grid()
        self.entry_nome.focus_set()

    def _delete_selected(self, event=None):
        sel = self.tree.selection()
        if not sel:
            return
        if not messagebox.askyesno("Remover", "Deseja remover este item?"):
            return
        idx  = self.tree.index(sel[0])
        filt = self._filter_var.get()
        visible = [i for i, it in enumerate(self.items)
                   if filt == "Todos" or it["status"] == filt]
        self.items.pop(visible[idx])
        save_items(self.items)
        self._refresh_table()

    def _refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        filt    = self._filter_var.get()
        visible = [it for it in self.items
                   if filt == "Todos" or it["status"] == filt]

        for it in visible:
            tag   = "comprado" if it["status"] == "Comprado" else "nao_comprado"
            preco = fmt_price(it["preco"]) if it.get("preco") is not None else "-"
            self.tree.insert("", "end",
                values=(it["nome"], it["data"], preco, it["status"]),
                tags=(tag,))

        total     = len(self.items)
        comprados = sum(1 for it in self.items if it["status"] == "Comprado")
        total_gasto = sum(it.get("preco") or 0 for it in self.items if it["status"] == "Comprado")

        self.summary_lbl.config(text=f"{comprados} / {total} comprados")
        self.total_lbl.config(text=f"Total gasto: {fmt_price(total_gasto)}")

    def _sort(self, col):
        rev = (self._sort_col == col) and not self._sort_rev
        self._sort_col, self._sort_rev = col, rev
        self.items.sort(key=lambda x: x.get(col, "") or "", reverse=rev)
        save_items(self.items)
        self._refresh_table()

    def _sort_price(self):
        rev = (self._sort_col == "preco") and not self._sort_rev
        self._sort_col, self._sort_rev = "preco", rev
        self.items.sort(key=lambda x: x.get("preco") or 0, reverse=rev)
        save_items(self.items)
        self._refresh_table()


if __name__ == "__main__":
    app = ListaCompras()
    app.mainloop()
