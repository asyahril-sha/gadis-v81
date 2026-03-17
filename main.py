#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
GADIS V81 - MAIN ENTRY POINT
=============================================================================
Native python-telegram-bot webhook dengan semua fitur V81
- PostgreSQL, Redis, RabbitMQ
- Multi-model AI
- Sexual systems lengkap
- Public areas
- Bot initiative
"""

import asyncio
import sys
import signal
from pathlib import Path

# Tambahkan path ke sys.path
sys.path.insert(0, str(Path(__file__).parent))

from config import settings
from utils.logger import setup_logging
from utils.exceptions import global_exception_handler

# Setup logging
logger = setup_logging("gadis_v81")

print("="*70)
print("    GADIS V81 - ULTIMATE AI BOT")
print("    Premium Edition - All Features")
print("="*70)
print(f"📊 Database: {settings.db.name} @ {settings.db.host}")
print(f"🤖 AI Model: {settings.ai.primary_model}")
print(f"👑 Admin ID: {settings.admin_id or 'Not set'}")
print(f"🔞 Sexual Features: ENABLED")
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
        
        # Initialize Redis
        from cache.redis_client import init_redis
        await init_redis()
        logger.info("✅ Redis initialized")
        
        # Initialize RabbitMQ
        from queue.rabbitmq import init_rabbitmq
        await init_rabbitmq()
        logger.info("✅ RabbitMQ initialized")
        
        # Create bot application
        from bot.application import create_application
        self.bot_app = await create_application()
        logger.info("✅ Bot application created")
        
        # Setup webhook
        from bot.webhook import setup_webhook
        webhook_url = await setup_webhook(self.bot_app)
        logger.info(f"✅ Webhook URL: {webhook_url}")
        
        # Start WebSocket server
        if settings.ws_host:
            from ws.server import start_websocket_server
            self.ws_server = await start_websocket_server()
            logger.info(f"✅ WebSocket server started on {settings.ws_host}:{settings.ws_port}")
        
        # Start background tasks
        self.background_tasks = await self._start_background_tasks()
        logger.info(f"✅ Background tasks started: {len(self.background_tasks)}")
        
        logger.info("🚀 GADIS V81 is ready!")
        
    async def _start_background_tasks(self):
        """Start all background tasks"""
        tasks = []
        
        # Memory consolidation task
        from memory.consolidation import consolidation_loop
        tasks.append(asyncio.create_task(consolidation_loop()))
        
        # Backup task
        if settings.backup_enabled:
            from backup.automated import backup_loop
            tasks.append(asyncio.create_task(backup_loop()))
        
        # Analytics task
        from analytics.collector import analytics_loop
        tasks.append(asyncio.create_task(analytics_loop()))
        
        # Metrics server
        if settings.prometheus_port:
            from monitoring.metrics import start_metrics_server
            tasks.append(asyncio.create_task(start_metrics_server()))
        
        return tasks
    
    async def shutdown(self):
        """Graceful shutdown"""
        logger.info("🛑 Shutting down GADIS V81...")
        self.is_running = False
        
        # Cancel background tasks
        for task in self.background_tasks:
            task.cancel()
        
        # Stop bot application
        if self.bot_app:
            await self.bot_app.stop()
            await self.bot_app.shutdown()
        
        # Stop WebSocket server
        if self.ws_server:
            self.ws_server.close()
            await self.ws_server.wait_closed()
        
        # Close database connections
        from database.connection import close_db
        await close_db()
        
        # Close Redis
        from cache.redis_client import close_redis
        await close_redis()
        
        # Close RabbitMQ
        from queue.rabbitmq import close_rabbitmq
        await close_rabbitmq()
        
        logger.info("👋 Goodbye!")
    
    async def run(self):
        """Run the application"""
        try:
            await self.startup()
            
            # Run webhook (blocking)
            if self.bot_app:
                await self.bot_app.run_webhook(
                    listen="0.0.0.0",
                    port=settings.webhook.port,
                    url_path=settings.webhook.path,
                    webhook_url=settings.webhook.url
                )
        except KeyboardInterrupt:
            await self.shutdown()
        except Exception as e:
            logger.error(f"❌ Fatal error: {e}")
            await global_exception_handler.handle(e, {"phase": "runtime"})
            await self.shutdown()
            sys.exit(1)


# ===== SIGNAL HANDLERS =====

def handle_signal(sig, frame):
    """Handle shutdown signals"""
    logger.info(f"Received signal {sig}, shutting down...")
    asyncio.create_task(app.shutdown())
    sys.exit(0)


# ===== MAIN =====

if __name__ == "__main__":
    app = Application()
    
    # Register signal handlers
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)
    
    # Run application
    asyncio.run(app.run())
