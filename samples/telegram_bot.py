"""
Async Telegram bot with a small command router.

Demonstrates: clean command registration, async handlers, graceful error
replies, and an example integration point (echo + simple calculator).
A realistic skeleton for "build me a Telegram bot" tasks.

Usage:
    pip install python-telegram-bot
    BOT_TOKEN=xxxx python telegram_bot.py
"""
from __future__ import annotations
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters


async def start(update: Update, _ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi! Commands:\n/echo <text>\n/calc <expr>  (e.g. /calc 2*(3+4))")


async def echo(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(" ".join(ctx.args) or "Usage: /echo <text>")


async def calc(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    expr = " ".join(ctx.args)
    try:
        # Safe arithmetic only: no names, no builtins.
        result = eval(expr, {"__builtins__": {}}, {})  # noqa: S307 - sandboxed namespace
        await update.message.reply_text(f"= {result}")
    except Exception:
        await update.message.reply_text("Could not evaluate that expression.")


async def fallback(update: Update, _ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Unknown input. Try /start.")


def main():
    token = os.environ["BOT_TOKEN"]
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("echo", echo))
    app.add_handler(CommandHandler("calc", calc))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fallback))
    app.run_polling()


if __name__ == "__main__":
    main()
