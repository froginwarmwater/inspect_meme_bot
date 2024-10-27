from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, JobQueue
import requests
import asyncio
import json
import os
import telegram
from inspect_meme_get_filter import filter_new_or_updated_tokens, filter_last_10_tokens
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
# 假设我们用一个文件来保存用户 chat_id
USER_DATA_FILE = 'user_chat_ids.json'
# 初始化Telegram Bot
bot = telegram.Bot(token=TOKEN)
last_data = []
async def send_test_message_to_all(entry):
    formated_data = format_token_info_for_bot(entry)
    message = "new coin:\n" + formated_data

    # 创建异步任务列表
    tasks = [bot.send_message(chat_id=chat_id, text=message) for chat_id in user_chat_ids]

    # 并发发送消息
    await asyncio.gather(*tasks)

    print("消息已发送给所有用户")

# 初始化用户列表，如果文件存在就加载它
if os.path.exists(USER_DATA_FILE):
    with open(USER_DATA_FILE, 'r') as f:
        user_chat_ids = json.load(f)
else:
    user_chat_ids = []

START_MESSAGE = """
👋 欢迎使用 InspectMeme Bot，以下是我可以为你提供的功能：

📅 /add_listener - 接受监听提醒

📅 /remove_listener - 取消监听提醒

📅 /latest24hour - 查看过去24小时内新增或更新的加密货币

📅 /latest10tokens - 查看最新的10个token


有任何问题或建议，随时可以联系我！😊
"""
API_URL = 'https://moonshot.umi.cat/api/categories?limit=10'

def fetch_api_data():
    """访问API并获取数据"""
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            response_json = response.json()
            ret = []
            id_set = set()
            for item in response_json:
                for inner_item in item['coins']:
                    if inner_item.get('id') not in id_set:
                        id_set.add(inner_item.get('id'))
                        ret.append(inner_item)
            return ret
        else:
            print(f"Failed to fetch API data. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error while fetching API data: {e}")
        return None

async def add_listener(update: Update, context) -> None:
    chat_id = update.message.chat_id
    print(chat_id)
    if chat_id not in user_chat_ids:
        user_chat_ids.append(chat_id)
        with open(USER_DATA_FILE, 'w') as file:
            json.dump(user_chat_ids, file)
    await update.message.reply_text("已将您加入提醒列表，新的token上线会提醒您")


async def remove_listener(update: Update, context) -> None:
    chat_id = update.message.chat_id

    # 检查用户是否在用户列表中
    if chat_id in user_chat_ids:
        user_chat_ids.remove(chat_id)  # 从列表中移除该用户
        with open(USER_DATA_FILE, 'w') as file:
            json.dump(user_chat_ids, file)  # 更新存储的用户数据文件
        await update.message.reply_text("您将不再接收通知，感谢您的使用")
    else:
        await update.message.reply_text("您不在用户列表中")


# 处理 /start 命令
async def start(update: Update, context) -> None:
    await update.message.reply_text(START_MESSAGE)

async def print_all_user(update: Update, context) -> None:
    await update.message.reply_text(user_chat_ids)
# 处理用户发送的消息
async def echo(update: Update, context) -> None:
    # 打印用户发送的消息
    print(f"User said: {update.message.text}")
    # 回复同样的消息
    await update.message.reply_text(update.message.text)

async def latest_24hour(update: Update, context) -> None:
    api_data = fetch_api_data()
    data = filter_new_or_updated_tokens(api_data)
    if len(data) == 0:
        await update.message.reply_text("No updates found in latest 24 hours")
        return
    formated_data = format_token_info_for_bot(data)
    print(f"User said: {update.message.text}")
    await update.message.reply_text(formated_data)

async def broadcast_test(update: Update, context) -> None:
    api_data = fetch_api_data()
    data = filter_last_10_tokens(api_data)
    if len(data) == 0:
        await update.message.reply_text("No updates found in latest 24 hours")
    formated_data = format_token_info_for_bot(data)
    await send_test_message_to_all(formated_data)

    print("消息已发送给所有用户")


