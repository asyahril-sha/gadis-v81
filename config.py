#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
KONFIGURASI GADIS V81 - PYDANTIC SETTINGS
=============================================================================
Menggunakan Pydantic untuk validasi dan type safety dengan semua fitur V81
"""

import os
from typing import Optional, Dict, Any, List
from pydantic import Field, validator, BaseModel
from pydantic_settings import BaseSettings
from pathlib import Path


class DatabaseSettings(BaseModel):
    """Database configuration"""
    host: str = Field("localhost", env='DB_HOST')
    port: int = Field(5432, env='DB_PORT')
    name: str = Field("gadis_v81", env='DB_NAME')
    user: str = Field("postgres", env='DB_USER')
    password: str = Field("postgres", env='DB_PASSWORD')
    pool_size: int = Field(20, env='DB_POOL_SIZE')
    max_overflow: int = Field(40, env='DB_MAX_OVERFLOW')
    
    @property
    def url(self) -> str:
        """Get database URL"""
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class RedisSettings(BaseModel):
    """Redis cache configuration"""
    host: str = Field("localhost", env='REDIS_HOST')
    port: int = Field(6379, env='REDIS_PORT')
    password: Optional[str] = Field(None, env='REDIS_PASSWORD')
    db: int = Field(0, env='REDIS_DB')
    
    @property
    def url(self) -> str:
        """Get Redis URL"""
        if self.password:
            return f"redis://:{self.password}@{self.host}:{self.port}/{self.db}"
        return f"redis://{self.host}:{self.port}/{self.db}"


class RabbitMQSettings(BaseModel):
    """RabbitMQ configuration"""
    host: str = Field("localhost", env='RABBITMQ_HOST')
    port: int = Field(5672, env='RABBITMQ_PORT')
    user: str = Field("guest", env='RABBITMQ_USER')
    password: str = Field("guest", env='RABBITMQ_PASSWORD')
    
    @property
    def url(self) -> str:
        """Get RabbitMQ URL"""
        return f"amqp://{self.user}:{self.password}@{self.host}:{self.port}/"


class AISettings(BaseModel):
    """AI model configuration"""
    temperature: float = Field(0.9, env='AI_TEMPERATURE')
    max_tokens: int = Field(500, env='AI_MAX_TOKENS')
    timeout: int = Field(30, env='AI_TIMEOUT')
    primary_model: str = Field("deepseek", env='AI_MODEL_PRIMARY')
    secondary_model: str = Field("claude", env='AI_MODEL_SECONDARY')
    
    @validator('temperature')
    def validate_temperature(cls, v):
        if v < 0 or v > 1:
            raise ValueError("Temperature must be between 0 and 1")
        return v


class RateLimitSettings(BaseModel):
    """Rate limiting configuration"""
    messages_per_minute: int = Field(10, env='RATE_LIMIT_MESSAGES')
    window_seconds: int = Field(60, env='RATE_LIMIT_WINDOW')
    burst: int = Field(5, env='RATE_LIMIT_BURST')


class SexualSettings(BaseModel):
    """Sexual content configuration - V81 FEATURES"""
    enabled: bool = Field(True, env='SEXUAL_CONTENT_ENABLED')
    max_positions: int = Field(50, env='MAX_POSITIONS')
    max_areas: int = Field(100, env='MAX_AREAS')
    max_activities: int = Field(50, env='MAX_ACTIVITIES')
    climax_variations: int = Field(200, env='CLIMAX_VARIATIONS')
    public_risk_enabled: bool = Field(True, env='PUBLIC_RISK_ENABLED')
    bot_initiative_enabled: bool = Field(True, env='BOT_INITIATIVE_ENABLED')
    aftercare_enabled: bool = Field(True, env='AFTERCARE_ENABLED')


class WebhookSettings(BaseModel):
    """Webhook configuration"""
    url: Optional[str] = Field(None, env='WEBHOOK_URL')
    port: int = Field(8080, env='WEBHOOK_PORT')
    path: str = Field("/webhook", env='WEBHOOK_PATH')


class Settings(BaseSettings):
    """
    Main settings class - semua konfigurasi terpusat di sini
    """
    
    # API Keys
    deepseek_api_key: str = Field(..., env='DEEPSEEK_API_KEY')
    telegram_token: str = Field(..., env='TELEGRAM_TOKEN')
    admin_id: int = Field(0, env='ADMIN_ID')
    
    # Database
    db: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()
    rabbitmq: RabbitMQSettings = RabbitMQSettings()
    
    # AI
    ai: AISettings = AISettings()
    
    # Rate Limiting
    rate_limit: RateLimitSettings = RateLimitSettings()
    
    # Sexual Features (V81)
    sexual: SexualSettings = SexualSettings()
    
    # Webhook
    webhook: WebhookSettings = WebhookSettings()
    
    # WebSocket
    ws_host: str = Field("0.0.0.0", env='WS_HOST')
    ws_port: int = Field(8765, env='WS_PORT')
    
    # Paths
    base_dir: Path = Path(__file__).parent
    log_dir: Path = base_dir / "logs"
    memory_dir: Path = base_dir / "memory_storage"
    backup_dir: Path = base_dir / "backups"
    vector_db_dir: Path = base_dir / "vector_db"
    
    # Monitoring
    prometheus_port: int = Field(9090, env='PROMETHEUS_PORT')
    grafana_port: int = Field(3000, env='GRAFANA_PORT')
    
    # Backup
    backup_enabled: bool = Field(True, env='BACKUP_ENABLED')
    backup_interval: int = Field(3600, env='BACKUP_INTERVAL')
    backup_retention_days: int = Field(7, env='BACKUP_RETENTION_DAYS')
    backup_s3_bucket: Optional[str] = Field(None, env='BACKUP_S3_BUCKET')
    
    # Security
    encryption_key: Optional[str] = Field(None, env='ENCRYPTION_KEY')
    jwt_secret: Optional[str] = Field(None, env='JWT_SECRET')
    cors_origins: str = Field("*", env='CORS_ORIGINS')
    
    # Railway
    railway_public_domain: Optional[str] = Field(None, env='RAILWAY_PUBLIC_DOMAIN')
    railway_static_url: Optional[str] = Field(None, env='RAILWAY_STATIC_URL')
    
    @validator('deepseek_api_key')
    def validate_deepseek_key(cls, v):
        if not v or v == "your_deepseek_api_key_here":
            raise ValueError("DEEPSEEK_API_KEY tidak boleh kosong")
        return v
    
    @validator('telegram_token')
    def validate_telegram_token(cls, v):
        if not v or v == "your_telegram_bot_token_here":
            raise ValueError("TELEGRAM_TOKEN tidak boleh kosong")
        if ':' not in v:
            raise ValueError("Format TELEGRAM_TOKEN tidak valid")
        return v
    
    def create_directories(self):
        """Create all necessary directories"""
        self.log_dir.mkdir(exist_ok=True)
        self.memory_dir.mkdir(exist_ok=True)
        self.backup_dir.mkdir(exist_ok=True)
        self.vector_db_dir.mkdir(exist_ok=True)
        
        # Create subdirectories for sexual content
        sexual_dir = self.base_dir / "sexual" / "data"
        sexual_dir.mkdir(exist_ok=True, parents=True)
        
        print(f"✅ Directories created")
        return self
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        validate_assignment = True


# ===== GLOBAL SETTINGS INSTANCE =====
settings = Settings()
settings.create_directories()

print("="*70)
print("🚀 GADIS V81 - SETTINGS LOADED")
print("="*70)
print(f"📊 Database: {settings.db.name} @ {settings.db.host}")
print(f"🤖 AI Model: {settings.ai.primary_model}")
print(f"👑 Admin ID: {settings.admin_id or 'Not set'}")
print(f"🔞 Sexual Content: {'ENABLED' if settings.sexual.enabled else 'DISABLED'}")
print(f"  • Max Positions: {settings.sexual.max_positions}")
print(f"  • Max Areas: {settings.sexual.max_areas}")
print(f"  • Climax Variations: {settings.sexual.climax_variations}")
print(f"  • Public Risk: {'ON' if settings.sexual.public_risk_enabled else 'OFF'}")
print(f"  • Bot Initiative: {'ON' if settings.sexual.bot_initiative_enabled else 'OFF'}")
print("="*70)


# ===== EXPORT =====
__all__ = ['settings', 'DatabaseSettings', 'RedisSettings', 'RabbitMQSettings', 
           'AISettings', 'SexualSettings']
