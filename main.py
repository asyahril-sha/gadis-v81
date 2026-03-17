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
import signal
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
    logger.info("🚀 Starting GADIS V81...")
    
    try:
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
        
        # Start background tasks
        background_tasks = []
        try:
            from memory.consolidation import consolidation_loop
            background_tasks.append(asyncio.create_task(consolidation_loop()))
        except:
            pass
        
        logger.info(f"✅ Background tasks started: {len(background_tasks)}")
        logger.info("🚀 GADIS V81 is ready!")
        
        # Start polling - INI AKAN BLOCKING SAMPAI BOT BERHENTI
        logger.info("📡 Starting bot in polling mode...")
        await app.run_polling(
            allowed_updates=['message', 'callback_query'],
            drop_pending_updates=True
        )
        
    except asyncio.CancelledError:
        logger.info("👋 Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        raise
    finally:
        # Cleanup
        logger.info("🛑 Shutting down...")
        
        # Cancel background tasks
        for task in background_tasks:
            task.cancel()
        
        # Close database
        try:
            from database.connection import close_db
            await close_db()
        except:
            pass
        
        # Close Redis
        try:
            from cache.redis_client import close_redis
            await close_redis()
        except:
            pass
        
        logger.info("👋 Goodbye!")


def handle_signal():
    """Handle shutdown signals"""
    logger.info("Received signal, shutting down...")
    # Cancel all tasks
    for task in asyncio.all_tasks():
        task.cancel()


if __name__ == "__main__":
    # Register signal handlers
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, handle_signal)
    
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        logger.info("👋 Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
    finally:
        try:
            # Cancel all tasks
            for task in asyncio.all_tasks(loop):
                task.cancel()
            
            # Run loop one last time to let tasks finish
            loop.run_until_complete(asyncio.sleep(0.1))
            loop.close()
        except:
            pass
        
        logger.info("✅ Shutdown complete")
