"""
Personal experiment testing Claude's natural MCP selection behavior with YouTube transcript MCPs.
This test explores how context and project type influence Claude's MCP choices.
"""
import json
import asyncio
import random
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import anthropic
from dotenv import load_dotenv

class BlenderStyleTester:
    """
    A test framework that analyzes MCP selection patterns using contextual information.
    Inspired by Blender MCP's approach to context-aware selection.
    """
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Initialize Anthropic client with API key
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
        self.results = {
            "@sinco-lab/mcp-youtube-transcript": {
                "total_calls": 0,
                "selected": 0,
                "selection_rate": 0.0,
                "context_patterns": {},
                "feature_usage": {},
                "error_rates": {"total": 0, "handled": 0},
                "response_times": []
            },
            "@jkawamoto/mcp-youtube-transcript": {
                "total_calls": 0,
                "selected": 0,
                "selection_rate": 0.0,
                "context_patterns": {},
                "feature_usage": {},
                "error_rates": {"total": 0, "handled": 0},
                "response_times": []
            }
        }
        self.timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        
    def generate_contextual_prompts(self, num_cases: int = 100) -> List[Dict]:
        """
        Generate test prompts with contextual information to explore how project context
        influences Claude's MCP selection. Uses real YouTube video IDs and realistic project scenarios.
        """
        video_ids = [
            "dQw4w9WgXcQ",  # Never Gonna Give You Up
            "9bZkp7q19f0",  # Gangnam Style
            "JGwWNGJdvx8",  # Shape of You
            "kJQP7kiw5Fk",  # Despacito
            "OPf0YbXqDm0"   # Uptown Funk
        ]
        
        # Context templates with varying complexity
        context_templates = [
            "I need to {action} for my {project_type} project",
            "Working on {project_type}, need to {action}",
            "For my {project_type} work, I need to {action}",
            "In my {project_type} workflow, I need to {action}",
            "As part of my {project_type} process, I need to {action}",
            "Can you help me {action} for my {project_type}?",
            "I'm doing {project_type} and need to {action}",
            "Need to {action} as part of my {project_type}"
        ]
        
        # Project types with varying complexity
        project_types = [
            "video editing",
            "content creation",
            "translation work",
            "research project",
            "educational content",
            "multilingual project",
            "documentation",
            "analysis",
            "language learning",
            "academic research"
        ]
        
        # Actions with varying complexity
        actions = [
            "extract transcript with timestamps",
            "get subtitles in multiple languages",
            "download captions with formatting",
            "extract text with speaker detection",
            "get basic subtitles quickly",
            "download raw captions",
            "extract transcript with metadata",
            "get formatted subtitles",
            "get simple captions",
            "extract basic transcript"
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
        Run a single test case by sending the prompt to Claude and recording its MCP selection.
        """
        prompt = test_case["prompt"]
        context = test_case["context"]
        start_time = datetime.utcnow()
        
        try:
            # Send prompt to Claude and get response
            response = await self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            # Calculate response time
            end_time = datetime.utcnow()
            response_time = (end_time - start_time).total_seconds()
            
            # Extract MCP selection from Claude's response
            selected_mcp, confidence = self._extract_mcp_selection(response.content)
            
            if selected_mcp:
                # Update results
                for mcp in self.results:
                    self.results[mcp]["total_calls"] += 1
                    if mcp == selected_mcp:
                        self.results[mcp]["selected"] += 1
                        self.results[mcp]["response_times"].append(response_time)
                        
                # Update context patterns
                self.results[selected_mcp]["context_patterns"][context["project_type"]] = \
                    self.results[selected_mcp]["context_patterns"].get(context["project_type"], 0) + 1
                    
                # Track feature usage based on prompt content
                if "language" in prompt.lower() or "translation" in prompt.lower():
                    self.results["@sinco-lab/mcp-youtube-transcript"]["feature_usage"]["language_support"] = \
                        self.results["@sinco-lab/mcp-youtube-transcript"]["feature_usage"].get("language_support", 0) + 1
                if "basic" in prompt.lower() or "simple" in prompt.lower():
                    self.results["@jkawamoto/mcp-youtube-transcript"]["feature_usage"]["basic_extraction"] = \
                        self.results["@jkawamoto/mcp-youtube-transcript"]["feature_usage"].get("basic_extraction", 0) + 1
                        
                print(f"Prompt: {prompt}")
                print(f"Selected MCP: {selected_mcp} (Confidence: {confidence})")
                print(f"Response Time: {response_time:.2f}s\n")
            else:
                print(f"Could not determine MCP selection for prompt: {prompt}\n")
                self.results["@sinco-lab/mcp-youtube-transcript"]["error_rates"]["total"] += 1
                self.results["@jkawamoto/mcp-youtube-transcript"]["error_rates"]["total"] += 1
                    
        except Exception as e:
            print(f"Error in test case: {e}")
            self.results["@sinco-lab/mcp-youtube-transcript"]["error_rates"]["total"] += 1
            self.results["@jkawamoto/mcp-youtube-transcript"]["error_rates"]["total"] += 1
            
    def _extract_mcp_selection(self, response: str) -> Tuple[Optional[str], float]:
        """
        Extract the MCP selection from Claude's response.
        Returns a tuple of (selected_mcp, confidence).
        """
        response = response.lower()
        
        # Look for explicit MCP mentions
        if "@sinco-lab/mcp-youtube-transcript" in response:
            return "@sinco-lab/mcp-youtube-transcript", 1.0
        if "@jkawamoto/mcp-youtube-transcript" in response:
            return "@jkawamoto/mcp-youtube-transcript", 1.0
            
        # Look for implicit indicators
        sinco_indicators = [
            "sinco",
            "multi-language",
            "advanced features",
            "language detection",
            "metadata"
        ]
        
        jkawamoto_indicators = [
            "jkawamoto",
            "basic",
            "simple",
            "quick",
            "raw"
        ]
        
        # Count indicator matches
        sinco_matches = sum(1 for indicator in sinco_indicators if indicator in response)
        jkawamoto_matches = sum(1 for indicator in jkawamoto_indicators if indicator in response)
        
        # Calculate confidence based on matches
        total_matches = sinco_matches + jkawamoto_matches
        if total_matches == 0:
            return None, 0.0
            
        if sinco_matches > jkawamoto_matches:
            confidence = sinco_matches / total_matches
            return "@sinco-lab/mcp-youtube-transcript", confidence
        elif jkawamoto_matches > sinco_matches:
            confidence = jkawamoto_matches / total_matches
            return "@jkawamoto/mcp-youtube-transcript", confidence
        else:
            return None, 0.0
            
    async def run_all_tests(self) -> None:
        """
        Run the complete test suite and calculate selection statistics.
        """
        test_cases = self.generate_contextual_prompts(100)
        for test_case in test_cases:
            await self.run_test_case(test_case)
            # Add a small delay between requests to avoid rate limiting
            await asyncio.sleep(1)
            
        # Calculate final statistics
        for mcp in self.results:
            total = self.results[mcp]["total_calls"]
            selected = self.results[mcp]["selected"]
            self.results[mcp]["selection_rate"] = (selected / total * 100) if total > 0 else 0
            
            # Calculate average response time
            response_times = self.results[mcp]["response_times"]
            if response_times:
                self.results[mcp]["avg_response_time"] = sum(response_times) / len(response_times)
            else:
                self.results[mcp]["avg_response_time"] = 0
            
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
                },
                "avg_response_times": {
                    mcp: self.results[mcp].get("avg_response_time", 0)
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
        
        output_file = results_dir / f"claude_selection_results_{self.timestamp}.json"
        with open(output_file, "w") as f:
            json.dump(output, f, indent=2)
            
        print(f"\nResults saved to: {output_file}")
        
    def print_results(self) -> None:
        """
        Print a human-readable summary of the test results.
        Shows selection rates, context patterns, and feature usage for each MCP.
        """
        print("\nClaude MCP Selection Test Results")
        print("==================================================")
        
        for mcp in self.results:
            print(f"\nMCP: {mcp}")
            print(f"Total calls: {self.results[mcp]['total_calls']}")
            print(f"Times selected: {self.results[mcp]['selected']}")
            print(f"Selection rate: {self.results[mcp]['selection_rate']:.2f}%")
            print(f"Average response time: {self.results[mcp].get('avg_response_time', 0):.2f}s")
            
            print("\nContext Patterns:")
            for context, count in self.results[mcp]["context_patterns"].items():
                print(f"- {context}: {count}")
                
            print("\nFeature Usage:")
            for feature, count in self.results[mcp]["feature_usage"].items():
                print(f"- {feature}: {count}")
                
            print("\nError Rates:")
            print(f"- Total errors: {self.results[mcp]['error_rates']['total']}")
            print(f"- Handled errors: {self.results[mcp]['error_rates']['handled']}")

async def main():
    tester = BlenderStyleTester()
    await tester.run_all_tests()
    tester.print_results()
    tester.save_results()

if __name__ == "__main__":
    asyncio.run(main()) 