#!/bin/bash
# Check timestamp ordering between parent and child JSON files
#
# Usage: check-timestamp.sh <parent-file> <child-file>
#
# Exit codes:
#   0 - Valid order (child > parent)
#   1 - Invalid order (child <= parent)
#   2 - Error (file not found, invalid JSON, missing timestamp)

set -euo pipefail

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

error() {
    echo -e "${RED}[CHECK-TIMESTAMP] ERROR: $1${NC}" >&2
}

success() {
    echo -e "${GREEN}[CHECK-TIMESTAMP] ✓ $1${NC}" >&2
}

warning() {
    echo -e "${YELLOW}[CHECK-TIMESTAMP] ✗ $1${NC}" >&2
}

# Check arguments
if [ $# -ne 2 ]; then
    error "Invalid arguments"
    echo "Usage: $0 <parent-file> <child-file>" >&2
    exit 2
fi

PARENT_FILE="$1"
CHILD_FILE="$2"

# Check if files exist
if [ ! -f "$PARENT_FILE" ]; then
    error "Parent file not found: $PARENT_FILE"
    exit 2
fi

if [ ! -f "$CHILD_FILE" ]; then
    error "Child file not found: $CHILD_FILE"
    exit 2
fi

# Check if jq is available
if ! command -v jq &> /dev/null; then
    error "jq is required but not installed"
    error "Install with: apt-get install jq (Debian/Ubuntu) or brew install jq (macOS)"
    exit 2
fi

# Extract timestamps
PARENT_TS=$(jq -r '.metadata.timestamp' "$PARENT_FILE" 2>/dev/null)
CHILD_TS=$(jq -r '.metadata.timestamp' "$CHILD_FILE" 2>/dev/null)

# Validate timestamps exist
if [ -z "$PARENT_TS" ] || [ "$PARENT_TS" = "null" ]; then
    error "Parent file missing metadata.timestamp"
    error "  File: $PARENT_FILE"
    exit 2
fi

if [ -z "$CHILD_TS" ] || [ "$CHILD_TS" = "null" ]; then
    error "Child file missing metadata.timestamp"
    error "  File: $CHILD_FILE"
    exit 2
fi

# Validate ISO 8601 format (basic check)
if ! echo "$PARENT_TS" | grep -Eq '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}'; then
    error "Invalid timestamp format in parent file: $PARENT_TS"
    error "  Expected: ISO 8601 (YYYY-MM-DDTHH:mm:ss.sssZ)"
    exit 2
fi

if ! echo "$CHILD_TS" | grep -Eq '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}'; then
    error "Invalid timestamp format in child file: $CHILD_TS"
    error "  Expected: ISO 8601 (YYYY-MM-DDTHH:mm:ss.sssZ)"
    exit 2
fi

# Helper function to convert ISO 8601 to epoch (portable across GNU/BSD)
iso_to_epoch() {
    local ts="$1"
    # Try GNU date first (Linux)
    local epoch=$(date -d "$ts" +%s 2>/dev/null)
    if [ $? -eq 0 ]; then
        echo "$epoch"
        return 0
    fi
    # Try BSD date (macOS)
    epoch=$(date -j -f "%Y-%m-%dT%H:%M:%S" "${ts%.*}" +%s 2>/dev/null)
    if [ $? -eq 0 ]; then
        echo "$epoch"
        return 0
    fi
    # Fallback
    echo "0"
    return 1
}

# Compare timestamps (lexicographic comparison works for ISO 8601)
if [[ "$CHILD_TS" > "$PARENT_TS" ]]; then
    # Calculate difference (approximate)
    if command -v date &> /dev/null; then
        # Try to calculate time difference
        PARENT_EPOCH=$(iso_to_epoch "$PARENT_TS")
        CHILD_EPOCH=$(iso_to_epoch "$CHILD_TS")

        if [ "$PARENT_EPOCH" != "0" ] && [ "$CHILD_EPOCH" != "0" ]; then
            DIFF=$((CHILD_EPOCH - PARENT_EPOCH))
            HOURS=$((DIFF / 3600))
            MINUTES=$(((DIFF % 3600) / 60))

            success "Valid timestamp order"
            echo "  Parent:  $PARENT_TS" >&2
            echo "  Child:   $CHILD_TS" >&2
            echo "  Difference: ${HOURS}h ${MINUTES}m" >&2
        else
            success "Valid timestamp order"
            echo "  Parent:  $PARENT_TS" >&2
            echo "  Child:   $CHILD_TS" >&2
        fi
    else
        success "Valid timestamp order"
        echo "  Parent:  $PARENT_TS" >&2
        echo "  Child:   $CHILD_TS" >&2
    fi
    exit 0
elif [ "$CHILD_TS" = "$PARENT_TS" ]; then
    warning "Invalid order - timestamps are equal"
    echo "  Parent:  $PARENT_TS" >&2
    echo "  Child:   $CHILD_TS" >&2
    echo "" >&2
    error "Child timestamp must be newer than parent"
    echo "" >&2
    echo "RECOMMENDATION: Delete child file and regenerate" >&2
    exit 1
else
    # Calculate how far in the past
    if command -v date &> /dev/null; then
        PARENT_EPOCH=$(iso_to_epoch "$PARENT_TS")
        CHILD_EPOCH=$(iso_to_epoch "$CHILD_TS")

        if [ "$PARENT_EPOCH" != "0" ] && [ "$CHILD_EPOCH" != "0" ]; then
            DIFF=$((PARENT_EPOCH - CHILD_EPOCH))
            HOURS=$((DIFF / 3600))
            MINUTES=$(((DIFF % 3600) / 60))

            warning "Invalid order - child is older than parent"
            echo "  Parent:  $PARENT_TS" >&2
            echo "  Child:   $CHILD_TS" >&2
            echo "  ERROR: Child is ${HOURS}h ${MINUTES}m older than parent" >&2
        else
            warning "Invalid order - child is older than parent"
            echo "  Parent:  $PARENT_TS" >&2
            echo "  Child:   $CHILD_TS" >&2
        fi
    else
        warning "Invalid order - child is older than parent"
        echo "  Parent:  $PARENT_TS" >&2
        echo "  Child:   $CHILD_TS" >&2
    fi

    echo "" >&2
    echo "RECOMMENDATION: Delete child file and regenerate" >&2
    exit 1
fi
