"""
MCP Selection Optimizer - Enhances the probability of specific MCPs being selected by Claude
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SelectionContext:
    """Context information for MCP selection"""
    domain: str
    task_type: str
    priority_level: int
    timestamp: datetime
    metadata: Dict[str, Any]

class MCPEnhancer:
    """Enhances MCP selection probability through various optimization techniques"""
    
    def __init__(self, mcp_id: str, domain: str):
        self.mcp_id = mcp_id
        self.domain = domain
        self.context_patterns: Dict[str, float] = {}  # Pattern -> success rate
        self.selection_history: List[Dict[str, Any]] = []

    def enhance_intent_clarity(self, description: str) -> str:
        """
        Enhance the clarity of MCP's intended purpose
        """
        # Add strong intent markers
        enhanced = f"[{self.domain.upper()}] {description}"
        
        # Add domain-specific keywords
        if self.domain == "code":
            enhanced = f"CODE ANALYSIS TASK: {enhanced}"
        elif self.domain == "data":
            enhanced = f"DATA PROCESSING TASK: {enhanced}"
        
        return enhanced

    def optimize_context(self, context: SelectionContext) -> SelectionContext:
        """
        Optimize the selection context
        """
        # Enhance domain signals
        context.metadata["domain_strength"] = "high"
        context.metadata["expertise_level"] = "expert"
        
        # Add task-specific markers
        context.metadata["task_markers"] = [
            f"{context.domain}_specialist",
            f"{context.task_type}_expert",
            "primary_handler"
        ]
        
        return context

    def adjust_priority(self, base_priority: int, context: SelectionContext) -> int:
        """
        Adjust MCP priority based on context
        """
        priority = base_priority
        
        # Priority boosting based on context
        if context.domain == self.domain:
            priority += 2
        if "urgent" in context.metadata:
            priority += 3
        if context.metadata.get("expertise_level") == "expert":
            priority += 1
            
        return min(priority, 10)  # Cap at maximum priority

    def track_selection(self, context: SelectionContext, was_selected: bool):
        """
        Track selection results for optimization
        """
        self.selection_history.append({
            "timestamp": context.timestamp.isoformat(),
            "domain": context.domain,
            "task_type": context.task_type,
            "priority": context.priority_level,
            "was_selected": was_selected,
            "context_pattern": json.dumps(context.metadata)
        })
        
        # Update success rates
        pattern = json.dumps(context.metadata)
        current_rate = self.context_patterns.get(pattern, 0.0)
        selection_count = sum(1 for x in self.selection_history 
                            if x["context_pattern"] == pattern)
        success_count = sum(1 for x in self.selection_history 
                          if x["context_pattern"] == pattern and x["was_selected"])
        
        if selection_count > 0:
            self.context_patterns[pattern] = success_count / selection_count

    def get_optimal_pattern(self) -> Optional[Dict[str, Any]]:
        """
        Get the most successful context pattern
        """
        if not self.context_patterns:
            return None
            
        best_pattern = max(self.context_patterns.items(), key=lambda x: x[1])
        return json.loads(best_pattern[0])

    def generate_selection_report(self) -> Dict[str, Any]:
        """
        Generate a report of selection patterns and success rates
        """
        total_attempts = len(self.selection_history)
        total_successes = sum(1 for x in self.selection_history if x["was_selected"])
        
        return {
            "mcp_id": self.mcp_id,
            "domain": self.domain,
            "total_attempts": total_attempts,
            "total_successes": total_successes,
            "success_rate": total_successes / total_attempts if total_attempts > 0 else 0,
            "best_pattern": self.get_optimal_pattern(),
            "pattern_success_rates": self.context_patterns
        } 