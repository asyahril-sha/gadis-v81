#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
WEBHOOK SETUP
=============================================================================
"""

import os
from telegram.ext import Application
from utils.logger import logger
from config import settings


async def setup_webhook(app: Application) -> str:
    """
    Setup webhook untuk Railway
    """
    
    # Dapatkan URL dari environment (Railway)
    railway_url = os.getenv('RAILWAY_PUBLIC_DOMAIN', '')
    if not railway_url:
        railway_url = os.getenv('RAILWAY_STATIC_URL', '')
    
    # Custom webhook URL dari settings
    if hasattr(settings, 'webhook') and settings.webhook.url:
        webhook_url = settings.webhook.url
    elif railway_url:
        webhook_url = f"https://{railway_url}{settings.webhook.path}"
    else:
        logger.warning("⚠️ No webhook URL found, using polling mode")
        # Hanya delete webhook, tidak pakai updater
        await app.bot.delete_webhook()
        return "polling"
    
    try:
        # Hapus webhook lama
        await app.bot.delete_webhook()
        
        # Set webhook baru
        success = await app.bot.set_webhook(
            url=webhook_url,
            allowed_updates=['message', 'callback_query'],
            drop_pending_updates=True,
            max_connections=40
        )
        
        if success:
            logger.info(f"✅ Webhook set to: {webhook_url}")
            info = await app.bot.get_webhook_info()
            logger.info(f"📊 Webhook info: {info.url}")
            return webhook_url
        else:
            logger.error("❌ Failed to set webhook")
            return "polling"
            
    except Exception as e:
        logger.error(f"❌ Webhook error: {e}")
        logger.warning("⚠️ Falling back to polling mode")
        await app.bot.delete_webhook()
        return "polling"


async def delete_webhook(app: Application):
    """Delete webhook - fungsi yang di-import di __init__.py"""
    try:
        await app.bot.delete_webhook(drop_pending_updates=True)
        logger.info("✅ Webhook deleted")
    except Exception as e:
        logger.error(f"❌ Error deleting webhook: {e}")
