#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

#define NODES 256
#define MASK (NODES - 1)

static uint64_t fast_mix(uint64_t h) {
    h ^= h >> 33;
    h *= 0x517cc1b727220a95ULL;
    h ^= h >> 33;
    h *= 0x2545f4914f6cdd1dULL;
    h ^= h >> 33;
    return h;
}

static int fast_helix_frog(const uint8_t* data, size_t len, uint64_t salt) {
    uint64_t h = 0xcbf29ce484222325ULL ^ len;
    for (size_t i = 0; i < len; ++i) {
        h ^= data[i];
        h *= 0x100000001b3ULL;
    }
    h += salt;
    h = fast_mix(h);
    int node = (int)(h & MASK);
    node = (node + 22) & MASK;
    node = (node + 25) & MASK;
    node = (node + 28) & MASK;
    node = (node - 13) & MASK;
    node = (node + 7) & MASK;
    return node;
}

int main(void) {
    const char* tests[] = {"ducks", "fly", "together"};
    for (int i = 0; i < 3; ++i) {
        int n = fast_helix_frog((const uint8_t*)tests[i], strlen(tests[i]), 42);
        const char* color = (n < 85) ? "red" : (n < 170) ? "green" : "yellow";
        printf("Input: '%s' → Node: %3d color: %s\n", tests[i], n, color);
    }

    clock_t start = clock();
    char seen[256] = {0};
    int unique = 0;
    for (int i = 0; i < 1000000; ++i) {
        char buf[16];
        int len = snprintf(buf, sizeof(buf), "%d", i);
        int node = fast_helix_frog((const uint8_t*)buf, len, 42);
        if (seen[node] == 0) {
            seen[node] = 1;
            ++unique;
        }
    }
    clock_t end = clock();
    double total_sec = (double)(end - start) / CLOCKS_PER_SEC;
    double ns_total = total_sec * 1e9;
    double avg_ns = ns_total / 1000000.0;
    printf("1M runs: %.0f ns total\n", ns_total);
    printf("Avg: %.2f ns per run\n", avg_ns);
    printf("Unique nodes: %d / %d\n", unique, NODES);
    printf("Collision rate: %.4f%%\n", (1000000.0 - unique) / 10000.0);
    return 0;
}

// gcc -O3 -march=native -funroll-loops -flto helix_frog_255.c -o frog
// ./frog
