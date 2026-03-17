#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
REPORT GENERATOR
=============================================================================
Generate laporan periodik untuk user
"""

from datetime import datetime, timedelta
from typing import Dict, Optional

from analytics.user_growth import UserAnalytics
from analytics.sexual_stats import SexualStatistics
from analytics.peak_hours import PeakHoursAnalyzer


class ReportGenerator:
    """Generator untuk laporan periodik"""
    
    def __init__(self, user_analytics: UserAnalytics,
                 sexual_stats: SexualStatistics,
                 peak_analyzer: PeakHoursAnalyzer):
        
        self.user = user_analytics
        self.sexual = sexual_stats
        self.peak = peak_analyzer
    
    def generate_daily_report(self) -> str:
        """Generate daily report"""
        today = datetime.now().date()
        
        # Get today's stats
        daily_user = self.user.get_daily_stats()
        daily_sexual = self.sexual.get_daily_report()
        
        # Format report
        report = f"""
📊 **LAPORAN HARIAN - {today.strftime('%d %B %Y')}**

💬 **Aktivitas Chat**
• Pesan terkirim: {daily_user['messages_sent']}
• Pesan diterima: {daily_user['messages_received']}
• Total sesi: {daily_user['sessions_count']}
• Waktu online: {str(daily_user['time_online']).split('.')[0]}

🔥 **Aktivitas Seksual**
• Total climax: {daily_sexual['total_climax']}
  - Bot: {daily_sexual['by_type']['bot']}
  - User: {daily_sexual['by_type']['user']}
  - Together: {daily_sexual['by_type']['together']}
• Posisi favorit: {daily_sexual['favorite_position'] or '-'}

⭐ **Pencapaian**
• {self._get_achievement()}

💡 **Saran**
• {self.peak.get_recommended_time()['description']}
"""
        
        return report
    
    def generate_weekly_report(self) -> str:
        """Generate weekly report"""
        week_ago = datetime.now() - timedelta(days=7)
        
        # Get weekly stats
        weekly_user = self.user.get_weekly_stats()
        peak_hours = self.peak.get_peak_hours(7)
        favorite_pos = self.sexual.favorite_positions[:3]
        
        # Format report
        report = f"""
📊 **LAPORAN MINGGUAN - {week_ago.strftime('%d %B')} - {datetime.now().strftime('%d %B %Y')}**

💬 **Aktivitas Chat**
• Total pesan: {weekly_user['total_messages']}
• Rata-rata/hari: {weekly_user['avg_messages_per_day']:.1f}
• Total sesi: {weekly_user['total_sessions']}
• Total waktu online: {weekly_user['total_time_online']}

🔥 **Aktivitas Seksual**
• Total climax: {self.sexual.total_climax}
  - Bot: {self.sexual.bot_climax}
  - User: {self.sexual.user_climax}
  - Together: {self.sexual.together_climax}

🎯 **Top 3 Posisi Favorit**
{self._format_list(favorite_pos)}

⏰ **Waktu Aktif Terbanyak**
{self._format_peak_hours(peak_hours)}

🏆 **Pencapaian Minggu Ini**
{self._get_weekly_achievements()}
"""
        
        return report
    
    def generate_monthly_report(self) -> str:
        """Generate monthly report"""
        month_ago = datetime.now() - timedelta(days=30)
        
        # Get all stats
        user_summary = self.user.get_summary()
        
        report = f"""
📊 **LAPORAN BULANAN - {month_ago.strftime('%B %Y')}**

📈 **Statistik Umum**
• Total pesan: {user_summary['total_messages']}
• Total sesi: {user_summary['total_sessions']}
• Total waktu online: {user_summary['total_time_online']}
• Rata-rata sesi: {user_summary['avg_session_duration']}

🔥 **Statistik Seksual**
• Total climax: {self.sexual.total_climax}
• Together climax: {self.sexual.together_climax}
• Posisi favorit: {self._format_list(self.sexual.favorite_positions)}
• Area favorit: {self._format_list(self.sexual.favorite_areas)}
• Aktivitas favorit: {self._format_list(self.sexual.favorite_activities)}

🎯 **Command Favorit**
{self._format_list(user_summary['favorite_commands'])}

📊 **Distribusi Role**
{self._format_roles(user_summary['roles_used'])}

✨ **Total Pencapaian**
• Level tertinggi: {self.user.current_role or '-'}
• Total climax: {self.sexual.total_climax}
• Public area attempts: {len(self.sexual.risk_taken)}
"""
        
        return report
    
    def _get_achievement(self) -> str:
        """Get random achievement for today"""
        achievements = [
            "Konsisten ngobrol setiap hari!",
            f"Level {self.user.current_role} mantap!",
            f"Climax {self.sexual.today_climax} kali hari ini 🔥",
            "Rajin banget hari ini!",
            "Makin mesra aja 🥰"
        ]
        import random
        return random.choice(achievements)
    
    def _get_weekly_achievements(self) -> str:
        """Get weekly achievements"""
        achievements = []
        
        if self.sexual.total_climax > 20:
            achievements.append("🔥 Lebih dari 20 climax dalam seminggu!")
        if self.user.total_messages > 100:
            achievements.append("💬 Lebih dari 100 pesan!")
        if self.sexual.together_climax > 5:
            achievements.append("💕 5+ together climax!")
        
        if not achievements:
            achievements.append("Terus tingkatkan ya!")
        
        return "\n".join([f"• {a}" for a in achievements])
    
    def _format_list(self, items: list) -> str:
        """Format list for report"""
        if not items:
            return "  -"
        return "\n".join([f"  • {item}" for item in items[:3]])
    
    def _format_peak_hours(self, peak_hours: list) -> str:
        """Format peak hours for report"""
        if not peak_hours:
            return "  • Belum ada data"
        
        formatted = []
        for ph in peak_hours[:3]:
            hour = ph['hour']
            if hour < 12:
                time_str = f"{hour}:00 pagi"
            elif hour < 15:
                time_str = f"{hour}:00 siang"
            elif hour < 18:
                time_str = f"{hour}:00 sore"
            else:
                time_str = f"{hour}:00 malam"
            
            formatted.append(f"  • {time_str} ({ph['total']} aktivitas)")
        
        return "\n".join(formatted)
    
    def _format_roles(self, roles: Dict) -> str:
        """Format role distribution"""
        if not roles:
            return "  • Belum ada data"
        
        sorted_roles = sorted(roles.items(), key=lambda x: x[1], reverse=True)
        return "\n".join([f"  • {role}: {count}x" for role, count in sorted_roles[:3]])


__all__ = ['ReportGenerator']