async def latest_10token(update: Update, context) -> None:
    api_data = fetch_api_data()
    data = filter_last_10_tokens(api_data)
    if len(data) == 0:
        await update.message.reply_text("No updates found in latest 24 hours")
    formated_data = format_token_info_for_bot(data)
    print(f"User said: {update.message.text}")
    await update.message.reply_text(formated_data)

# async def send_telegram_message(update: Update, context) -> None:
#     # 回复同样的消息
#     await update.message.reply_text(update.message.text)


def format_token_info_for_bot(tokens):
    # 创建存储格式化信息的字符串
    formatted_info = ""

    # 遍历每个 token 并格式化其信息
    for token in tokens:
        name = token.get('name', 'Unknown')
        chain = token.get('chain', 'Unknown')
        address = token.get('contractAddress') or 'Not available'

        # 使用多行格式化 token 的信息
        formatted_info += f"Token Name: {name}\nChain: {chain.capitalize()}\nAddress: {address}\n\n"

    return formatted_info.strip()

last_data = []
is_initial = True
address_set = set()
# 实际结果是获取最近24小时的新token
async def check_for_new_data(context):
    global last_data
    global address_set
    current_data = fetch_api_data()
    if len(last_data) == 0:
        for token in current_data:
            address_set.add(token.get('contractAddress'))
        return []

    new_entries = []
    for token in current_data:
        contract_address = token.get('contractAddress')
        if contract_address not in address_set:  # 如果地址不在 address_set 中，说明是新的 token
            new_entries.append(token)  # 将新的 token 添加到新条目列表中
            address_set.add(contract_address)  # 同时将其添加到 address_set，避免重复处理

    if new_entries:
        formated_data = format_token_info_for_bot(new_entries)
        await send_notification_to_all_users(context, formated_data)

# 将通知发送给所有用户
async def send_notification_to_all_users(context, message):
    for chat_id in user_chat_ids:
        await context.bot.send_message(chat_id=chat_id, text=message)


def start_listener(job_queue: JobQueue):
    # 每10秒检查一次事件（如API数据）
    job_queue.run_repeating(check_for_new_data, interval=60, first=0)

def main():


    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add_listener", add_listener))
    app.add_handler(CommandHandler("remove_listener", remove_listener))
    app.add_handler(CommandHandler("print_all_user", print_all_user))
    app.add_handler(CommandHandler("latest24hour", latest_24hour))
    app.add_handler(CommandHandler("latest10tokens", latest_10token))
    app.add_handler(CommandHandler("broadcast_test", broadcast_test))
    # app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    # 创建一个 JobQueue 对象并启动监听
    job_queue = app.job_queue
    start_listener(job_queue)

    app.run_polling()


if __name__ == '__main__':
    main()




"""
[
  {
    "id": "top_gainers",
    "name": "Top Gainers",
    "order": null,
    "coins": [
      {
        "id": "PMMERaJsgLuFkqItx7lyoro2",
        "ticker": "RICKROLL",
        "categoryId": null,
        "contractAddress": "B9pmGiVoXPyPKFViY6se32qtRGX85qv4mYB7Gp1os4w4",
        "name": "RICKROLL",
        "chain": "solana",
        "description": "I just wanna tell you how I'm feeling\r\nGotta make you understand",
        "imageUrl": "https://cdn.moonshot.money/p5mu9Qlr0L0DlDLx4dSxmwlv.png",
        "twitter": null,
        "decimals": 9,
        "circulatingSupply": "996669530787773013",
        "isHidden": false,
        "balances": null,
        "bookmarks": null,
        "createdAt": "2023-12-26T20:16:00Z",
        "updatedAt": "2024-10-09T15:43:11.5887Z",
        "listedAt": "2024-10-09T15:43:14.193246Z",
        "day": {
          "price": 0.0022593448114135834,
          "change": 260.43736315974144,
          "volume": 184917.0313276857,
          "holders": 3314,
          "allTimeHigh": null,
          "allTimeHighAt": null,
          "allTimeLow": null,
          "allTimeLowAt": null
        },
        "prices": null
      },
      {..
      }
]
"""
