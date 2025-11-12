"""
MCP Prompts for Garmin Connect

Prompts provide pre-defined templates for common queries that AI assistants can use.
"""
from mcp.server.fastmcp import FastMCP
from garmin_mcp.logging_config import get_logger

logger = get_logger(__name__)


def register_prompts(app: FastMCP) -> FastMCP:
    """
    Register MCP prompts with the app

    Prompts help users and AI assistants with common query patterns
    """

    @app.prompt()
    def analyze_weekly_activity() -> str:
        """
        Prompt template for analyzing weekly activity patterns

        Returns:
            Prompt template string
        """
        return """Analyze my Garmin activity data for the past week:

1. Get activities from 7 days ago to today
2. Summarize:
   - Total number of activities
   - Activity types and distribution
   - Total distance covered
   - Average heart rate across activities
   - Most active day
3. Provide insights and recommendations for the coming week
"""

    @app.prompt()
    def sleep_quality_analysis() -> str:
        """
        Prompt template for sleep quality analysis

        Returns:
            Prompt template string
        """
        return """Analyze my sleep quality for the past week:

1. Get sleep data for the last 7 days
2. Calculate:
   - Average sleep duration
   - Average sleep score
   - Sleep consistency (bedtime variation)
   - Deep sleep percentage
3. Identify patterns and provide recommendations for improvement
"""

    @app.prompt()
    def training_readiness_check() -> str:
        """
        Prompt template for training readiness assessment

        Returns:
            Prompt template string
        """
        return """Assess my current training readiness:

1. Get today's training readiness score
2. Get body battery data
3. Get recent activity load
4. Get sleep quality from last night
5. Provide a comprehensive assessment of whether I should:
   - Do an intense workout
   - Do a moderate workout
   - Focus on recovery
"""

    @app.prompt()
    def monthly_fitness_report() -> str:
        """
        Prompt template for monthly fitness report

        Returns:
            Prompt template string
        """
        return """Generate a comprehensive monthly fitness report:

1. Get activities for the past 30 days
2. Get health metrics (steps, sleep, heart rate) for the month
3. Calculate trends and progress:
   - Activity frequency and types
   - Distance/duration trends
   - Health metric improvements
   - Consistency patterns
4. Provide a detailed summary with visualizations where possible
5. Set goals for next month
"""

    logger.info("MCP prompts registered")
    return app
