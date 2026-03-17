#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
GADIS V81 - MAIN ENTRY POINT
=============================================================================
Native python-telegram-bot dengan polling mode
"""

import asyncio
import sys
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


async def main():
    """Main function"""
    try:
        logger.info("🚀 Starting GADIS V81...")
        
        # Initialize database
        from database.connection import init_db
        await init_db()
        logger.info("✅ Database initialized")
        
        # Initialize Redis (mock)
        from cache.redis_client import init_redis
        await init_redis()
        logger.info("✅ Redis initialized")
        
        # Create bot application
        from bot.application import create_application
        app = await create_application()
        logger.info("✅ Bot application created")
        
        # Setup webhook (polling mode)
        from bot.webhook import setup_webhook
        mode = await setup_webhook(app)
        logger.info(f"✅ Webhook URL: {mode}")
        
        logger.info("🚀 GADIS V81 is ready!")
        logger.info("📡 Starting bot in polling mode...")
        
        # Start polling - INI AKAN BLOCKING
        await app.run_polling(
            allowed_updates=['message', 'callback_query'],
            drop_pending_updates=True
        )
        
    except KeyboardInterrupt:
        logger.info("👋 Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        raise
    finally:
        logger.info("👋 Goodbye!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
