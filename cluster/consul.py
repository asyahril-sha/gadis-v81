#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
SERVICE DISCOVERY - CONSUL
=============================================================================
Untuk multiple instances (di-sederhanakan untuk single-user)
"""

from typing import Dict, List, Optional


class ServiceDiscovery:
    """
    Service discovery untuk multiple instances
    DISEDERHANAKAN UNTUK SINGLE-USER
    """
    
    def __init__(self):
        self.service_name = "gadis-v81"
        self.service_id = "gadis-v81-1"
        self.service_address = "localhost"
        self.service_port = 8080
        self.is_registered = False
    
    def register(self) -> bool:
        """Register service (dummy)"""
        self.is_registered = True
        return True
    
    def deregister(self) -> bool:
        """Deregister service (dummy)"""
        self.is_registered = False
        return True
    
    def get_service(self, service_name: str) -> Optional[Dict]:
        """Get service info (return self)"""
        if service_name == self.service_name:
            return {
                'id': self.service_id,
                'address': self.service_address,
                'port': self.service_port
            }
        return None
    
    def get_all_services(self) -> List[Dict]:
        """Get all services (return list with self)"""
        return [{
            'id': self.service_id,
            'name': self.service_name,
            'address': self.service_address,
            'port': self.service_port
        }]
    
    def health_check(self) -> bool:
        """Health check (always True)"""
        return True


# ===== SINGLETON =====
service_discovery = ServiceDiscovery()


__all__ = ['service_discovery', 'ServiceDiscovery']
