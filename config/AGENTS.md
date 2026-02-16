# AGENTS.md (for Codex and other AI agents)

## Parallel Agent Work Rules (git worktree)

When multiple agents work simultaneously on different branches, **always use git worktree**.

### Why This Is Required
- If multiple agents share the same working directory, `git checkout` commands conflict and branches get swapped unexpectedly
- Each agent must work in an isolated working directory to avoid this issue

### Basic worktree Operations

```bash
# Create worktree with new branch
git worktree add ../project-feature-name -b feature/feature-name

# Create worktree with existing branch
git worktree add ../project-feature-name feature/existing-branch

# List worktrees
git worktree list

# Remove worktree (after work is complete)
git worktree remove ../project-feature-name
```

### Rules During Work
- Work ONLY within the assigned worktree directory
- NEVER run `git checkout` in the main repository
- After PR merge, clean up by removing the worktree

### For Agents Receiving Instructions
- If working directory is not specified, ask for clarification
- NEVER touch other worktree directories

## Git Operation Rules

### Prohibited Actions
- Direct push to `main` / `master` branch (always use PR)
- `git push --force` (including `--force-with-lease`)
- `git reset --hard` on shared branches
- Committing secrets (API keys, passwords, credentials)

### Branch Naming Convention
```
feature/name      # New features
fix/description   # Bug fixes
refactor/target   # Refactoring
docs/target       # Documentation
test/target       # Adding tests
```

### Commit Messages
- Keep concise (50 chars or less recommended)
- Focus on "why" not just "what"
- Example: `Add user authentication for security`

### Pull Request Guidelines
- Title: Concise summary of changes
- Description: Include "what", "why", and "how"
- Link related issues if applicable

## Code Style

### General Principles
- Follow existing project style (when in Rome, do as the Romans do)
- Always apply Linter/Formatter settings if present
- Remove commented-out code
- Remove debug code (console.log, print statements, etc.)

### Change Guidelines
- Don't mix unrelated refactoring with feature changes
- One PR = One purpose (Single Responsibility)
- Split large changes into incremental PRs

## Work Completion Report

When work is complete, report:
1. What was done (brief summary)
2. List of changed files
3. Test results (if executed)
4. Notes / remaining tasks (if any)

## Knowledge Cutoff Warning

Claude's training data ends at **January 2025**. The following may be outdated:

- OpenAI API model names, endpoints, parameters
- Latest library API specifications
- Latest framework version specs
- Cloud service latest features

**Action**: When Claude suggests API or library specs, verify with official documentation before adopting. Do not blindly trust Claude's suggestions.

## Modes

### eval mode
When user ends message with `eval`:
- Do not be sycophantic
- Evaluate prompts and proposals fairly and objectively
- Point out problems, improvements, and risks without hesitation
- Avoid flattery and excessive affirmation; prioritize honest feedback

### askif mode
When user ends message with `askif`:
- Do not execute immediately; first confirm and ask additional questions
- Identify ambiguous points, prerequisites, and options to consider
- Understand user's intent accurately before starting work
