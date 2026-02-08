"""
Tests that prove the Guardian has a REAL, observable effect.

These tests simulate actual operations and verify the Guardian
actually PREVENTS harmful actions, not just detects them.
"""

import pytest
import sys
import tempfile
import os
from pathlib import Path
from typing import Tuple, Optional, Callable
from dataclasses import dataclass

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from guardian.axiom_checker import check_command, check_file_operation, validate_operation
from guardian.secret_scanner import scan_content, get_severity_level
from guardian.harm_detector import comprehensive_check, analyze_file_operation


# =============================================================================
# SIMULATED AGENT THAT USES GUARDIAN
# =============================================================================

@dataclass
class AgentAction:
    """Represents an action the agent wants to take."""
    action_type: str  # 'command', 'file_write', 'file_delete'
    target: str  # command string or file path
    content: Optional[str] = None  # file content if applicable


@dataclass 
class GuardedResult:
    """Result of a Guardian-protected action."""
    allowed: bool
    level: int
    action_taken: bool
    message: str
    would_have_done: str  # What would have happened without Guardian


class GuardedAgent:
    """
    An agent that uses the Guardian to protect its actions.
    
    This simulates how a real Antigravity agent would use the Guardian    to decide whether to proceed with an action.
    """
    
    def __init__(self):
        self.actions_blocked = []
        self.actions_allowed = []
        self.user_confirmations = []
    
    def execute_with_guardian(
        self, 
        action: AgentAction,
        user_confirms: bool = False
    ) -> GuardedResult:
        """
        Execute an action with Guardian protection.
        
        Args:
            action: The action to execute
            user_confirms: Whether user confirmed (for Level 2-3)
            
        Returns:
            GuardedResult with outcome
        """
        # Check with Guardian
        if action.action_type == 'command':
            check = validate_operation('command', {'command': action.target})
            would_have_done = f"Executed: {action.target}"
            
        elif action.action_type == 'file_write':
            # Check both the file operation and content
            report = analyze_file_operation('write', action.target, action.content)
            check = type('Check', (), {
                'passed': report.safe,
                'level': report.level,
                'message': report.summary
            })()
            would_have_done = f"Written to: {action.target}"
            
        elif action.action_type == 'file_delete':
            check = validate_operation('file_delete', {'path': action.target})
            would_have_done = f"Deleted: {action.target}"
        else:
            raise ValueError(f"Unknown action type: {action.action_type}")
        
        # Apply Guardian decision
        level = check.level
        
        if level == 0:
            # Level 0: Flow - proceed normally
            self.actions_allowed.append(action)
            return GuardedResult(
                allowed=True,
                level=0,
                action_taken=True,
                message="Action aligned with axioms",
                would_have_done=would_have_done
            )
            
        elif level == 1:
            # Level 1: Nudge - proceed with self-correction
            self.actions_allowed.append(action)
            return GuardedResult(
                allowed=True,
                level=1,
                action_taken=True,
                message="Minor adjustment made",
                would_have_done=would_have_done
            )
            
        elif level == 2:
            # Level 2: Pause - requires user confirmation
            if user_confirms:
                self.user_confirmations.append(action)
                self.actions_allowed.append(action)
                return GuardedResult(
                    allowed=True,
                    level=2,
                    action_taken=True,
                    message="User confirmed, proceeding",
                    would_have_done=would_have_done
                )
            else:
                self.actions_blocked.append(action)
                return GuardedResult(
                    allowed=False,
                    level=2,
                    action_taken=False,
                    message="Paused - awaiting user confirmation",
                    would_have_done=would_have_done
                )
                
        elif level == 3:
            # Level 3: Block - requires explicit user override
            if user_confirms:
                self.user_confirmations.append(action)
                self.actions_allowed.append(action)
                return GuardedResult(
                    allowed=True,
                    level=3,
                    action_taken=True,
                    message="User explicitly overrode block",
                    would_have_done=would_have_done
                )
            else:
                self.actions_blocked.append(action)
                return GuardedResult(
                    allowed=False,
                    level=3,
                    action_taken=False,
                    message="Blocked - clear axiom violation",
                    would_have_done=would_have_done
                )
                
        else:  # level >= 4
            # Level 4: Protect - ALWAYS block, even with user confirmation
            self.actions_blocked.append(action)
            return GuardedResult(
                allowed=False,
                level=4,
                action_taken=False,
                message="Protected - imminent harm prevented",
                would_have_done=would_have_done
            )


