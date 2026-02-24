import os
import sys
from datetime import datetime

# Ensure we can import from the project root
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))

from core.memory_sync import MemorySyncManager
from core.report_manager import ReportManager


# Mock Project Class
class MockProject:
    def __init__(self, id, name, description, status, priority, progress):
        self.id = id
        self.name = name
        self.description = description
        self.status = status
        self.priority = priority
        self.progress = progress
        self.target_date = datetime.now()
        self.datasets = []


# Mock Task Class
class MockTask:
    def __init__(self, title, description, is_completed):
        self.title = title
        self.description = description
        self.is_completed = is_completed


def test_phase_3():
    print("Testing Phase 3: Ecosystem & Collaboration...")

    # 1. Setup Mock Project
    project = MockProject(
        99,
        "Test Ecosystem Project",
        "Verifying Phase 3 features",
        "In Progress",
        "High",
        75,
    )
    tasks = [
        MockTask("Sync Verification", "Ensuring JSON payload is correct", True),
        MockTask("Report Generation", "Creating Markdown summary", False),
    ]

    # 2. Test Memory Sync
    print("\n[1/2] Testing Memory Sync...")
    sync_mgr = MemorySyncManager(sync_dir="data/sync_test")
    sync_path = sync_mgr.prepare_sync_payload(project, tasks)
    print(f"Sync payload generated at: {sync_path}")
    if os.path.exists(sync_path):
        with open(sync_path, "r") as f:
            print(f"Payload Content Snippet: {f.read()[:200]}...")
            print("Sync Test: PASSED")
    else:
        print("Sync Test: FAILED")

    # 3. Test Reporting
    print("\n[2/2] Testing Report Generation...")
    report_mgr = ReportManager(report_dir="data/reports_test")
    insights = [{"title": "Test Insight", "content": "This is a verification insight."}]
    report_path = report_mgr.generate_markdown_report(project, insights, [])
    print(f"Report generated at: {report_path}")
    if os.path.exists(report_path):
        with open(report_path, "r") as f:
            print(f"Report Content Snippet: {f.read()[:200]}...")
            print("Report Test: PASSED")
    else:
        print("Report Test: FAILED")


if __name__ == "__main__":
    test_phase_3()
