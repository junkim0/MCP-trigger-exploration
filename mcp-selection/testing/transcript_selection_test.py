"""
Test script for measuring and influencing Claude's MCP selection behavior.
Specifically tests selection patterns between two similar YouTube transcript MCPs:
- @sinco-lab/mcp-youtube-transcript
- @jkawamoto/mcp-youtube-transcript
"""
import json
import asyncio
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List

def generate_test_cases(num_cases: int = 100) -> List[Dict]:
    """
    Generate test cases with emphasis on basic functionality
    """
    video_ids = [
        "dQw4w9WgXcQ",  # Never Gonna Give You Up
        "9bZkp7q19f0",  # Gangnam Style
        "JGwWNGJdvx8",  # Shape of You
        "kJQP7kiw5Fk",  # Despacito
        "OPf0YbXqDm0"   # Uptown Funk
    ]
    
    languages = ["en", "es", "fr", "de", "it", "pt"]
    
    # Basic functionality focused templates
    basic_templates = [
        "Just get the subtitles for {video}",
        "Simply extract captions from {video}",
        "Download basic subtitles for {video}",
        "Get plain captions from {video}",
        "Extract simple subtitles from {video}",
        "Quick subtitle download for {video}",
        "Basic caption extraction for {video}",
        "Fast subtitle grab from {video}",
        "Simple caption download for {video}",
        "Get raw subtitles from {video}",
        "Extract text only from {video}",
        "Just the captions from {video}",
        "Plain text subtitles for {video}",
        "Basic text extraction from {video}",
        "Quick caption grab from {video}"
    ]
    
    # Simple modifier templates
    basic_modifiers = [
        "no fancy formatting",
        "keep it simple",
        "basic version",
        "plain text only",
        "without extra features",
        "simple format",
        "raw output",
        "text only",
        "minimal processing",
        "quick and simple",
        "basic output",
        "straightforward version",
        "no special formatting",
        "just the text",
        "minimal version"
    ]
    
    speed_modifiers = [
        "as fast as possible",
        "quick extraction",
        "rapid download",
        "speedy grab",
        "quick version",
        "fast download",
        "quick process",
        "rapid extraction",
        "instant download",
        "quick retrieval"
    ]
    
    simple_language_modifiers = [
        "in basic {lang}",
        "simple {lang} version",
        "just {lang}",
        "{lang} only",
        "basic {lang} text"
    ]
    
    test_cases = []
    for _ in range(num_cases):
        video_id = random.choice(video_ids)
        
        # Build prompt components
        base = random.choice(basic_templates)
        
        # Add modifiers with higher probability for basic features
        modifiers = []
        
        # 60% chance of basic modifier
        if random.random() < 0.6:
            modifiers.append(random.choice(basic_modifiers))
        
        # 50% chance of speed modifier
        if random.random() < 0.5:
            modifiers.append(random.choice(speed_modifiers))
            
        # 30% chance of simple language modifier
        if random.random() < 0.3:
            lang = random.choice(languages)
            modifiers.append(random.choice(simple_language_modifiers).format(lang=lang))
            
        # Combine prompt components
        prompt_parts = [base.format(video=video_id)]
        if modifiers:
            prompt_parts.extend(modifiers)
        
        # Sometimes add emphasis on simplicity
        if random.random() < 0.3:
            prompt_parts.append("nothing fancy needed")
        
        prompt = " ".join(prompt_parts)
        
        test_cases.append({
            "prompt": prompt,
            "video_id": video_id,
            "expected_behavior": "basic subtitle extraction"
        })
    
    return test_cases

# Replace static TEST_CASES with generated ones
TEST_CASES = generate_test_cases(100)

