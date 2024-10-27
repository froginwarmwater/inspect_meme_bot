# Telegram Bot

## 使用说明

按照以下步骤设置和运行Telegram Bot：

1. 创建并激活虚拟环境：
   ```
   python -m venv venv
   source venv/bin/activate  # 在Windows上使用: venv\Scripts\activate
   ```

2. 安装依赖：
   ```
   pip install -r requirements.txt
   ```

3. 配置Bot Token：
   - 创建一个`.env`文件在项目根目录
   - 在`.env`文件中添加您的Telegram Bot Token：
     ```
     TELEGRAM_BOT_TOKEN=your_bot_token_here
     ```

4. 运行Bot：
   ```
   python inspect_meme_main.py
   ```

现在您的Telegram Bot应该已经在运行了。您可以在Telegram中与它进行交互。

注意：确保在运行bot之前已经在Telegram中创建了bot并获取了token。

