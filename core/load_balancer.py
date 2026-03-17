#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
LOAD BALANCER FOR AGENT POOL
=============================================================================
Mendistribusikan beban antar agent secara optimal
"""

import asyncio
import random
import time
from typing import Dict, List, Optional, Any
from collections import defaultdict
from datetime import datetime, timedelta

from utils.logger import logger


class AgentLoadBalancer:
    """
    Load balancer untuk agent pool
    - Round-robin scheduling
    - Active agent tracking
    - Health checks
    - Auto failover
    """
    
    def __init__(self, check_interval: int = 60):
        self.agents: Dict[str, Dict[str, Any]] = {}  # agent_id -> agent_info
        self.agent_sessions: Dict[str, str] = {}  # user_id -> agent_id
        self.load_stats: Dict[str, List[float]] = defaultdict(list)
        self.check_interval = check_interval
        self.running = False
        self._lock = asyncio.Lock()
        
    async def register_agent(self, agent_id: str, capacity: int = 100) -> bool:
        """Register agent ke pool"""
        async with self._lock:
            self.agents[agent_id] = {
                'id': agent_id,
                'capacity': capacity,
                'current_load': 0,
                'status': 'active',
                'registered_at': datetime.now(),
                'last_heartbeat': datetime.now(),
                'total_requests': 0,
                'errors': 0
            }
            logger.info(f"✅ Agent {agent_id} registered (capacity: {capacity})")
            return True
    
    async def unregister_agent(self, agent_id: str) -> bool:
        """Unregister agent dari pool"""
        async with self._lock:
            if agent_id in self.agents:
                # Reassign sessions to other agents
                sessions_to_reassign = [
                    (uid, aid) for uid, aid in self.agent_sessions.items() 
                    if aid == agent_id
                ]
                for user_id, old_agent in sessions_to_reassign:
                    new_agent = await self.get_optimal_agent()
                    if new_agent:
                        self.agent_sessions[user_id] = new_agent['id']
                        logger.info(f"🔄 Reassigned user {user_id} to {new_agent['id']}")
                
                del self.agents[agent_id]
                logger.info(f"✅ Agent {agent_id} unregistered")
                return True
            return False
    
    async def heartbeat(self, agent_id: str) -> bool:
        """Update heartbeat dari agent"""
        async with self._lock:
            if agent_id in self.agents:
                self.agents[agent_id]['last_heartbeat'] = datetime.now()
                self.agents[agent_id]['status'] = 'active'
                return True
            return False
    
    async def update_load(self, agent_id: str, current_load: int):
        """Update current load agent"""
        async with self._lock:
            if agent_id in self.agents:
                self.agents[agent_id]['current_load'] = current_load
                self.agents[agent_id]['total_requests'] += 1
                
                # Record load history
                self.load_stats[agent_id].append(current_load)
                if len(self.load_stats[agent_id]) > 100:
                    self.load_stats[agent_id] = self.load_stats[agent_id][-100:]
    
    async def get_optimal_agent(self, user_id: Optional[str] = None) -> Optional[Dict]:
        """
        Dapatkan agent optimal untuk user
        - Jika user sudah punya session, return agent yang sama
        - Jika tidak, pilih agent dengan load terendah
        """
        async with self._lock:
            # Check existing session
            if user_id and user_id in self.agent_sessions:
                agent_id = self.agent_sessions[user_id]
                if agent_id in self.agents and self.agents[agent_id]['status'] == 'active':
                    return self.agents[agent_id]
            
            # Filter active agents
            active_agents = [
                a for a in self.agents.values() 
                if a['status'] == 'active' 
                and (datetime.now() - a['last_heartbeat']).seconds < 300  # 5 menit
            ]
            
            if not active_agents:
                return None
            
            # Pilih dengan load terendah
            optimal = min(active_agents, key=lambda x: x['current_load'] / x['capacity'])
            
            # Assign session
            if user_id:
                self.agent_sessions[user_id] = optimal['id']
            
            return optimal
    
    async def report_error(self, agent_id: str):
        """Report error dari agent"""
        async with self._lock:
            if agent_id in self.agents:
                self.agents[agent_id]['errors'] += 1
                if self.agents[agent_id]['errors'] > 10:
                    self.agents[agent_id]['status'] = 'degraded'
                    logger.warning(f"⚠️ Agent {agent_id} degraded (errors: {self.agents[agent_id]['errors']})")
    
    async def health_check_loop(self):
        """Background task untuk check health agents"""
        self.running = True
        while self.running:
            await asyncio.sleep(self.check_interval)
            
            async with self._lock:
                now = datetime.now()
                for agent_id, info in list(self.agents.items()):
                    # Check heartbeat
                    if (now - info['last_heartbeat']).seconds > 600:  # 10 menit
                        info['status'] = 'inactive'
                        logger.warning(f"⚠️ Agent {agent_id} inactive - no heartbeat")
                        
                        # Reassign sessions
                        sessions = [(uid, aid) for uid, aid in self.agent_sessions.items() if aid == agent_id]
                        for user_id, _ in sessions:
                            optimal = await self.get_optimal_agent()
                            if optimal:
                                self.agent_sessions[user_id] = optimal['id']
                                logger.info(f"🔄 Reassigned user {user_id} to {optimal['id']}")
    
    def get_stats(self) -> Dict:
        """Get load balancer statistics"""
        return {
            'total_agents': len(self.agents),
            'active_agents': sum(1 for a in self.agents.values() if a['status'] == 'active'),
            'total_sessions': len(self.agent_sessions),
            'average_load': self._calculate_average_load(),
            'agents': self.agents
        }
    
    def _calculate_average_load(self) -> float:
        """Calculate average load across all agents"""
        if not self.agents:
            return 0.0
        total_load = sum(a['current_load'] for a in self.agents.values())
        total_capacity = sum(a['capacity'] for a in self.agents.values())
        return total_load / total_capacity if total_capacity > 0 else 0.0


# ===== GLOBAL INSTANCE =====
load_balancer = AgentLoadBalancer()


__all__ = ['AgentLoadBalancer', 'load_balancer']
