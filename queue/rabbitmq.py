#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
RABBITMQ CLIENT FOR BACKGROUND TASKS
=============================================================================
Message queue untuk async processing dan background jobs
"""

import json
import asyncio
from typing import Optional, Callable, Any, Dict
from datetime import datetime

try:
    import aio_pika
    RABBITMQ_AVAILABLE = True
except ImportError:
    RABBITMQ_AVAILABLE = False

from config import settings
from utils.logger import logger


class RabbitMQClient:
    """
    RabbitMQ client untuk background task processing
    - Async connection
    - Queue management
    - Publisher/Consumer pattern
    """
    
    def __init__(self):
        self.connection = None
        self.channel = None
        self._connected = False
        self._consumers = {}
    
    async def initialize(self):
        """Initialize RabbitMQ connection"""
        if self._connected:
            return
        
        if not RABBITMQ_AVAILABLE:
            logger.warning("RabbitMQ not available, using fallback")
            return
        
        try:
            # Connect to RabbitMQ
            self.connection = await aio_pika.connect_robust(
                settings.rabbitmq.url,
                timeout=10
            )
            
            # Create channel
            self.channel = await self.connection.channel()
            await self.channel.set_qos(prefetch_count=10)
            
            self._connected = True
            logger.info(f"✅ RabbitMQ connected: {settings.rabbitmq.host}:{settings.rabbitmq.port}")
            
        except Exception as e:
            logger.error(f"❌ RabbitMQ connection failed: {e}")
            self.connection = None
            self.channel = None
    
    async def close(self):
        """Close RabbitMQ connection"""
        if self.connection:
            await self.connection.close()
            self._connected = False
            logger.info("✅ RabbitMQ connection closed")
    
    async def publish(self, queue_name: str, message: Dict[str, Any], 
                     priority: int = 0, delay: int = 0) -> bool:
        """
        Publish message to queue
        """
        if not self._connected:
            await self.initialize()
        
        if not self.channel:
            logger.error("RabbitMQ channel not available")
            return False
        
        try:
            # Declare queue
            queue = await self.channel.declare_queue(
                queue_name,
                durable=True,
                arguments={
                    'x-max-priority': 10,
                    'x-message-ttl': 86400000  # 24 hours
                }
            )
            
            # Prepare message
            message_body = json.dumps({
                'data': message,
                'timestamp': datetime.now().isoformat(),
                'priority': priority
            }).encode()
            
            # Publish
            await self.channel.default_exchange.publish(
                aio_pika.Message(
                    body=message_body,
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                    priority=priority,
                    expiration=str(delay * 1000) if delay > 0 else None
                ),
                routing_key=queue_name
            )
            
            logger.debug(f"📤 Published message to {queue_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to publish message: {e}")
            return False
    
    async def consume(self, queue_name: str, callback: Callable, 
                     prefetch_count: int = 1):
        """
        Consume messages from queue
        """
        if not self._connected:
            await self.initialize()
        
        if not self.channel:
            logger.error("RabbitMQ channel not available")
            return
        
        try:
            # Declare queue
            queue = await self.channel.declare_queue(
                queue_name,
                durable=True
            )
            
            # Set prefetch count
            await self.channel.set_qos(prefetch_count=prefetch_count)
            
            # Start consuming
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        try:
                            # Parse message
                            body = json.loads(message.body.decode())
                            
                            # Execute callback
                            await callback(body['data'], body)
                            
                        except Exception as e:
                            logger.error(f"Error processing message: {e}")
                            # Reject and requeue
                            await message.reject(requeue=True)
            
            logger.info(f"👂 Started consuming from {queue_name}")
            
        except Exception as e:
            logger.error(f"Failed to consume from {queue_name}: {e}")
    
    async def get_queue_size(self, queue_name: str) -> Optional[int]:
        """Get number of messages in queue"""
        if not self.channel:
            return None
        
        try:
            queue = await self.channel.declare_queue(
                queue_name,
                durable=True,
                passive=True
            )
            return queue.declaration_result.message_count
        except Exception as e:
            logger.error(f"Failed to get queue size: {e}")
            return None
    
    async def purge_queue(self, queue_name: str) -> bool:
        """Delete all messages in queue"""
        if not self.channel:
            return False
        
        try:
            queue = await self.channel.declare_queue(
                queue_name,
                durable=True,
                passive=True
            )
            await queue.purge()
            logger.info(f"🧹 Purged queue: {queue_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to purge queue: {e}")
            return False
    
    async def delete_queue(self, queue_name: str) -> bool:
        """Delete queue"""
        if not self.channel:
            return False
        
        try:
            await self.channel.queue_delete(queue_name)
            logger.info(f"🗑️ Deleted queue: {queue_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete queue: {e}")
            return False


class TaskQueue:
    """
    Task queue untuk background jobs
    """
    
    def __init__(self, rabbitmq: RabbitMQClient):
        self.rabbitmq = rabbitmq
    
    async def publish_task(self, task_name: str, data: Dict[str, Any], 
                          priority: int = 0, delay: int = 0) -> bool:
        """Publish task to queue"""
        queue_map = {
            'memory_consolidation': 'memory_tasks',
            'backup': 'backup_tasks',
            'analytics': 'analytics_tasks',
            'email': 'email_tasks',
            'cleanup': 'cleanup_tasks'
        }
        
        queue_name = queue_map.get(task_name, 'default_tasks')
        
        message = {
            'task': task_name,
            'data': data,
            'priority': priority
        }
        
        return await self.rabbitmq.publish(queue_name, message, priority, delay)
    
    async def subscribe_memory_tasks(self, callback: Callable):
        """Subscribe to memory consolidation tasks"""
        await self.rabbitmq.consume('memory_tasks', callback)
    
    async def subscribe_backup_tasks(self, callback: Callable):
        """Subscribe to backup tasks"""
        await self.rabbitmq.consume('backup_tasks', callback)
    
    async def subscribe_analytics_tasks(self, callback: Callable):
        """Subscribe to analytics tasks"""
        await self.rabbitmq.consume('analytics_tasks', callback)


# ===== GLOBAL INSTANCES =====
rabbitmq_client = RabbitMQClient()
task_queue = TaskQueue(rabbitmq_client)


__all__ = [
    'RabbitMQClient',
    'TaskQueue',
    'rabbitmq_client',
    'task_queue'
]
