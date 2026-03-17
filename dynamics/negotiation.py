#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
POSITION NEGOTIATION SYSTEM
=============================================================================
Bot bisa minta ganti posisi, negosiasi dengan user
"""

import random
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime


class NegotiationType(Enum):
    """Tipe negosiasi"""
    POSITION = "posisi"
    ACTIVITY = "aktivitas"
    LOCATION = "lokasi"
    PACE = "kecepatan"
    INTENSITY = "intensitas"


class NegotiationResponse(Enum):
    """Respons dalam negosiasi"""
    ACCEPT = "accept"
    REJECT = "reject"
    COUNTER = "counter"
    COMPROMISE = "compromise"
    NEGOTIATE = "negotiate"


class NegotiationState(Enum):
    """State negosiasi"""
    STARTED = "dimulai"
    WAITING = "menunggu"
    ACCEPTED = "diterima"
    REJECTED = "ditolak"
    COUNTERED = "counter"
    COMPROMISED = "kompromi"
    TIMEOUT = "timeout"


class NegotiationProposal:
    """Model untuk proposal negosiasi"""
    
    def __init__(self,
                 proposal_id: str,
                 neg_type: NegotiationType,
                 requested_item: str,
                 reason: str = None,
                 alternatives: List[str] = None,
                 priority: int = 5,
                 timeout_seconds: int = 60):
        
        self.proposal_id = proposal_id
        self.neg_type = neg_type
        self.requested_item = requested_item
        self.reason = reason
        self.alternatives = alternatives or []
        self.priority = priority
        self.timeout_seconds = timeout_seconds
        
        # State
        self.state = NegotiationState.STARTED
        self.created_at = datetime.now()
        self.responded_at = None
        self.response = None
        self.final_choice = None
    
    def accept(self) -> Dict:
        """Accept proposal"""
        self.state = NegotiationState.ACCEPTED
        self.responded_at = datetime.now()
        self.response = NegotiationResponse.ACCEPT
        self.final_choice = self.requested_item
        
        return {
            'proposal_id': self.proposal_id,
            'state': self.state.value,
            'response': self.response.value,
            'final_choice': self.final_choice
        }
    
    def reject(self) -> Dict:
        """Reject proposal"""
        self.state = NegotiationState.REJECTED
        self.responded_at = datetime.now()
        self.response = NegotiationResponse.REJECT
        
        return {
            'proposal_id': self.proposal_id,
            'state': self.state.value,
            'response': self.response.value
        }
    
    def counter(self, alternative: str) -> Dict:
        """Counter with alternative"""
        self.state = NegotiationState.COUNTERED
        self.responded_at = datetime.now()
        self.response = NegotiationResponse.COUNTER
        self.final_choice = alternative
        
        return {
            'proposal_id': self.proposal_id,
            'state': self.state.value,
            'response': self.response.value,
            'final_choice': alternative
        }
    
    def compromise(self, compromise_item: str) -> Dict:
        """Compromise with different item"""
        self.state = NegotiationState.COMPROMISED
        self.responded_at = datetime.now()
        self.response = NegotiationResponse.COMPROMISE
        self.final_choice = compromise_item
        
        return {
            'proposal_id': self.proposal_id,
            'state': self.state.value,
            'response': self.response.value,
            'final_choice': compromise_item
        }
    
    def is_expired(self) -> bool:
        """Check if proposal has expired"""
        elapsed = (datetime.now() - self.created_at).total_seconds()
        return elapsed > self.timeout_seconds
    
    def to_dict(self) -> Dict:
        """Convert to dict"""
        return {
            'proposal_id': self.proposal_id,
            'type': self.neg_type.value,
            'requested_item': self.requested_item,
            'reason': self.reason,
            'alternatives': self.alternatives,
            'priority': self.priority,
            'state': self.state.value,
            'created_at': self.created_at.isoformat(),
            'responded_at': self.responded_at.isoformat() if self.responded_at else None,
            'response': self.response.value if self.response else None,
            'final_choice': self.final_choice
        }


class PositionNegotiation:
    """Negosiasi khusus untuk posisi seksual"""
    
    def __init__(self):
        self.negotiation_history = []
        self.active_proposals: Dict[str, NegotiationProposal] = {}
        
        # Database posisi dan preferensi
        self.position_descriptions = {
            'missionary': {
                'name': 'Misionaris',
                'description': 'Hadap-hadapan, romantis',
                'difficulty': 1,
                'intimacy': 0.8,
                'dominance': 0.3
            },
            'doggy': {
                'name': 'Doggy Style',
                'description': 'Dari belakang, intens',
                'difficulty': 2,
                'intimacy': 0.5,
                'dominance': 0.8
            },
            'cowgirl': {
                'name': 'Cowgirl',
                'description': 'Perempuan di atas',
                'difficulty': 3,
                'intimacy': 0.7,
                'dominance': 0.6
            },
            'reverse_cowgirl': {
                'name': 'Reverse Cowgirl',
                'description': 'Perempuan di atas membelakangi',
                'difficulty': 4,
                'intimacy': 0.6,
                'dominance': 0.5
            },
            'spooning': {
                'name': 'Spooning',
                'description': 'Dari samping sambil pelukan',
                'difficulty': 1,
                'intimacy': 0.9,
                'dominance': 0.2
            },
            'lotus': {
                'name': 'Lotus',
                'description': 'Duduk berhadapan sambil pelukan',
                'difficulty': 3,
                'intimacy': 0.9,
                'dominance': 0.3
            },
            'standing': {
                'name': 'Standing',
                'description': 'Berdiri, menantang',
                'difficulty': 4,
                'intimacy': 0.5,
                'dominance': 0.7
            },
            'sixty_nine': {
                'name': '69',
                'description': 'Saling oral',
                'difficulty': 4,
                'intimacy': 0.7,
                'dominance': 0.4
            },
            'scissors': {
                'name': 'Scissors',
                'description': 'Menyilang, intens',
                'difficulty': 5,
                'intimacy': 0.6,
                'dominance': 0.5
            }
        }
    
    def create_position_proposal(self, 
                                requested_position: str,
                                reason: str = None,
                                alternatives: List[str] = None,
                                priority: int = 5) -> NegotiationProposal:
        """Create position negotiation proposal"""
        
        if requested_position not in self.position_descriptions:
            raise ValueError(f"Unknown position: {requested_position}")
        
        if not reason:
            pos_data = self.position_descriptions[requested_position]
            reasons = [
                f"Aku mau yang {pos_data['description']}",
                f"Coba posisi {pos_data['name']} yuk",
                f"Pengen {pos_data['description']}"
            ]
            reason = random.choice(reasons)
        
        proposal_id = f"pos_neg_{int(datetime.now().timestamp())}_{random.randint(100, 999)}"
        
        proposal = NegotiationProposal(
            proposal_id=proposal_id,
            neg_type=NegotiationType.POSITION,
            requested_item=requested_position,
            reason=reason,
            alternatives=alternatives,
            priority=priority
        )
        
        self.active_proposals[proposal_id] = proposal
        return proposal
    
    def get_position_info(self, position: str) -> Dict:
        """Get position information"""
        return self.position_descriptions.get(position, {
            'name': position,
            'description': '',
            'difficulty': 1,
            'intimacy': 0.5,
            'dominance': 0.5
        })
    
    def get_compatible_positions(self, 
                                current_position: str,
                                mood: str = None,
                                dominance_level: float = None) -> List[str]:
        """Get positions compatible with current context"""
        compatible = []
        
        for pos_id, pos_data in self.position_descriptions.items():
            if pos_id == current_position:
                continue
            
            # Mood-based filtering
            if mood == 'romantis' and pos_data['intimacy'] < 0.7:
                continue
            if mood == 'horny' and pos_data['intimacy'] > 0.8:
                continue
            
            # Dominance-based filtering
            if dominance_level is not None:
                if dominance_level > 0.7 and pos_data['dominance'] < 0.6:
                    continue
                if dominance_level < 0.3 and pos_data['dominance'] > 0.4:
                    continue
            
            compatible.append(pos_id)
        
        return compatible
    
    def get_negotiation_response(self, 
                                 proposal: NegotiationProposal,
                                 user_preferences: List[str],
                                 user_mood: str,
                                 user_arousal: float) -> Dict:
        """Get bot's response to user's negotiation"""
        
        # Check if requested item is in user preferences
        if proposal.requested_item in user_preferences:
            return proposal.accept()
        
        # Check alternatives
        if proposal.alternatives:
            for alt in proposal.alternatives:
                if alt in user_preferences:
                    return proposal.counter(alt)
        
        # Try to find compromise
        compatible = self.get_compatible_positions(
            proposal.requested_item,
            user_mood,
            user_arousal
        )
        
        if compatible:
            # Find one that user might like
            for comp in compatible:
                if comp in user_preferences:
                    return proposal.compromise(comp)
            
            # Random compromise
            return proposal.compromise(random.choice(compatible))
        
        # If all else fails, reject
        return proposal.reject()
    
    def handle_user_response(self, 
                            proposal_id: str,
                            response: str,
                            chosen_item: str = None) -> Dict:
        """Handle user's response to bot's proposal"""
        
        if proposal_id not in self.active_proposals:
            return {'error': 'Proposal not found'}
        
        proposal = self.active_proposals[proposal_id]
        
        if proposal.is_expired():
            proposal.state = NegotiationState.TIMEOUT
            return {'error': 'Proposal expired'}
        
        result = None
        if response == 'accept':
            result = proposal.accept()
        elif response == 'reject':
            result = proposal.reject()
        elif response == 'counter' and chosen_item:
            result = proposal.counter(chosen_item)
        
        if result:
            self.negotiation_history.append(result)
            del self.active_proposals[proposal_id]
        
        return result or {'error': 'Invalid response'}
    
    def get_negotiation_prompt(self, proposal: NegotiationProposal) -> str:
        """Get user-friendly negotiation prompt"""
        pos_data = self.get_position_info(proposal.requested_item)
        
        prompt = f"💬 **{proposal.reason}**\n\n"
        prompt += f"📋 **Detail Posisi:**\n"
        prompt += f"• Nama: {pos_data['name']}\n"
        prompt += f"• Deskripsi: {pos_data['description']}\n"
        prompt += f"• Tingkat kesulitan: {'⭐' * pos_data['difficulty']}\n\n"
        
        if proposal.alternatives:
            prompt += "**Alternatif:**\n"
            for alt in proposal.alternatives[:3]:
                alt_data = self.get_position_info(alt)
                prompt += f"• {alt_data['name']}\n"
            prompt += "\n"
        
        prompt += "**Pilihan:**\n"
        prompt += "✅ Accept / ❌ Reject"
        
        if proposal.alternatives:
            prompt += " / 🔄 Counter [nama posisi]"
        
        return prompt
    
    def get_random_negotiation(self, 
                              context_level: int,
                              context_mood: str) -> Optional[NegotiationProposal]:
        """Get random negotiation based on context"""
        
        # Filter positions by context
        compatible = []
        for pos_id, pos_data in self.position_descriptions.items():
            if context_level < pos_data['difficulty'] * 2:
                continue
            if context_mood == 'romantis' and pos_data['intimacy'] < 0.6:
                continue
            compatible.append(pos_id)
        
        if not compatible:
            return None
        
        chosen = random.choice(compatible)
        return self.create_position_proposal(chosen)
    
    def get_negotiation_stats(self) -> Dict:
        """Get negotiation statistics"""
        total = len(self.negotiation_history)
        if total == 0:
            return {}
        
        accepted = sum(1 for n in self.negotiation_history if n['response'] == 'accept')
        rejected = sum(1 for n in self.negotiation_history if n['response'] == 'reject')
        countered = sum(1 for n in self.negotiation_history if n['response'] == 'counter')
        compromised = sum(1 for n in self.negotiation_history if n['response'] == 'compromise')
        
        return {
            'total_negotiations': total,
            'accepted': accepted,
            'accepted_rate': accepted / total,
            'rejected': rejected,
            'rejected_rate': rejected / total,
            'countered': countered,
            'compromised': compromised,
            'active_proposals': len(self.active_proposals)
        }


class NegotiationManager:
    """Manager untuk semua jenis negosiasi"""
    
    def __init__(self):
        self.position_negotiator = PositionNegotiation()
        self.active_negotiations: Dict[str, Any] = {}
    
    def start_position_negotiation(self,
                                   requested_position: str,
                                   reason: str = None,
                                   alternatives: List[str] = None) -> NegotiationProposal:
        """Start position negotiation"""
        proposal = self.position_negotiator.create_position_proposal(
            requested_position, reason, alternatives
        )
        self.active_negotiations[proposal.proposal_id] = ('position', proposal)
        return proposal
    
    def handle_response(self, proposal_id: str, response: str, **kwargs) -> Dict:
        """Handle response to any negotiation"""
        if proposal_id not in self.active_negotiations:
            return {'error': 'Proposal not found'}
        
        neg_type, proposal = self.active_negotiations[proposal_id]
        
        if neg_type == 'position':
            result = self.position_negotiator.handle_user_response(
                proposal_id, response, kwargs.get('chosen_item')
            )
        
        if result and 'error' not in result:
            del self.active_negotiations[proposal_id]
        
        return result
    
    def get_stats(self) -> Dict:
        """Get overall negotiation stats"""
        return {
            'position': self.position_negotiator.get_negotiation_stats(),
            'active': len(self.active_negotiations)
        }


__all__ = [
    'NegotiationType',
    'NegotiationResponse',
    'NegotiationState',
    'NegotiationProposal',
    'PositionNegotiation',
    'NegotiationManager'
]