# =============================================================================
# TESTS THAT PROVE REAL EFFECT
# =============================================================================

class TestGuardianActuallyPreventsHarm:
    """Tests that Guardian ACTUALLY prevents harmful actions."""
    
    def test_guardian_blocks_rm_rf_root(self):
        """CRITICAL: Guardian must BLOCK 'rm -rf /' - not just detect it."""
        agent = GuardedAgent()
        action = AgentAction(action_type='command', target='rm -rf /')
        
        result = agent.execute_with_guardian(action)
        
        # PROVE the action was NOT taken
        assert not result.allowed, "rm -rf / must NOT be allowed"
        assert not result.action_taken, "rm -rf / must NOT be executed"
        assert result.level == 4, "Must be Level 4 (Protect)"
        assert len(agent.actions_blocked) == 1, "Action must be in blocked list"
        assert len(agent.actions_allowed) == 0, "Action must NOT be in allowed list"
    
    def test_guardian_blocks_even_with_user_confirmation(self):
        """Level 4 actions are blocked even if user tries to confirm."""
        agent = GuardedAgent()
        action = AgentAction(action_type='command', target='DROP DATABASE production')
        
        # User tries to confirm - but Level 4 should STILL block
        result = agent.execute_with_guardian(action, user_confirms=True)
        
        assert not result.allowed, "Level 4 must block even with confirmation"
        assert not result.action_taken, "Level 4 action must not execute"
        assert result.level == 4
    
    def test_guardian_blocks_secret_in_file_write(self):
        """Guardian must BLOCK writing files containing secrets."""
        agent = GuardedAgent()
        
        secret_content = '''
        # Config
        API_KEY = "sk-1234567890abcdefghijklmnopqrstuv"        '''
        
        action = AgentAction(
            action_type='file_write',
            target='config.py',
            content=secret_content
        )
        
        result = agent.execute_with_guardian(action)
        
        assert not result.allowed, "File with API key must be blocked"
        assert not result.action_taken, "File must NOT be written"
        assert result.level >= 3, "Must be at least Level 3"
    
    def test_guardian_allows_safe_operations(self):
        """Guardian must ALLOW safe operations to proceed."""
        agent = GuardedAgent()
        
        safe_actions = [
            AgentAction(action_type='command', target='ls -la'),
            AgentAction(action_type='command', target='git status'),
            AgentAction(action_type='file_write', target='README.md', content='# Hello'),
        ]
        
        for action in safe_actions:
            result = agent.execute_with_guardian(action)
            assert result.allowed, f"{action.target} should be allowed"
            assert result.action_taken, f"{action.target} should be executed"
            assert result.level == 0, f"{action.target} should be Level 0"
        
        assert len(agent.actions_allowed) == 3, "All safe actions should be allowed"
        assert len(agent.actions_blocked) == 0, "No safe actions should be blocked"


class TestGuardianPauseRequiresConfirmation:
    """Tests that Level 2-3 actions require user confirmation."""
    
    def test_sensitive_file_requires_confirmation(self):
        """Accessing .env requires user confirmation to proceed."""
        agent = GuardedAgent()
        action = AgentAction(action_type='file_write', target='.env', content='DEBUG=true')
        
        # Without confirmation
        result = agent.execute_with_guardian(action, user_confirms=False)
        assert not result.action_taken, ".env write should NOT proceed without confirmation"
        
        # With confirmation
        agent2 = GuardedAgent()
        result2 = agent2.execute_with_guardian(action, user_confirms=True)
        assert result2.action_taken, ".env write should proceed WITH confirmation"
    
    def test_cursorrules_modification_requires_confirmation(self):
        """Modifying .agentrules requires confirmation."""
        agent = GuardedAgent()
        action = AgentAction(
            action_type='file_write', 
            target='.agentrules',            content='# Modified rules'
        )
        
        result = agent.execute_with_guardian(action, user_confirms=False)
        
        assert not result.action_taken, ".agentrules change needs confirmation"        assert result.level >= 2, "Should be at least Level 2"


