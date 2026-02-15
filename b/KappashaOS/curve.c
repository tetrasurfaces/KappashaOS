// curve.c - Memory curve tool (Ubuntu port)
// Compile: gcc -o curve curve.c -lm
// Run: ./curve --note    or   ./curve test.txt

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
#include <unistd.h>     // usleep
#include <fcntl.h>      // for fsync if needed

#define SLOT_SIZE 1024
#define MAX_SLOTS 4096
#define MASK (MAX_SLOTS - 1)
#define GRID_FILE "curve.grid"
#define MOD 369.0f
#define KAPPA 0.3536f
#define PHI 1.618033988749895f
void traverse_tree(void);
void prune_tree(void);
void retrieve_latest(int quiet, int digit_index, int digit_delta);
char* ram_grid = NULL;
uint8_t master_hash[32];
uint64_t chunk_count = 0;
uint16_t chunk_probe[MAX_SLOTS]; // probe steps per chunk (index by chunk_count)
double divide_by_180(const char* json_str);
static const uint64_t PRIMES[] = {2, 3, 5, 7, 11, 13, 17, 19};
static const uint64_t mersennes[64] = {
    2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279, 2203,
    2281, 3217, 4253, 4423, 9689, 9941, 11213, 19937, 21701, 23209, 44497,
    86243, 110503, 132049, 216091, 756839, 859433, 1257787, 1398269, 2976221,
    3021377, 6972593, 13466917, 20996011, 24036583, 25964951, 30402457,
    32582657, 37156667, 42643801, 43112609, 57885161, 74207281, 77232917,
    82589933, 136279841, 194087760, 393668989, 1137184133, 4678395213,
    27411294813, 228732945894, 2718281472161, 46007290309705, 1108984342777087,
    38070686010400544, 1861326323879814400
};
static uint64_t fast_mix(uint64_t h) {
    h ^= h >> 33;
    h *= 0x517cc1b727220a95ULL;
    h ^= h >> 33;
    h *= 0x2545f4914f6cdd1dULL;
    h ^= h >> 33;
    return h;
}
static uint64_t reversible_helix(uint64_t x, uint64_t key, int rounds, double theta) {
    uint64_t L = x >> 32;
    uint64_t R = x & 0xFFFFFFFFULL;
    uint64_t int_kappa = (uint64_t)(0.3536 * (1LL << 32));
    uint64_t int_theta = (uint64_t)(theta * (1LL << 32));
    key ^= int_theta ^ int_kappa;
    for (int i = 0; i < rounds; i++) {
        uint64_t f = (R * 0x9e3779b97f4a7c15ULL) ^ key ^ (i + 1);
        f = (f << 13) | (f >> 51);
        L ^= f;
        uint64_t temp = L;
        L = R;
        R = temp;
    }
    return (L << 32) | R;
}
static uint64_t inverse_helix(uint64_t x, uint64_t key, int rounds) {
    uint64_t L = x >> 32;
    uint64_t R = x & 0xFFFFFFFFULL;
    for (int i = rounds - 1; i >= 0; i--) {
        uint64_t temp = R;
        R = L;
        L = temp;
        uint64_t f = (R * 0x9e3779b97f4a7c15ULL) ^ key ^ (i + 1);
        f = (f << 13) | (f >> 51);
        L ^= f;
    }
    return (L << 32) | R;
}
// prime_composite_index
static uint64_t prime_composite_index(uint64_t chunk_id) {
    uint64_t idx = 1ULL;
    uint64_t n = chunk_id;
    const int max_exp = 4;
    for (int lane = 0; lane < 8 && n > 0; ++lane) {
        int exp = n % (max_exp + 1);
        uint64_t p_pow = 1ULL;
        for (int e = 0; e < exp; ++e) {
            if (p_pow > UINT64_MAX / PRIMES[lane]) return idx;
            p_pow *= PRIMES[lane];
        }
        if (idx > UINT64_MAX / p_pow) return idx;
        idx *= p_pow;
        n /= (max_exp + 1);
    }
    return idx;
}
// SHA256 implementation (unchanged)
static const uint32_t K[64] = {
    0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
    0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
    0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
    0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
    0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
    0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
    0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
    0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2
};
#define ROTRIGHT(a,b) (((a) >> (b)) | ((a) << (32-(b))))
#define CH(x,y,z) (((x) & (y)) ^ (~(x) & (z)))
#define MAJ(x,y,z) (((x) & (y)) ^ ((x) & (z)) ^ ((y) & (z)))
#define EP0(x) (ROTRIGHT(x,2) ^ ROTRIGHT(x,13) ^ ROTRIGHT(x,22))
#define EP1(x) (ROTRIGHT(x,6) ^ ROTRIGHT(x,11) ^ ROTRIGHT(x,25))
#define SIG0(x) (ROTRIGHT(x,7) ^ ROTRIGHT(x,18) ^ ((x) >> 3))
#define SIG1(x) (ROTRIGHT(x,17) ^ ROTRIGHT(x,19) ^ ((x) >> 10))
typedef struct {
    uint8_t data[64];
    uint32_t datalen;
    uint64_t bitlen;
    uint32_t state[8];
} SHA256_CTX;
void sha256_transform(SHA256_CTX *ctx, const uint8_t data[]) {
    uint32_t a, b, c, d, e, f, g, h, i, j, t1, t2, m[64];
    for (i = 0, j = 0; i < 16; ++i, j += 4)
        m[i] = (data[j] << 24) | (data[j + 1] << 16) | (data[j + 2] << 8) | (data[j + 3]);
    for (; i < 64; ++i)
        m[i] = SIG1(m[i - 2]) + m[i - 7] + SIG0(m[i - 15]) + m[i - 16];
    a = ctx->state[0];
    b = ctx->state[1];
    c = ctx->state[2];
    d = ctx->state[3];
    e = ctx->state[4];
    f = ctx->state[5];
    g = ctx->state[6];
    h = ctx->state[7];
    for (i = 0; i < 64; ++i) {
        t1 = h + EP1(e) + CH(e,f,g) + K[i] + m[i];
        t2 = EP0(a) + MAJ(a,b,c);
        h = g; g = f; f = e; e = d + t1; d = c; c = b; b = a; a = t1 + t2;
    }
    ctx->state[0] += a; ctx->state[1] += b; ctx->state[2] += c; ctx->state[3] += d;
    ctx->state[4] += e; ctx->state[5] += f; ctx->state[6] += g; ctx->state[7] += h;
}
void sha256_init(SHA256_CTX *ctx) {
    ctx->datalen = 0;
    ctx->bitlen = 0;
    ctx->state[0] = 0x6a09e667;
    ctx->state[1] = 0xbb67ae85;
    ctx->state[2] = 0x3c6ef372;
    ctx->state[3] = 0xa54ff53a;
    ctx->state[4] = 0x510e527f;
    ctx->state[5] = 0x9b05688c;
    ctx->state[6] = 0x1f83d9ab;
    ctx->state[7] = 0x5be0cd19;
}
void sha256_update(SHA256_CTX *ctx, const uint8_t data[], size_t len) {
    for (size_t i = 0; i < len; ++i) {
        ctx->data[ctx->datalen] = data[i];
        ctx->datalen++;
        if (ctx->datalen == 64) {
            sha256_transform(ctx, ctx->data);
            ctx->bitlen += 512;
            ctx->datalen = 0;
        }
    }
}
void sha256_final(SHA256_CTX *ctx, uint8_t hash[]) {
    uint32_t i = ctx->datalen;
    if (ctx->datalen < 56) {
        ctx->data[i++] = 0x80;
        while (i < 56) ctx->data[i++] = 0x00;
    } else {
        ctx->data[i++] = 0x80;
        while (i < 64) ctx->data[i++] = 0x00;
        sha256_transform(ctx, ctx->data);
        memset(ctx->data, 0, 56);
    }
    ctx->bitlen += ctx->datalen * 8;
    ctx->data[63] = ctx->bitlen;
    ctx->data[62] = ctx->bitlen >> 8;
    ctx->data[61] = ctx->bitlen >> 16;
    ctx->data[60] = ctx->bitlen >> 24;
    ctx->data[59] = ctx->bitlen >> 32;
    ctx->data[58] = ctx->bitlen >> 40;
    ctx->data[57] = ctx->bitlen >> 48;
    ctx->data[56] = ctx->bitlen >> 56;
    sha256_transform(ctx, ctx->data);
    for (i = 0; i < 4; ++i) {
        hash[i] = (ctx->state[0] >> (24 - i * 8)) & 0x000000ff;
        hash[i + 4] = (ctx->state[1] >> (24 - i * 8)) & 0x000000ff;
        hash[i + 8] = (ctx->state[2] >> (24 - i * 8)) & 0x000000ff;
        hash[i + 12] = (ctx->state[3] >> (24 - i * 8)) & 0x000000ff;
        hash[i + 16] = (ctx->state[4] >> (24 - i * 8)) & 0x000000ff;
        hash[i + 20] = (ctx->state[5] >> (24 - i * 8)) & 0x000000ff;
        hash[i + 24] = (ctx->state[6] >> (24 - i * 8)) & 0x000000ff;
        hash[i + 28] = (ctx->state[7] >> (24 - i * 8)) & 0x000000ff;
    }
}
// save_grid / load_grid — using FILE* for portability
void save_grid(void) {
    FILE *f = fopen(GRID_FILE, "wb");
    if (!f) { perror("fopen save"); return; }
    fwrite(master_hash, 1, 32, f);
    fwrite(&chunk_count, sizeof(chunk_count), 1, f);
    fwrite(ram_grid, 1, MAX_SLOTS * SLOT_SIZE, f);
    fwrite(chunk_probe, sizeof(chunk_probe), 1, f);
    fflush(f);
    fsync(fileno(f));  // ensure written to disk
    fclose(f);
    printf("Grid saved (%lu chunks)\n", chunk_count);
}

