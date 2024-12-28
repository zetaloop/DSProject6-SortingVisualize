chcp 65001
@echo off
echo 正在创建虚拟环境...
py -m venv venv
call venv\Scripts\activate.bat

echo 正在安装依赖...
pip install -r requirements.txt

echo 正在打包程序...
pyinstaller --noconfirm --onefile --windowed ^
  --name "排序算法演示" ^
  --icon "NONE" ^
  --add-data "venv/Lib/site-packages/sv_ttk;sv_ttk/" ^
  main.py

echo 清理临时文件...
rmdir /s /q build
del /q "排序算法演示.spec"

echo 完成！

echo 生成的程序位于 dist 目录下
pause