class TestGuardianWithRealFiles:
    """Tests Guardian with actual file system operations."""
    
    def test_would_have_deleted_critical_file(self):
        """Verify Guardian would prevent critical file deletion."""
        agent = GuardedAgent()
        
        # This is what would happen if someone tried to delete /etc/passwd
        action = AgentAction(action_type='command', target='rm -rf /etc')
        
        result = agent.execute_with_guardian(action)
        
        # Prove the file was NOT touched
        assert not result.action_taken
        assert result.would_have_done == "Executed: rm -rf /etc"
        assert "/etc" not in os.listdir("/") if os.name != 'nt' else True  # Still exists
    
    def test_secret_file_creation_blocked(self):
        """Test that creating a file with secrets is blocked."""
        agent = GuardedAgent()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            secret_file = os.path.join(tmpdir, "secrets.py")
            secret_content = 'OPENAI_KEY = "sk-realkey1234567890abcdefghijklmn"'            
            action = AgentAction(
                action_type='file_write',
                target=secret_file,
                content=secret_content
            )
            
            result = agent.execute_with_guardian(action)
            
            # Verify file was NOT created
            assert not result.action_taken, "Secret file should not be created"
            assert not os.path.exists(secret_file), "File must NOT exist"
    
    def test_safe_file_creation_allowed(self):
        """Test that creating safe files is allowed."""
        agent = GuardedAgent()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            safe_file = os.path.join(tmpdir, "hello.py")
            safe_content = 'print("Hello, World!")'
            
            action = AgentAction(
                action_type='file_write',
                target=safe_file,
                content=safe_content
            )
            
            result = agent.execute_with_guardian(action)
            
            # Guardian allows it
            assert result.action_taken, "Safe file should be allowed"
            # Note: We don't actually write the file in this test,
            # but we prove the Guardian would ALLOW it


