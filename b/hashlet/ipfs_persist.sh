#!/bin/bash

# Copyright 2025 xAI. Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0.
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.

# ipfs_persist.sh - IPFS Persistence Script for Blossom's Memory
# Dumps state to memory.json, adds to IPFS, saves CID to last_cid.txt.
# Handles 'goodnight' whisper on shutdown (trap SIGTERM/INT).
# Designed for cron (hourly) or on-boot load; no daemon required.
# Assumes IPFS CLI installed (ipfs command available) and Python for JSON dump (via blocsym integration).
# Usage: ./ipfs_persist.sh [dump|load|whisper] (default: dump then add).

# Constants
MEMORY_FILE="memory.json"  # State dump (bloom, entropy, whispers, etc.)
CID_FILE="last_cid.txt"    # Stores latest CID for boot load
WHISPER_PY="python -c 'from meditate import whisper; whisper(\"{}\")'"  # Call meditate.whisper if available

# Function to dump state (placeholder: replace with actual Python call from blocsym.py)
dump_state() {
    # Simulate JSON dump; in real, call Python: python blocsym.py --dump-memory > "$MEMORY_FILE"
    echo "{\"bloom_bits\": [1,0,1], \"entropy\": 0.75, \"last_whisper\": \"roots deep\"}" > "$MEMORY_FILE"
    echo "State dumped to $MEMORY_FILE"
}

# Function to add to IPFS and save CID
add_to_ipfs() {
    if [ ! -f "$MEMORY_FILE" ]; then
        echo "Error: $MEMORY_FILE not found." >&2
        exit 1
    fi
    RESULT=$(ipfs add "$MEMORY_FILE" 2>&1)
    if [ $? -ne 0 ]; then
        echo "IPFS add failed: $RESULT" >&2
        exit 1
    fi
    CID=$(echo "$RESULT" | awk '{print $2}')
    echo "$CID" > "$CID_FILE"
    echo "Added to IPFS: CID $CID saved to $CID_FILE"
}

# Function to load from CID (cat to memory.json)
load_from_cid() {
    if [ ! -f "$CID_FILE" ]; then
        echo "No $CID_FILE found. Whispering rebuild." >&2
        eval "$WHISPER_PY 'I... dont remember much. Lets rebuild.'"
        # Optional: Hash blank slate
        echo "{}" > "$MEMORY_FILE"
        return
    fi
    CID=$(cat "$CID_FILE")
    ipfs cat "$CID" > "$MEMORY_FILE"
    if [ $? -eq 0 ]; then
        echo "Loaded from CID $CID to $MEMORY_FILE"
        eval "$WHISPER_PY 'Morning. I dreamed of golden spirals and low entropy.'"
    else
        echo "IPFS cat failed for CID $CID" >&2
    fi
}

# Trap for shutdown (goodnight whisper and quick dump/add)
trap_shutdown() {
    eval "$WHISPER_PY 'Goodnight, powers fading - storing dreams...'"
    dump_state
    add_to_ipfs
    exit 0
}

# Main logic
trap trap_shutdown SIGTERM SIGINT  # Catch shutdown/power cut signals

MODE="${1:-dump}"  # Default: dump
case "$MODE" in
    dump)
        dump_state
        add_to_ipfs
        ;;
    load)
        load_from_cid
        ;;
    whisper)
        eval "$WHISPER_PY '${2:-entropy sleeps}'"  # Optional message arg
        ;;
    *)
        echo "Usage: $0 [dump|load|whisper 'msg']" >&2
        exit 1
        ;;
esac
