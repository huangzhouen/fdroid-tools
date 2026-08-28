#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, json, hashlib, subprocess, threading, webbrowser, shutil
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
ICON_FILE = BASE_DIR / 'icon.png'

class App:
    def __init__(self, root):
        self.root = root
        self.root.title('F-Droid 仓库管理器')
        self.root.geometry('900x700')
        self.server = None
        self.create_ui()
        APP_DIR.mkdir(exist_ok=True)
        REPO_DIR.mkdir(exist_ok=True)
        self.refresh()

    def create_ui(self):
        main = ttk.Frame(self.root, padding='10')
        main.pack(fill=tk.BOTH, expand=True)

        # 仓库配置
        cfg = ttk.LabelFrame(main, text='仓库配置', padding='10')
        cfg.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(cfg, text='名称:').grid(row=0, column=0, sticky=tk.W)
        self.name_var = tk.StringVar(value='我的 F-Droid 仓库')
        ttk.Entry(cfg, textvariable=self.name_var, width=30).grid(row=0, column=1, padx=5)
        ttk.Label(cfg, text='端口:').grid(row=0, column=2, padx=(20, 0))
        self.port_var = tk.StringVar(value='8000')
        ttk.Entry(cfg, textvariable=self.port_var, width=10).grid(row=0, column=3, padx=5)
        ttk.Button(cfg, text='保存', command=self.save).grid(row=0, column=4, padx=10)

        # 图标配置
        icon_frame = ttk.LabelFrame(main, text='仓库图标', padding='10')
        icon_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(icon_frame, text='当前图标:').grid(row=0, column=0, sticky=tk.W)
        self.icon_label = ttk.Label(icon_frame, text='无图标')
        self.icon_label.grid(row=0, column=1, padx=5)
        ttk.Button(icon_frame, text='浏览图标', command=self.select_icon).grid(row=0, column=2, padx=5)
        ttk.Button(icon_frame, text='删除图标', command=self.delete_icon).grid(row=0, column=3, padx=5)

        # 控制按钮
        btn = ttk.Frame(main)
        btn.pack(fill=tk.X, pady=10)
        self.start_btn = ttk.Button(btn, text='启动服务器', command=self.start)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        ttk.Button(btn, text='停止服务器', command=self.stop, state=tk.DISABLED).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn, text='打开网页', command=self.web).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn, text='刷新列表', command=self.refresh).pack(side=tk.LEFT, padx=5)

        # 应用列表
        lst = ttk.LabelFrame(main, text='应用列表', padding='10')
        lst.pack(fill=tk.BOTH, expand=True, pady=10)
        self.tree = ttk.Treeview(lst, columns=('name','size','date'), show='headings', height=10)
        self.tree.heading('name', text='名称')
        self.tree.heading('size', text='大小')
        self.tree.heading('date', text='时间')
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        ttk.Scrollbar(lst, orient=tk.VERTICAL, command=self.tree.yview).pack(side=tk.RIGHT, fill=tk.Y)

        # 底部按钮
        bottom = ttk.Frame(main)
        bottom.pack(fill=tk.X)
        ttk.Button(bottom, text='添加 APK', command=self.add).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom, text='删除选中', command=self.delete).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom, text='清空所有', command=self.clear).pack(side=tk.LEFT, padx=5)

        # 日志
        log = ttk.LabelFrame(main, text='日志', padding='10')
        log.pack(fill=tk.BOTH, expand=True, pady=10)
        self.log_text = scrolledtext.ScrolledText(log, height=5)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        self.status = tk.StringVar(value='就绪')
        ttk.Label(main, textvariable=self.status, relief=tk.SUNKEN).pack(fill=tk.X)

    def log(self, msg):
        ts = datetime.now().strftime('%H:%M:%S')
        self.log_text.insert(tk.END, '[' + ts + '] ' + str(msg) + chr(10))
        self.log_text.see(tk.END)

    def save(self):
        self.log('配置已保存')

    def select_icon(self):
        """选择图标文件"""
        file_path = filedialog.askopenfilename(
            title='选择仓库图标',
            filetypes=[('PNG 图片', '*.png'), ('JPEG 图片', '*.jpg *.jpeg'), ('所有图片', '*.png *.jpg *.jpeg *.ico'), ('所有文件', '*.*')]
        )
        if file_path:
            try:
                shutil.copy2(file_path, ICON_FILE)
                self.log('图标已更新: ' + Path(file_path).name)
                self.icon_label.config(text='OK: ' + Path(file_path).stem)
                self.regenerate_repo()
            except Exception as e:
                messagebox.showerror('错误', '图标保存失败: ' + str(e))
                self.log('图标保存失败: ' + str(e))

    def delete_icon(self):
        """删除图标"""
        if ICON_FILE.exists():
            ICON_FILE.unlink()
            self.log('图标已删除')
            self.icon_label.config(text='无图标')
            self.regenerate_repo()
        else:
            messagebox.showinfo('提示', '当前没有图标')

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        if APP_DIR.exists():
            apps = sorted([f for f in APP_DIR.glob('*.apk')])
            for app in apps:
                size = app.stat().st_size
                s = str(round(size/1024/1024, 2)) + ' MB' if size > 1024*1024 else str(round(size/1024, 1)) + ' KB'
                t = datetime.fromtimestamp(app.stat().st_mtime).strftime('%m-%d %H:%M')
                self.tree.insert('', tk.END, values=(app.stem, s, t))
            self.log('刷新完成: ' + str(len(apps)) + ' 个应用')
        
        # 更新图标显示
        if ICON_FILE.exists():
            self.icon_label.config(text='OK: ' + ICON_FILE.stem)
        else:
            self.icon_label.config(text='无图标')

    def add(self):
        files = filedialog.askopenfilenames(title='选择 APK 文件', filetypes=[('APK 文件', '*.apk'), ('所有文件', '*.*')])
        if files:
            for f in files:
                try:
                    shutil.copy2(f, APP_DIR / Path(f).name)
                    self.log('已添加: ' + Path(f).name)
                except Exception as e:
                    messagebox.showerror('错误', '添加失败: ' + str(e))
            self.refresh()

    def delete(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning('提示', '请先选择应用')
            return
        if messagebox.askyesno('确认', '删除选中的应用?'):
            for item in sel:
                name = self.tree.item(item, 'values')[0]
                (APP_DIR / (name + '.apk')).unlink(missing_ok=True)
                self.log('已删除: ' + name + '.apk')
            self.refresh()

    def clear(self):
        if messagebox.askyesno('确认', '清空所有应用? 此操作不可恢复!'):
            for f in APP_DIR.glob('*.apk'):
                f.unlink()
            self.log('已清空所有应用')
            self.refresh()

    def regenerate_repo(self):
        """重新生成仓库 XML"""
        try:
            import xml.etree.ElementTree as ET
            apps = list(APP_DIR.glob('*.apk'))
            root = ET.Element('repositories')
            root.set('xmlns', 'http://f-droid.org/xml/delivery')
            repo = ET.SubElement(root, 'repo')
            repo.set('name', self.name_var.get())
            repo.set('url', 'http://localhost:' + self.port_var.get())
            
            for app in apps:
                with open(app, 'rb') as f:
                    h = hashlib.sha256(f.read()).hexdigest()
                elem = ET.SubElement(repo, 'app')
                elem.set('package', app.stem)
                elem.set('versionCode', '1')
                elem.set('versionName', '1.0.0')
                elem.set('contentHash', h)
                elem.set('size', str(app.stat().st_size))
            
            tree = ET.ElementTree(root)
            ET.indent(tree, space='  ')
            tree.write(REPO_DIR / 'repos.xml', encoding='utf-8', xml_declaration=True)
            self.log('仓库元数据已更新')
        except Exception as e:
            self.log('生成仓库失败: ' + str(e))

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
            self.log('服务器已停止')

    def web(self):
        import webbrowser
        url = 'http://localhost:' + self.port_var.get()
        webbrowser.open(url)
        self.log('已打开: ' + url)

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()