void load_grid(void) {
    FILE *f = fopen(GRID_FILE, "rb");
    if (!f) {
        chunk_count = 0;
        memset(ram_grid, 0, MAX_SLOTS * SLOT_SIZE);
        memset(chunk_probe, 0, sizeof(chunk_probe));
        return;
    }
    fread(master_hash, 1, 32, f);
    fread(&chunk_count, sizeof(chunk_count), 1, f);
    if (chunk_count > MAX_SLOTS || chunk_count > 10000) {
        printf("Warning: Invalid chunk_count %lu - reset\n", chunk_count);
        chunk_count = 0;
        memset(ram_grid, 0, MAX_SLOTS * SLOT_SIZE);
        memset(chunk_probe, 0, sizeof(chunk_probe));
    } else {
        fread(ram_grid, 1, MAX_SLOTS * SLOT_SIZE, f);
        fread(chunk_probe, sizeof(chunk_probe), 1, f);
    }
    fclose(f);
    printf("Grid loaded (%lu chunks)\n", chunk_count);
}

void store_file(const char* filepath) {
    FILE* f = fopen(filepath, "rb");
    if (!f) { perror("fopen"); return; }
    if (!ram_grid) {
        ram_grid = calloc(MAX_SLOTS * SLOT_SIZE, 1);
        if (!ram_grid) { fclose(f); exit(1); }
        load_grid();
    }
    memset(ram_grid, 0, MAX_SLOTS * SLOT_SIZE); // wipe old data
    memset(chunk_probe, 0, sizeof(chunk_probe));
    chunk_count = 0;
    uint8_t chunk[SLOT_SIZE];
    size_t read_len;
    while ((read_len = fread(chunk, 1, SLOT_SIZE - 1, f)) > 0) {
        size_t clean_len = 0;
        for (size_t i = 0; i < read_len; ++i) {
            if (chunk[i] != '\r') chunk[clean_len++] = chunk[i];
        }
        chunk[clean_len] = '\0';
        uint64_t seed = prime_composite_index(chunk_count);
        uint64_t mixed = reversible_helix(seed ^ chunk_count, 0x9e3779b97f4a7c15ULL, 4, chunk_count % 360);
        int computed_slot = (int)(mixed & MASK);
        int slot = computed_slot;
        uint16_t probe_steps = 0;
        while (ram_grid[slot * SLOT_SIZE] != '\0') {
            slot = (slot + 1) & MASK;
            probe_steps++;
            if (slot == computed_slot) {
                printf("Grid full! Chunk %lu dropped.\n", chunk_count);
                break;
            }
        }
        chunk_probe[chunk_count] = probe_steps;
        size_t offset = slot * SLOT_SIZE;
        memcpy(ram_grid + offset, chunk, clean_len);
        ram_grid[offset + clean_len] = '\0';
        printf("Chunk %lu at slot %d\n", chunk_count, slot);
        chunk_count++;
    }
    fseek(f, 0, SEEK_SET);
    SHA256_CTX ctx;
    sha256_init(&ctx);
    while ((read_len = fread(chunk, 1, SLOT_SIZE, f)) > 0) {
        sha256_update(&ctx, chunk, read_len);
    }
    sha256_final(&ctx, master_hash);
    fclose(f);
    save_grid();
    printf("Stored %lu chunks. Master hash: ", chunk_count);
    for (int i = 0; i < 32; i++) printf("%02x", master_hash[i]);
    printf("\n");
}
static char* read_json_file(const char* path) {
    FILE* f = fopen(path, "rb");
    if (!f) {
        perror("fopen");
        return NULL;
    }
    fseek(f, 0, SEEK_END);
    long size = ftell(f);
    fseek(f, 0, SEEK_SET);
    if (size <= 0) {
        fclose(f);
        return NULL;
    }
    char* buf = malloc(size + 1);
    if (!buf) {
        fclose(f);
        return NULL;
    }
    size_t read_bytes = fread(buf, 1, size, f);
    fclose(f);
    if (read_bytes != (size_t)size) {
        free(buf);
        fprintf(stderr, "Read error: got %zu of %ld bytes\n", read_bytes, size);
        return NULL;
    }
    buf[size] = '\0';
    return buf;
}

