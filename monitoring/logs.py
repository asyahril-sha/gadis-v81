#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
LOG MANAGEMENT
=============================================================================
Integrasi dengan ELK Stack untuk centralized logging
"""

import json
from datetime import datetime
from typing import Dict, List, Optional

try:
    from elasticsearch import Elasticsearch
    ELASTIC_AVAILABLE = True
except ImportError:
    ELASTIC_AVAILABLE = False

from utils.logger import logger
from config import settings


class LogManager:
    """Manager untuk log aggregation dengan ELK"""
    
    def __init__(self):
        self.es_client = None
        self.index_prefix = "gadis-logs-"
        self.buffer = []
        self.buffer_size = 100
        
        if ELASTIC_AVAILABLE and settings.elasticsearch_url:
            self._init_elasticsearch()
    
    def _init_elasticsearch(self):
        """Initialize Elasticsearch connection"""
        try:
            self.es_client = Elasticsearch(settings.elasticsearch_url)
            logger.info("✅ Elasticsearch connected")
        except Exception as e:
            logger.error(f"Failed to connect to Elasticsearch: {e}")
    
    def log(self, level: str, message: str, **kwargs):
        """Send log to Elasticsearch"""
        log_entry = {
            '@timestamp': datetime.now().isoformat(),
            'level': level,
            'message': message,
            'service': 'gadis-v81',
            **kwargs
        }
        
        # Add to buffer
        self.buffer.append(log_entry)
        
        # Flush if buffer full
        if len(self.buffer) >= self.buffer_size:
            self.flush()
    
    def flush(self):
        """Flush buffer to Elasticsearch"""
        if not self.buffer:
            return
        
        if self.es_client:
            try:
                actions = []
                for entry in self.buffer:
                    action = {
                        "_index": f"{self.index_prefix}{datetime.now().strftime('%Y.%m.%d')}",
                        "_source": entry
                    }
                    actions.append(action)
                
                # Bulk insert
                self.es_client.bulk(operations=actions)
                logger.debug(f"Flushed {len(self.buffer)} logs to Elasticsearch")
                
            except Exception as e:
                logger.error(f"Failed to flush logs: {e}")
        
        self.buffer.clear()
    
    def search(self, query: str, size: int = 100) -> List[Dict]:
        """Search logs in Elasticsearch"""
        if not self.es_client:
            return []
        
        try:
            result = self.es_client.search(
                index=f"{self.index_prefix}*",
                body={
                    "query": {
                        "query_string": {
                            "query": query
                        }
                    },
                    "sort": [{"@timestamp": "desc"}],
                    "size": size
                }
            )
            
            return [hit['_source'] for hit in result['hits']['hits']]
        
        except Exception as e:
            logger.error(f"Failed to search logs: {e}")
            return []
    
    def get_stats(self) -> Dict:
        """Get log statistics"""
        if not self.es_client:
            return {}
        
        try:
            result = self.es_client.search(
                index=f"{self.index_prefix}*",
                body={
                    "aggs": {
                        "logs_per_day": {
                            "date_histogram": {
                                "field": "@timestamp",
                                "calendar_interval": "day"
                            }
                        },
                        "logs_per_level": {
                            "terms": {
                                "field": "level.keyword"
                            }
                        }
                    },
                    "size": 0
                }
            )
            
            return {
                'total_logs': result['hits']['total']['value'],
                'logs_per_day': result['aggregations']['logs_per_day']['buckets'],
                'logs_per_level': result['aggregations']['logs_per_level']['buckets']
            }
        
        except Exception as e:
            logger.error(f"Failed to get log stats: {e}")
            return {}


__all__ = ['LogManager']
