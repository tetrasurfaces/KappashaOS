// reaper.c - BlockChan Bloom Reaper

// Monitors bloom_state.bin for overflipped bits (>3 per bit).

// Prints SHA-256 hash to console and logs to reaper_log.txt, then deletes file.

// AGPL-3.0 licensed. -- OliviaLynnArchive fork, 2025

#include <stdio.h>

#include <stdlib.h>

#include <string.h>

#include <unistd.h>

#include <sys/stat.h>

#include <openssl/sha.h>  // For SHA-256; link with -lcrypto

// Constants

#define BLOOM_FILE "bloom_state.bin"  // Serialized bit array (128 bytes for 1024 bits)

#define BIT_SIZE 1024

#define BYTE_SIZE (BIT_SIZE / 8)  // 128 bytes

#define MAX_FLIPS 3

#define FLIP_LOG "flip_log.txt"  // Side file for per-bit flip counts (one int per bit)

#define REAPER_LOG "reaper_log.txt"  // Local log file for alerts instead of email

// Pack/unpack helpers (Bloom array is [0/1] ints, but serialize as bits in bytes)

void pack_bits(unsigned char *bytes, int *array, int size) {

    for (int i = 0; i < size; i++) {

        int byte_idx = i / 8;

        int bit_idx = 7 - (i % 8);

        if (array[i]) bytes[byte_idx] |= (1 << bit_idx);

    }

}

void unpack_bits(int *array, unsigned char *bytes, int size) {

    for (int i = 0; i < size; i++) {

        int byte_idx = i / 8;

        int bit_idx = 7 - (i % 8);

        array[i] = (bytes[byte_idx] & (1 << bit_idx)) ? 1 : 0;

    }

}

// Local alert logger (replaces SMTP; appends to reaper_log.txt)

int log_alert(const char *hash_hex) {

    FILE *log = fopen(REAPER_LOG, "a");

    if (!log) {

        fprintf(stderr, "Failed to open reaper_log.txt\n");

        return -1;

    }

    fprintf(log, "Subject: Bloom Reaper Alert\n\nOverflipped bits detected. Hash: %s\n\n", hash_hex);

    fclose(log);

    return 0;

}

// Load flip counts from log (one int per bit, newline separated)

int *load_flip_counts() {

    FILE *log = fopen(FLIP_LOG, "r");

    if (!log) return NULL;  // No log? Assume 0 flips

    int *flips = calloc(BIT_SIZE, sizeof(int));

    if (!flips) return NULL;

    int idx = 0;

    while (idx < BIT_SIZE && fscanf(log, "%d", &flips[idx]) == 1) {

        idx++;

    }

    fclose(log);

    return flips;

}

// Save updated flips (called if no delete, but here we delete on trigger)

void save_flip_counts(int *flips) {

    FILE *log = fopen(FLIP_LOG, "w");

    if (!log) return;

    for (int i = 0; i < BIT_SIZE; i++) {

        fprintf(log, "%d\n", flips[i]);

    }

    fclose(log);

}

int main() {

    // Load serialized Bloom state

    FILE *file = fopen(BLOOM_FILE, "rb");

    if (!file) {

        fprintf(stderr, "No bloom_state.bin found. Nothing to reap.\n");

        return 0;

    }

    unsigned char bytes[BYTE_SIZE];

    fread(bytes, 1, BYTE_SIZE, file);

    fclose(file);

    int array[BIT_SIZE];

    unpack_bits(array, bytes, BIT_SIZE);

    // Load flip counts

    int *flips = load_flip_counts();

    if (!flips) {

        flips = calloc(BIT_SIZE, sizeof(int));  // Assume 0

    }

    // Scan for overflips (simulate diff: if bit==1, assume odd flips; but use log)

    int overflip_idx = -1;

    for (int i = 0; i < BIT_SIZE; i++) {

        // Simulate increment on load (for this run's adds; in prod, diff prev state)

        if (array[i] == 1) flips[i]++;  // Rough sim; real would diff states

        if (flips[i] > MAX_FLIPS) {

            overflip_idx = i;

            break;

        }

    }

    if (overflip_idx == -1) {

        // No overflip; save and exit

        save_flip_counts(flips);

        free(flips);

        printf("Reaper: All bits healthy.\n");

        return 0;

    }

    // Trigger: Hash the array

    unsigned char hash_bin[SHA256_DIGEST_LENGTH];

    SHA256(bytes, BYTE_SIZE, hash_bin);

    char hash_hex[SHA256_DIGEST_LENGTH * 2 + 1];

    for (int i = 0; i < SHA256_DIGEST_LENGTH; i++) {

        sprintf(hash_hex + 2*i, "%02x", hash_bin[i]);

    }

    char state_str[256];  // Buffer for state description

    sprintf(state_str, "overflip at bit %d. Hash: %s", overflip_idx, hash_hex);

    // Log alert locally

    if (log_alert(hash_hex) == 0) {

        printf("Reaper: Alert logged for %s\n", state_str);

    } else {

        fprintf(stderr, "Reaper: Logging failed.\n");

    }

    // Delete file

    unlink(BLOOM_FILE);

    unlink(FLIP_LOG);  // Clean log too

    // Meditation print post-unlink

    printf("\033[34mMeditation: %s entropy holds.\033[0m\n", state_str);

    free(flips);

    printf("Reaper: State deleted. Breath restored.\n");

    return 0;

}
