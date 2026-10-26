#!/usr/bin/env bash
# scripts/verify.sh
# Verification and test suite for the Gemini Founder Skill plugin.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "==> Verifying Gemini Founder Skill Plugin at: $REPO_ROOT"
ERRORS=0

# 1. Verify JSON manifests
echo "1. Checking JSON manifests..."
for json_file in "$REPO_ROOT/plugin.json" "$REPO_ROOT/plugins/gemini-founder-skill/plugin.json" "$REPO_ROOT/gemini-extension.json"; do
    if [ -f "$json_file" ]; then
        if python3 -m json.tool "$json_file" > /dev/null 2>&1; then
            echo "  ✓ Valid JSON: ${json_file#$REPO_ROOT/}"
        else
            echo "  ✗ INVALID JSON: ${json_file#$REPO_ROOT/}"
            ERRORS=$((ERRORS + 1))
        fi
    else
        echo "  ✗ Missing JSON file: ${json_file#$REPO_ROOT/}"
        ERRORS=$((ERRORS + 1))
    fi
done

# 2. Verify all 11 Skills and Frontmatter
echo "2. Checking 11 founder skills and frontmatter..."
SKILLS=(
    "founder-board"
    "founder-competitors"
    "founder-consumer"
    "founder-pricing"
    "founder-offer"
    "founder-cfo"
    "founder-marketing"
    "founder-brand"
    "founder-ops"
    "founder-launch"
    "founder-plan"
)

for s in "${SKILLS[@]}"; do
    SKILL_FILE="$REPO_ROOT/skills/$s/SKILL.md"
    if [ -f "$SKILL_FILE" ]; then
        if grep -q "^name: $s" "$SKILL_FILE" && grep -q "^description:" "$SKILL_FILE"; then
            echo "  ✓ Valid frontmatter: skills/$s/SKILL.md"
        else
            echo "  ✗ Invalid frontmatter: skills/$s/SKILL.md"
            ERRORS=$((ERRORS + 1))
        fi
    else
        echo "  ✗ Missing skill file: skills/$s/SKILL.md"
        ERRORS=$((ERRORS + 1))
    fi
done

# 3. Verify Rules & Assets
echo "3. Checking rules, assets, and documentation..."
REQUIRED_FILES=(
    "rules/AGENTS.md"
    "rules/GEMINI.md"
    "assets/logo.svg"
    "README.md"
    "LICENSE"
)

for req in "${REQUIRED_FILES[@]}"; do
    if [ -f "$REPO_ROOT/$req" ]; then
        echo "  ✓ Exists: $req"
    else
        echo "  ✗ Missing file: $req"
        ERRORS=$((ERRORS + 1))
    fi
done

# 4. Verify Shell Scripts syntax
echo "4. Checking shell scripts syntax..."
for scr in "scripts/install.sh" "scripts/verify.sh"; do
    if [ -f "$REPO_ROOT/$scr" ]; then
        if bash -n "$REPO_ROOT/$scr"; then
            echo "  ✓ Bash syntax clean: $scr"
        else
            echo "  ✗ Bash syntax errors in $scr"
            ERRORS=$((ERRORS + 1))
        fi
    else
        echo "  ✗ Missing script: $scr"
        ERRORS=$((ERRORS + 1))
    fi
done

# 5. Run Python Unit Test Suite
echo "5. Running Python unit test suite..."
if python3 -m unittest discover -s "$REPO_ROOT/tests" -v; then
    echo "  ✓ Python unit tests passed"
else
    echo "  ✗ Python unit tests FAILED"
    ERRORS=$((ERRORS + 1))
fi

echo ""
if [ "$ERRORS" -eq 0 ]; then
    echo "==> ALL CHECKS PASSED! Gemini Founder Skill plugin is healthy."
    exit 0
else
    echo "==> FAILED with $ERRORS error(s)."
    exit 1
fi