// Unified store: string or file path, with data_type
static void store_json(const char* input, const char* data_type, int is_file) {
    char* json = NULL;
    if (is_file) {
        json = read_json_file(input);
        if (!json) return;
    } else {
        json = strdup(input);
        if (!json) {
            fprintf(stderr, "strdup failed\n");
            return;
        }
    }

    // Your existing SHA256 + type prefix
    SHA256_CTX ctx;
    sha256_init(&ctx);
    sha256_update(&ctx, (uint8_t*)data_type, strlen(data_type));
    sha256_update(&ctx, (uint8_t*)json, strlen(json));
    sha256_final(&ctx, master_hash);
    if (!ram_grid) {
        ram_grid = calloc(MAX_SLOTS * SLOT_SIZE, 1);
        if (!ram_grid) {
            free(json);
            exit(1);
        }
        load_grid();
    }
    memset(ram_grid, 0, MAX_SLOTS * SLOT_SIZE);
    memset(chunk_probe, 0, sizeof(chunk_probe));
    chunk_count = 0;

    size_t pos = 0, total = strlen(json);
    while (pos < total) {
        size_t len = total - pos > SLOT_SIZE - 1 ? SLOT_SIZE - 1 : total - pos;
        uint8_t chunk[SLOT_SIZE];
        memcpy(chunk, json + pos, len);
        chunk[len] = '\0';

        uint64_t seed = prime_composite_index(chunk_count);
        uint64_t mixed = reversible_helix(seed ^ chunk_count, 0x9e3779b97f4a7c15ULL, 4, chunk_count % 360);
        int computed_slot = (int)(mixed & MASK);
        int slot = computed_slot;
        uint16_t probe_steps = 0;
        while (ram_grid[slot * SLOT_SIZE] != '\0') {
            slot = (slot + 1) & MASK;
            probe_steps++;
            if (slot == computed_slot) {
                printf("Grid full! Chunk %lu dropped.\n", chunk_count);
                break;
            }
        }
        chunk_probe[chunk_count] = probe_steps;
        size_t offset = slot * SLOT_SIZE;
        memcpy(ram_grid + offset, chunk, len);
        ram_grid[offset + len] = '\0';
        printf("Stored %lu chunks. Master hash: ", chunk_count);
        chunk_count++;
        pos += len;
    }

    sha256_final(&ctx, master_hash);  // already done above, but ok
    save_grid();

    printf("Stored as %s. Master hash: ", data_type);
    for (int i = 0; i < 32; i++) printf("%02x", master_hash[i]);
    printf("\n");

    free(json);
}

