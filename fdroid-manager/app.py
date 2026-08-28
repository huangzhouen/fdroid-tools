#!/usr/bin/env python3
import os, sys, json, hashlib, subprocess, threading, webbrowser
from pathlib import Path
from datetime import datetime

try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox, scrolledtext
except ImportError:
    sys.exit(1)

BASE_DIR = Path(__file__).parent
APP_DIR = BASE_DIR / 'apps'
REPO_DIR = BASE_DIR / 'repo'

class App:
    def __init__(self, root):
        self.root = root
        self.root.title('F-Droid 仓库管理器')
        self.root.geometry('800x600')
        self.server = None
        self.create_ui()
        APP_DIR.mkdir(exist_ok=True)
        REPO_DIR.mkdir(exist_ok=True)
        self.refresh()

    def create_ui(self):
        main = ttk.Frame(self.root, padding='10')
        main.pack(fill=tk.BOTH, expand=True)

        cfg = ttk.LabelFrame(main, text='仓库配置', padding='10')
        cfg.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(cfg, text='名称:').grid(row=0, column=0)
        self.name_var = tk.StringVar(value='我的 F-Droid 仓库')
        ttk.Entry(cfg, textvariable=self.name_var, width=30).grid(row=0, column=1, padx=5)
        ttk.Label(cfg, text='端口:').grid(row=0, column=2, padx=(10, 0))
        self.port_var = tk.StringVar(value='8000')
        ttk.Entry(cfg, textvariable=self.port_var, width=10).grid(row=0, column=3, padx=5)
        ttk.Button(cfg, text='保存', command=self.save).grid(row=0, column=4, padx=10)

        btn = ttk.Frame(main)
        btn.pack(fill=tk.X, pady=10)
        self.start_btn = ttk.Button(btn, text='启动', command=self.start)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        ttk.Button(btn, text='停止', command=self.stop, state=tk.DISABLED).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn, text='网页', command=self.web).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn, text='刷新', command=self.refresh).pack(side=tk.LEFT, padx=5)

        lst = ttk.LabelFrame(main, text='应用列表', padding='10')
        lst.pack(fill=tk.BOTH, expand=True, pady=10)
        self.tree = ttk.Treeview(lst, columns=('name','size','date'), show='headings', height=10)
        self.tree.heading('name', text='名称')
        self.tree.heading('size', text='大小')
        self.tree.heading('date', text='时间')
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        ttk.Scrollbar(lst, orient=tk.VERTICAL, command=self.tree.yview).pack(side=tk.RIGHT, fill=tk.Y)

        bottom = ttk.Frame(main)
        bottom.pack(fill=tk.X)
        ttk.Button(bottom, text='添加 APK', command=self.add).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom, text='删除', command=self.delete).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom, text='清空', command=self.clear).pack(side=tk.LEFT, padx=5)

        log = ttk.LabelFrame(main, text='日志', padding='10')
        log.pack(fill=tk.BOTH, expand=True, pady=10)
        self.log_text = scrolledtext.ScrolledText(log, height=5)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        self.status = tk.StringVar(value='就绪')
        ttk.Label(main, textvariable=self.status, relief=tk.SUNKEN).pack(fill=tk.X)

    def log(self, msg):
        ts = datetime.now().strftime('%H:%M:%S')
        line = '[' + ts + '] ' + str(msg)
        self.log_text.insert(tk.END, line + chr(10))
        self.log_text.see(tk.END)

    def save(self):
        self.log('配置已保存')

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        if APP_DIR.exists():
            apps = sorted([f for f in APP_DIR.glob('*.apk')])
            for app in apps:
                size = app.stat().st_size
                if size > 1024*1024:
                    s = str(round(size/1024/1024, 2)) + ' MB'
                else:
                    s = str(round(size/1024, 1)) + ' KB'
                t = datetime.fromtimestamp(app.stat().st_mtime).strftime('%m-%d %H:%M')
                self.tree.insert('', tk.END, values=(app.stem, s, t))
            self.log('刷新完成: ' + str(len(apps)) + ' 个应用')

    def add(self):
        files = filedialog.askopenfilenames(filetypes=[('APK', '*.apk'), ('所有', '*.*')])
        if files:
            for f in files:
                import shutil
                shutil.copy2(f, APP_DIR / Path(f).name)
                self.log('已添加: ' + Path(f).name)
            self.refresh()

    def delete(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning('提示', '请选择应用')
            return
        if messagebox.askyesno('确认', '删除选中的应用?'):
            for item in sel:
                name = self.tree.item(item, 'values')[0]
                (APP_DIR / (name + '.apk')).unlink(missing_ok=True)
            self.refresh()

    def clear(self):
        if messagebox.askyesno('确认', '清空所有应用?'):
            for f in APP_DIR.glob('*.apk'):
                f.unlink()
            self.refresh()

    def start(self):
        port = self.port_var.get()
        self.server = subprocess.Popen([sys.executable, str(BASE_DIR/'server.py'), port])
        self.start_btn.config(state=tk.DISABLED)
        self.status.set('运行中 (端口 ' + port + ')')
        self.log('服务器已启动')

    def stop(self):
        if self.server:
            self.server.terminate()
            self.server = None
            self.start_btn.config(state=tk.NORMAL)
            self.status.set('已停止')

    def web(self):
        import webbrowser
        url = 'http://localhost:' + self.port_var.get()
        webbrowser.open(url)

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
