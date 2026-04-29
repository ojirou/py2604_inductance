# import tkinter as tk
from tkinter import font
import math

# --- 定数 ---
MU0 = 4 * math.pi * 1e-7  # 真空の透磁率 [H/m]

# --- 共通UI関数 ---

def ask_float(prompt):
    root = tk.Tk()
    root.withdraw()
    dialog = tk.Toplevel(root)
    dialog.title("入力")
    custom_font = font.Font(size=12)

    label = tk.Label(dialog, text=prompt, font=custom_font)
    label.pack(padx=20, pady=10)

    entry_var = tk.StringVar()
    entry = tk.Entry(dialog, textvariable=entry_var, font=custom_font)
    entry.pack(padx=20, pady=10)
    entry.focus_set()

    result = {"value": None}

    def on_submit():
        try:
            result["value"] = float(entry_var.get())
            dialog.destroy()
        except ValueError:
            pass

    submit_button = tk.Button(dialog, text="OK", command=on_submit, font=custom_font)
    submit_button.pack(pady=20)
    dialog.bind('<Return>', lambda e: on_submit())

    dialog.wait_window(dialog)
    root.destroy()
    return result["value"]

def show_custom_messagebox(title, message, font_size=12):
    root = tk.Tk()
    root.withdraw()
    messagebox = tk.Toplevel(root)
    messagebox.title(title)
    custom_font = font.Font(size=font_size)

    label = tk.Label(messagebox, text=message, font=custom_font, justify=tk.LEFT)
    label.pack(padx=20, pady=20)

    def on_ok():
        messagebox.destroy()

    ok_button = tk.Button(messagebox, text="OK", command=on_ok, font=custom_font)
    ok_button.pack(pady=10)

    messagebox.wait_window(messagebox)
    root.destroy()

# --- 各インダクタンス計算関数 ---

def calc_circle_loop():
    """1. 円形ループのインダクタンス"""
    R_mm = ask_float("ループ半径 R (mm) を入力してください:")
    if R_mm is None: return
    a_mm = ask_float("導線半径 a (mm) を入力してください:")
    if a_mm is None: return
    
    L_uh = R_mm * MU0 * (math.log(8 * R_mm / a_mm) - 2) *1e3
        
    show_custom_messagebox("結果", f"円形ループのインダクタンス:\n{L_uh:.4f} [μH]\n({L_uh*1e3:.4f} [nH])")

def calc_rect_wire_simple():
    """2. 矩形導線 (簡易式)"""
    l_cm = ask_float("導線の長さ l (cm) を入力してください:")
    if l_cm is None: return
    w_cm = ask_float("導線の幅 w (cm) を入力してください:")
    if w_cm is None: return
    
    # L = 0.002 * l * ln(2l/w) [uH]
    L_uh = 0.002 * l_cm * math.log(2 * l_cm / w_cm)
    
    show_custom_messagebox("結果", f"矩形導線(簡易)のインダクタンス:\n{L_uh:.4f} [μH]\n({L_uh*1e3:.4f} [nH])")

def calc_rect_wire_detail():
    """3. 矩形導線 (詳細式)"""
    l_cm = ask_float("導線の長さ l (cm) を入力してください:")
    if l_cm is None: return
    w_cm = ask_float("導線の幅 w (cm) を入力してください:")
    if w_cm is None: return
    t_cm = ask_float("導線の厚さ t (cm) を入力してください:")
    if t_cm is None: return
    
    # L = 0.002 * l * [ln(2l/(w+t)) + 0.5 + 0.2235 * ((w+t)/l)] [uH]
    L_uh = 0.002 * l_cm * (math.log(2 * l_cm / (w_cm + t_cm)) + 0.5 + 0.2235 * ((w_cm + t_cm) / l_cm))
    
    show_custom_messagebox("結果", f"矩形導線(詳細)のインダクタンス:\n{L_uh:.4f} [μH]\n({L_uh*1e3:.4f} [nH])")

def calc_cylindrical_wire():
    """4. 円筒導線"""
    l_cm = ask_float("導線の長さ l (cm) を入力してください:")
    if l_cm is None: return
    r_cm = ask_float("導線の半径 r (cm) を入力してください:")
    if r_cm is None: return
    
    L_h = (MU0 / (2 * math.pi)) * l_cm * (math.log(2 * l_cm / r_cm) - 1 + (r_cm / l_cm))
    
    show_custom_messagebox("結果", f"円筒導線のインダクタンス:\n{L_h*1e6:.4f} [μH]\n({L_h*1e9:.4f} [nH])")

# --- メインメニュー ---

def main_menu():
    while True:
        root = tk.Tk()
        root.title("インダクタンス計算")
        
        custom_font = font.Font(size=12)
        title_font = font.Font(size=14, weight="bold")

        tk.Label(root, text="計算する種類を選択してください", font=title_font).pack(padx=30, pady=20)

        choice = {"val": None}
        def set_choice(v):
            choice["val"] = v
            root.destroy()

        btn_params = {"font": custom_font, "width": 35, "pady": 5}
        
        tk.Button(root, text="1. 円形ループ (R, a: mm)", command=lambda: set_choice(1), **btn_params).pack(pady=2)
        tk.Button(root, text="2. 矩形導線 簡易 (l, w: cm)", command=lambda: set_choice(2), **btn_params).pack(pady=2)
        tk.Button(root, text="3. 矩形導線 詳細 (l, w, t: cm)", command=lambda: set_choice(3), **btn_params).pack(pady=2)
        tk.Button(root, text="4. 円形導線 (l, r: cm)", command=lambda: set_choice(4), **btn_params).pack(pady=2)
        tk.Button(root, text="終了", command=lambda: set_choice(0), **btn_params, bg="#ffcccc").pack(pady=20)

        root.mainloop()

        if choice["val"] == 1: calc_circle_loop()
        elif choice["val"] == 2: calc_rect_wire_simple()
        elif choice["val"] == 3: calc_rect_wire_detail()
        elif choice["val"] == 4: calc_cylindrical_wire()
        elif choice["val"] == 0 or choice["val"] is None:
            break

if __name__ == "__main__":
    main_menu()