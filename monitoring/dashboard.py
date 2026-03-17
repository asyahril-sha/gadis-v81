#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
GRAFANA DASHBOARD
=============================================================================
Template dashboard Grafana untuk monitoring bot
"""

import json
from typing import Dict


class DashboardManager:
    """Manager untuk dashboard Grafana"""
    
    @staticmethod
    def get_bot_dashboard() -> Dict:
        """Get Grafana dashboard JSON for bot monitoring"""
        
        dashboard = {
            "dashboard": {
                "title": "GADIS V81 - Bot Monitoring",
                "tags": ["gadis", "telegram", "bot"],
                "timezone": "browser",
                "panels": [
                    {
                        "title": "Active Users",
                        "type": "graph",
                        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0},
                        "targets": [
                            {
                                "expr": "bot_active_users",
                                "legendFormat": "Active Users"
                            }
                        ]
                    },
                    {
                        "title": "Messages & Commands",
                        "type": "graph",
                        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0},
                        "targets": [
                            {
                                "expr": "rate(bot_messages_total[5m])",
                                "legendFormat": "Messages/s"
                            },
                            {
                                "expr": "rate(bot_commands_total[5m])",
                                "legendFormat": "Commands/s"
                            }
                        ]
                    },
                    {
                        "title": "Climax Events",
                        "type": "graph",
                        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 8},
                        "targets": [
                            {
                                "expr": "rate(bot_climax_total[5m])",
                                "legendFormat": "{{type}}"
                            }
                        ]
                    },
                    {
                        "title": "Response Time",
                        "type": "graph",
                        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 8},
                        "targets": [
                            {
                                "expr": "rate(bot_response_time_seconds_sum[5m]) / rate(bot_response_time_seconds_count[5m])",
                                "legendFormat": "Avg Response Time"
                            },
                            {
                                "expr": "bot_response_time_seconds_bucket{le='0.1'}",
                                "legendFormat": "<100ms"
                            },
                            {
                                "expr": "bot_response_time_seconds_bucket{le='0.5'}",
                                "legendFormat": "<500ms"
                            }
                        ]
                    },
                    {
                        "title": "System Resources",
                        "type": "graph",
                        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 16},
                        "targets": [
                            {
                                "expr": "bot_cpu_usage",
                                "legendFormat": "CPU %"
                            },
                            {
                                "expr": "bot_memory_usage",
                                "legendFormat": "Memory %"
                            }
                        ]
                    },
                    {
                        "title": "Error Rate",
                        "type": "graph",
                        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 16},
                        "targets": [
                            {
                                "expr": "rate(bot_errors_total[5m])",
                                "legendFormat": "Errors/s"
                            }
                        ]
                    },
                    {
                        "title": "Arousal Level",
                        "type": "graph",
                        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 24},
                        "targets": [
                            {
                                "expr": "bot_arousal_level",
                                "legendFormat": "Arousal"
                            }
                        ]
                    },
                    {
                        "title": "Role Distribution",
                        "type": "pie",
                        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 24},
                        "targets": [
                            {
                                "expr": "bot_messages_total",
                                "legendFormat": "{{role}}"
                            }
                        ]
                    }
                ],
                "schemaVersion": 27,
                "version": 1
            },
            "overwrite": True
        }
        
        return dashboard
    
    @staticmethod
    def get_sexual_dashboard() -> Dict:
        """Get Grafana dashboard for sexual statistics"""
        
        dashboard = {
            "dashboard": {
                "title": "GADIS V81 - Sexual Analytics",
                "tags": ["gadis", "sexual", "analytics"],
                "timezone": "browser",
                "panels": [
                    {
                        "title": "Position Usage",
                        "type": "table",
                        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0},
                        "targets": [
                            {
                                "expr": "bot_position_usage",
                                "format": "table",
                                "instant": True
                            }
                        ]
                    },
                    {
                        "title": "Climax by Position",
                        "type": "bar",
                        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0},
                        "targets": [
                            {
                                "expr": "bot_position_climax",
                                "legendFormat": "{{position}}"
                            }
                        ]
                    },
                    {
                        "title": "Area Sensitivity",
                        "type": "heatmap",
                        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 8},
                        "targets": [
                            {
                                "expr": "bot_area_sensitivity",
                                "legendFormat": "{{area}}"
                            }
                        ]
                    },
                    {
                        "title": "Peak Hours",
                        "type": "graph",
                        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 8},
                        "targets": [
                            {
                                "expr": "bot_activity_hour",
                                "legendFormat": "Messages"
                            }
                        ]
                    }
                ],
                "schemaVersion": 27,
                "version": 1
            },
            "overwrite": True
        }
        
        return dashboard
    
    @staticmethod
    def save_dashboard(file_path: str, dashboard_type: str = "bot"):
        """Save dashboard to file"""
        if dashboard_type == "bot":
            dashboard = DashboardManager.get_bot_dashboard()
        else:
            dashboard = DashboardManager.get_sexual_dashboard()
        
        with open(file_path, 'w') as f:
            json.dump(dashboard, f, indent=2)
        
        return file_path


__all__ = ['DashboardManager']
