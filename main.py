#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
GADIS V81 - MAIN ENTRY POINT
=============================================================================
Native python-telegram-bot v20+ dengan polling mode
"""

import asyncio
import sys
import traceback
from pathlib import Path

# Tambahkan path ke sys.path
sys.path.insert(0, str(Path(__file__).parent))

from config import settings
from utils.logger import setup_logging

# Setup logging
logger = setup_logging("gadis_v81")

print("="*70)
print("    GADIS V81 - ULTIMATE AI BOT")
print("    Premium Edition - All Features")
print("="*70)
print(f"📊 Database: {settings.db.name} @ {settings.db.host}")
print(f"🤖 AI Model: {settings.ai.primary_model}")
print(f"👑 Admin ID: {settings.admin_id}")
print(f"🔞 Sexual Features: {'ENABLED' if settings.sexual.enabled else 'DISABLED'}")
print(f"🌍 Public Areas: {settings.sexual.max_positions} positions")
print(f"🎯 Bot Initiative: {'ON' if settings.sexual.bot_initiative_enabled else 'OFF'}")
print("="*70)


def init_database():
    """Initialize database synchronously"""
    try:
        from database.connection import init_db_sync
        init_db_sync()
        logger.info("✅ Database initialized")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise


def init_redis():
    """Initialize Redis synchronously"""
    try:
        from cache.redis_client import init_redis_sync
        init_redis_sync()
        logger.info("✅ Redis initialized")
    except Exception as e:
        logger.error(f"❌ Redis initialization failed: {e}")
        # Non-critical, continue


def init_components():
    """Initialize all components - SYNCHRONOUS"""
    logger.info("🚀 Starting GADIS V81...")
    
    # Initialize database (synchronous)
    init_database()
    
    # Initialize Redis (synchronous)
    init_redis()
    
    # Create bot application (synchronous)
    from bot.application import create_application
    app = create_application()  # ← ini synchronous!
    logger.info("✅ Bot application created")
    
    # Setup webhook (synchronous - tapi panggil async function)
    from bot.webhook import setup_webhook_sync
    mode = setup_webhook_sync(app)
    logger.info(f"✅ Webhook URL: {mode}")
    
    logger.info("🚀 GADIS V81 is ready!")
    
    return app


def main():
    """Main function - fully synchronous"""
    try:
        # Initialize all components synchronously
        app = init_components()
        
        logger.info("📡 Starting bot in polling mode...")
        
        # Run polling - blocking synchronous call (PTB v20+ style)
        # Ini akan manage event loop sendiri
        app.run_polling(
            allowed_updates=['message', 'callback_query'],
            drop_pending_updates=True
        )
        
    except KeyboardInterrupt:
        logger.info("👋 Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        traceback.print_exc()
        sys.exit(1)
    finally:
        logger.info("👋 Goodbye!")


if __name__ == "__main__":
    main()
