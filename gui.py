"""
排序算法可视化界面模块

提供了一个基于 tkinter 的图形用户界面，用于演示和比较不同排序算法的性能。
支持实时可视化排序过程，并提供算法执行时间统计。
"""

import time
import tkinter as tk
from tkinter import ttk
import sv_ttk
import darkdetect

from data_generator import generate_data
from sorting_algorithms import (
    bubble_sort, quick_sort, shell_sort,
    heap_sort, radix_sort
)

class SortApp(tk.Tk):
    """
    排序算法演示应用的主窗口类
    
    提供了以下功能：
    - 选择不同的排序算法
    - 可视化排序过程
    - 显示排序时间统计
    - 支持明暗主题切换
    """
    
    def __init__(self):
        """初始化应用窗口和所有UI组件"""
        super().__init__()
        self.title("排序算法对比演示")
        self.geometry("800x600")

        # 根据系统主题设置初始主题
        initial_theme = "dark" if darkdetect.isDark() else "light"
        sv_ttk.set_theme(initial_theme)
        
        # =======================
        # 上方主框架：控制区
        # =======================
        frame_top = ttk.Frame(self, padding=(10, 10, 10, 5))
        frame_top.pack(side=tk.TOP, fill=tk.X)

        # 1. 算法选择下拉框
        self.algorithms = {
            "全部算法": "all",
            "冒泡排序": "bubble",
            "快速排序": "quick",
            "希尔排序": "shell",
            "堆排序": "heap",
            "基数排序": "radix"
        }
        self.algorithm_var = tk.StringVar(value="全部算法")
        self.algorithm_combo = ttk.Combobox(
            frame_top, 
            textvariable=self.algorithm_var,
            values=list(self.algorithms.keys()),
            state="readonly",
            width=12
        )
        self.algorithm_combo.pack(side=tk.LEFT, padx=5)

        # 2. 排序按钮
        self.btn_sort = ttk.Button(frame_top, text="开始排序", command=self.sort_and_time, style="Accent.TButton")
        self.btn_sort.pack(side=tk.LEFT, padx=5)

        # 3. 清空结果按钮
        self.btn_clear = ttk.Button(frame_top, text="清空结果", command=self.clear_results)
        self.btn_clear.pack(side=tk.LEFT, padx=5)

        # 4. 可视化开关
        self.visual_var = tk.BooleanVar(value=False)
        self.chk_visual = ttk.Checkbutton(
            frame_top, 
            text="启用可视化", 
            variable=self.visual_var,
            style="Switch.TCheckbutton"  # 使用开关样式
        )
        self.chk_visual.pack(side=tk.LEFT, padx=10)

        # 添加慢速模式开关
        self.slow_mode_var = tk.BooleanVar(value=False)
        self.chk_slow_mode = ttk.Checkbutton(
            frame_top, 
            text="慢速模式", 
            variable=self.slow_mode_var,
            style="Switch.TCheckbutton"
        )
        self.chk_slow_mode.pack(side=tk.LEFT, padx=10)

        # 5. 主题切换按钮
        self.theme_button = ttk.Button(
            frame_top,
            text="切换主题",
            command=self.toggle_theme,
            style="Secondary.TButton"
        )
        self.theme_button.pack(side=tk.RIGHT, padx=5)

        # =======================
        # 状态显示区
        # =======================
        frame_status = ttk.Frame(self, padding=(10, 0, 10, 5))
        frame_status.pack(side=tk.TOP, fill=tk.X)
        
        self.status_text = tk.StringVar(value="就绪")
        self.status_label = ttk.Label(
            frame_status, 
            textvariable=self.status_text,
            font=("Segoe UI", 10)
        )
        self.status_label.pack(side=tk.LEFT)

        # =======================
        # 中部画布：用于可视化
        # =======================
        frame_canvas = ttk.Frame(self, padding=(10, 5, 10, 5))
        frame_canvas.pack(side=tk.TOP, fill=tk.X)
        
        self.canvas = tk.Canvas(
            frame_canvas, 
            bg="#2b2b2b",  # 深色主题下的背景色
            height=300,
            highlightthickness=0  # 移除边框
        )
        self.canvas.pack(side=tk.TOP, fill=tk.X)

        # =======================
        # 下方文本框：显示结果
        # =======================
        frame_text = ttk.Frame(self, padding=(10, 5, 10, 10))
        frame_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.text_result = tk.Text(
            frame_text, 
            height=10,
            bg="#2b2b2b",  # 深色主题下的背景色
            fg="#ffffff",  # 深色主题下的文字颜色
            font=("Consolas", 10),
            relief="flat"
        )
        self.text_result.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(frame_text, orient="vertical", command=self.text_result.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_result.configure(yscrollcommand=scrollbar.set)

        # 缓存数据
        self.original_data = None
        
        # 更新主题相关的颜色
        self.update_theme_colors()

    def toggle_theme(self):
        """
        切换应用的明暗主题
        在深色和浅色主题之间切换
        """
        if sv_ttk.get_theme() == "dark":
            sv_ttk.set_theme("light")
        else:
            sv_ttk.set_theme("dark")
        self.update_theme_colors()

    def update_theme_colors(self):
        """
        根据当前主题更新UI组件的颜色
        包括画布背景色、文本颜色等
        """
        is_dark = sv_ttk.get_theme() == "dark"
        bg_color = "#2b2b2b" if is_dark else "#ffffff"
        fg_color = "#ffffff" if is_dark else "#000000"
        
        self.canvas.configure(bg=bg_color)
        self.text_result.configure(
            bg=bg_color,
            fg=fg_color,
            insertbackground=fg_color  # 光标颜色
        )

    def sort_and_time(self):
        """
        执行选中的排序算法并统计时间
        
        如果选择"全部算法"，则会依次执行所有排序算法并比较其性能
        支持实时可视化和慢速模式
        """
        # 如果没有数据，先生成数据
        if not self.original_data:
            self.original_data = generate_data()
            self.log("已生成 10000 个随机整数，范围 [1, 100000].")
            if self.visual_var.get():
                self.draw_data(self.original_data)

        # 获取选择的算法
        algorithm = self.algorithms[self.algorithm_var.get()]
        
        # 使用数据的拷贝
        data = self.original_data[:]
        
        # 回调函数（可视化开关决定是否传入）
        draw_callback = self.draw_data if self.visual_var.get() else None

        # 记录排序时间
        times = {}

        if algorithm == "all" or algorithm == "bubble":
            self.status_text.set("正在执行：冒泡排序")
            start_time = time.perf_counter()
            # 根据慢速模式调整刷新率
            refresh_rate = 10 if self.slow_mode_var.get() else 200
            bubble_sort(data.copy(), draw_callback=draw_callback, refresh_rate=refresh_rate)
            times["冒泡排序"] = time.perf_counter() - start_time

        if algorithm == "all" or algorithm == "quick":
            self.status_text.set("正在执行：快速排序")
            start_time = time.perf_counter()
            refresh_rate = 10 if self.slow_mode_var.get() else 200
            quick_sort(data.copy(), draw_callback=draw_callback, refresh_rate=refresh_rate)
            times["快速排序"] = time.perf_counter() - start_time

        if algorithm == "all" or algorithm == "shell":
            self.status_text.set("正在执行：希尔排序")
            start_time = time.perf_counter()
            refresh_rate = 10 if self.slow_mode_var.get() else 200
            shell_sort(data.copy(), draw_callback=draw_callback, refresh_rate=refresh_rate)
            times["希尔排序"] = time.perf_counter() - start_time

        if algorithm == "all" or algorithm == "heap":
            self.status_text.set("正在执行：堆排序")
            start_time = time.perf_counter()
            refresh_rate = 10 if self.slow_mode_var.get() else 200
            heap_sort(data.copy(), draw_callback=draw_callback, refresh_rate=refresh_rate)
            times["堆排序"] = time.perf_counter() - start_time

        if algorithm == "all" or algorithm == "radix":
            self.status_text.set("正在执行：基数排序")
            start_time = time.perf_counter()
            refresh_rate = 10 if self.slow_mode_var.get() else 200
            radix_sort(data.copy(), draw_callback=draw_callback, refresh_rate=refresh_rate)
            times["基数排序"] = time.perf_counter() - start_time

        # 输出结果
        self.status_text.set("排序完成")
        self.log("\n排序完成，耗时统计(单位: 秒)：")
        for sort_name, t in times.items():
            self.log(f"{sort_name}: {t:.6f}")

    def clear_results(self):
        """
        清空所有显示结果
        
        重置文本框、画布和数据，将状态恢复到初始状态
        """
        self.text_result.delete("1.0", tk.END)
        self.canvas.delete("all")
        self.original_data = None
        self.status_text.set("就绪")

    def log(self, msg):
        """
        在文本框中添加日志信息
        
        :param msg: 要显示的日志消息
        """
        self.text_result.insert(tk.END, msg + "\n")
        self.text_result.see(tk.END)

    def draw_data(self, arr, current_pos=None):
        """
        在画布上可视化数组的当前状态
        
        使用柱状图表示数组元素，突出显示当前处理的位置
        为提高性能，采用了采样和批量绘制策略
        
        :param arr: 要显示的数组
        :param current_pos: 当前正在处理的位置（可选）
        """
        self.canvas.delete("all")

        if not arr:
            return

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        n = len(arr)
        # 增加采样间隔，减少绘制的数据点
        sample_size = min(n, 200)  # 减少到200个采样点
        step = n // sample_size

        max_val = max(arr)
        if max_val == 0:
            max_val = 1

        bar_width = w / sample_size
        
        # 根据主题选择颜色
        is_dark = sv_ttk.get_theme() == "dark"
        normal_color = "#00B4D8" if is_dark else "#0077B6"  # 蓝色
        highlight_color = "#FF4D4D" if is_dark else "#D00000"  # 红色
        
        # 批量创建矩形，减少canvas的绘制调用次数
        rectangles = []
        for i in range(sample_size):
            index = i * step
            val = arr[index]
            bar_height = (val / max_val) * (h - 25)  # 留出顶部空间显示文本
            x0 = i * bar_width
            y0 = h - bar_height
            x1 = (i+1) * bar_width
            y1 = h
            
            # 如果是当前处理的位置，使用高亮颜色
            color = highlight_color if current_pos is not None and index == current_pos else normal_color
            rectangles.append((x0, y0, x1, y1, color))
            
        # 一次性创建所有矩形
        for rect in rectangles:
            self.canvas.create_rectangle(*rect[:-1], fill=rect[-1], outline="")

        # 每50ms才进行一次画布更新
        if not hasattr(self, '_last_update') or time.time() - self._last_update >= 0.05:
            self.update_idletasks()
            self._last_update = time.time()
