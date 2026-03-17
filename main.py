#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
GADIS V81 - MAIN ENTRY POINT
=============================================================================
Native python-telegram-bot webhook dengan semua fitur V81
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
print(f"👑 Admin ID: {settings.admin_id or 'Not set'}")
print(f"🔞 Sexual Features: {'ENABLED' if settings.sexual.enabled else 'DISABLED'}")
print(f"🌍 Public Areas: {settings.sexual.max_positions} positions")
print(f"🎯 Bot Initiative: {'ON' if settings.sexual.bot_initiative_enabled else 'OFF'}")
print("="*70)


class Application:
    """Main application class"""
    
    def __init__(self):
        self.bot_app = None
        self.ws_server = None
        self.background_tasks = []
        self.is_running = True
        
    async def startup(self):
        """Initialize all components"""
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
        self.bot_app = await create_application()
        logger.info("✅ Bot application created")
        
        # Setup webhook
        from bot.webhook import setup_webhook
        webhook_url = await setup_webhook(self.bot_app)
        logger.info(f"✅ Webhook URL: {webhook_url}")
        
        # Start WebSocket server (optional)
        if hasattr(settings, 'ws_host') and settings.ws_host:
            try:
                from ws.server import start_websocket_server
                self.ws_server = await start_websocket_server()
                logger.info(f"✅ WebSocket server started on {settings.ws_host}:{settings.ws_port}")
            except (ImportError, AttributeError) as e:
                logger.debug(f"WebSocket server not available: {e}")
        
        # Start background tasks
        self.background_tasks = await self._start_background_tasks()
        logger.info(f"✅ Background tasks started: {len(self.background_tasks)}")
        
        logger.info("🚀 GADIS V81 is ready!")
        
    async def _start_background_tasks(self):
        """Start all background tasks"""
        tasks = []
        
        # Memory consolidation task (if available)
        try:
            from memory.consolidation import consolidation_loop
            tasks.append(asyncio.create_task(consolidation_loop()))
        except (ImportError, AttributeError):
            logger.debug("Memory consolidation not available")
        
        # Backup task (if available)
        if settings.backup_enabled:
            try:
                from backup.automated import backup_loop
                tasks.append(asyncio.create_task(backup_loop()))
            except (ImportError, AttributeError):
                logger.debug("Backup system not available")
        
        # Analytics task (if available)
        try:
            from analytics.collector import analytics_loop
            tasks.append(asyncio.create_task(analytics_loop()))
        except (ImportError, AttributeError):
            logger.debug("Analytics not available")
        
        # Metrics server (if available)
        if hasattr(settings, 'prometheus_port') and settings.prometheus_port:
            try:
                from monitoring.metrics import start_metrics_server
                tasks.append(asyncio.create_task(start_metrics_server()))
            except (ImportError, AttributeError):
                logger.debug("Metrics server not available")
        
        return tasks
    
    async def shutdown(self):
        """Graceful shutdown"""
        logger.info("🛑 Shutting down GADIS V81...")
        self.is_running = False
        
        # Cancel background tasks
        for task in self.background_tasks:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
        
        # Stop bot application
        if self.bot_app:
            try:
                # Stop the bot properly
                await self.bot_app.stop()
                await self.bot_app.shutdown()
            except Exception as e:
                logger.error(f"Error stopping bot: {e}")
        
        # Stop WebSocket server
        if self.ws_server:
            try:
                self.ws_server.close()
                await self.ws_server.wait_closed()
            except Exception as e:
                logger.error(f"Error stopping WebSocket: {e}")
        
        # Close database connections
        try:
            from database.connection import close_db
            await close_db()
            logger.info("✅ Database connection closed")
        except Exception as e:
            logger.error(f"Error closing database: {e}")
        
        # Close Redis
        try:
            from cache.redis_client import close_redis
            await close_redis()
            logger.info("✅ Redis connection closed")
        except Exception as e:
            logger.error(f"Error closing Redis: {e}")
        
        logger.info("👋 Goodbye!")
    
    async def run(self):
        """Run the application"""
        try:
            await self.startup()
            
            # Run based on webhook setup
            if self.bot_app:
                # Cek hasil dari setup_webhook
                from bot.webhook import setup_webhook
                webhook_result = await setup_webhook(self.bot_app)
                
                if webhook_result == "polling":
                    # Mode polling
                    logger.info("📡 Starting bot in polling mode...")
                    
                    # HAPUS WEBHOOK DULU UNTUK MEMASTIKAN
                    await self.bot_app.bot.delete_webhook(drop_pending_updates=True)
                    
                    # Run polling
                    await self.bot_app.run_polling(
                        allowed_updates=['message', 'callback_query'],
                        drop_pending_updates=True,
                        close_loop=False
                    )
                else:
                    # Mode webhook
                    logger.info(f"🌐 Starting bot in webhook mode on port {settings.webhook.port}...")
                    
                    # Run webhook
                    await self.bot_app.run_webhook(
                        listen="0.0.0.0",
                        port=settings.webhook.port,
                        url_path=settings.webhook.path,
                        webhook_url=webhook_result,
                        close_loop=False
                    )
        except KeyboardInterrupt:
            logger.info("👋 Bot stopped by user")
        except Exception as e:
            logger.error(f"❌ Fatal error: {e}")
            # Import exception handler
            from utils.exceptions import exception_handler
            await exception_handler.handle(e, {"phase": "runtime"})
        finally:
            # Shutdown only if still running
            if self.is_running:
                await self.shutdown()


# ===== SIGNAL HANDLERS =====

def handle_signal(sig, frame):
    """Handle shutdown signals"""
    logger.info(f"Received signal {sig}, shutting down...")
    
    # Set flag to stop
    app.is_running = False


# ===== MAIN =====

if __name__ == "__main__":
    app = Application()
    
    # Register signal handlers
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)
    
    # Simple run with asyncio
    try:
        asyncio.run(app.run())
    except KeyboardInterrupt:
        logger.info("👋 Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
