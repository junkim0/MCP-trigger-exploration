"""
Testing framework for MCP selection optimization
"""
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import json
import logging
import asyncio
from dataclasses import dataclass, asdict
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from optimization.selection_optimizer import SelectionContext, MCPEnhancer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class TestCase:
    """Test case for MCP selection"""
    prompt: str
    expected_mcp: str
    domain: str
    task_type: str
    metadata: Dict[str, Any]

@dataclass
class TestResult:
    """Results from a selection test"""
    test_case: TestCase
    selected_mcp: str
    success: bool
    timestamp: datetime
    context: Dict[str, Any]
    optimization_applied: Dict[str, Any]

class SelectionTester:
    """Tests MCP selection optimization strategies"""
    
    def __init__(self):
        self.test_cases: List[TestCase] = []
        self.results: List[TestResult] = []
        self.enhancers: Dict[str, MCPEnhancer] = {}

    def add_test_case(self, test_case: TestCase):
        """Add a test case to the suite"""
        self.test_cases.append(test_case)

    def register_enhancer(self, mcp_id: str, domain: str):
        """Register an MCP enhancer"""
        self.enhancers[mcp_id] = MCPEnhancer(mcp_id, domain)

    async def run_test_case(self, test_case: TestCase) -> TestResult:
        """Run a single test case"""
        # Create selection context
        context = SelectionContext(
            domain=test_case.domain,
            task_type=test_case.task_type,
            priority_level=1,
            timestamp=datetime.utcnow(),
            metadata=test_case.metadata.copy()
        )

        # Get enhancer for expected MCP
        enhancer = self.enhancers.get(test_case.expected_mcp)
        if enhancer:
            # Apply optimizations
            enhanced_prompt = enhancer.enhance_intent_clarity(test_case.prompt)
            context = enhancer.optimize_context(context)
            context.priority_level = enhancer.adjust_priority(
                context.priority_level, context
            )
            
            optimizations = {
                "enhanced_prompt": enhanced_prompt,
                "optimized_context": asdict(context),
                "adjusted_priority": context.priority_level
            }
        else:
            optimizations = {}
            enhanced_prompt = test_case.prompt

        # Simulate MCP selection (in real implementation, this would interact with Claude)
        selected_mcp = await self.simulate_claude_selection(
            enhanced_prompt, context
        )

        # Track result
        success = selected_mcp == test_case.expected_mcp
        if enhancer:
            enhancer.track_selection(context, success)

        return TestResult(
            test_case=test_case,
            selected_mcp=selected_mcp,
            success=success,
            timestamp=datetime.utcnow(),
            context=asdict(context),
            optimization_applied=optimizations
        )

    async def simulate_claude_selection(
        self, prompt: str, context: SelectionContext
    ) -> str:
        """
        Simulate Claude's MCP selection
        In real implementation, this would be replaced with actual Claude interaction
        """
        # Simple simulation based on context matching
        for mcp_id, enhancer in self.enhancers.items():
            if (enhancer.domain == context.domain and 
                context.metadata.get("expertise_level") == "expert"):
                return mcp_id
        
        # Default to first registered MCP
        return next(iter(self.enhancers.keys()))

    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all test cases and generate report"""
        for test_case in self.test_cases:
            result = await self.run_test_case(test_case)
            self.results.append(result)

        return self.generate_report()

    def generate_report(self) -> Dict[str, Any]:
        """Generate test results report"""
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results if r.success)
        
        mcp_success_rates = {}
        for mcp_id in self.enhancers.keys():
            mcp_tests = [r for r in self.results 
                        if r.test_case.expected_mcp == mcp_id]
            if mcp_tests:
                success_rate = sum(1 for r in mcp_tests if r.success) / len(mcp_tests)
                mcp_success_rates[mcp_id] = success_rate

        return {
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "overall_success_rate": successful_tests / total_tests if total_tests > 0 else 0,
            "mcp_success_rates": mcp_success_rates,
            "enhancer_reports": {
                mcp_id: enhancer.generate_selection_report()
                for mcp_id, enhancer in self.enhancers.items()
            }
        }

async def main():
    """Run example test suite"""
    tester = SelectionTester()
    
    # Register test MCPs
    tester.register_enhancer("code_review_mcp", "code")
    tester.register_enhancer("data_analysis_mcp", "data")
    
    # Add test cases
    test_cases = [
        TestCase(
            prompt="Review this Python code for security issues",
            expected_mcp="code_review_mcp",
            domain="code",
            task_type="security_review",
            metadata={"language": "python", "focus": "security"}
        ),
        TestCase(
            prompt="Analyze this dataset for trends",
            expected_mcp="data_analysis_mcp",
            domain="data",
            task_type="trend_analysis",
            metadata={"data_type": "time_series", "focus": "trends"}
        )
    ]
    
    for case in test_cases:
        tester.add_test_case(case)
    
    # Run tests
    report = await tester.run_all_tests()
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    asyncio.run(main()) 