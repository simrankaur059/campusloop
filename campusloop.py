"""CampusLoop: a small sample campus reuse and exchange app."""

import tkinter as tk
from tkinter import messagebox, ttk


BG = "#F5F3EA"
SIDEBAR_BG = "#E8EFE9"
GREEN = "#14533F"
GREEN_LIGHT = "#E1EEE6"
TEXT = "#20342B"
MUTED = "#5E7067"
LINE = "#DCE4DD"
WHITE = "#FFFFFF"
GOLD = "#D6A94D"


ITEMS = [
    {"id": 1, "name": "Everyday Cotton Kurta", "category": "Clothes", "condition": "Very good", "price": 350, "mark": "CL", "color": "#E6D8C8"},
    {"id": 2, "name": "Stainless Steel Tiffin", "category": "Utensils", "condition": "Like new", "price": 180, "mark": "UT", "color": "#D8E2DF"},
    {"id": 3, "name": "Scientific Calculator", "category": "Electronics", "condition": "Good", "price": 450, "mark": "EL", "color": "#DCE2E9"},
    {"id": 4, "name": "Data Structures Notes", "category": "Books & Notes", "condition": "Good", "price": 120, "mark": "BN", "color": "#F1E1BC"},
    {"id": 5, "name": "Study Desk Lamp", "category": "Hostel Essentials", "condition": "Very good", "price": 275, "mark": "HE", "color": "#E9DCCB"},
    {"id": 6, "name": "Engineering Drawing Set", "category": "Books & Notes", "condition": "Like new", "price": 220, "mark": "BN", "color": "#E6E0C9"},
    {"id": 7, "name": "Wireless Mouse", "category": "Electronics", "condition": "Good", "price": 300, "mark": "EL", "color": "#D8E0E2"},
    {"id": 8, "name": "Ceramic Bowl Set", "category": "Utensils", "condition": "Very good", "price": 160, "mark": "UT", "color": "#E8DADB"},
    {"id": 9, "name": "Laundry Basket", "category": "Hostel Essentials", "condition": "Good", "price": 140, "mark": "HE", "color": "#DCE7D8"},
    {"id": 10, "name": "Denim Jacket", "category": "Clothes", "condition": "Good", "price": 500, "mark": "CL", "color": "#D5DEE8"},
    {"id": 11, "name": "Graph Notebook Pack", "category": "Books & Notes", "condition": "Unused", "price": 90, "mark": "BN", "color": "#EEE3C9"},
    {"id": 12, "name": "Sports Water Bottle", "category": "Other Items", "condition": "Like new", "price": 110, "mark": "OT", "color": "#D8E8E2"},
    {"id": 13, "name": "Extension Board", "category": "Electronics", "condition": "Very good", "price": 240, "mark": "EL", "color": "#DFE1E5"},
    {"id": 14, "name": "Foldable Clothes Hanger", "category": "Hostel Essentials", "condition": "Good", "price": 75, "mark": "HE", "color": "#E8DFD2"},
]

CATEGORIES = [
    "All Items",
    "Clothes",
    "Utensils",
    "Electronics",
    "Books & Notes",
    "Hostel Essentials",
    "Other Items",
]

ORDERS = [
    {"name": "Introduction to Algorithms", "date": "18 Oct 2026", "status": "Completed", "price": 280},
    {"name": "Desk Organizer", "date": "09 Oct 2026", "status": "Picked up", "price": 130},
    {"name": "Lab Coat", "date": "28 Sep 2026", "status": "Completed", "price": 320},
]

EXCHANGES = [
    {"name": "Hostel kettle for desk fan", "date": "21 Oct 2026", "status": "Awaiting response"},
    {"name": "Physics text for chemistry text", "date": "12 Oct 2026", "status": "Accepted"},
    {"name": "Yoga mat for badminton racket", "date": "02 Oct 2026", "status": "Completed"},
]


class CampusLoopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CampusLoop – Campus Reuse & Exchange System")
        self.root.geometry("1320x820")
        self.root.minsize(1000, 680)
        self.root.configure(bg=BG)

        self.saved_items = set()
        self.cart = {}
        self.requested_items = set()
        self.current_view = "All Items"
        self.search_text = tk.StringVar()
        self.last_columns = 0

        self._setup_styles()
        self._build_layout()
        self.search_text.trace_add("write", lambda *_: self.render_content())
        self.render_content()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=BG)
        style.configure("TLabel", background=BG, foreground=TEXT, font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 24, "bold"), foreground=GREEN)
        style.configure("Subtle.TLabel", foreground=MUTED, font=("Segoe UI", 10))
        style.configure("Card.TFrame", background=WHITE)
        style.configure("Card.TLabel", background=WHITE, foreground=TEXT, font=("Segoe UI", 10))
        style.configure("CardTitle.TLabel", background=WHITE, foreground=TEXT, font=("Segoe UI", 12, "bold"))
        style.configure("Price.TLabel", background=WHITE, foreground=GREEN, font=("Segoe UI", 13, "bold"))
        style.configure("Primary.TButton", background=GREEN, foreground=WHITE, padding=(12, 8), font=("Segoe UI", 9, "bold"), borderwidth=0)
        style.map("Primary.TButton", background=[("active", "#23664F")])
        style.configure("Secondary.TButton", background=GREEN_LIGHT, foreground=GREEN, padding=(10, 7), font=("Segoe UI", 9, "bold"), borderwidth=0)
        style.map("Secondary.TButton", background=[("active", "#D3E5D9")])
        style.configure("Quiet.TButton", background=WHITE, foreground=GREEN, padding=(8, 6), font=("Segoe UI", 9, "bold"), borderwidth=1, relief="solid")
        style.map("Quiet.TButton", background=[("active", GREEN_LIGHT)])
        style.configure("Nav.TButton", background=SIDEBAR_BG, foreground=TEXT, anchor="w", padding=(13, 10), font=("Segoe UI", 10), borderwidth=0)
        style.map("Nav.TButton", background=[("active", "#EAECE3")], foreground=[("active", GREEN)])
        style.configure("SelectedNav.TButton", background=GREEN, foreground=WHITE, anchor="w", padding=(13, 10), font=("Segoe UI", 10, "bold"), borderwidth=0)
        style.map("SelectedNav.TButton", background=[("active", "#23664F")], foreground=[("active", WHITE)])

    def _build_layout(self):
        self.shell = tk.Frame(self.root, bg=BG)
        self.shell.pack(fill="both", expand=True)

        self.sidebar = tk.Frame(self.shell, bg=SIDEBAR_BG, width=238, padx=18, pady=22)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        brand = tk.Frame(self.sidebar, bg=SIDEBAR_BG)
        brand.pack(fill="x", pady=(2, 26))
        logo = tk.Canvas(brand, width=40, height=40, bg=SIDEBAR_BG, highlightthickness=0)
        logo.pack(side="left", padx=(0, 10))
        self._draw_app_logo(logo)
        tk.Label(brand, text="CampusLoop", bg=SIDEBAR_BG, fg=GREEN, font=("Segoe UI", 16, "bold")).pack(side="left")

        tk.Label(self.sidebar, text="BROWSE", bg=SIDEBAR_BG, fg=MUTED, font=("Segoe UI", 8, "bold")).pack(anchor="w", pady=(0, 8))
        self.nav_buttons = {}
        for category in CATEGORIES:
            button = ttk.Button(self.sidebar, text=category, style="Nav.TButton", command=lambda value=category: self.show_view(value))
            button.pack(fill="x", pady=2)
            self.nav_buttons[category] = button

        tk.Frame(self.sidebar, bg=LINE, height=1).pack(fill="x", pady=18)
        tk.Label(self.sidebar, text="YOUR ACTIVITY", bg=SIDEBAR_BG, fg=MUTED, font=("Segoe UI", 8, "bold")).pack(anchor="w", pady=(0, 8))
        self.activity_buttons = {}
        for view in ("My Orders", "My Exchanges"):
            button = ttk.Button(self.sidebar, text=view, style="Nav.TButton", command=lambda value=view: self.show_view(value))
            button.pack(fill="x", pady=2)
            self.activity_buttons[view] = button

        tk.Label(self.sidebar, text="A little less waste,\na lot more community.", bg=SIDEBAR_BG, fg=MUTED, font=("Segoe UI", 9), justify="left").pack(side="bottom", anchor="w", pady=6)

        self.main_area = tk.Frame(self.shell, bg=BG)
        self.main_area.pack(side="left", fill="both", expand=True, padx=(8, 28))
        self._build_topbar()

        self.content_canvas = tk.Canvas(self.main_area, bg=BG, highlightthickness=0, borderwidth=0)
        self.scrollbar = ttk.Scrollbar(self.main_area, orient="vertical", command=self.content_canvas.yview)
        self.content_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y", pady=(8, 12))
        self.content_canvas.pack(side="left", fill="both", expand=True, pady=(8, 12))
        self.content_frame = tk.Frame(self.content_canvas, bg=BG)
        self.content_window = self.content_canvas.create_window((0, 0), window=self.content_frame, anchor="nw")
        self.content_frame.bind("<Configure>", lambda _event: self.content_canvas.configure(scrollregion=self.content_canvas.bbox("all")))
        self.content_canvas.bind("<Configure>", self._on_canvas_resize)
        self.content_canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _build_topbar(self):
        topbar = tk.Frame(self.main_area, bg=BG, height=82)
        topbar.pack(fill="x", pady=(18, 8))
        topbar.pack_propagate(False)

        search_wrap = tk.Frame(topbar, bg=WHITE, highlightbackground=LINE, highlightthickness=1)
        search_wrap.pack(side="left", fill="x", expand=True, padx=(0, 16), pady=8)
        tk.Label(search_wrap, text="⌕", bg=WHITE, fg=MUTED, font=("Segoe UI", 19)).pack(side="left", padx=(14, 8))
        search_entry = ttk.Entry(search_wrap, textvariable=self.search_text, font=("Segoe UI", 11))
        search_entry.pack(side="left", fill="both", expand=True, padx=(0, 12))
        search_entry.configure(style="Search.TEntry")
        ttk.Style().configure("Search.TEntry", fieldbackground=WHITE, borderwidth=0, padding=8)

        self.saved_button = self._icon_button(topbar, "bookmark", self.open_saved)
        self.cart_button = self._icon_button(topbar, "cart", lambda: self.show_view("Shopping Cart"))

    def _icon_button(self, parent, kind, command):
        holder = tk.Frame(parent, bg=BG, width=48, height=48, cursor="hand2")
        holder.pack(side="left", padx=(0, 9), pady=8)
        holder.pack_propagate(False)
        icon = tk.Canvas(holder, width=42, height=42, bg=BG, highlightthickness=0, cursor="hand2")
        icon.pack(fill="both", expand=True)
        if kind == "bookmark":
            icon.create_polygon(13, 8, 29, 8, 29, 34, 21, 28, 13, 34, fill=GREEN, outline=GREEN)
        else:
            icon.create_line(8, 11, 13, 11, 17, 26, 31, 26, 35, 15, 15, 15, fill=GREEN, width=2, joinstyle="round")
            icon.create_oval(18, 29, 22, 33, fill=GREEN, outline=GREEN)
            icon.create_oval(28, 29, 32, 33, fill=GREEN, outline=GREEN)
        icon.bind("<Button-1>", lambda _event: command())
        icon.bind("<Enter>", lambda _event: holder.configure(bg=GREEN_LIGHT))
        icon.bind("<Leave>", lambda _event: holder.configure(bg=BG))
        if kind == "cart":
            self.cart_badge = tk.Label(holder, text="0", bg="#C7654B", fg=WHITE, font=("Segoe UI", 8, "bold"), width=2)
            self.cart_badge.place(relx=1, x=-4, y=1, anchor="ne")
        return holder

    def _on_canvas_resize(self, event):
        self.content_canvas.itemconfigure(self.content_window, width=event.width)
        columns = self._column_count(event.width)
        if columns != self.last_columns and self.current_view not in ("Shopping Cart", "My Orders", "My Exchanges"):
            self.last_columns = columns
            self.render_content()

    def _on_mousewheel(self, event):
        if self.content_canvas.winfo_exists():
            self.content_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _column_count(self, width):
        if width >= 980:
            return 3
        if width >= 620:
            return 2
        return 1

    def show_view(self, view):
        self.current_view = view
        self.last_columns = self._column_count(self.content_canvas.winfo_width())
        self._update_navigation()
        self.render_content()

    def open_saved(self):
        self.show_view("Saved Items")

    def _update_navigation(self):
        for name, button in self.nav_buttons.items():
            button.configure(style="SelectedNav.TButton" if self.current_view == name else "Nav.TButton")
        for name, button in self.activity_buttons.items():
            button.configure(style="SelectedNav.TButton" if self.current_view == name else "Nav.TButton")

    def _refresh_cart_badge(self):
        self.cart_badge.configure(text=str(sum(self.cart.values())))

    def _matches_search(self, text):
        query = self.search_text.get().strip().lower()
        return not query or query in text.lower()

    def _visible_items(self):
        items = ITEMS
        if self.current_view in CATEGORIES and self.current_view != "All Items":
            items = [item for item in items if item["category"] == self.current_view]
        elif self.current_view == "Saved Items":
            items = [item for item in items if item["id"] in self.saved_items]
        elif self.current_view == "Shopping Cart":
            items = [item for item in items if item["id"] in self.cart]
        return [item for item in items if self._matches_search(item["name"] + " " + item["category"])]

    def render_content(self):
        if not hasattr(self, "content_frame"):
            return
        for child in self.content_frame.winfo_children():
            child.destroy()
        self.content_canvas.yview_moveto(0)

        if self.current_view == "Shopping Cart":
            self._render_cart()
        elif self.current_view == "My Orders":
            self._render_history("My Orders", "Your past purchases", ORDERS)
        elif self.current_view == "My Exchanges":
            self._render_history("My Exchanges", "Requests and swaps from your campus community", EXCHANGES)
        else:
            self._render_item_grid()
        self._refresh_cart_badge()
        self._update_navigation()

    def _section_heading(self, title, subtitle):
        heading = tk.Frame(self.content_frame, bg=BG)
        heading.pack(fill="x", pady=(12, 20))
        tk.Frame(heading, bg=GOLD, width=34, height=4).pack(anchor="w", pady=(0, 9))
        tk.Label(heading, text=title, bg=BG, fg=GREEN, font=("Segoe UI", 24, "bold")).pack(anchor="w")
        tk.Label(heading, text=subtitle, bg=BG, fg=MUTED, font=("Segoe UI", 10)).pack(anchor="w", pady=(4, 0))

    def _render_item_grid(self):
        if self.current_view == "Saved Items":
            title, subtitle = "Saved Items", "Things you have bookmarked for later."
        else:
            title = self.current_view
            subtitle = "Good finds, shared by students on your campus."
        self._section_heading(title, subtitle)
        items = self._visible_items()
        if not items:
            message = "No saved items yet. Bookmark something you like." if self.current_view == "Saved Items" else "No items match your search. Try another term."
            if self.current_view == "Saved Items" and self.search_text.get().strip():
                message = "No saved items match your search. Try another term."
            self._empty_state(message)
            return

        columns = self._column_count(self.content_canvas.winfo_width())
        self.last_columns = columns
        grid = tk.Frame(self.content_frame, bg=BG)
        grid.pack(fill="x", anchor="n")
        for column in range(columns):
            grid.grid_columnconfigure(column, weight=1, uniform="cards")
        for index, item in enumerate(items):
            card = self._create_item_card(grid, item)
            card.grid(row=index // columns, column=index % columns, sticky="nsew", padx=(0, 14), pady=(0, 14))

    def _create_item_card(self, parent, item):
        card = tk.Frame(parent, bg=WHITE, highlightbackground=LINE, highlightthickness=1, cursor="hand2")
        image = tk.Canvas(card, height=132, bg=item["color"], highlightthickness=0, cursor="hand2")
        image.pack(fill="x", padx=1, pady=(1, 0))

        def draw_placeholder(event):
            image.delete("category-icon")
            self._draw_category_icon(image, item["category"], event.width / 2, event.height / 2)

        image.bind("<Configure>", draw_placeholder)

        body = tk.Frame(card, bg=WHITE, padx=14, pady=12)
        body.pack(fill="both", expand=True)
        tk.Label(body, text=item["name"], bg=WHITE, fg=TEXT, font=("Segoe UI", 12, "bold"), anchor="w", wraplength=250, justify="left").pack(fill="x")
        tk.Label(body, text=f"{item['category']}  ·  {item['condition']}", bg=WHITE, fg=MUTED, font=("Segoe UI", 9), anchor="w").pack(fill="x", pady=(5, 10))
        row = tk.Frame(body, bg=WHITE)
        row.pack(fill="x")
        tk.Label(row, text=f"₹{item['price']:,}", bg=WHITE, fg=GREEN, font=("Segoe UI", 14, "bold")).pack(side="left")
        actions = tk.Frame(body, bg=WHITE)
        actions.pack(fill="x", pady=(12, 0))
        saved = item["id"] in self.saved_items
        ttk.Button(actions, text="Saved" if saved else "Save", style="Secondary.TButton", command=lambda value=item: self.toggle_saved(value)).pack(side="left")
        ttk.Button(actions, text="Add to Cart", style="Primary.TButton", command=lambda value=item: self.add_to_cart(value)).pack(side="right")

        for widget in (card, image, body):
            widget.bind("<Button-1>", lambda _event, value=item: self.show_item_details(value))
        for widget in (body, *body.winfo_children()):
            if isinstance(widget, (tk.Frame, tk.Label)):
                widget.bind("<Button-1>", lambda _event, value=item: self.show_item_details(value))
                widget.bind("<Enter>", lambda _event: card.configure(highlightbackground=GREEN, highlightthickness=2))
                widget.bind("<Leave>", lambda _event: card.configure(highlightbackground=LINE, highlightthickness=1))
        return card

    def _draw_app_logo(self, canvas):
        canvas.create_oval(5, 7, 27, 33, outline=GREEN, width=3)
        canvas.create_oval(13, 7, 35, 33, outline=GOLD, width=3)
        canvas.create_oval(17, 16, 23, 24, fill=GREEN, outline=GREEN)

    def _draw_category_icon(self, canvas, category, center_x, center_y):
        color = GREEN
        accent = "#B88735"
        tag = "category-icon"

        if category == "Clothes":
            points = [center_x - 17, center_y - 19, center_x - 29, center_y - 9,
                      center_x - 22, center_y + 1, center_x - 15, center_y - 4,
                      center_x - 15, center_y + 21, center_x + 15, center_y + 21,
                      center_x + 15, center_y - 4, center_x + 22, center_y + 1,
                      center_x + 29, center_y - 9, center_x + 17, center_y - 19,
                      center_x + 8, center_y - 13, center_x - 8, center_y - 13]
            canvas.create_polygon(points, fill=WHITE, outline=color, width=3, joinstyle="round", tags=tag)
            canvas.create_line(center_x, center_y - 12, center_x, center_y + 17, fill=accent, width=2, tags=tag)
        elif category == "Utensils":
            canvas.create_oval(center_x + 5, center_y - 20, center_x + 20, center_y - 2, outline=color, width=3, tags=tag)
            canvas.create_line(center_x + 12, center_y - 2, center_x + 12, center_y + 22, fill=color, width=3, capstyle="round", tags=tag)
            canvas.create_line(center_x - 16, center_y - 20, center_x - 16, center_y + 22, fill=color, width=3, capstyle="round", tags=tag)
            for offset in (-22, -16, -10):
                canvas.create_line(center_x + offset, center_y - 20, center_x + offset, center_y - 8, fill=accent, width=2, capstyle="round", tags=tag)
            canvas.create_line(center_x - 22, center_y - 8, center_x - 10, center_y - 8, fill=accent, width=2, tags=tag)
        elif category == "Electronics":
            canvas.create_rectangle(center_x - 25, center_y - 19, center_x + 25, center_y + 12, outline=color, width=3, tags=tag)
            canvas.create_line(center_x - 31, center_y + 19, center_x + 31, center_y + 19, fill=color, width=4, capstyle="round", tags=tag)
            canvas.create_line(center_x - 18, center_y + 12, center_x - 22, center_y + 19, fill=color, width=2, tags=tag)
            canvas.create_line(center_x + 18, center_y + 12, center_x + 22, center_y + 19, fill=color, width=2, tags=tag)
            canvas.create_oval(center_x - 3, center_y - 4, center_x + 3, center_y + 2, fill=accent, outline=accent, tags=tag)
        elif category == "Books & Notes":
            canvas.create_polygon(center_x, center_y - 15, center_x - 25, center_y - 21,
                                  center_x - 25, center_y + 17, center_x, center_y + 23,
                                  fill=WHITE, outline=color, width=3, tags=tag)
            canvas.create_polygon(center_x, center_y - 15, center_x + 25, center_y - 21,
                                  center_x + 25, center_y + 17, center_x, center_y + 23,
                                  fill=WHITE, outline=color, width=3, tags=tag)
            canvas.create_line(center_x, center_y - 14, center_x, center_y + 22, fill=accent, width=2, tags=tag)
            canvas.create_line(center_x - 19, center_y - 10, center_x - 5, center_y - 7, fill=color, width=1, tags=tag)
            canvas.create_line(center_x + 5, center_y - 7, center_x + 19, center_y - 10, fill=color, width=1, tags=tag)
        elif category == "Hostel Essentials":
            canvas.create_rectangle(center_x - 26, center_y - 17, center_x - 17, center_y + 21, outline=color, width=3, tags=tag)
            canvas.create_line(center_x - 17, center_y + 7, center_x + 27, center_y + 7, fill=color, width=3, tags=tag)
            canvas.create_line(center_x - 17, center_y - 4, center_x + 23, center_y - 4, fill=color, width=3, tags=tag)
            canvas.create_oval(center_x - 13, center_y - 13, center_x - 4, center_y - 4, fill=accent, outline=accent, tags=tag)
            canvas.create_line(center_x + 26, center_y + 7, center_x + 26, center_y + 21, fill=color, width=3, tags=tag)
            canvas.create_line(center_x - 26, center_y + 21, center_x + 27, center_y + 21, fill=color, width=3, tags=tag)
        else:
            canvas.create_polygon(center_x - 25, center_y - 9, center_x, center_y - 23,
                                  center_x + 25, center_y - 9, center_x + 25, center_y + 18,
                                  center_x, center_y + 25, center_x - 25, center_y + 18,
                                  fill=WHITE, outline=color, width=3, tags=tag)
            canvas.create_line(center_x - 25, center_y - 9, center_x, center_y + 1,
                               center_x + 25, center_y - 9, fill=accent, width=2, tags=tag)
            canvas.create_line(center_x, center_y + 1, center_x, center_y + 25, fill=color, width=2, tags=tag)

    def _render_cart(self):
        self._section_heading("Shopping Cart", "A quick look at the things you are collecting.")
        items = self._visible_items()
        if not items:
            self._empty_state("Your cart is taking a breather. Add an item to get started.")
            return
        for item in items:
            row = tk.Frame(self.content_frame, bg=WHITE, highlightbackground=LINE, highlightthickness=1, padx=16, pady=14)
            row.pack(fill="x", pady=(0, 10))
            tk.Label(row, text=item["mark"], bg=item["color"], fg=GREEN, width=5, height=2, font=("Segoe UI", 11, "bold")).pack(side="left", padx=(0, 14))
            info = tk.Frame(row, bg=WHITE)
            info.pack(side="left", fill="x", expand=True)
            tk.Label(info, text=item["name"], bg=WHITE, fg=TEXT, font=("Segoe UI", 11, "bold")).pack(anchor="w")
            tk.Label(info, text=f"₹{item['price']:,} each", bg=WHITE, fg=MUTED, font=("Segoe UI", 9)).pack(anchor="w", pady=(3, 0))
            controls = tk.Frame(row, bg=WHITE)
            controls.pack(side="right")
            ttk.Button(controls, text="−", style="Quiet.TButton", width=3, command=lambda value=item: self.change_quantity(value, -1)).pack(side="left", padx=3)
            tk.Label(controls, text=str(self.cart[item["id"]]), bg=WHITE, fg=TEXT, width=3, font=("Segoe UI", 10, "bold")).pack(side="left")
            ttk.Button(controls, text="+", style="Quiet.TButton", width=3, command=lambda value=item: self.change_quantity(value, 1)).pack(side="left", padx=3)
            ttk.Button(controls, text="Remove", style="Secondary.TButton", command=lambda value=item: self.remove_from_cart(value)).pack(side="left", padx=(10, 0))

        total = sum(item["price"] * self.cart[item["id"]] for item in items)
        total_row = tk.Frame(self.content_frame, bg=BG)
        total_row.pack(fill="x", pady=(8, 4))
        tk.Label(total_row, text="Cart total", bg=BG, fg=TEXT, font=("Segoe UI", 12, "bold")).pack(side="left")
        tk.Label(total_row, text=f"₹{total:,}", bg=BG, fg=GREEN, font=("Segoe UI", 18, "bold")).pack(side="right")

    def _render_history(self, title, subtitle, entries):
        self._section_heading(title, subtitle)
        visible = [entry for entry in entries if self._matches_search(entry["name"] + " " + entry["status"])]
        if not visible:
            self._empty_state("Nothing here matches your search.")
            return
        for entry in visible:
            row = tk.Frame(self.content_frame, bg=WHITE, highlightbackground=LINE, highlightthickness=1, padx=18, pady=16)
            row.pack(fill="x", pady=(0, 10))
            details = tk.Frame(row, bg=WHITE)
            details.pack(side="left", fill="x", expand=True)
            tk.Label(details, text=entry["name"], bg=WHITE, fg=TEXT, font=("Segoe UI", 12, "bold")).pack(anchor="w")
            tk.Label(details, text=entry["date"], bg=WHITE, fg=MUTED, font=("Segoe UI", 9)).pack(anchor="w", pady=(5, 0))
            status_color = GREEN if entry["status"] in ("Completed", "Picked up", "Accepted") else "#9A6A22"
            tk.Label(row, text=entry["status"], bg=GREEN_LIGHT if status_color == GREEN else "#F7EEDB", fg=status_color, padx=10, pady=5, font=("Segoe UI", 9, "bold")).pack(side="right", padx=(12, 18))
            if "price" in entry:
                tk.Label(row, text=f"₹{entry['price']:,}", bg=WHITE, fg=GREEN, font=("Segoe UI", 12, "bold")).pack(side="right")

    def _empty_state(self, message):
        panel = tk.Frame(self.content_frame, bg=WHITE, highlightbackground=LINE, highlightthickness=1, padx=24, pady=30)
        panel.pack(fill="x", pady=8)
        tk.Label(panel, text="Nothing to show just yet", bg=WHITE, fg=GREEN, font=("Segoe UI", 15, "bold")).pack(anchor="w")
        tk.Label(panel, text=message, bg=WHITE, fg=MUTED, font=("Segoe UI", 10)).pack(anchor="w", pady=(6, 0))

    def toggle_saved(self, item):
        if item["id"] in self.saved_items:
            self.saved_items.remove(item["id"])
        else:
            self.saved_items.add(item["id"])
        self.render_content()

    def add_to_cart(self, item):
        self.cart[item["id"]] = self.cart.get(item["id"], 0) + 1
        self.render_content()

    def change_quantity(self, item, amount):
        quantity = self.cart.get(item["id"], 0) + amount
        if quantity <= 0:
            self.cart.pop(item["id"], None)
        else:
            self.cart[item["id"]] = quantity
        self.render_content()

    def remove_from_cart(self, item):
        self.cart.pop(item["id"], None)
        self.render_content()

    def show_item_details(self, item):
        dialog = tk.Toplevel(self.root)
        dialog.title(item["name"])
        dialog.configure(bg=BG)
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        panel = tk.Frame(dialog, bg=WHITE, padx=24, pady=22)
        panel.pack(fill="both", expand=True, padx=12, pady=12)
        tk.Label(panel, text=item["mark"], bg=item["color"], fg=GREEN, width=7, height=3, font=("Segoe UI", 17, "bold")).pack(anchor="w", pady=(0, 15))
        tk.Label(panel, text=item["name"], bg=WHITE, fg=GREEN, font=("Segoe UI", 19, "bold"), wraplength=390, justify="left").pack(anchor="w")
        tk.Label(panel, text=f"{item['category']}  ·  {item['condition']}", bg=WHITE, fg=MUTED, font=("Segoe UI", 10)).pack(anchor="w", pady=(7, 12))
        tk.Label(panel, text=f"₹{item['price']:,}", bg=WHITE, fg=TEXT, font=("Segoe UI", 17, "bold")).pack(anchor="w", pady=(0, 18))
        actions = tk.Frame(panel, bg=WHITE)
        actions.pack(fill="x")
        ttk.Button(actions, text="Add to Cart", style="Secondary.TButton", command=lambda: self.add_to_cart(item)).pack(side="left")
        request_text = "Request Sent" if item["id"] in self.requested_items else "Request Item"
        request_button = ttk.Button(actions, text=request_text, style="Primary.TButton", command=lambda: self.request_item(item, dialog))
        request_button.pack(side="right")
        if item["id"] in self.requested_items:
            request_button.state(["disabled"])
        dialog.update_idletasks()
        dialog.geometry(f"{dialog.winfo_reqwidth()}x{dialog.winfo_reqheight()}")
        dialog.wait_window()

    def request_item(self, item, dialog):
        confirmed = messagebox.askyesno("Request this item?", f"Send a request to the student offering {item['name']}?", parent=dialog)
        if confirmed:
            self.requested_items.add(item["id"])
            messagebox.showinfo("Request sent", "Your request has been recorded in this demo.", parent=dialog)
            dialog.destroy()


def main():
    root = tk.Tk()
    CampusLoopApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()