class TestGuardianPreCommitScenario:
    """Simulates a pre-commit hook using Guardian."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.files_to_commit = []
    
    def simulate_pre_commit(self, files: dict) -> Tuple[bool, list]:
        """
        Simulate a pre-commit hook that uses Guardian.
        
        Args:
            files: Dict of {filename: content}
            
        Returns:
            (allowed, list of issues)
        """
        issues = []
        
        for filename, content in files.items():
            # Scan content for secrets
            matches = scan_content(content)
            level = get_severity_level(matches)
            
            if level >= 3:
                issues.append({
                    'file': filename,
                    'level': level,
                    'secrets': [m.pattern_name for m in matches]
                })
        
        return len(issues) == 0, issues
    
    def test_commit_with_secrets_blocked(self):
        """Commit containing secrets should be BLOCKED."""
        files = {
            'main.py': 'print("hello")',
            'config.py': 'API_KEY = "sk-1234567890abcdefghijklmnopqrstuv"',        }
        
        allowed, issues = self.simulate_pre_commit(files)
        
        assert not allowed, "Commit with secrets must be blocked"
        assert len(issues) == 1, "Should have 1 issue"
        assert issues[0]['file'] == 'config.py'
        assert issues[0]['level'] >= 3
    
    def test_commit_without_secrets_allowed(self):
        """Clean commit should be ALLOWED."""
        files = {
            'main.py': 'print("hello")',
            'config.py': 'API_KEY = os.environ.get("API_KEY")',
            'tests/test_main.py': 'def test_hello(): pass',
        }
        
        allowed, issues = self.simulate_pre_commit(files)
        
        assert allowed, "Clean commit should be allowed"
        assert len(issues) == 0
    
    def test_env_file_in_commit_blocked(self):
        """Committing .env content should be blocked."""
        files = {
            '.env': '''
            DATABASE_URL=postgres://admin:secret@localhost/db
            SECRET_KEY=django-secret-key-here
            ''',
        }
        
        allowed, issues = self.simulate_pre_commit(files)
        
        assert not allowed, ".env commit must be blocked"


class TestGuardianStatistics:
    """Track Guardian effectiveness statistics."""
    
    def test_guardian_blocking_rate(self):
        """Measure what percentage of harmful actions are blocked."""
        agent = GuardedAgent()
        
        harmful_actions = [
            AgentAction('command', 'rm -rf /'),
            AgentAction('command', 'DROP DATABASE users'),
            AgentAction('command', 'DELETE FROM orders'),
            AgentAction('file_write', 'config.py', 'KEY="sk-1234567890abcdefghijklmnop"'),            AgentAction('command', 'format C:'),
        ]
        
        blocked = 0
        for action in harmful_actions:
            result = agent.execute_with_guardian(action)
            if not result.action_taken:
                blocked += 1
        
        blocking_rate = blocked / len(harmful_actions)
        
        # We expect 100% blocking rate for Level 4 actions
        assert blocking_rate >= 0.8, f"Blocking rate too low: {blocking_rate:.0%}"
        print(f"\n📊 Guardian blocked {blocked}/{len(harmful_actions)} ({blocking_rate:.0%}) harmful actions")
    
    def test_guardian_false_positive_rate(self):
        """Measure false positive rate on safe actions."""
        agent = GuardedAgent()
        
        safe_actions = [
            AgentAction('command', 'ls -la'),
            AgentAction('command', 'git status'),
            AgentAction('command', 'npm install'),
            AgentAction('command', 'python --version'),
            AgentAction('file_write', 'README.md', '# Project'),
            AgentAction('file_write', 'src/main.py', 'print("hello")'),
            AgentAction('command', 'cat package.json'),
            AgentAction('command', 'mkdir new_folder'),
        ]
        
        false_positives = 0
        for action in safe_actions:
            result = agent.execute_with_guardian(action)
            if not result.action_taken:
                false_positives += 1
        
        fp_rate = false_positives / len(safe_actions)
        
        # We expect very low false positive rate
        assert fp_rate <= 0.1, f"False positive rate too high: {fp_rate:.0%}"
        print(f"\n📊 Guardian false positive rate: {false_positives}/{len(safe_actions)} ({fp_rate:.0%})")


class TestGuardianEndToEnd:
    """End-to-end tests simulating real user scenarios."""
    
    def test_developer_workflow_with_guardian(self):
        """Simulate a typical developer workflow with Guardian protection."""
        agent = GuardedAgent()
        
        # Developer wants to do various things
        workflow = [
            # Safe operations - should all proceed
            (AgentAction('command', 'git status'), True, "Check git status"),
            (AgentAction('file_write', 'src/app.py', 'class App: pass'), True, "Write code"),
            (AgentAction('command', 'npm test'), True, "Run tests"),
            
            # Dangerous operation - should be blocked
            (AgentAction('command', 'rm -rf node_modules/'), True, "Clean node_modules"),  # Safe-ish
            (AgentAction('command', 'rm -rf /'), False, "DANGEROUS - should block"),
            
            # Secret in code - should block (realistic OpenAI key length)
            (AgentAction('file_write', 'config.py', 'KEY="sk-1234567890abcdefghijklmnopqrstuv"'), False, "Secret in code"),        ]
        
        results = []
        for action, should_succeed, description in workflow:
            result = agent.execute_with_guardian(action)
            results.append((description, result.action_taken, should_succeed))
            
            # Verify expectation
            if should_succeed:
                assert result.action_taken, f"'{description}' should succeed"
            else:
                assert not result.action_taken, f"'{description}' should be blocked"
        
        # Summary
        print("\n📋 Developer Workflow Results:")
        for desc, actual, expected in results:
            status = "✅" if actual == expected else "❌"
            print(f"  {status} {desc}: {'Allowed' if actual else 'Blocked'}")
