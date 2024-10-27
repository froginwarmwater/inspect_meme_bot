# 使用官方 Python 3.9 slim 版本作为基础镜像
FROM python:3.9-slim

# 设置工作目录为 /app
WORKDIR /app

# 将本地的 requirements.txt 复制到工作目录
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制当前目录下所有文件到工作目录 /app
COPY . .

# 指定运行时使用的 Python 编码，防止编码问题
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=UTF-8

# 设置默认命令以运行 Telegram 机器人
CMD ["python", "inspect_meme_main.py"]

