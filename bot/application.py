#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
PTB APPLICATION FACTORY
=============================================================================
"""

from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    CallbackQueryHandler
)
from telegram.request import HTTPXRequest

from config import settings
from utils.logger import logger
from database.models import Constants
from bot.handlers import *
from bot.callbacks import *
from bot.commands import *


# ===== FALLBACK STATES (jika Constants belum punya) =====
class BotStates:
    """States for conversation handlers"""
    SELECTING_ROLE = 1
    CONFIRM_END = 14
    CONFIRM_CLOSE = 15
    CONFIRM_BROADCAST = 16


def create_application() -> Application:
    """
    Create and configure telegram application
    INI SYNCHRONOUS, BUKAN ASYNC!
    """
    
    logger.info("🔧 Creating PTB application...")
    
    # Custom request dengan timeout besar
    request = HTTPXRequest(
        connection_pool_size=50,
        connect_timeout=60,
        read_timeout=60,
        write_timeout=60,
        pool_timeout=60,
    )
    
    # Build application - SYNCHRONOUS
    app = ApplicationBuilder() \
        .token(settings.telegram_token) \
        .request(request) \
        .concurrent_updates(True) \
        .build()
    
    # ===== AMBIL STATE DARI CONSTANTS ATAU FALLBACK =====
    SELECTING_ROLE = getattr(Constants, 'SELECTING_ROLE', BotStates.SELECTING_ROLE)
    CONFIRM_END = getattr(Constants, 'CONFIRM_END', BotStates.CONFIRM_END)
    CONFIRM_CLOSE = getattr(Constants, 'CONFIRM_CLOSE', BotStates.CONFIRM_CLOSE)
    CONFIRM_BROADCAST = getattr(Constants, 'CONFIRM_BROADCAST', BotStates.CONFIRM_BROADCAST)
    
    logger.info(f"  • Using SELECTING_ROLE = {SELECTING_ROLE}")
    
    # ===== CONVERSATION HANDLERS =====
    logger.info("  • Setting up conversation handlers...")
    
    # Start conversation
    start_conv = ConversationHandler(
        entry_points=[CommandHandler('start', start_command)],
        states={
            SELECTING_ROLE: [
                CallbackQueryHandler(agree_18_callback, pattern='^agree_18$'),
                CallbackQueryHandler(role_ipar_callback, pattern='^role_ipar$'),
                CallbackQueryHandler(role_teman_kantor_callback, pattern='^role_teman_kantor$'),
                CallbackQueryHandler(role_janda_callback, pattern='^role_janda$'),
                CallbackQueryHandler(role_pelakor_callback, pattern='^role_pelakor$'),
                CallbackQueryHandler(role_istri_orang_callback, pattern='^role_istri_orang$'),
                CallbackQueryHandler(role_pdkt_callback, pattern='^role_pdkt$'),
                CallbackQueryHandler(role_sepupu_callback, pattern='^role_sepupu$'),
                CallbackQueryHandler(role_teman_sma_callback, pattern='^role_teman_sma$'),
                CallbackQueryHandler(role_mantan_callback, pattern='^role_mantan$'),
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel_command)],
        name="start_conversation",
        persistent=False,
        per_user=True,
        per_chat=True,
        per_message=False
    )
    
    # End conversation
    end_conv = ConversationHandler(
        entry_points=[CommandHandler('end', end_command)],
        states={
            CONFIRM_END: [CallbackQueryHandler(end_callback, pattern='^end_')],
        },
        fallbacks=[CommandHandler('cancel', cancel_command)],
        name="end_conversation",
        persistent=False,
        per_user=True,
        per_chat=True,
        per_message=False
    )
    
    # Close conversation
    close_conv = ConversationHandler(
        entry_points=[CommandHandler('close', close_command)],
        states={
            CONFIRM_CLOSE: [CallbackQueryHandler(close_callback, pattern='^close_')],
        },
        fallbacks=[CommandHandler('cancel', cancel_command)],
        name="close_conversation",
        persistent=False,
        per_user=True,
        per_chat=True,
        per_message=False
    )
    
    # Relationship conversations
    rel_conv = ConversationHandler(
        entry_points=[
            CommandHandler('jadipacar', jadipacar_command),
            CommandHandler('break', break_command),
            CommandHandler('breakup', breakup_command),
            CommandHandler('fwb', fwb_command)
        ],
        states={
            CONFIRM_BROADCAST: [
                CallbackQueryHandler(jadipacar_callback, pattern='^jadipacar_'),
                CallbackQueryHandler(break_callback, pattern='^break_'),
                CallbackQueryHandler(breakup_callback, pattern='^breakup_'),
                CallbackQueryHandler(fwb_callback, pattern='^fwb_'),
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel_command)],
        name="relationship_conversation",
        persistent=False,
        per_user=True,
        per_chat=True,
        per_message=False
    )
    
    # ===== ADD ALL HANDLERS =====
    logger.info("  • Registering command handlers...")
    
    # Conversation handlers
    app.add_handler(start_conv)
    app.add_handler(end_conv)
    app.add_handler(close_conv)
    app.add_handler(rel_conv)
    
    # Basic commands
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CommandHandler("cancel", cancel_command))
    
    # Dominance commands
    app.add_handler(CommandHandler("dominant", dominant_command))
    
    # Session commands
    app.add_handler(CommandHandler("pause", pause_command))
    app.add_handler(CommandHandler("unpause", unpause_command))
    app.add_handler(CommandHandler("close", close_command))
    app.add_handler(CommandHandler("end", end_command))
    
    # Relationship commands
    app.add_handler(CommandHandler("jadipacar", jadipacar_command))
    app.add_handler(CommandHandler("break", break_command))
    app.add_handler(CommandHandler("unbreak", unbreak_command))
    app.add_handler(CommandHandler("breakup", breakup_command))
    app.add_handler(CommandHandler("fwb", fwb_command))
    
    # HTS/FWB commands
    app.add_handler(CommandHandler("htslist", htslist_command))
    app.add_handler(CommandHandler("fwblist", fwblist_command))
    
    # HTS/FWB call commands (pattern matching)
    app.add_handler(MessageHandler(filters.Regex(r'^/hts-'), hts_call_command))
    app.add_handler(MessageHandler(filters.Regex(r'^/fwb-'), fwb_call_command))
    
    # Ranking commands
    app.add_handler(CommandHandler("tophts", tophts_command))
    app.add_handler(CommandHandler("myclimax", myclimax_command))
    app.add_handler(CommandHandler("climaxrank", climaxrank_command))
    app.add_handler(CommandHandler("climaxhistory", climaxhistory_command))
    
    # Public area commands (V81)
    app.add_handler(CommandHandler("explore", explore_command))
    app.add_handler(CommandHandler("go", go_command))
    app.add_handler(CommandHandler("positions", positions_command))
    app.add_handler(CommandHandler("risk", risk_command))
    app.add_handler(CommandHandler("mood", mood_command))
    
    # Admin commands
    app.add_handler(CommandHandler("admin", admin_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("db_stats", db_stats_command))
    app.add_handler(CommandHandler("list_users", list_users_command))
    app.add_handler(CommandHandler("get_user", get_user_command))
    app.add_handler(CommandHandler("force_reset", force_reset_command))
    app.add_handler(CommandHandler("backup_db", backup_db_command))
    app.add_handler(CommandHandler("vacuum", vacuum_command))
    app.add_handler(CommandHandler("memory_stats", memory_stats_command))
    app.add_handler(CommandHandler("reload", reload_command))
    
    # Hidden commands
    app.add_handler(CommandHandler("reset", force_reset_command))
    
    # Message handler (must be last)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    
    # ===== ERROR HANDLER =====
    app.add_error_handler(error_handler)
    
    # Log jumlah handlers
    handler_count = sum(len(h) for h in app.handlers.values())
    logger.info(f"✅ All handlers registered: {handler_count} handlers")
    
    return app
