#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MESSAGE HANDLERS
=============================================================================
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

from config import settings
from utils.logger import logger
from utils.exceptions import handle_errors
from utils.rate_limiter import get_rate_limiter, rate_limit
from database.models import Constants


# ===== START COMMAND =====

@handle_errors
@rate_limit
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command"""
    user_id = update.effective_user.id
    username = update.effective_user.username or update.effective_user.first_name
    
    logger.info(f"▶️ /start from {username} ({user_id})")
    
    # Cek admin
    if user_id != settings.admin_id:
        await update.message.reply_text("⛔ Maaf, bot ini hanya untuk pemiliknya.")
        return ConversationHandler.END
    
    context.user_data.clear()
    
    # Tampilkan disclaimer
    disclaimer = (
        "⚠️ **PERINGATAN DEWASA (18+)** ⚠️\n\n"
        "Bot ini mengandung konten dewasa.\n\n"
        "Klik 'Saya setuju' untuk melanjutkan."
    )
    
    keyboard = [[InlineKeyboardButton("✅ Saya setuju (18+)", callback_data="agree_18")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        disclaimer, 
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    return Constants.SELECTING_ROLE


# ===== HELP COMMAND =====

@handle_errors
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command"""
    await update.message.reply_text(
        "📚 **BANTUAN**\n\n"
        "/start - Mulai\n"
        "/help - Bantuan ini\n"
        "/status - Status\n"
        "/cancel - Batal"
    )


# ===== STATUS COMMAND =====

@handle_errors
async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Status command"""
    await update.message.reply_text("✅ Bot berjalan normal")


# ===== MESSAGE HANDLER =====

@handle_errors
@rate_limit
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle semua pesan"""
    user_id = update.effective_user.id
    message = update.message.text
    
    logger.info(f"💬 {user_id}: {message[:50]}...")
    
    await update.message.reply_text(f"Pesan diterima: {message[:30]}...")


# ===== ERROR HANDLER =====

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Global error handler"""
    logger.error(f"Exception: {context.error}")


# ===== CANCEL COMMAND =====

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel conversation"""
    await update.message.reply_text("❌ Dibatalkan.")
    return ConversationHandler.END


# ===== HTS/FWB CALL COMMANDS =====

async def hts_call_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /hts- command"""
    await update.message.reply_text("🔍 Fitur HTS sedang dalam pengembangan")


async def fwb_call_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /fwb- command"""
    await update.message.reply_text("🔍 Fitur FWB sedang dalam pengembangan")
