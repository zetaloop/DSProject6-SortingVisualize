# 排序算法可视化演示程序（课程作业）

<img width="600" alt="Snipaste_2024-12-28_14-23-45" src="https://github.com/user-attachments/assets/570da6fe-a037-4d75-a790-91f1156880bb" />

这是一个用Python开发的排序算法可视化演示程序，旨在帮助用户直观地理解和比较不同排序算法的工作原理和性能特点。

## 功能特性

- 支持5种经典排序算法的可视化演示：
  - 冒泡排序 (Bubble Sort)
  - 快速排序 (Quick Sort)
  - 希尔排序 (Shell Sort)
  - 堆排序 (Heap Sort)
  - 基数排序 (Radix Sort)
- 实时动态可视化排序过程
- 支持算法执行时间统计和性能对比
- 可调节排序速度（支持慢速模式）
- 自适应深色/浅色主题
- 美观的现代化GUI界面

## 环境要求

- Python 3.12+
- 操作系统：Windows/macOS/Linux

## 依赖安装

```bash
pip install -r requirements.txt
```

主要依赖包括：
- sv-ttk：现代化的ttk主题
- darkdetect：系统亮暗色主题检测
- pyinstaller：用于构建可执行文件

## 使用说明

### 从源码运行

1. 克隆或下载本项目
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 运行程序：
   ```bash
   python main.py
   ```

### 使用可执行文件

1. 在Windows系统下，直接运行 `make_bin.cmd` 生成可执行文件
2. 运行生成的exe文件（位于 `dist` 目录下）

### 程序操作说明

1. 选择排序算法：从下拉菜单中选择想要演示的算法
2. 启用可视化：勾选"启用可视化"选项可以看到排序过程的动态展示
3. 调节速度：勾选"慢速模式"可以降低排序速度，更清晰地观察排序过程
4. 开始排序：点击"开始排序"按钮开始演示
5. 查看结果：在下方文本框中可以看到各个算法的执行时间统计
6. 切换主题：点击"切换主题"按钮可以在深色/浅色主题间切换

## 构建说明

### Windows系统

运行 `make_bin.cmd` 脚本即可自动构建可执行文件：

```bash
make_bin.cmd
```

构建完成后，可执行文件将位于 `dist` 目录下。

## 项目结构

- `main.py`：程序入口
- `gui.py`：图形界面实现
- `sorting_algorithms.py`：排序算法实现
- `data_generator.py`：测试数据生成器
- `requirements.txt`：项目依赖
- `make_bin.cmd`：构建脚本

## 注意事项

- 启用可视化会降低排序速度，这是为了便于观察
- 在性能测试时建议关闭可视化功能
- 程序会自动适应系统的深色/浅色主题
- 可以随时通过"清空结果"按钮重置程序状态