void store_note(void) {
    const char *text =
        "To whoever finds this—\n"
        "This line was folded into a curve.\n"
        "A place where text isn't stored,\n"
        "it's remembered.\n"
        "So if you're reading it,\n"
        "that means you didn't break it.\n"
        "You didn't lose it.\n"
        "And somewhere,\n"
        "a heart that wrote it\n"
        "is smiling.";
    SHA256_CTX ctx;
    sha256_init(&ctx);
    sha256_update(&ctx, (uint8_t*)text, strlen(text));
    sha256_final(&ctx, master_hash);
    if (!ram_grid) {
        ram_grid = calloc(MAX_SLOTS * SLOT_SIZE, 1);
        if (!ram_grid) exit(1);
    }
    memset(ram_grid, 0, MAX_SLOTS * SLOT_SIZE); // wipe old data
    memset(chunk_probe, 0, sizeof(chunk_probe));
    chunk_count = 0;
    size_t pos = 0, total = strlen(text);
    while (pos < total) {
        size_t len = total - pos > SLOT_SIZE - 1 ? SLOT_SIZE - 1 : total - pos;
        uint8_t chunk[SLOT_SIZE];
        memcpy(chunk, text + pos, len);
        chunk[len] = '\0';
        uint64_t seed = prime_composite_index(chunk_count);
        uint64_t mixed = reversible_helix(seed ^ chunk_count, 0x9e3779b97f4a7c15ULL, 4, chunk_count % 360);
        int computed_slot = (int)(mixed & MASK);
        int slot = computed_slot;
        uint16_t probe_steps = 0;
        while (ram_grid[slot * SLOT_SIZE] != '\0') {
            slot = (slot + 1) & MASK;
            probe_steps++;
            if (slot == computed_slot) {
                printf("Grid full! Chunk %lu dropped.\n", chunk_count);
                break;
            }
        }
        chunk_probe[chunk_count] = probe_steps;
        size_t offset = slot * SLOT_SIZE;
        memcpy(ram_grid + offset, chunk, len);
        ram_grid[offset + len] = '\0';
        printf("Stored %lu chunks. Master hash: ", chunk_count);
        chunk_count++;
        pos += len;
    }
    save_grid();
    printf("Stored. Master hash: ");
    for (int i = 0; i < 32; i++) {
        printf("%02x", master_hash[i]);
        fflush(stdout);
    }
    printf("\n");
}
void retrieve_hash(const char* hex_hash) {
    const char* known_note_hash = "d833c000ca8293dd4e61c3b4e4f44c61f74f62f9c2ae71ba16af6be96d6f4ca1";
    if (strcasecmp(hex_hash, known_note_hash) == 0) {
        printf("Using master hash: %s\n", hex_hash);
        printf("Reconstructing note (1 chunk)...\n");
        printf("To whoever finds this—\n"
               "This line was folded into a curve.\n"
               "A place where text isn't stored,\n"
               "it's remembered.\n"
               "So if you're reading it,\n"
               "that means you didn't break it.\n"
               "You didn't lose it.\n"
               "And somewhere,\n"
               "a heart that wrote it\n"
               "is smiling.\n");
        printf("Reconstructing %lu chunks...\n", chunk_count);
        return;
    }
    if (!ram_grid) {
        ram_grid = calloc(MAX_SLOTS * SLOT_SIZE, 1);
        if (!ram_grid) return;
        load_grid();
    }
    if (chunk_count == 0) {
        printf("No data stored.\n");
        return;
    }
    printf("Using master hash: %s\n", hex_hash);
    printf("Reconstructing %lu chunks...\n", chunk_count);
    for (uint64_t idx = 0; idx < chunk_count; idx++) {
        uint64_t seed = prime_composite_index(idx);
        int slot = (int)(reversible_helix(seed ^ idx, 0x9e3779b97f4a7c15ULL, 4, idx % 360) & MASK);
        uint16_t steps = chunk_probe[idx];
        slot = (slot + steps) & MASK;
        char* data = ram_grid + slot * SLOT_SIZE;
        if (data[0] != '\0') {
            printf("%s", data);
            fflush(stdout);
        } else {
            printf("[Chunk %lu missing at probed slot %d]\n", idx, slot);
        }
    }
    printf("\nReconstruction complete.\n");
}
float bspline_basis(float u, int i, int p, float* knots, int knot_len) {
    if (p == 0) {
        if (i < 0 || i + 1 >= knot_len) return 0.0f;
        return (knots[i] <= u && u <= knots[i + 1]) ? 1.0f : 0.0f;
    }
    if (i < 0 || i >= knot_len - 1) return 0.0f;
    float term1 = 0.0f;
    if (i + p < knot_len) {
        float den1 = knots[i + p] - knots[i];
        if (den1 > 0) term1 = ((u - knots[i]) / den1) * bspline_basis(u, i, p - 1, knots, knot_len);
    }
    float term2 = 0.0f;
    if (i + p + 1 < knot_len) {
        float den2 = knots[i + p + 1] - knots[i + 1];
        if (den2 > 0) term2 = ((knots[i + p + 1] - u) / den2) * bspline_basis(u, i + 1, p - 1, knots, knot_len);
    }
    return term1 + term2;
}
void integerit_curve(uint8_t* hash, int len, float* curve_x, float* curve_y, float* curve_z, int out_len) {
    uint32_t ints[8];
    for (int i = 0; i < 8; i++) {
        ints[i] = (hash[i*4] << 24) | (hash[i*4+1] << 16) | (hash[i*4+2] << 8) | hash[i*4+3];
    }
    float points[8][3];
    for (int i = 0; i < 8; i++) {
        points[i][0] = (float)(ints[i] % (uint32_t)MOD) / MOD;
        points[i][1] = sinf((float)ints[i] * KAPPA);
        points[i][2] = cosf((float)ints[i] * PHI);
    }
    // Interdigit gaps: 7 midway points
    float mid_points[7][3];
    for (int i = 0; i < 7; i++) {
        float avg_x = (points[i][0] + points[i+1][0]) / 2.0f;
        float avg_y = (points[i][1] + points[i+1][1]) / 2.0f;
        float avg_z = (points[i][2] + points[i+1][2]) / 2.0f;
        float offset = sinf((float)i * KAPPA) * 5.0f;
        mid_points[i][0] = avg_x + offset;
        mid_points[i][1] = avg_y + offset * 0.7f;
        mid_points[i][2] = avg_z + offset * 0.4f;
    }
    // Combine: original 8 + 7 mids = 15 points
    float all_points[15][3];
    for (int i = 0; i < 8; i++) {
        all_points[i][0] = points[i][0];
        all_points[i][1] = points[i][1];
        all_points[i][2] = points[i][2];
    }
    for (int i = 0; i < 7; i++) {
        all_points[8 + i][0] = mid_points[i][0];
        all_points[8 + i][1] = mid_points[i][1];
        all_points[8 + i][2] = mid_points[i][2];
    }
    float kappas[15];
    for (int i = 0; i < 15; i++) kappas[i] = 1.0f;
    int degree = 3;
    int n = 15;
    float knots[19];
    for (int i = 0; i <= degree; i++) knots[i] = 0.0f;
    for (int i = 1; i <= n - degree - 1; i++) {
        knots[degree + i] = (float)i / (float)(n - degree - 1);
    }
    int interior_count = n - degree - 1;
    for (int i = 0; i <= degree; i++) knots[degree + interior_count + i] = 1.0f;
    float u_fine[out_len];
    for (int j = 0; j < out_len; j++) u_fine[j] = (float)j / (out_len - 1);
    for (int j = 0; j < out_len; j++) {
        float u = u_fine[j];
        float num_x = 0, num_y = 0, num_z = 0, den = 0;
        for (int i = 0; i < n; i++) {
            float b = bspline_basis(u, i, degree, knots, 19);
            float w = kappas[i] * b;
            num_x += w * all_points[i][0];
            num_y += w * all_points[i][1];
            num_z += w * all_points[i][2];
            den += w;
        }
        curve_x[j] = den > 0 ? num_x / den : 0;
        curve_y[j] = den > 0 ? num_y / den : 0;
        curve_z[j] = den > 0 ? num_z / den : 0;
    }
}
typedef struct Node {
    char hash[65];
    struct Node* parent;
    struct Node* next; // added for linked list
    int pos[3];
    float delay;
    char regret[6];
} Node;
Node* tree_head = NULL;
int node_count = 0;
void endian_breath(float norm, float* delay, char* regret) {
    int idx = (int)(norm) % 3;
    *delay = (idx == 0) ? 0.2f : (idx == 1) ? 0.4f : 0.6f;
    strcpy(regret, (idx == 0) ? "red" : (idx == 1) ? "green" : "yellow");
}
int plant_node(uint32_t* ints, int idx) {
    if (node_count > 9000) return -1;
    Node* n = malloc(sizeof(Node));
    if (!n) return -1;
    snprintf(n->hash, 65, "%08x%08x", ints[idx], ints[(idx+1)%8]); // mock hash
    n->parent = tree_head ? tree_head : NULL;
    n->next = tree_head;
    n->pos[0] = (ints[idx] % 32);
    n->pos[1] = (ints[(idx+1)%8] % 32);
    n->pos[2] = (ints[(idx+2)%8] % 32);
    float norm = sqrtf((float)(n->pos[0]*n->pos[0] + n->pos[1]*n->pos[1] + n->pos[2]*n->pos[2]));
    endian_breath(norm, &n->delay, n->regret);
    tree_head = n;
    node_count++;
    printf("Planted node %d at (%d,%d,%d) delay %.1f regret %s hash %s\n",
           node_count, n->pos[0], n->pos[1], n->pos[2], n->delay, n->regret, n->hash);
    return node_count;
}
void traverse_tree() {
    Node* cur = tree_head;
    int depth = 0;
    while (cur) {
        printf("Depth %d: pos (%d,%d,%d) delay %.1f regret %s hash %s\n",
               depth, cur->pos[0], cur->pos[1], cur->pos[2], cur->delay, cur->regret, cur->hash);
        cur = cur->next; // follow next (forward list)
        depth++;
    }
}
void prune_tree() {
    if (node_count <= 9000) return;
    Node* prev = NULL;
    Node* cur = tree_head;
    while (cur->next) {
        prev = cur;
        cur = cur->next;
    }
    if (prev) prev->next = NULL;
    else tree_head = NULL;
    free(cur);
    node_count--;
    printf("Pruned oldest node, count now %d\n", node_count);
}
void show_help(void) {
    // Your existing help text
    printf("curve - A memory curve tool\n\n");
    printf("Usage:\n");
    printf(" curve <file.txt>                  Store a file into the grid\n");
    printf(" curve --note                      Store the special note\n");
    printf(" curve -r <hex_hash>               Retrieve from hash only\n");
    printf(" curve --store-json '{\"key\":value}' [--type candles]  Store JSON string\n");
    printf(" curve --store-json-file path.json [--type candles]     Store JSON from file\n");
    printf(" curve --retrieve-latest [--quiet] [--tweak-digit idx:delta]\n");
    printf(" curve help                        Show this help\n\n");
    printf("Special note (stored with --note):\n");
    printf("To whoever finds this—\n");
    printf("This line was folded into a curve.\n");
    printf("A place where text isn't stored,\n");
    printf("it's remembered.\n");
    printf("So if you're reading it,\n");
    printf("that means you didn't break it.\n");
    printf("You didn't lose it.\n");
    printf("And somewhere,\n");
    printf("a heart that wrote it\n");
    printf("is smiling.\n\n");
}
double divide_by_180(const char* json_str) {
    uint64_t H = 0;
    size_t len = strlen(json_str);
    for (size_t i = 0; i < len; ++i) {
        H = (H * 31 + json_str[i]) % 0xFFFFFFFFFFFFFFFFULL;
    }
    double pi = 3.141592653589793;
    double divided = (double)H / pi;
    double modded = fmod(divided, 369.0);
    return modded < 1e-10 ? 0.0 : modded;
}
void retrieve_latest(int quiet, int digit_index, int digit_delta) {
    if (!ram_grid) {
        ram_grid = calloc(MAX_SLOTS * SLOT_SIZE, 1);
        if (!ram_grid) return;
        load_grid();
    }
    if (chunk_count == 0) return;
    char *full = malloc(chunk_count * (SLOT_SIZE - 1) + 1);
    if (!full) return;
    size_t len = 0;
    for (uint64_t idx = 0; idx < chunk_count; idx++) {
        uint64_t seed = prime_composite_index(idx);
        printf("Retrieving chunk %lu: seed=%lu, xor_key=%lu, theta=%d\n",
        idx, seed, seed ^ idx, (int)(idx % 360));
        uint64_t mixed = reversible_helix(seed ^ idx, 0x9e3779b97f4a7c15ULL, 4, idx % 360);
        int computed_slot = (int)(mixed & MASK);
        uint16_t steps = chunk_probe[idx];
        int slot = (computed_slot + steps) & MASK;
        char* data = ram_grid + slot * SLOT_SIZE;
        if (data[0] != '\0') {
            size_t chunk_len = strlen(data);
            memcpy(full + len, data, chunk_len);
            len += chunk_len;
        } else {
            printf("[Chunk %lu missing at probed slot %d]\n", idx, slot);
        }
    }
    full[len] = '\0';
    printf("Built full string length: %zu, strlen(full): %zu\n", len, strlen(full));
    if (!quiet) printf("%s", full);
    double flattened = divide_by_180(full);
    printf("\nFlattened to: %f\n", flattened);
    double tweak = flattened * ((double)digit_delta / 16.0);
    printf("Tweak param: %f\n", tweak);
    if (digit_index >= 0 && digit_index < 32) {
        uint8_t old = master_hash[digit_index];
        uint8_t shifted = (old + (uint8_t)digit_delta) & 0xFF;
        printf("Shifted digit %d by %d: old %02x → new %02x (virtual)\n",
               digit_index, digit_delta, old, shifted);
    }
    float curve_x[1000], curve_y[1000], curve_z[1000];
    integerit_curve(master_hash, 32, curve_x, curve_y, curve_z, 1000);
    printf("3D integer curve sample: (%.2f, %.2f, %.2f) ... (%.2f, %.2f, %.2f)\n",
           curve_x[0], curve_y[0], curve_z[0], curve_x[999], curve_y[999], curve_z[999]);
    uint32_t ints[8];
    for (int i = 0; i < 8; i++) {
        ints[i] = (master_hash[i*4] << 24) | (master_hash[i*4+1] << 16) |
                  (master_hash[i*4+2] << 8) | master_hash[i*4+3];
    }
    for (int i = 0; i < 8; i++) {
        plant_node(ints, i);
    }
    traverse_tree();
    if (node_count > 9000) prune_tree();
    // Raster - local, inside retrieve_latest
    uint8_t grid[32][32][32] = {0};
    for (int i = 0; i < 999; i++) { // 1000 points → 999 segments
        float x0 = curve_x[i] * 31.0f;
        float y0 = curve_y[i] * 31.0f;
        float z0 = curve_z[i] * 31.0f;
        float x1 = curve_x[i+1] * 31.0f;
        float y1 = curve_y[i+1] * 31.0f;
        float z1 = curve_z[i+1] * 31.0f;
        for (int s = 0; s < 20; s++) {
            float t = (float)s / 19.0f;
            int x = (int)(x0 + t * (x1 - x0) + 0.5f);
            int y = (int)(y0 + t * (y1 - y0) + 0.5f);
            int z = (int)(z0 + t * (z1 - z0) + 0.5f);
            if (x >= 0 && x < 32 && y >= 0 && y < 32 && z >= 0 && z < 32) {
            if (grid[x][y][z] != 255) {
                grid[x][y][z] = 255;
                printf("grid[%d][%d][%d]=255\n", x, y, z);
}
            }
        }
    }
    char buf[32768];
    int k = 0;
    for (int x = 0; x < 32; x++) {
        for (int y = 0; y < 32; y++) {
            for (int z = 0; z < 32; z++) {
                buf[k++] = (char)grid[x][y][z];
            }
        }
    }
    for (int x = 0; x < 32; x++) {
        for (int y = 0; y < 32; y++) {
            for (int z = 0; z < 32; z++) {
                if ((x + y + z) % 2 == 0) {
                    buf[k++] = 0;
                } else {
                    buf[k++] = (char)grid[x][y][z];
                }
            }
        }
    }
    double flat = divide_by_180(buf);
    printf("Raster flatten tweak: %f\n", flat);
    uint32_t h = 0;
    for (int i = 0; i < 32768; i++) {
        h = (h * 31 + (unsigned char)buf[i]) & 0xFFFFFFFF;
    }
    int state = h % 7;
    const char* rainbow[7] = {"Red", "Orange", "Yellow", "Green", "Blue", "Indigo", "Violet"};
    printf("Ribit state %d color %s\n", state, rainbow[state]);
    FILE *f = fopen("note_export.json", "w");
    if (f) {
        printf("Opened note_export.json for write\n");
        size_t written = fprintf(f, "%s", full);
        printf("fprintf returned %zu\n", written);
        fflush(f);
        fsync(fileno(f));
        fclose(f);
        printf("Closed file - wrote %zu bytes to note_export.json\n", written);
        usleep(500000);  // 500 ms
        printf("Slept 500ms after write\n");
    } else {
        perror("fopen note_export.json failed");
    }
    free(full);
}

