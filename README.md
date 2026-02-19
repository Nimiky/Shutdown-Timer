# 自动关机助手 (Shutdown Timer)

这是一个美观、现代化的Windows自动关机小工具，使用Python编写。

## 功能介绍

1.  **按时刻关机**：
    *   设置具体的24小时制时间（如 `23:30`）。
    *   到达指定时间后自动执行关机流程。

2.  **倒计时关机**：
    *   设置小时、分钟、秒数。
    *   倒计时结束后自动关机。

3.  **安全机制**：
    *   **60秒缓冲**：触发关机时，系统会提示并在60秒后执行，防止数据丢失。
    *   **撤销功能**：在60秒缓冲期内，点击程序中的“撤销关机 (Abort)”按钮可立即取消关机。
    *   **进度条**：直观显示剩余时间进度。

## 使用方法 (Windows)

1.  **傻瓜式一键运行**：
    *   为了方便用户，本项目提供了 `run_timer.bat` 批处理文件。
    *   **双击该文件**即可直接启动程序，无需手动打开命令行或配置环境，实现“傻瓜式”一键使用。

2.  **设置任务**：
    *   在界面中选择“按时刻关机”或“倒计时关机”标签页。
    *   输入时间。
    *   点击 **“开始任务”**。

3.  **取消任务**：
    *   任务运行中，点击 **“取消任务”** 即可停止倒计时。

## 使用方法 (Linux)

如果您希望在 Linux 环境下运行本工具：

1.  **准备环境**：
    *   确保已安装 Python 3.x。
    *   部分 Linux 发行版可能需要手动安装 Tkinter 支持：
        ```bash
        sudo apt-get install python3-tk  # Ubuntu/Debian
        sudo pacman -S tk                # Arch Linux
        ```

2.  **安装依赖**：
    *   在终端中打开项目目录，运行：
        ```bash
        pip install -r requirements.txt
        ```

3.  **运行程序**：
    ```bash
    python3 shutdown_timer.py
    ```

> **注意**：程序默认使用 Windows 关机指令 (`shutdown /s`)。Linux 用户如果需要实际执行关机功能，请在源码 `shutdown_timer.py` 中搜索 `os.system`，并将关机命令修改为适用于 Linux 的指令（例如 `shutdown -h now` 或 `shutdown -h +1`）。

## 开发与源码说明

如果您是开发者或需要重新配置环境 (Windows/Linux)：

1.  确保已安装 Python。
2.  安装依赖库：
    ```bash
    pip install -r requirements.txt
    ```
3.  运行：
    ```bash
    python shutdown_timer.py
    ```
