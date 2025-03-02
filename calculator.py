

def run():
    import tkinter as tk
    from tkinter import ttk, messagebox
    import math

    class CalculatorApp:
        def __init__(self, root):
            self.root = root
            root.title("All-in-One Calculator")
            root.geometry("750x750")
            root.configure(bg="#1E1E1E")
            
            # Set TTK style
            style = ttk.Style()
            style.theme_use("clam")
            style.configure("TButton", font=("Arial", 12), padding=5, background="#3A3A3A", foreground="white")
            style.configure("TLabel", font=("Arial", 12), background="#1E1E1E", foreground="white")
            style.configure("TEntry", font=("Arial", 12), padding=5)
            style.configure("Header.TLabel", font=("Arial", 16, "bold"), background="#1E1E1E", foreground="white")
            
            # Create Notebook (Tabbed interface)
            self.notebook = ttk.Notebook(root)
            self.notebook.pack(expand=True, fill="both")
            
            # Create Tabs
            self.create_basic_tab()
            self.create_geometry_tab()
            self.create_financial_tab()
            self.create_algebra_tab()
        
        # ----------------- Basic Calculator Tab -----------------
        def create_basic_tab(self):
            self.basic_frame = ttk.Frame(self.notebook)
            self.notebook.add(self.basic_frame, text="Basic")
            
            # Display
            self.basic_display = ttk.Entry(self.basic_frame, font=("Arial", 20), justify="right")
            self.basic_display.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
            
            # Buttons layout
            buttons = [
                ("7", "8", "9", "/"),
                ("4", "5", "6", "*"),
                ("1", "2", "3", "-"),
                ("C", "0", "=", "+")
            ]
            for r, row in enumerate(buttons):
                for c, text in enumerate(row):
                    btn = ttk.Button(self.basic_frame, text=text, command=lambda t=text: self.basic_button_click(t))
                    btn.grid(row=r+1, column=c, padx=5, pady=5, sticky="nsew")
            
            # Configure grid weights for responsiveness
            for i in range(4):
                self.basic_frame.columnconfigure(i, weight=1)
            for i in range(6):
                self.basic_frame.rowconfigure(i, weight=1)
        
        def basic_button_click(self, char):
            if char == "=":
                try:
                    # Using eval -- caution in production!
                    result = eval(self.basic_display.get())
                    self.basic_display.delete(0, tk.END)
                    self.basic_display.insert(tk.END, str(result))
                except Exception:
                    messagebox.showerror("Error", "Invalid Expression")
            elif char == "C":
                self.basic_display.delete(0, tk.END)
            else:
                self.basic_display.insert(tk.END, char)
        
        # ----------------- Geometry Calculator Tab -----------------
        def create_geometry_tab(self):
            self.geometry_frame = ttk.Frame(self.notebook)
            self.notebook.add(self.geometry_frame, text="Geometry")
            
            header = ttk.Label(self.geometry_frame, text="Geometry Calculator", style="Header.TLabel")
            header.pack(pady=10)
            
            # Calculation type selection using a Combobox
            self.geo_calc_type = tk.StringVar()
            geo_options = [
                "Area of Circle", "Circumference of Circle", 
                "Area of Rectangle", "Perimeter of Rectangle", 
                "Slope", "Pythagorean Theorem", "Area of Triangle", 
                "Volume of Sphere", "Surface Area of Sphere", 
                "Volume of Cylinder", "Surface Area of Cylinder", 
                "Area of Ellipse",
                "Area of Regular Polygon", "Perimeter of Regular Polygon",
                "Volume of Cube", "Surface Area of Cube",
                "Volume of Cone", "Surface Area of Cone",
                "Volume of Rectangular Prism", "Surface Area of Rectangular Prism",
                "Circumference of Ellipse"
            ]
            ttk.Label(self.geometry_frame, text="Select Calculation:").pack(pady=5)
            self.geo_combobox = ttk.Combobox(self.geometry_frame, textvariable=self.geo_calc_type, values=geo_options, state="readonly")
            self.geo_combobox.pack(pady=5)
            self.geo_combobox.bind("<<ComboboxSelected>>", self.update_geometry_inputs)
            
            # Input frame for parameters
            self.geo_input_frame = ttk.Frame(self.geometry_frame)
            self.geo_input_frame.pack(pady=10, fill="x", padx=20)
            
            # Radio buttons for Units
            self.geo_unit = tk.StringVar(value="cm")
            unit_frame = ttk.Frame(self.geometry_frame)
            unit_frame.pack(pady=5)
            ttk.Label(unit_frame, text="Units:").pack(side="left", padx=5)
            for unit in ["cm", "m", "in"]:
                ttk.Radiobutton(unit_frame, text=unit, variable=self.geo_unit, value=unit).pack(side="left", padx=5)
            
            self.geo_result_label = ttk.Label(self.geometry_frame, text="Result: ", font=("Arial", 14, "bold"))
            self.geo_result_label.pack(pady=10)
            
            ttk.Button(self.geometry_frame, text="Calculate", command=self.calculate_geometry).pack(pady=10)
            
            self.geometry_params = {
                "Area of Circle": ["Radius"],
                "Circumference of Circle": ["Radius"],
                "Area of Rectangle": ["Length", "Width"],
                "Perimeter of Rectangle": ["Length", "Width"],
                "Slope": ["x1", "y1", "x2", "y2"],
                "Pythagorean Theorem": ["Side A", "Side B"],
                "Area of Triangle": ["Base", "Height"],
                "Volume of Sphere": ["Radius"],
                "Surface Area of Sphere": ["Radius"],
                "Volume of Cylinder": ["Radius", "Height"],
                "Surface Area of Cylinder": ["Radius", "Height"],
                "Area of Ellipse": ["Axis a", "Axis b"],
                "Area of Regular Polygon": ["Number of Sides", "Side Length"],
                "Perimeter of Regular Polygon": ["Number of Sides", "Side Length"],
                "Volume of Cube": ["Side"],
                "Surface Area of Cube": ["Side"],
                "Volume of Cone": ["Radius", "Height"],
                "Surface Area of Cone": ["Radius", "Height"],
                "Volume of Rectangular Prism": ["Length", "Width", "Height"],
                "Surface Area of Rectangular Prism": ["Length", "Width", "Height"],
                "Circumference of Ellipse": ["Axis a", "Axis b"]
            }
            self.geo_entries = []
        
        def update_geometry_inputs(self, event=None):
            # Clear current input widgets
            for widget in self.geo_input_frame.winfo_children():
                widget.destroy()
            self.geo_entries.clear()
            calc_type = self.geo_calc_type.get()
            if calc_type in self.geometry_params:
                for param in self.geometry_params[calc_type]:
                    frame = ttk.Frame(self.geo_input_frame)
                    frame.pack(fill="x", pady=2)
                    ttk.Label(frame, text=param + ": ", width=25).pack(side="left")
                    entry = ttk.Entry(frame)
                    entry.pack(side="left", fill="x", expand=True)
                    self.geo_entries.append(entry)
        
        def calculate_geometry(self):
            try:
                values = [float(e.get()) for e in self.geo_entries]
                calc_type = self.geo_calc_type.get()
                result = None
                if calc_type == "Area of Circle":
                    result = math.pi * values[0] ** 2
                elif calc_type == "Circumference of Circle":
                    result = 2 * math.pi * values[0]
                elif calc_type == "Area of Rectangle":
                    result = values[0] * values[1]
                elif calc_type == "Perimeter of Rectangle":
                    result = 2 * (values[0] + values[1])
                elif calc_type == "Slope":
                    result = (values[3] - values[1]) / (values[2] - values[0])
                elif calc_type == "Pythagorean Theorem":
                    result = math.sqrt(values[0] ** 2 + values[1] ** 2)
                elif calc_type == "Area of Triangle":
                    result = 0.5 * values[0] * values[1]
                elif calc_type == "Volume of Sphere":
                    result = (4/3) * math.pi * values[0] ** 3
                elif calc_type == "Surface Area of Sphere":
                    result = 4 * math.pi * values[0] ** 2
                elif calc_type == "Volume of Cylinder":
                    result = math.pi * values[0] ** 2 * values[1]
                elif calc_type == "Surface Area of Cylinder":
                    result = 2 * math.pi * values[0] * (values[0] + values[1])
                elif calc_type == "Area of Ellipse":
                    result = math.pi * values[0] * values[1]
                elif calc_type == "Area of Regular Polygon":
                    n, s = values[0], values[1]
                    result = (n * s**2) / (4 * math.tan(math.pi/n))
                elif calc_type == "Perimeter of Regular Polygon":
                    n, s = values[0], values[1]
                    result = n * s
                elif calc_type == "Volume of Cube":
                    result = values[0] ** 3
                elif calc_type == "Surface Area of Cube":
                    result = 6 * values[0] ** 2
                elif calc_type == "Volume of Cone":
                    result = (1/3) * math.pi * values[0] ** 2 * values[1]
                elif calc_type == "Surface Area of Cone":
                    r, h = values[0], values[1]
                    result = math.pi * r * (r + math.sqrt(r**2 + h**2))
                elif calc_type == "Volume of Rectangular Prism":
                    result = values[0] * values[1] * values[2]
                elif calc_type == "Surface Area of Rectangular Prism":
                    l, w, h = values[0], values[1], values[2]
                    result = 2 * (l*w + l*h + w*h)
                elif calc_type == "Circumference of Ellipse":
                    a, b = values[0], values[1]
                    result = math.pi * (3*(a+b) - math.sqrt((3*a+b)*(a+3*b)))
                unit = self.geo_unit.get()
                if result is not None:
                    self.geo_result_label.config(text=f"Result: {result:.2f} {unit}")
                else:
                    self.geo_result_label.config(text="Result: Invalid Calculation")
            except Exception:
                self.geo_result_label.config(text="Error in Calculation")
        
        # ----------------- Financial Calculator Tab -----------------
        def create_financial_tab(self):
            self.financial_frame = ttk.Frame(self.notebook)
            self.notebook.add(self.financial_frame, text="Financial")
            
            header = ttk.Label(self.financial_frame, text="Financial Calculator", style="Header.TLabel")
            header.pack(pady=10)
            
            self.fin_calc_type = tk.StringVar()
            fin_options = [
                "Simple Interest", "Compound Interest", "Loan Payment", 
                "Future Value of Lump Sum", "Present Value", 
                "Future Value of Annuity", "Present Value of Annuity",
                "Effective Annual Rate", "Continuous Compound Interest",
                "Straight-Line Depreciation",
                "Markup Percentage", "Discount Percentage", 
                "Profit Margin", "Break-Even Point", "Payback Period"
            ]
            ttk.Label(self.financial_frame, text="Select Calculation:").pack(pady=5)
            self.fin_combobox = ttk.Combobox(self.financial_frame, textvariable=self.fin_calc_type, values=fin_options, state="readonly")
            self.fin_combobox.pack(pady=5)
            self.fin_combobox.bind("<<ComboboxSelected>>", self.update_financial_inputs)
            
            self.fin_input_frame = ttk.Frame(self.financial_frame)
            self.fin_input_frame.pack(pady=10, fill="x", padx=20)
            
            # Radio group for currency selection
            self.fin_currency = tk.StringVar(value="USD")
            currency_frame = ttk.Frame(self.financial_frame)
            currency_frame.pack(pady=5)
            ttk.Label(currency_frame, text="Currency:").pack(side="left", padx=5)
            for cur in ["USD", "EUR", "GBP"]:
                ttk.Radiobutton(currency_frame, text=cur, variable=self.fin_currency, value=cur).pack(side="left", padx=5)
            
            self.fin_result_label = ttk.Label(self.financial_frame, text="Result: ", font=("Arial", 14, "bold"))
            self.fin_result_label.pack(pady=10)
            
            ttk.Button(self.financial_frame, text="Calculate", command=self.calculate_financial).pack(pady=10)
            
            self.financial_params = {
                "Simple Interest": ["Principal", "Rate (%)", "Time (Years)"],
                "Compound Interest": ["Principal", "Rate (%)", "Time (Years)", "Compounds per Year"],
                "Loan Payment": ["Principal", "Annual Interest Rate (%)", "Term (Years)"],
                "Future Value of Lump Sum": ["Principal", "Rate (%)", "Time (Years)"],
                "Present Value": ["Future Value", "Rate (%)", "Time (Years)"],
                "Future Value of Annuity": ["Payment", "Rate (%)", "Number of Periods"],
                "Present Value of Annuity": ["Payment", "Rate (%)", "Number of Periods"],
                "Effective Annual Rate": ["Nominal Rate (%)", "Compounds per Year"],
                "Continuous Compound Interest": ["Principal", "Rate (%)", "Time (Years)"],
                "Straight-Line Depreciation": ["Initial Value", "Salvage Value", "Useful Life (Years)"],
                "Markup Percentage": ["Cost", "Selling Price"],
                "Discount Percentage": ["Original Price", "Sale Price"],
                "Profit Margin": ["Profit", "Revenue"],
                "Break-Even Point": ["Fixed Costs", "Unit Price", "Unit Variable Cost"],
                "Payback Period": ["Investment", "Annual Cash Inflow"]
            }
            self.fin_entries = []
        
        def update_financial_inputs(self, event=None):
            for widget in self.fin_input_frame.winfo_children():
                widget.destroy()
            self.fin_entries.clear()
            calc_type = self.fin_calc_type.get()
            if calc_type in self.financial_params:
                for param in self.financial_params[calc_type]:
                    frame = ttk.Frame(self.fin_input_frame)
                    frame.pack(fill="x", pady=2)
                    ttk.Label(frame, text=param + ": ", width=30).pack(side="left")
                    entry = ttk.Entry(frame)
                    entry.pack(side="left", fill="x", expand=True)
                    self.fin_entries.append(entry)
        
        def calculate_financial(self):
            try:
                values = [float(e.get()) for e in self.fin_entries]
                calc_type = self.fin_calc_type.get()
                result = None
                if calc_type == "Simple Interest":
                    result = (values[0] * values[1] * values[2]) / 100
                elif calc_type == "Compound Interest":
                    result = values[0] * (1 + (values[1] / (100 * values[3]))) ** (values[3] * values[2])
                elif calc_type == "Loan Payment":
                    r = values[1] / (12 * 100)
                    n = values[2] * 12
                    result = (values[0] * r * (1 + r) ** n) / ((1 + r) ** n - 1)
                elif calc_type == "Future Value of Lump Sum":
                    result = values[0] * ((1 + values[1] / 100) ** values[2])
                elif calc_type == "Present Value":
                    result = values[0] / ((1 + values[1] / 100) ** values[2])
                elif calc_type == "Future Value of Annuity":
                    result = values[0] * (((1 + values[1] / 100) ** values[2] - 1) / (values[1] / 100))
                elif calc_type == "Present Value of Annuity":
                    result = values[0] * (1 - 1 / ((1 + values[1] / 100) ** values[2])) / (values[1] / 100)
                elif calc_type == "Effective Annual Rate":
                    result = ((1 + values[0] / (100 * values[1])) ** values[1] - 1) * 100
                elif calc_type == "Continuous Compound Interest":
                    result = values[0] * math.exp(values[1] / 100 * values[2])
                elif calc_type == "Straight-Line Depreciation":
                    result = (values[0] - values[1]) / values[2]
                elif calc_type == "Markup Percentage":
                    result = ((values[1] - values[0]) / values[0]) * 100
                elif calc_type == "Discount Percentage":
                    result = ((values[0] - values[1]) / values[0]) * 100
                elif calc_type == "Profit Margin":
                    result = (values[0] / values[1]) * 100
                elif calc_type == "Break-Even Point":
                    result = values[0] / (values[1] - values[2])
                elif calc_type == "Payback Period":
                    result = values[0] / values[1]
                if result is not None:
                    self.fin_result_label.config(text=f"Result: {result:.2f} {self.fin_currency.get()}")
                else:
                    self.fin_result_label.config(text="Result: Invalid Calculation")
            except Exception:
                self.fin_result_label.config(text="Error in Calculation")
        
        # ----------------- Algebra Calculator Tab -----------------
        def create_algebra_tab(self):
            self.algebra_frame = ttk.Frame(self.notebook)
            self.notebook.add(self.algebra_frame, text="Algebra")
            
            header = ttk.Label(self.algebra_frame, text="Algebra Calculator", style="Header.TLabel")
            header.pack(pady=10)
            
            # Combobox for selecting algebra calculation type
            self.alg_calc_type = tk.StringVar()
            alg_options = [
                "Quadratic Equation", "Linear Equation", "2x2 Linear System",
                "Exponential Equation", "Logarithmic Equation", "Absolute Value Equation",
                "Rational Equation", "Proportion Equation", "Cubic Equation",
                "Combined Linear Equation", "Inverse Rational Equation", "Fraction Equation",
                "Quadratic Variation", "Log-Linear Equation", "Direct Variation"
            ]
            ttk.Label(self.algebra_frame, text="Select Calculation:").pack(pady=5)
            self.alg_combobox = ttk.Combobox(self.algebra_frame, textvariable=self.alg_calc_type, values=alg_options, state="readonly")
            self.alg_combobox.pack(pady=5)
            self.alg_combobox.bind("<<ComboboxSelected>>", self.update_algebra_inputs)
            
            self.alg_input_frame = ttk.Frame(self.algebra_frame)
            self.alg_input_frame.pack(pady=10, fill="x", padx=20)
            
            self.alg_result_label = ttk.Label(self.algebra_frame, text="Result: ", font=("Arial", 14, "bold"))
            self.alg_result_label.pack(pady=10)
            
            ttk.Button(self.algebra_frame, text="Calculate", command=self.calculate_algebra).pack(pady=10)
            
            self.algebra_params = {
                "Quadratic Equation": ["a", "b", "c"],
                "Linear Equation": ["a", "b"],
                "2x2 Linear System": ["a1", "b1", "c1", "a2", "b2", "c2"],
                "Exponential Equation": ["a", "b", "c"],           # a * exp(b*x) = c  -> x = ln(c/a)/b
                "Logarithmic Equation": ["a", "b"],                 # log_a(x) = b  -> x = a**b (a>0, a≠1)
                "Absolute Value Equation": ["a", "b"],              # |x - a| = b  -> x = a+b and a-b
                "Rational Equation": ["a"],                         # 1/x = a  -> x = 1/a
                "Proportion Equation": ["a", "b", "c"],             # a/x = b/c  -> x = a*c/b
                "Cubic Equation": ["a"],                            # x^3 = a  -> cube root of a
                "Combined Linear Equation": ["a", "b", "c"],        # a*x + b*x = c  -> x = c/(a+b)
                "Inverse Rational Equation": ["a", "b", "c"],       # a/(x+b)=c  -> x = a/c - b
                "Fraction Equation": ["a", "b", "c"],               # a*x/(b+x)=c  -> x = (c*b)/(a-c) if a != c
                "Quadratic Variation": ["a", "c"],                # a*x^2 = c  -> x = ±sqrt(c/a)
                "Log-Linear Equation": ["a", "b"],                  # a*log(x)=b  -> x = exp(b/a)
                "Direct Variation": ["a", "b"]                      # a*x = b  -> x = b/a
            }
            self.alg_entries = []
        
        def update_algebra_inputs(self, event=None):
            for widget in self.alg_input_frame.winfo_children():
                widget.destroy()
            self.alg_entries.clear()
            calc_type = self.alg_calc_type.get()
            if calc_type in self.algebra_params:
                for param in self.algebra_params[calc_type]:
                    frame = ttk.Frame(self.alg_input_frame)
                    frame.pack(fill="x", pady=2)
                    ttk.Label(frame, text=param + ": ", width=15).pack(side="left")
                    entry = ttk.Entry(frame)
                    entry.pack(side="left", fill="x", expand=True)
                    self.alg_entries.append(entry)
        
        def calculate_algebra(self):
            try:
                calc_type = self.alg_calc_type.get()
                if calc_type == "Quadratic Equation":
                    a = float(self.alg_entries[0].get())
                    b = float(self.alg_entries[1].get())
                    c = float(self.alg_entries[2].get())
                    discriminant = b**2 - 4 * a * c
                    if discriminant < 0:
                        self.alg_result_label.config(text="Result: Complex roots")
                    else:
                        root1 = (-b + math.sqrt(discriminant)) / (2 * a)
                        root2 = (-b - math.sqrt(discriminant)) / (2 * a)
                        self.alg_result_label.config(text=f"Results: {root1:.2f}, {root2:.2f}")
                elif calc_type == "Linear Equation":
                    a = float(self.alg_entries[0].get())
                    b = float(self.alg_entries[1].get())
                    if a == 0:
                        if b == 0:
                            self.alg_result_label.config(text="Result: Infinite solutions")
                        else:
                            self.alg_result_label.config(text="Result: No solution")
                    else:
                        x = -b / a
                        self.alg_result_label.config(text=f"Result: x = {x:.2f}")
                elif calc_type == "2x2 Linear System":
                    a1 = float(self.alg_entries[0].get())
                    b1 = float(self.alg_entries[1].get())
                    c1 = float(self.alg_entries[2].get())
                    a2 = float(self.alg_entries[3].get())
                    b2 = float(self.alg_entries[4].get())
                    c2 = float(self.alg_entries[5].get())
                    denom = a1 * b2 - a2 * b1
                    if denom == 0:
                        self.alg_result_label.config(text="Result: No unique solution")
                    else:
                        x = (c1 * b2 - b1 * c2) / denom
                        y = (a1 * c2 - c1 * a2) / denom
                        self.alg_result_label.config(text=f"Results: x = {x:.2f}, y = {y:.2f}")
                elif calc_type == "Exponential Equation":
                    a = float(self.alg_entries[0].get())
                    b = float(self.alg_entries[1].get())
                    c = float(self.alg_entries[2].get())
                    if a <= 0 or c <= 0 or b == 0:
                        self.alg_result_label.config(text="Invalid parameters")
                    else:
                        x = math.log(c/a) / b
                        self.alg_result_label.config(text=f"Result: x = {x:.2f}")
                elif calc_type == "Logarithmic Equation":
                    a = float(self.alg_entries[0].get())
                    b = float(self.alg_entries[1].get())
                    if a <= 0 or a == 1:
                        self.alg_result_label.config(text="Invalid base")
                    else:
                        x = a ** b
                        self.alg_result_label.config(text=f"Result: x = {x:.2f}")
                elif calc_type == "Absolute Value Equation":
                    a = float(self.alg_entries[0].get())
                    b = float(self.alg_entries[1].get())
                    if b < 0:
                        self.alg_result_label.config(text="Invalid: b must be >= 0")
                    else:
                        sol1 = a + b
                        sol2 = a - b
                        self.alg_result_label.config(text=f"Results: x = {sol1:.2f}, {sol2:.2f}")
                elif calc_type == "Rational Equation":
                    a = float(self.alg_entries[0].get())
                    if a == 0:
                        self.alg_result_label.config(text="No solution (a=0)")
                    else:
                        x = 1 / a
                        self.alg_result_label.config(text=f"Result: x = {x:.2f}")
                elif calc_type == "Proportion Equation":
                    a = float(self.alg_entries[0].get())
                    b = float(self.alg_entries[1].get())
                    c = float(self.alg_entries[2].get())
                    if b == 0:
                        self.alg_result_label.config(text="Invalid: b cannot be 0")
                    else:
                        x = a * c / b
                        self.alg_result_label.config(text=f"Result: x = {x:.2f}")
                elif calc_type == "Cubic Equation":
                    a = float(self.alg_entries[0].get())
                    x = math.copysign(abs(a)**(1/3), a)
                    self.alg_result_label.config(text=f"Result: x = {x:.2f}")
                elif calc_type == "Combined Linear Equation":
                    a = float(self.alg_entries[0].get())
                    b = float(self.alg_entries[1].get())
                    c = float(self.alg_entries[2].get())
                    if (a + b) == 0:
                        self.alg_result_label.config(text="No solution")
                    else:
                        x = c / (a + b)
                        self.alg_result_label.config(text=f"Result: x = {x:.2f}")
                elif calc_type == "Inverse Rational Equation":
                    a = float(self.alg_entries[0].get())
                    b = float(self.alg_entries[1].get())
                    c = float(self.alg_entries[2].get())
                    if c == 0:
                        self.alg_result_label.config(text="Invalid: c cannot be 0")
                    else:
                        x = a / c - b
                        self.alg_result_label.config(text=f"Result: x = {x:.2f}")
                elif calc_type == "Fraction Equation":
                    a = float(self.alg_entries[0].get())
                    b = float(self.alg_entries[1].get())
                    c = float(self.alg_entries[2].get())
                    if a == c:
                        self.alg_result_label.config(text="No unique solution (a=c)")
                    else:
                        x = (c * b) / (a - c)
                        self.alg_result_label.config(text=f"Result: x = {x:.2f}")
                elif calc_type == "Quadratic Variation":
                    a = float(self.alg_entries[0].get())
                    c = float(self.alg_entries[1].get())
                    if a == 0:
                        self.alg_result_label.config(text="Invalid: a cannot be 0")
                    else:
                        ratio = c/a
                        if ratio < 0:
                            self.alg_result_label.config(text="No real solutions")
                        else:
                            sol1 = math.sqrt(ratio)
                            sol2 = -math.sqrt(ratio)
                            self.alg_result_label.config(text=f"Results: x = {sol1:.2f}, {sol2:.2f}")
                elif calc_type == "Log-Linear Equation":
                    a = float(self.alg_entries[0].get())
                    b = float(self.alg_entries[1].get())
                    if a == 0:
                        self.alg_result_label.config(text="Invalid: a cannot be 0")
                    else:
                        x = math.exp(b/a)
                        self.alg_result_label.config(text=f"Result: x = {x:.2f}")
                elif calc_type == "Direct Variation":
                    a = float(self.alg_entries[0].get())
                    b = float(self.alg_entries[1].get())
                    if a == 0:
                        self.alg_result_label.config(text="Invalid: a cannot be 0")
                    else:
                        x = b / a
                        self.alg_result_label.config(text=f"Result: x = {x:.2f}")
                else:
                    self.alg_result_label.config(text="Unknown Calculation")
            except Exception:
                self.alg_result_label.config(text="Error in Calculation")

    
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
run()