#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
VECTOR DATABASE FOR MEMORY
=============================================================================
ChromaDB integration untuk semantic memory search
"""

import os
import numpy as np
from typing import List, Dict, Any, Optional
from datetime import datetime

# Coba import chromadb
try:
    import chromadb
    from chromadb.config import Settings
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False

# Coba import sentence-transformers
try:
    from sentence_transformers import SentenceTransformer
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

from config import settings
from utils.logger import logger


class VectorMemory:
    """
    Vector database untuk semantic memory search
    Menggunakan ChromaDB sebagai backend
    """
    
    def __init__(self, user_id: int, collection_name: Optional[str] = None):
        self.user_id = user_id
        self.collection_name = collection_name or f"user_{user_id}_memories"
        
        # Initialize embedding model
        self.model = self._init_embedding_model()
        
        # Initialize ChromaDB
        self.client = self._init_chroma()
        self.collection = self._get_or_create_collection()
        
        # Fallback memory (jika ChromaDB tidak tersedia)
        self.fallback_memories = []
        
        logger.info(f"📊 VectorMemory initialized for user {user_id}")
    
    def _init_embedding_model(self):
        """Initialize sentence transformer model"""
        if TRANSFORMERS_AVAILABLE:
            try:
                model = SentenceTransformer('all-MiniLM-L6-v2')
                logger.info("✅ Sentence transformer model loaded")
                return model
            except Exception as e:
                logger.error(f"Failed to load sentence transformer: {e}")
        
        logger.warning("Using dummy embedding model")
        return DummyEmbeddingModel()
    
    def _init_chroma(self):
        """Initialize ChromaDB client"""
        if not CHROMA_AVAILABLE:
            logger.warning("ChromaDB not available, using fallback")
            return None
        
        try:
            client = chromadb.PersistentClient(
                path=str(settings.vector_db_dir),
                settings=Settings(anonymized_telemetry=False)
            )
            logger.info(f"✅ ChromaDB initialized at {settings.vector_db_dir}")
            return client
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            return None
    
    def _get_or_create_collection(self):
        """Get or create collection for this user"""
        if not self.client:
            return None
        
        try:
            # Try to get existing collection
            return self.client.get_collection(self.collection_name)
        except:
            # Create new collection
            return self.client.create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
    
    def _get_embedding(self, text: str) -> List[float]:
        """Get embedding for text"""
        if self.model:
            return self.model.encode(text).tolist()
        
        # Fallback: random embedding
        return list(np.random.randn(384))
    
    async def add_memory(self, content: str, memory_type: str,
                        importance: float = 0.5, emotion: str = None,
                        context: Dict = None) -> str:
        """Add memory to vector database"""
        memory_id = f"mem_{int(datetime.now().timestamp())}_{hash(content) % 10000}"
        
        metadata = {
            'type': memory_type,
            'importance': importance,
            'emotion': emotion or 'neutral',
            'timestamp': datetime.now().isoformat(),
            'user_id': self.user_id
        }
        
        if context:
            metadata.update(context)
        
        # Get embedding
        embedding = self._get_embedding(content)
        
        # Store in ChromaDB
        if self.collection:
            try:
                self.collection.add(
                    embeddings=[embedding],
                    documents=[content],
                    metadatas=[metadata],
                    ids=[memory_id]
                )
            except Exception as e:
                logger.error(f"Failed to add to ChromaDB: {e}")
                self.fallback_memories.append({
                    'id': memory_id,
                    'content': content,
                    'metadata': metadata,
                    'embedding': embedding
                })
        else:
            # Fallback
            self.fallback_memories.append({
                'id': memory_id,
                'content': content,
                'metadata': metadata,
                'embedding': embedding
            })
        
        return memory_id
    
    async def retrieve_relevant(self, query: str, limit: int = 10,
                               memory_types: List[str] = None,
                               min_importance: float = 0.0,
                               bias: Dict = None) -> List[Dict]:
        """Retrieve relevant memories using semantic search"""
        bias = bias or {}
        
        # Get query embedding
        query_embedding = self._get_embedding(query)
        
        # Search in ChromaDB
        results = []
        if self.collection:
            try:
                # Build filter
                where_filter = {}
                if memory_types:
                    where_filter['type'] = {'$in': memory_types}
                if min_importance > 0:
                    where_filter['importance'] = {'$gte': min_importance}
                
                # Query
                query_results = self.collection.query(
                    query_embeddings=[query_embedding],
                    n_results=limit * 2,
                    where=where_filter if where_filter else None
                )
                
                # Format results
                if query_results['ids']:
                    for i, mem_id in enumerate(query_results['ids'][0]):
                        results.append({
                            'id': mem_id,
                            'content': query_results['documents'][0][i],
                            'metadata': query_results['metadatas'][0][i],
                            'distance': query_results['distances'][0][i] if 'distances' in query_results else 0
                        })
            except Exception as e:
                logger.error(f"Failed to query ChromaDB: {e}")
        
        # Fallback: brute force search
        if not results and self.fallback_memories:
            results = self._fallback_search(query_embedding, limit, memory_types, min_importance)
        
        # Apply cognitive biases
        results = self._apply_biases(results, bias)
        
        return results[:limit]
    
    def _fallback_search(self, query_embedding: List[float], limit: int,
                        memory_types: List[str], min_importance: float) -> List[Dict]:
        """Fallback: brute force similarity search"""
        results = []
        query_np = np.array(query_embedding)
        
        for mem in self.fallback_memories:
            # Filter by type
            if memory_types and mem['metadata'].get('type') not in memory_types:
                continue
            
            # Filter by importance
            if mem['metadata'].get('importance', 0) < min_importance:
                continue
            
            # Calculate cosine similarity
            mem_np = np.array(mem['embedding'])
            similarity = np.dot(query_np, mem_np) / (np.linalg.norm(query_np) * np.linalg.norm(mem_np))
            
            results.append({
                'id': mem['id'],
                'content': mem['content'],
                'metadata': mem['metadata'],
                'similarity': float(similarity)
            })
        
        # Sort by similarity
        results.sort(key=lambda x: x.get('similarity', 0), reverse=True)
        return results
    
    def _apply_biases(self, results: List[Dict], bias: Dict) -> List[Dict]:
        """Apply cognitive biases to search results"""
        if not bias:
            return results
        
        # Recency bias
        if bias.get('recency', 0) > 0:
            for r in results:
                timestamp = r['metadata'].get('timestamp')
                if timestamp:
                    try:
                        age = (datetime.now() - datetime.fromisoformat(timestamp)).total_seconds()
                        recency_boost = 1.0 / (1.0 + age / 3600)
                        r['score'] = r.get('score', 1) * (1 + bias['recency'] * recency_boost)
                    except:
                        pass
        
        # Negativity bias
        if bias.get('negativity', 0) > 0:
            for r in results:
                if r['metadata'].get('emotion') in ['anger', 'sadness', 'fear']:
                    r['score'] = r.get('score', 1) * (1 + bias['negativity'])
        
        # Re-sort with biases
        results.sort(key=lambda x: x.get('score', 1), reverse=True)
        
        return results
    
    async def get_memories_by_type(self, memory_type: str, limit: int = 50) -> List[Dict]:
        """Get memories by type"""
        return await self.retrieve_relevant(
            query="",
            limit=limit,
            memory_types=[memory_type]
        )
    
    async def get_important_memories(self, threshold: float = 0.7, limit: int = 20) -> List[Dict]:
        """Get important memories"""
        return await self.retrieve_relevant(
            query="important memories",
            limit=limit,
            min_importance=threshold
        )
    
    def delete_memory(self, memory_id: str):
        """Delete memory by ID"""
        if self.collection:
            try:
                self.collection.delete(ids=[memory_id])
            except Exception as e:
                logger.error(f"Failed to delete memory: {e}")
        
        # Also remove from fallback
        self.fallback_memories = [m for m in self.fallback_memories if m['id'] != memory_id]


class DummyEmbeddingModel:
    """Dummy embedding model for fallback"""
    def encode(self, text: str) -> np.ndarray:
        """Generate deterministic pseudo-embedding"""
        import hashlib
        hash_obj = hashlib.sha256(text.encode())
        hash_bytes = hash_obj.digest()
        embedding = np.frombuffer(hash_bytes[:48], dtype=np.uint16) / 65535.0
        return embedding[:384]


__all__ = ['VectorMemory']