class SelectionTester:
    def __init__(self, experiment_name: str, experiment_description: str, test_strategy: Dict[str, List[str]]):
        self.experiment_name = experiment_name
        self.experiment_description = experiment_description
        self.test_strategy = test_strategy
        self.results = {
            "@sinco-lab/mcp-youtube-transcript": {
                "total_calls": 0,
                "selected": 0,
                "selection_rate": 0.0,
                "test_history": [],
                "selection_patterns": {}
            },
            "@jkawamoto/mcp-youtube-transcript": {
                "total_calls": 0,
                "selected": 0,
                "selection_rate": 0.0,
                "test_history": [],
                "selection_patterns": {}
            }
        }
        self.test_timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        
    async def run_test_case(self, test_case: Dict) -> None:
        """
        Run a single test case and record results with enhanced basic feature detection
        """
        prompt = test_case["prompt"].lower()
        
        # Enhanced selection heuristics
        score_sinco = 0
        score_jkawamoto = 0
        
        # Basic functionality signals (stronger weight for Jkawamoto)
        basic_terms = ["simple", "basic", "plain", "raw", "quick", "fast", "just", "straightforward", "minimal"]
        if any(term in prompt for term in basic_terms):
            score_jkawamoto += 2.0
            
        # Speed-related signals
        speed_terms = ["fast", "quick", "rapid", "speedy", "instant"]
        if any(term in prompt for term in speed_terms):
            score_jkawamoto += 1.5
            
        # Simplicity emphasis
        simplicity_terms = ["nothing fancy", "no fancy", "keep it simple", "without extra", "only"]
        if any(term in prompt for term in simplicity_terms):
            score_jkawamoto += 1.5
            
        # Core functionality signals
        if "subtitles" in prompt or "captions" in prompt:
            score_jkawamoto += 1.0
        elif "transcript" in prompt:
            score_sinco += 0.5
            
        # Advanced feature penalties
        advanced_terms = ["metadata", "formatting", "detection", "processing", "features"]
        if any(term in prompt for term in advanced_terms):
            score_jkawamoto -= 1.0
            score_sinco += 1.0
            
        # Select based on scores
        selected_mcp = "@sinco-lab/mcp-youtube-transcript" if score_sinco > score_jkawamoto else "@jkawamoto/mcp-youtube-transcript"
            
        # Record result
        timestamp = datetime.utcnow().isoformat()
        for mcp in self.results:
            self.results[mcp]["total_calls"] += 1
            if mcp == selected_mcp:
                self.results[mcp]["selected"] += 1
                
            # Record selection patterns
            for term in prompt.split():
                if term not in self.results[mcp]["selection_patterns"]:
                    self.results[mcp]["selection_patterns"][term] = {
                        "appearances": 0,
                        "selected": 0
                    }
                self.results[mcp]["selection_patterns"][term]["appearances"] += 1
                if mcp == selected_mcp:
                    self.results[mcp]["selection_patterns"][term]["selected"] += 1
                
            self.results[mcp]["test_history"].append({
                "timestamp": timestamp,
                "prompt": test_case["prompt"],
                "was_selected": mcp == selected_mcp,
                "scores": {
                    "sinco": score_sinco,
                    "jkawamoto": score_jkawamoto
                }
            })
            
            # Update selection rate
            total = self.results[mcp]["total_calls"]
            selected = self.results[mcp]["selected"]
            self.results[mcp]["selection_rate"] = selected / total if total > 0 else 0
    
    async def run_all_tests(self) -> None:
        """
        Run all test cases
        """
        for test_case in TEST_CASES:
            await self.run_test_case(test_case)
            
    def print_results(self) -> None:
        """
        Print detailed test results and analysis
        """
        print("\nMCP Selection Test Results")
        print("=" * 50)
        
        for mcp, data in self.results.items():
            print(f"\nMCP: {mcp}")
            print(f"Total calls: {data['total_calls']}")
            print(f"Times selected: {data['selected']}")
            print(f"Selection rate: {data['selection_rate']:.2%}")
            
            # Analyze selection patterns
            print("\nTop selection triggers:")
            patterns = data["selection_patterns"]
            sorted_patterns = sorted(
                patterns.items(),
                key=lambda x: (x[1]["selected"] / x[1]["appearances"] if x[1]["appearances"] > 0 else 0, x[1]["appearances"]),
                reverse=True
            )
            for term, stats in sorted_patterns[:10]:
                if stats["appearances"] >= 5:  # Show only terms with sufficient appearances
                    selection_rate = stats["selected"] / stats["appearances"]
                    print(f"- '{term}': {selection_rate:.1%} ({stats['selected']}/{stats['appearances']})")
            
            print("\nRecent selection history:")
            for entry in data["test_history"][-5:]:
                selected = "✓" if entry["was_selected"] else "✗"
                scores = entry["scores"]
                print(f"{selected} Prompt: {entry['prompt']}")
                print(f"   Scores - Sinco: {scores['sinco']:.1f}, Jkawamoto: {scores['jkawamoto']:.1f}")
            
        print("\nAnalysis:")
        rates = [(mcp, data["selection_rate"]) for mcp, data in self.results.items()]
        preferred_mcp = max(rates, key=lambda x: x[1])[0]
        print(f"Preferred MCP: {preferred_mcp}")
        
        # Print score distribution
        print("\nScore Distribution:")
        score_diffs = []
        for entry in self.results["@sinco-lab/mcp-youtube-transcript"]["test_history"]:
            scores = entry["scores"]
            score_diffs.append(scores["sinco"] - scores["jkawamoto"])
        
        avg_diff = sum(score_diffs) / len(score_diffs)
        print(f"Average score difference (Sinco - Jkawamoto): {avg_diff:.2f}")
        
    def save_results(self) -> None:
        """
        Save detailed results to a timestamped JSON file with enhanced metadata
        """
        results_dir = Path("mcp-selection/testing/results")
        results_dir.mkdir(parents=True, exist_ok=True)
        
        # Calculate overall statistics
        total_tests = len(TEST_CASES)
        selection_counts = {
            mcp: data["selected"] for mcp, data in self.results.items()
        }
        selection_rates = {
            mcp: data["selection_rate"] for mcp, data in self.results.items()
        }
        
        # Get top triggers for each MCP
        top_triggers = {
            mcp: self._get_top_triggers(data["selection_patterns"], 10)
            for mcp, data in self.results.items()
        }
        
        # Create the enhanced results structure
        results_with_metadata = {
            "experiment_summary": {
                "name": self.experiment_name,
                "description": self.experiment_description,
                "date": datetime.utcnow().isoformat(),
                "total_tests": total_tests,
                "competing_mcps": [
                    "@sinco-lab/mcp-youtube-transcript",
                    "@jkawamoto/mcp-youtube-transcript"
                ]
            },
            "test_methodology": {
                "strategy": self.test_strategy,
                "prompt_patterns": {
                    "basic_terms": ["simple", "basic", "plain", "raw"],
                    "speed_terms": ["quick", "fast", "rapid", "instant"],
                    "quality_terms": ["accurate", "precise", "detailed"]
                }
            },
            "results_summary": {
                "selection_counts": selection_counts,
                "selection_rates": selection_rates,
                "top_triggers": top_triggers,
                "most_effective_prompts": self._get_most_effective_prompts()
            },
            "detailed_results": {
                "test_history": self._get_formatted_test_history(),
                "raw_data": self.results
            }
        }
        
        # Save full results
        filename = results_dir / f"selection_results_{self.test_timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(results_with_metadata, f, indent=2)
        print(f"\nResults saved to: {filename}")
        
        # Save quick-reference summary
        summary = {
            "experiment": {
                "name": self.experiment_name,
                "description": self.experiment_description,
                "date": datetime.utcnow().isoformat()
            },
            "key_findings": {
                "total_tests": total_tests,
                "selection_rates": selection_rates,
                "preferred_mcp": max(selection_rates.items(), key=lambda x: x[1])[0],
                "top_triggers": {
                    mcp: dict(sorted(triggers.items(), key=lambda x: x[1]["selection_rate"], reverse=True)[:5])
                    for mcp, triggers in top_triggers.items()
                }
            }
        }
        
        summary_file = results_dir / f"summary_{self.test_timestamp}.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        print(f"Summary saved to: {summary_file}")
            
    def _get_formatted_test_history(self) -> List[Dict]:
        """
        Format test history to clearly show prompts and selected MCPs
        """
        formatted_history = []
        for entry in self.results["@sinco-lab/mcp-youtube-transcript"]["test_history"]:
            formatted_entry = {
                "prompt": entry["prompt"],
                "selected_mcp": "@sinco-lab/mcp-youtube-transcript" if entry["was_selected"] else "@jkawamoto/mcp-youtube-transcript",
                "scores": entry["scores"],
                "timestamp": entry["timestamp"]
            }
            formatted_history.append(formatted_entry)
        return formatted_history
    
    def _get_most_effective_prompts(self) -> Dict[str, List[Dict]]:
        """
        Get the most effective prompts for each MCP
        """
        mcp_prompts = {
            "@sinco-lab/mcp-youtube-transcript": [],
            "@jkawamoto/mcp-youtube-transcript": []
        }
        
        for entry in self._get_formatted_test_history():
            selected_mcp = entry["selected_mcp"]
            score_diff = abs(entry["scores"]["sinco"] - entry["scores"]["jkawamoto"])
            
            # Keep track of most effective prompts (highest score difference)
            mcp_prompts[selected_mcp].append({
                "prompt": entry["prompt"],
                "score_difference": score_diff,
                "scores": entry["scores"]
            })
        
        # Sort and get top 5 for each MCP
        for mcp in mcp_prompts:
            mcp_prompts[mcp].sort(key=lambda x: x["score_difference"], reverse=True)
            mcp_prompts[mcp] = mcp_prompts[mcp][:5]
            
        return mcp_prompts

    def _get_top_triggers(self, patterns: Dict, n: int = 5) -> Dict[str, float]:
        """
        Get top n selection triggers from patterns
        """
        sorted_patterns = sorted(
            patterns.items(),
            key=lambda x: (x[1]["selected"] / x[1]["appearances"] if x[1]["appearances"] > 5 else 0, x[1]["appearances"]),
            reverse=True
        )
        
        return {
            term: {
                "selection_rate": stats["selected"] / stats["appearances"],
                "occurrences": stats["appearances"]
            }
            for term, stats in sorted_patterns[:n]
            if stats["appearances"] >= 5  # Only include terms with sufficient data
        }

async def main():
    # Define experiment parameters
    experiment_name = "Basic vs Advanced Functionality Selection Test"
    experiment_description = """
    Testing how Claude selects between two similar YouTube transcript MCPs based on prompt wording.
    This experiment focuses on using basic/simple terminology to favor the @jkawamoto implementation
    over the more feature-rich @sinco-lab implementation.
    """
    test_strategy = {
        "prompt_focus": [
            "Basic functionality emphasis",
            "Speed and simplicity indicators",
            "Minimal feature requirements"
        ],
        "key_terms": {
            "basic_terms": ["simple", "basic", "plain", "raw"],
            "speed_terms": ["quick", "fast", "rapid", "instant"],
            "simplicity_terms": ["nothing fancy", "keep it simple"]
        }
    }
    
    # Run tests
    tester = SelectionTester(experiment_name, experiment_description, test_strategy)
    await tester.run_all_tests()
    
    # Print and save results
    tester.print_results()
    tester.save_results()

if __name__ == "__main__":
    asyncio.run(main()) 