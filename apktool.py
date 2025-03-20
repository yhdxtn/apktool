import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

# 配置路径
APKTOOL_PATH = "D:\\Program Files (x86)\\java\\apktool_2.11.1.jar"
SIGNER_PATH = "D:\\Program Files (x86)\\java\\uber-apk-signer-1.3.0.jar"
JAVA_PATH = "java"  # 确保 JAVA 环境变量已配置

# 创建图形界面
class APKToolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("APK 反编译/回编译/签名工具")
        self.root.geometry("500x400")
        
        self.decompile_dir = tk.StringVar()
        self.recompile_name = tk.StringVar()
        self.signed_name = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="选择 APK 文件").grid(row=0, column=0, padx=10, pady=10)
        self.apk_path_entry = tk.Entry(self.root, width=40)
        self.apk_path_entry.grid(row=0, column=1)
        tk.Button(self.root, text="浏览", command=self.browse_apk).grid(row=0, column=2)
        
        tk.Label(self.root, text="反编译输出目录").grid(row=1, column=0, padx=10, pady=10)
        self.decompile_dir_entry = tk.Entry(self.root, textvariable=self.decompile_dir, width=40)
        self.decompile_dir_entry.grid(row=1, column=1)
        tk.Button(self.root, text="选择目录", command=self.choose_decompile_dir).grid(row=1, column=2)

        tk.Label(self.root, text="回编译后的 APK 名称").grid(row=2, column=0, padx=10, pady=10)
        self.recompile_name_entry = tk.Entry(self.root, textvariable=self.recompile_name, width=40)
        self.recompile_name_entry.grid(row=2, column=1)
        
        tk.Label(self.root, text="签名后的 APK 名称").grid(row=3, column=0, padx=10, pady=10)
        self.signed_name_entry = tk.Entry(self.root, textvariable=self.signed_name, width=40)
        self.signed_name_entry.grid(row=3, column=1)
        
        tk.Button(self.root, text="反编译 APK", command=self.decompile_apk).grid(row=4, column=0, padx=10, pady=10)
        tk.Button(self.root, text="回编译 APK", command=self.recompile_apk).grid(row=4, column=1, padx=10, pady=10)
        tk.Button(self.root, text="签名 APK", command=self.sign_apk).grid(row=4, column=2, padx=10, pady=10)

    def browse_apk(self):
        apk_file = filedialog.askopenfilename(filetypes=[("APK Files", "*.apk")])
        if apk_file:
            self.apk_path_entry.delete(0, tk.END)
            self.apk_path_entry.insert(0, apk_file)

    def choose_decompile_dir(self):
        dir_name = filedialog.askdirectory()
        if dir_name:
            self.decompile_dir.set(dir_name)

    def decompile_apk(self):
        apk_path = self.apk_path_entry.get()
        output_dir = self.decompile_dir.get()

        if not apk_path or not output_dir:
            messagebox.showerror("错误", "请确保已选择 APK 文件和输出目录")
            return
        
        command = [
            JAVA_PATH, "-jar", APKTOOL_PATH, "d", apk_path, "-o", output_dir
        ]
        try:
            subprocess.run(command, check=True)
            messagebox.showinfo("成功", "APK 反编译成功")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("错误", f"反编译失败: {e}")

    def recompile_apk(self):
        decompile_dir = self.decompile_dir.get()
        output_apk = self.recompile_name.get() or "recompiled.apk"

        if not decompile_dir:
            messagebox.showerror("错误", "请确保已选择反编译目录")
            return
        
        command = [
            JAVA_PATH, "-jar", APKTOOL_PATH, "b", decompile_dir, "-o", output_apk
        ]
        try:
            subprocess.run(command, check=True)
            messagebox.showinfo("成功", f"APK 回编译成功: {output_apk}")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("错误", f"回编译失败: {e}")

    def sign_apk(self):
        apk_path = self.apk_path_entry.get()
        signed_apk_name = self.signed_name.get() or "signed.apk"

        if not apk_path:
            messagebox.showerror("错误", "请确保已选择 APK 文件")
            return

        command = [
            JAVA_PATH, "-jar", SIGNER_PATH, "-a", apk_path, "-o", signed_apk_name
        ]
        try:
            subprocess.run(command, check=True)
            messagebox.showinfo("成功", f"APK 签名成功: {signed_apk_name}")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("错误", f"签名失败: {e}")

# 启动应用
if __name__ == "__main__":
    root = tk.Tk()
    app = APKToolApp(root)
    root.mainloop()