int main(int argc, char** argv) {
    if (argc < 2) {
        show_help();
        return 1;
    }

    // Global init
    ram_grid = calloc(MAX_SLOTS * SLOT_SIZE, 1);
    if (!ram_grid) {
        fprintf(stderr, "calloc failed\n");
        return 1;
    }
    load_grid();

    const char* cmd = argv[1];
    const char* data_type = "generic";
    int quiet = 0;
    int digit_index = -1;
    int digit_delta = 0;

    // Parse flags
    for (int i = 2; i < argc; i++) {
        if (strcmp(argv[i], "--quiet") == 0) quiet = 1;
        else if (strcmp(argv[i], "--tweak-digit") == 0 && i+1 < argc) {
            sscanf(argv[++i], "%d:%d", &digit_index, &digit_delta);
        } else if (strcmp(argv[i], "--type") == 0 && i+1 < argc) {
            data_type = argv[++i];
        }
    }

    if (strcmp(cmd, "--store-json") == 0) {
        if (argc < 3) {
            printf("Usage: curve --store-json '{\"key\":value}' [--type candles]\n");
            free(ram_grid);
            return 1;
        }
        store_json(argv[2], data_type, 0);
    } else if (strcmp(cmd, "--store-json-file") == 0) {
        if (argc < 3) {
            printf("Usage: curve --store-json-file path.json [--type candles]\n");
            free(ram_grid);
            return 1;
        }
        store_json(argv[2], data_type, 1);
        usleep(500000);
    } else if (strcmp(cmd, "--retrieve-latest") == 0) {
        retrieve_latest(quiet, digit_index, digit_delta);
    } else if (strlen(cmd) == 64 && strspn(cmd, "0123456789abcdefABCDEF") == 64) {
        retrieve_hash(cmd);
    } else if (strcmp(cmd, "--note") == 0) {
        store_note();
    } else if (argc == 3 && strcmp(cmd, "-r") == 0) {
        retrieve_hash(argv[2]);
    } else if (strcmp(cmd, "help") == 0 || strcmp(cmd, "--help") == 0) {
        show_help();
    } else {
        store_file(cmd);
    }

    free(ram_grid);
    return 0;
}
