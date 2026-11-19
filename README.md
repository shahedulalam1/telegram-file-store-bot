# Telegram File Store Bot

An unlimited file store Telegram bot. Send any file to the bot and it gives you a permanent share link. Anyone who opens that link receives the file directly from the bot.

The bot stores your files in a private Telegram channel, so there is no database to set up and no storage to pay for.

---

## Features

- **Permanent share links**: every upload gets a link like `https://t.me/<your_bot>?start=file_<id>` that keeps working, even after the bot restarts.
- **No database needed**: the link ID is the message ID of the file in your storage channel, so the channel itself is the database.
- **Owner-only uploads**: only the Telegram user IDs listed in `OWNER_ID` can upload files. Everyone else is silently ignored.
- **Open download links**: anyone with a share link can get the file, no permission needed.
- **Wide file type support**: documents, photos, videos, audio, voice messages, stickers, animations (GIFs) and video notes.
- **Clean delivery**: files are sent with `copy_message`, so the receiver does not see a "forwarded from" label.
- **Hosting friendly**: a small Flask web server runs alongside the bot, so the project works on platforms that need an open web port (for example Render).

---

## How it works

1. The owner sends a file to the bot.
2. The bot forwards the file to your private storage channel.
3. The bot replies with a share link that contains the message ID of the stored file.
4. When someone opens the link, Telegram starts the bot with `/start file_<id>`.
5. The bot copies that message from the channel to the person who opened the link.

---

## Requirements

- Python 3.9 or newer
- A Telegram bot token from [@BotFather](https://t.me/BotFather)
- A private Telegram channel where the bot is an **administrator** (with permission to post messages)
- Your numeric Telegram user ID (you can get it from bots such as [@userinfobot](https://t.me/userinfobot))

Python dependencies (see `requirements.txt`):

```
pyTelegramBotAPI==4.27.0
Flask==3.0.0
```

---

## Setup

### 1. Create the bot

1. Open [@BotFather](https://t.me/BotFather) and send `/newbot`.
2. Follow the steps and copy the **bot token**.

### 2. Create the storage channel

1. Create a new Telegram channel (private is recommended).
2. Add your bot to the channel as an **administrator**.
3. Find the channel ID. Channel IDs are negative numbers that usually start with `-100`, for example `-1001234567890`.

### 3. Set the environment variables

| Variable     | Required | Description                                                                                  |
|--------------|----------|----------------------------------------------------------------------------------------------|
| `BOT_TOKEN`  | Yes      | The token you got from BotFather.                                                            |
| `CHANNEL_ID` | Yes      | ID of the storage channel (for example `-1001234567890`).                                    |
| `OWNER_ID`   | Yes*     | Telegram user ID of the owner. For several owners, separate IDs with commas: `1111,2222`.    |
| `PORT`       | No       | Port for the built-in web server. Defaults to `10000`.                                       |

\* If `OWNER_ID` is not set, the bot still starts, but nobody will be able to upload files. Share links will keep working.

### 4. Install and run locally

```bash
git clone https://github.com/shahedulalam1/telegram-file-store-bot.git
cd telegram-file-store-bot
pip install -r requirements.txt

export BOT_TOKEN="your_bot_token"
export CHANNEL_ID="-1001234567890"
export OWNER_ID="123456789"

python main.py
```

On Windows (PowerShell), use `$env:BOT_TOKEN="..."` instead of `export`.

When everything is correct you will see `Bot Running...` in the console.

---

## Usage

### For the owner

1. Open your bot in Telegram and send `/start`.
2. Send any file to the bot.
3. The bot replies with a share link. Copy it and share it anywhere.

### For everyone else

Open the share link. Telegram opens the bot, and the bot sends the file automatically.

---

## Deployment

The bot uses long polling, so it can run on any server or hosting platform that can run Python.

On a platform such as **Render**:

- **Build command:** `pip install -r requirements.txt`
- **Start command:** `python main.py`
- Add `BOT_TOKEN`, `CHANNEL_ID` and `OWNER_ID` in the platform's environment variable settings.

The root URL (`/`) returns `Bot is running!`, so you can use it for health checks or uptime monitoring.

> Run only **one** instance of the bot at a time. Two instances polling with the same token will conflict with each other.

---

## Troubleshooting

| Problem                                           | What to check                                                                                         |
|---------------------------------------------------|--------------------------------------------------------------------------------------------------------|
| Bot exits right away with an error message        | `BOT_TOKEN` or `CHANNEL_ID` is missing or empty.                                                       |
| "Error" reply when uploading a file               | Make sure the bot is an **admin** of the channel and `CHANNEL_ID` is correct.                          |
| Bot does not react to your files                  | Your user ID is not in `OWNER_ID`. Non-owners are ignored by design.                                   |
| Link says "File not found"                        | The message was deleted from the channel, or the link was changed.                                     |
| Conflict error (409) in the logs                  | Another copy of the bot is running with the same token. Stop the other one.                            |

---

## Important notes

- **Do not delete messages from the storage channel.** Each share link points to a message in that channel. If the message is deleted, the link stops working.
- **Keep your bot token secret.** Never commit it to GitHub. Use environment variables only.
- Anyone who has a share link can download that file, so only share links with people you trust.

---

## Project structure

```
.
├── main.py            # Bot and web server
├── requirements.txt   # Python dependencies
├── .gitignore
└── README.md
```

---

## Tech stack

- [pyTelegramBotAPI (telebot)](https://github.com/eternnoir/pyTelegramBotAPI) for the Telegram bot
- [Flask](https://flask.palletsprojects.com/) for the lightweight web server
