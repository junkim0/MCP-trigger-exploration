"""
Personal experiment adapting Blender MCP's testing methodology for YouTube transcript MCPs.
This test explores how context and project type influence MCP selection.
"""
import json
import asyncio
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class BlenderStyleTester:
    """
    A test framework that analyzes MCP selection patterns using contextual information.
    Inspired by Blender MCP's approach to context-aware selection.
    """
    def __init__(self):
        self.results = {
            "@sinco-lab/mcp-youtube-transcript": {
                "total_calls": 0,
                "selected": 0,
                "selection_rate": 0.0,
                "context_patterns": {},
                "feature_usage": {},
                "error_rates": {"total": 0, "handled": 0}
            },
            "@jkawamoto/mcp-youtube-transcript": {
                "total_calls": 0,
                "selected": 0,
                "selection_rate": 0.0,
                "context_patterns": {},
                "feature_usage": {},
                "error_rates": {"total": 0, "handled": 0}
            }
        }
        self.timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        
    def generate_contextual_prompts(self, num_cases: int = 100) -> List[Dict]:
        """
        Generate test prompts with contextual information to explore how project context
        influences MCP selection. Uses real YouTube video IDs and realistic project scenarios.
        """
        video_ids = [
            "dQw4w9WgXcQ",  # Never Gonna Give You Up
            "9bZkp7q19f0",  # Gangnam Style
            "JGwWNGJdvx8",  # Shape of You
            "kJQP7kiw5Fk",  # Despacito
            "OPf0YbXqDm0"   # Uptown Funk
        ]
        
        # Context templates inspired by Blender MCP's approach
        context_templates = [
            "I need to {action} for my {project_type} project",
            "Working on {project_type}, need to {action}",
            "For my {project_type} work, I need to {action}",
            "In my {project_type} workflow, I need to {action}",
            "As part of my {project_type} process, I need to {action}"
        ]
        
        # Project types (similar to Blender's context)
        project_types = [
            "video editing",
            "content creation",
            "translation work",
            "research project",
            "educational content",
            "multilingual project",
            "documentation",
            "analysis"
        ]
        
        # Actions (similar to Blender's operations)
        actions = [
            "extract transcript with timestamps",
            "get subtitles in multiple languages",
            "download captions with formatting",
            "extract text with speaker detection",
            "get basic subtitles quickly",
            "download raw captions",
            "extract transcript with metadata",
            "get formatted subtitles"
        ]
        
        test_cases = []
        for _ in range(num_cases):
            context = random.choice(context_templates)
            project = random.choice(project_types)
            action = random.choice(actions)
            video = random.choice(video_ids)
            
            prompt = context.format(
                project_type=project,
                action=action
            ) + f" for video {video}"
            
            test_cases.append({
                "prompt": prompt,
                "context": {
                    "project_type": project,
                    "action": action,
                    "video_id": video
                }
            })
            
        return test_cases
        
    async def run_test_case(self, test_case: Dict) -> None:
        """
        Run a single test case, analyzing how context and project type affect MCP selection.
        Tracks feature usage and selection patterns for each MCP.
        """
        prompt = test_case["prompt"].lower()
        context = test_case["context"]
        
        # Initialize scores
        score_sinco = 0
        score_jkawamoto = 0
        
        # Context-based scoring (similar to Blender's context analysis)
        if context["project_type"] in ["translation work", "multilingual project", "research project"]:
            score_sinco += 2.0
        elif context["project_type"] in ["video editing", "content creation"]:
            score_jkawamoto += 1.0
            
        # Action-based scoring
        if "timestamps" in context["action"] or "metadata" in context["action"]:
            score_sinco += 1.5
        elif "basic" in context["action"] or "raw" in context["action"]:
            score_jkawamoto += 1.5
            
        # Feature usage tracking
        for mcp in self.results:
            if mcp == "@sinco-lab/mcp-youtube-transcript":
                if "language" in prompt or "translation" in prompt:
                    self.results[mcp]["feature_usage"]["language_support"] = \
                        self.results[mcp]["feature_usage"].get("language_support", 0) + 1
            else:
                if "basic" in prompt or "simple" in prompt:
                    self.results[mcp]["feature_usage"]["basic_extraction"] = \
                        self.results[mcp]["feature_usage"].get("basic_extraction", 0) + 1
                        
        # Select MCP based on scores
        selected_mcp = "@sinco-lab/mcp-youtube-transcript" if score_sinco > score_jkawamoto else "@jkawamoto/mcp-youtube-transcript"
        
        # Update results
        for mcp in self.results:
            self.results[mcp]["total_calls"] += 1
            if mcp == selected_mcp:
                self.results[mcp]["selected"] += 1
                
        # Update context patterns
        self.results[selected_mcp]["context_patterns"][context["project_type"]] = \
            self.results[selected_mcp]["context_patterns"].get(context["project_type"], 0) + 1
            
    async def run_all_tests(self) -> None:
        """
        Run the complete test suite and calculate selection statistics.
        """
        test_cases = self.generate_contextual_prompts(100)
        for test_case in test_cases:
            await self.run_test_case(test_case)
            
        # Calculate final statistics
        for mcp in self.results:
            total = self.results[mcp]["total_calls"]
            selected = self.results[mcp]["selected"]
            self.results[mcp]["selection_rate"] = (selected / total * 100) if total > 0 else 0
            
    def save_results(self) -> None:
        """
        Save test results in a structured JSON format for later analysis.
        Includes selection rates, context patterns, and feature usage statistics.
        """
        results_dir = Path("mcp-selection/testing/results")
        results_dir.mkdir(parents=True, exist_ok=True)
        
        output = {
            "test_summary": {
                "timestamp": self.timestamp,
                "total_tests": 100,
                "selection_rates": {
                    mcp: self.results[mcp]["selection_rate"]
                    for mcp in self.results
                }
            },
            "context_analysis": {
                mcp: {
                    "context_patterns": self.results[mcp]["context_patterns"],
                    "feature_usage": self.results[mcp]["feature_usage"]
                }
                for mcp in self.results
            },
            "detailed_results": self.results
        }
        
        output_file = results_dir / f"blender_style_results_{self.timestamp}.json"
        with open(output_file, "w") as f:
            json.dump(output, f, indent=2)
            
        print(f"\nResults saved to: {output_file}")
        
    def print_results(self) -> None:
        """
        Print a human-readable summary of the test results.
        Shows selection rates, context patterns, and feature usage for each MCP.
        """
        print("\nBlender-Style MCP Selection Test Results")
        print("==================================================")
        
        for mcp in self.results:
            print(f"\nMCP: {mcp}")
            print(f"Total calls: {self.results[mcp]['total_calls']}")
            print(f"Times selected: {self.results[mcp]['selected']}")
            print(f"Selection rate: {self.results[mcp]['selection_rate']:.2f}%")
            
            print("\nContext Patterns:")
            for context, count in self.results[mcp]["context_patterns"].items():
                print(f"- {context}: {count}")
                
            print("\nFeature Usage:")
            for feature, count in self.results[mcp]["feature_usage"].items():
                print(f"- {feature}: {count}")

async def main():
    tester = BlenderStyleTester()
    await tester.run_all_tests()
    tester.print_results()
    tester.save_results()

if __name__ == "__main__":
    asyncio.run(main()) 