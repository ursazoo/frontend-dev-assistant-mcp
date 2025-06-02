import asyncio
from src.mcp_local.usage_tracker import UsageTracker

async def main():
    tracker = UsageTracker()
    report = await tracker.get_stats("month")
    print(report)

if __name__ == "__main__":
    asyncio.run(main()) 