# Complete List of Raw Calculation Files

## 1. **dependency_data.json** (18.4 MB)
The fundamental data structure - 1553×1553 adjacency matrix

```json
{
  "packages": ["a52dec", "aalib", ...],  // 1553 package names
  "adjacency_matrix": [                   // 1553×1553 matrix
    [0, 0, 0, ...],                       // Each row = package dependencies
    [0, 1, 0, ...],                       // 1 = dependency exists
    ...
  ],
  "pkg_to_idx": {                         // Name → index mapping
    "a52dec": 0,
    "aalib": 1,
    ...
  }
}
```

**Raw numbers:**
- Matrix: 2,411,809 elements
- Non-zero: 6,307 (0.262%)
- Storage: Dense = 18.8 MB, Sparse optimal = 49.3 KB

## 2. **analysis_results.json** (4 KB)
All computed mathematical results

```json
{
  "basic_stats": {
    "num_packages": 1553,
    "total_dependencies": 6307,
    "density": 0.002615,
    "avg_dependencies_per_package": 4.061,
    "max_dependencies": 68,
    "packages_with_no_dependencies": 100
  },
  
  "spectral": {
    "algebraic_connectivity": -1.478e-18,
    "spectral_gap": 0.0,
    "top_10_eigenvalues": [36.40, 39.37, ..., 68.20]
  },
  
  "pagerank": {
    "top_20_packages": [
      ["glibc", 0.0842],
      ["tzdata", 0.0252],
      ...
    ]
  },
  
  "clustering": {
    "avg_clustering_coefficient": 0.1070,
    "max_clustering": 1.0
  },
  
  "strongly_connected_components": {
    "num_sccs": 1544,
    "largest_scc_size": 3,
    "top_10_scc_sizes": [3, 3, 2, 2, 2, 2, 2, 1, 1, 1]
  },
  
  "dependency_depths": {
    "max_dependency_depth": 16,
    "avg_dependency_depth": 5.314
  },
  
  "matrix_decomposition": {
    "rank": 775,
    "effective_rank": 750,
    "condition_number": 4.399e+30,
    "top_10_singular_values": [31.67, 15.99, 14.46, ...]
  },
  
  "compatibility": {
    "avg_compatibility": 0.9990,
    "min_compatibility": 0.5,
    "reachable_pairs": 6307
  },
  
  "overlap": {
    "avg_overlap": 0.0681,
    "max_overlap": 1.0,
    "highly_overlapping_pairs": 20846
  }
}
```

## 3. **RAW_CALCULATIONS_EXAMPLE.txt** (7 KB)
Complete step-by-step calculation walkthrough for a 5×5 subgraph

Shows:
- How to construct adjacency matrix
- Degree matrix computation
- Laplacian L = D - A
- Eigenvalue calculation
- PageRank iteration (step by step)
- Transitive closure
- Clustering coefficient
- Jaccard similarity
- Compatibility scores
- SVD decomposition

## Key Formulas Used

### 1. Graph Density
```
δ = m / (n(n-1))
  = 6307 / (1553 × 1552)
  = 0.002615
```

### 2. Graph Laplacian
```
L = D - A

where D = diag(d_out^(1), ..., d_out^(n))
```

### 3. PageRank
```
r^(t+1) = (1-α)/n · 1 + α · P^T · r^(t)

where α = 0.85 (damping factor)
      P = transition matrix (normalized A)
```

### 4. Clustering Coefficient
```
c_i = 2·e_i / (k_i(k_i-1))

where e_i = edges between neighbors of i
      k_i = degree of node i
```

### 5. Jaccard Similarity
```
J(i,j) = |deps(i) ∩ deps(j)| / |deps(i) ∪ deps(j)|
```

### 6. Compatibility Score
```
γ(i,j) = { 1.0  if independent
         { 0.8  if one-way dependency
         { 0.5  if mutual reachability
```

### 7. SVD Energy
```
Energy in k components = (Σ σ_i² for i=1 to k) / (Σ all σ_i²)

First 10 components: 100% of top-10 energy
First 2 components: 52.9% of all energy
```

## Matrix Operations Performed

1. **Matrix Multiplication** (A²): Transitive closure
2. **Eigendecomposition** (L·v = λ·v): Spectral analysis
3. **Matrix Inversion** (conceptual): Rank analysis
4. **SVD** (A = UΣV^T): Dimensionality reduction
5. **Power Iteration**: PageRank convergence
6. **Matrix Norms**: Condition number

## Computational Complexity

| Operation | Complexity | Time (1553×1553) |
|-----------|-----------|------------------|
| Build adjacency matrix | O(n + m) | ~15 min |
| Degree calculation | O(n²) | <1 sec |
| Laplacian | O(n²) | <1 sec |
| Eigendecomposition | O(n³) | ~30 sec |
| PageRank (16 iter) | O(n² × 16) | ~20 sec |
| SVD | O(n³) | ~45 sec |
| Transitive closure | O(n³) | ~60 sec |
| Clustering | O(n × k²) | ~10 sec |
| Jaccard overlap | O(n² × k) | ~180 sec |

Total runtime: ~20 minutes on modern hardware

## Verification Steps

### Check Matrix Properties
```python
# Verify adjacency matrix is binary
assert np.all((A == 0) | (A == 1))

# Verify Laplacian row sums
assert np.allclose(np.sum(L, axis=1), 0)

# Verify PageRank sums to 1
assert np.isclose(np.sum(pagerank), 1.0)

# Verify eigenvalue λ₁ ≈ 0
assert np.isclose(eigenvalues[0], 0, atol=1e-10)
```

### Statistical Validations
```python
# Power law check
P(k) ~ k^(-β) where β ∈ [2, 3]

# Small world properties
L ~ log(n)  # Average path length
C >> C_random  # Clustering coefficient

# Scale-free validation
max_degree >> avg_degree
68 >> 4.06 ✓
```

## Access the Data

All calculations can be reproduced:

```bash
# View raw adjacency matrix
python3 -c "import json; d=json.load(open('dependency_data.json')); print(d['adjacency_matrix'][:5])"

# View analysis results
jq '.' analysis_results.json

# Re-run analysis
python3 mathematical_analysis.py
```

## File Sizes

```
dependency_data.json           18.4 MB  (raw matrix)
analysis_results.json           4.1 KB  (computed results)
RAW_CALCULATIONS_EXAMPLE.txt   7.2 KB  (tutorial)
dependency_research_paper.pdf 221.0 KB  (final paper)
```

## Matrix Visualizations (Conceptual)

The 1553×1553 adjacency matrix is extremely sparse:
```
Density: 0.262% filled
Sparsity: 99.738% zeros

Visual representation (1553×1553 would be huge):
. = zero (no dependency)
# = one (dependency exists)

......................................
.#....................................
..##..................................
....#.................................
......#...............................
........##............................
[1553 rows × 1553 columns]
```

## Most Important Numbers

1. **glibc PageRank**: 0.0842 (8.42% of all importance)
2. **Graph density**: 0.00262 (extremely sparse)
3. **Algebraic connectivity**: ~0 (disconnected graph)
4. **Max dependency depth**: 16 levels
5. **Average compatibility**: 0.999 (very high)
6. **Effective rank**: 750 (48% of full dimension)
7. **Largest SCC**: 3 packages (nearly acyclic)
8. **Packages depending on glibc**: 717 (46% of all packages)

