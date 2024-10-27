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
5. 配置supervisor：
   - 在`/etc/supervisor/conf.d/`目录下创建一个文件，例如`telegram-bot.conf`，并添加以下内容：
   ```
   [program:telegram-bot]
   command=/root/telegram-bot/venv/bin/python /root/telegram-bot/inspect_meme_main.py
   directory=/root/telegram-bot
   user=root
   autostart=true
   autorestart=true
   stderr_logfile=/root/telegram-bot/telegram-bot.err.log
   stdout_logfile=/root/telegram-bot/telegram-bot.out.log
   ```
   - 启动supervisor配置：
   ```
   supervisord -c /etc/supervisor/supervisord.conf
   ```
   - 重新加载supervisor配置：
   ```
   sudo supervisorctl reread
   sudo supervisorctl update
   ```
   管理 supervisor 控制的程序：
   - 停止程序：
   ```
   sudo supervisorctl stop telegram-bot
   ```
   - 启动程序：
   ```
   sudo supervisorctl start telegram-bot
   ```
   - 重启程序：
   ```
   sudo supervisorctl restart telegram-bot
   ```
   - 查看所有程序状态：
   ```
   sudo supervisorctl status
   ```

现在您的Telegram Bot应该已经在运行了。您可以在Telegram中与它进行交互。
