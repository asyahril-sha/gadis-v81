#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
CLOUD VECTOR DATABASE
=============================================================================
Pinecone/Weaviate integration untuk unlimited memory storage
"""

import os
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime

# Coba import pinecone
try:
    import pinecone
    PINECONE_AVAILABLE = True
except ImportError:
    PINECONE_AVAILABLE = False

# Coba import weaviate
try:
    import weaviate
    WEAVIATE_AVAILABLE = True
except ImportError:
    WEAVIATE_AVAILABLE = False

from config import settings
from utils.logger import logger


class CloudVectorMemory:
    """
    Cloud vector database untuk memory skala besar
    Support Pinecone dan Weaviate
    """
    
    def __init__(self, user_id: int, provider: str = "pinecone"):
        self.user_id = user_id
        self.provider = provider
        self.index_name = f"user-{user_id}"
        self.client = None
        self.index = None
        self.initialized = False
        
    async def initialize(self):
        """Initialize cloud vector database connection"""
        if self.initialized:
            return
        
        if self.provider == "pinecone":
            await self._init_pinecone()
        elif self.provider == "weaviate":
            await self._init_weaviate()
        else:
            logger.error(f"Unknown provider: {self.provider}")
            return
        
        self.initialized = True
        logger.info(f"✅ CloudVectorMemory initialized for user {self.user_id} with {self.provider}")
    
    async def _init_pinecone(self):
        """Initialize Pinecone connection"""
        if not PINECONE_AVAILABLE:
            logger.warning("Pinecone not available, using fallback")
            return
        
        try:
            # Initialize pinecone
            pinecone.init(
                api_key=os.getenv("PINECONE_API_KEY", ""),
                environment=os.getenv("PINECONE_ENVIRONMENT", "gcp-starter")
            )
            
            # Check if index exists
            if self.index_name not in pinecone.list_indexes():
                # Create index
                pinecone.create_index(
                    name=self.index_name,
                    dimension=384,  # all-MiniLM-L6-v2 dimension
                    metric="cosine",
                    pods=1,
                    pod_type="p1.x1"
                )
                logger.info(f"✅ Created Pinecone index: {self.index_name}")
            
            # Connect to index
            self.index = pinecone.Index(self.index_name)
            logger.info(f"✅ Connected to Pinecone index: {self.index_name}")
            
        except Exception as e:
            logger.error(f"Failed to initialize Pinecone: {e}")
    
    async def _init_weaviate(self):
        """Initialize Weaviate connection"""
        if not WEAVIATE_AVAILABLE:
            logger.warning("Weaviate not available, using fallback")
            return
        
        try:
            # Connect to Weaviate
            self.client = weaviate.Client(
                url=os.getenv("WEAVIATE_URL", "http://localhost:8080"),
                auth_client_secret=weaviate.AuthApiKey(
                    api_key=os.getenv("WEAVIATE_API_KEY", "")
                )
            )
            
            # Check if class exists
            class_name = f"User{self.user_id}Memory"
            
            if not self.client.schema.exists(class_name):
                # Create class
                class_obj = {
                    "class": class_name,
                    "vectorizer": "none",  # We provide our own vectors
                    "properties": [
                        {"name": "content", "dataType": ["text"]},
                        {"name": "type", "dataType": ["string"]},
                        {"name": "importance", "dataType": ["number"]},
                        {"name": "emotion", "dataType": ["string"]},
                        {"name": "timestamp", "dataType": ["date"]},
                        {"name": "metadata", "dataType": ["object"]}
                    ]
                }
                self.client.schema.create_class(class_obj)
                logger.info(f"✅ Created Weaviate class: {class_name}")
            
            logger.info(f"✅ Connected to Weaviate")
            
        except Exception as e:
            logger.error(f"Failed to initialize Weaviate: {e}")
    
    async def add_memory(self, content: str, memory_type: str,
                        embedding: List[float], importance: float = 0.5,
                        emotion: str = None, metadata: Dict = None) -> str:
        """Add memory to cloud vector DB"""
        await self.initialize()
        
        memory_id = f"mem_{int(datetime.now().timestamp())}_{hash(content) % 10000}"
        
        if self.provider == "pinecone" and self.index:
            try:
                # Prepare metadata
                meta = {
                    'content': content[:1000],  # Truncate for storage
                    'type': memory_type,
                    'importance': importance,
                    'emotion': emotion or 'neutral',
                    'timestamp': datetime.now().isoformat(),
                    'user_id': self.user_id
                }
                if metadata:
                    meta.update(metadata)
                
                # Upsert to Pinecone
                self.index.upsert(
                    vectors=[(memory_id, embedding, meta)]
                )
                
            except Exception as e:
                logger.error(f"Failed to add to Pinecone: {e}")
        
        elif self.provider == "weaviate" and self.client:
            try:
                # Prepare data
                data = {
                    "content": content,
                    "type": memory_type,
                    "importance": importance,
                    "emotion": emotion or 'neutral',
                    "timestamp": datetime.now().isoformat(),
                    "metadata": metadata or {}
                }
                
                # Add to Weaviate
                self.client.data_object.create(
                    data,
                    class_name=f"User{self.user_id}Memory",
                    uuid=memory_id,
                    vector=embedding
                )
                
            except Exception as e:
                logger.error(f"Failed to add to Weaviate: {e}")
        
        return memory_id
    
    async def retrieve_relevant(self, query_embedding: List[float],
                               limit: int = 10, memory_types: List[str] = None,
                               min_importance: float = 0.0) -> List[Dict]:
        """Retrieve relevant memories from cloud"""
        await self.initialize()
        
        results = []
        
        if self.provider == "pinecone" and self.index:
            try:
                # Query Pinecone
                query_response = self.index.query(
                    vector=query_embedding,
                    top_k=limit,
                    include_metadata=True,
                    include_values=False
                )
                
                # Format results
                for match in query_response.matches:
                    results.append({
                        'id': match.id,
                        'score': match.score,
                        'metadata': match.metadata
                    })
                
            except Exception as e:
                logger.error(f"Failed to query Pinecone: {e}")
        
        elif self.provider == "weaviate" and self.client:
            try:
                # Build nearVector query
                near_vector = {
                    "vector": query_embedding,
                    "certainty": 0.7
                }
                
                # Build filters
                where_filter = {}
                if memory_types:
                    where_filter = {
                        "operator": "And",
                        "operands": [
                            {"path": ["type"], "operator": "In", "values": memory_types}
                        ]
                    }
                
                # Query Weaviate
                response = (
                    self.client.query
                    .get(f"User{self.user_id}Memory", ["content", "type", "importance", "emotion", "timestamp", "metadata"])
                    .with_near_vector(near_vector)
                    .with_limit(limit)
                    .with_where(where_filter) if where_filter else None
                    .do()
                )
                
                # Parse results
                if response and 'data' in response:
                    objects = response['data']['Get'][f"User{self.user_id}Memory"]
                    for obj in objects:
                        results.append({
                            'id': obj['_additional']['id'],
                            'score': obj['_additional'].get('certainty', 0),
                            'content': obj.get('content'),
                            'metadata': obj
                        })
                
            except Exception as e:
                logger.error(f"Failed to query Weaviate: {e}")
        
        return results
    
    async def delete_memory(self, memory_id: str):
        """Delete memory by ID"""
        await self.initialize()
        
        if self.provider == "pinecone" and self.index:
            try:
                self.index.delete(ids=[memory_id])
            except Exception as e:
                logger.error(f"Failed to delete from Pinecone: {e}")
        
        elif self.provider == "weaviate" and self.client:
            try:
                self.client.data_object.delete(
                    uuid=memory_id,
                    class_name=f"User{self.user_id}Memory"
                )
            except Exception as e:
                logger.error(f"Failed to delete from Weaviate: {e}")
    
    async def get_stats(self) -> Dict:
        """Get cloud vector DB statistics"""
        await self.initialize()
        
        stats = {
            'provider': self.provider,
            'initialized': self.initialized
        }
        
        if self.provider == "pinecone" and self.index:
            try:
                index_stats = self.index.describe_index_stats()
                stats.update({
                    'dimension': index_stats.dimension,
                    'total_vectors': index_stats.total_vector_count,
                    'namespaces': index_stats.namespaces
                })
            except Exception as e:
                logger.error(f"Failed to get Pinecone stats: {e}")
        
        elif self.provider == "weaviate" and self.client:
            try:
                class_name = f"User{self.user_id}Memory"
                aggregate = self.client.query.aggregate(class_name).with_meta_count().do()
                stats['total_objects'] = aggregate['data']['Aggregate'][class_name][0]['meta']['count']
            except Exception as e:
                logger.error(f"Failed to get Weaviate stats: {e}")
        
        return stats


class CloudVectorFactory:
    """Factory untuk membuat cloud vector instances"""
    
    @staticmethod
    async def create_for_user(user_id: int, provider: str = "pinecone") -> CloudVectorMemory:
        """Create cloud vector memory for user"""
        memory = CloudVectorMemory(user_id, provider)
        await memory.initialize()
        return memory


__all__ = ['CloudVectorMemory', 'CloudVectorFactory']
