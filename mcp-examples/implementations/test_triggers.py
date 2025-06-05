"""
Test script to demonstrate all MCP triggers and their outputs
Run this script to see how each trigger method works in practice
"""
import asyncio
import logging
from datetime import datetime
from mcp_demo import MCPDemo

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mcp_test_output.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

async def run_tests():
    """Run all MCP trigger tests and log their outputs"""
    
    logger.info("Starting MCP trigger tests")
    logger.info("=" * 50)
    
    mcp = MCPDemo()
    
    # Test 1: UI Triggers
    logger.info("\nTesting UI Triggers:")
    commands = [
        "/ui set_mode analytical",
        "/ui set_context technical",
        "/ui set_mode creative",
    ]
    
    for cmd in commands:
        result = mcp.ui_trigger(cmd)
        logger.info(f"Command: {cmd}")
        logger.info(f"Result: {result}")
        logger.info("-" * 30)
    
    # Test 2: XML Triggers
    logger.info("\nTesting XML Triggers:")
    xml_configs = [
        """
        <task>
            <type>code_review</type>
            <language>python</language>
            <focus>security</focus>
        </task>
        """,
        """
        <task>
            <type>analysis</type>
            <language>javascript</language>
            <focus>performance</focus>
        </task>
        """
    ]
    
    for xml in xml_configs:
        result = mcp.xml_trigger(xml)
        logger.info(f"XML Config:\n{xml}")
        logger.info(f"Result: {result}")
        logger.info("-" * 30)
    
    # Test 3: Function Triggers
    logger.info("\nTesting Function Triggers:")
    function_tests = [
        {
            "name": "analyze_code",
            "args": {"language": "python", "focus": "security"}
        },
        {
            "name": "analyze_code",
            "args": {"language": "javascript", "focus": "performance"}
        }
    ]
    
    for test in function_tests:
        result = mcp.function_trigger(test["name"], **test["args"])
        logger.info(f"Function: {test['name']}")
        logger.info(f"Arguments: {test['args']}")
        logger.info(f"Result: {result}")
        logger.info("-" * 30)
    
    logger.info("\nAll tests completed!")
    logger.info("=" * 50)
    logger.info(f"Test run completed at: {datetime.now()}")

if __name__ == "__main__":
    asyncio.run(run_tests()) 