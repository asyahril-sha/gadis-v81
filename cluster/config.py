#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
CLUSTER CONFIGURATION
=============================================================================
Konfigurasi untuk cluster mode (di-sederhanakan untuk single-user)
"""

from typing import Dict, Optional


class ClusterConfig:
    """
    Konfigurasi cluster untuk multiple instances
    DISEDERHANAKAN UNTUK SINGLE-USER
    """
    
    def __init__(self):
        # Node info
        self.node_id = "node-1"
        self.node_name = "gadis-v81-primary"
        self.node_role = "primary"
        
        # Cluster settings
        self.cluster_enabled = False
        self.total_nodes = 1
        self.replication_factor = 1
        
        # Network
        self.bind_address = "0.0.0.0"
        self.advertise_address = "localhost"
        self.port = 8080
        self.peers = []
        
        # Heartbeat
        self.heartbeat_interval = 5  # seconds
        self.heartbeat_timeout = 15   # seconds
    
    def enable_cluster(self, enabled: bool = True):
        """Enable/disable cluster mode"""
        self.cluster_enabled = enabled
    
    def add_peer(self, peer_address: str):
        """Add peer node (dummy)"""
        if peer_address not in self.peers:
            self.peers.append(peer_address)
            self.total_nodes = len(self.peers) + 1
    
    def remove_peer(self, peer_address: str):
        """Remove peer node (dummy)"""
        if peer_address in self.peers:
            self.peers.remove(peer_address)
            self.total_nodes = len(self.peers) + 1
    
    def is_leader(self) -> bool:
        """Check if this node is leader (always True for single)"""
        return True
    
    def get_status(self) -> Dict:
        """Get cluster status"""
        return {
            'cluster_enabled': self.cluster_enabled,
            'node_id': self.node_id,
            'node_name': self.node_name,
            'node_role': self.node_role,
            'total_nodes': self.total_nodes,
            'replication_factor': self.replication_factor,
            'peers': self.peers,
            'is_leader': self.is_leader()
        }
    
    def to_dict(self) -> Dict:
        """Convert to dict"""
        return {
            'node_id': self.node_id,
            'node_name': self.node_name,
            'node_role': self.node_role,
            'cluster_enabled': self.cluster_enabled,
            'bind_address': self.bind_address,
            'advertise_address': self.advertise_address,
            'port': self.port,
            'peers': self.peers
        }


# ===== SINGLETON =====
cluster_config = ClusterConfig()


__all__ = ['cluster_config', 'ClusterConfig']
