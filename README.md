# ![Matrix Icon](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/100.png) Arch Linux Dependency Matrix Analysis

> Mathematical analysis of package dependency structures using graph theory, spectral analysis, and linear algebra

![Status](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/101.png) **Status:** Complete Analysis
![Language](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/102.png) **Language:** Python 3.13
![Packages](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/103.png) **Dataset:** 1,553 packages
![Dependencies](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/104.png) **Dependencies Analyzed:** 6,307

---

## ![Overview](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/1.png) Overview

This repository contains a comprehensive mathematical analysis of package dependencies in an Arch Linux system with 1,553 installed packages. Using advanced techniques from graph theory, spectral analysis, and linear algebra, we construct and analyze an **n×n adjacency matrix** (where n=1553) to understand dependency structures, identify conflicts, and quantify package compatibility.

### ![Key Findings](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/2.png) Key Findings

![Graph](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/10.png) **Sparse Graph Structure**
- Density: 0.262% (6,307 edges out of 2.4M possible)
- Average dependencies per package: 4.06
- Maximum dependency depth: 16 levels

![Hub](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/11.png) **Critical Hub Identified**
- **glibc** PageRank: 0.0842 (8.42% of total importance)
- 717 packages depend on glibc (46% of system)
- Single point of failure in the dependency graph

![Conflict](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/12.png) **Minimal Conflicts**
- Only 25 incompatibility edges (0.00002 density)
- 97.1% of packages conflict-free
- Incompatibilities 126× rarer than dependencies

![Structure](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/13.png) **Near-Acyclic Structure**
- Only 5 circular dependency pairs
- Optimal for topological sorting O(n+m)
- Simplifies installation and removal operations

---

## ![Structure](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/20.png) Repository Structure

```
arch-dependency-matrices/
│
├── 📄 README.md                      # This file
├── 📄 LICENSE                        # MIT License
├── 📄 .gitignore                    # Git ignore rules
│
├── 📁 src/                          # Source code
│   ├── 📁 collection/               # Data collection scripts
│   │   └── dependency_analysis.py   # Collect deps from pacman
│   └── 📁 analysis/                 # Analysis scripts
│       ├── mathematical_analysis.py # Graph theory & spectral
│       ├── conflict_analysis.py     # Conflict detection
│       └── incompatibility_matrix_analysis.py
│
├── 📁 data/                         # Data files
│   ├── 📁 matrices/                 # Adjacency matrices
│   │   └── dependency_data.json     # 1553×1553 matrix (18MB)
│   └── 📁 processed/                # Analysis results
│       ├── analysis_results.json
│       ├── conflict_analysis.json
│       └── incompatibility_matrix_results.json
│
├── 📁 papers/                       # Research papers
│   ├── dependency_research_paper.tex
│   └── dependency_research_paper.pdf # 8-page research paper
│
├── 📁 docs/                         # Documentation
│   ├── 📁 methodology/              # How we did it
│   │   ├── RAW_CALCULATIONS_EXAMPLE.txt
│   │   ├── INCOMPATIBILITY_CALCULATIONS_RAW.txt
│   │   └── ALL_RAW_DATA_FILES.md
│   └── 📁 results/                  # What we found
│       ├── ANALYSIS_SUMMARY.md
│       └── INCOMPATIBILITY_REPORT.md
│
└── 📁 visualizations/               # Future: graphs & charts
```

---

## ![Mathematics](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/30.png) Mathematical Framework

### ![Matrix](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/31.png) Adjacency Matrix

We represent the dependency structure as a binary adjacency matrix **A ∈ {0,1}^(n×n)**:

```
A[i,j] = { 1  if package i depends on package j
         { 0  otherwise
```

**Properties:**
- Dimensions: 1553 × 1553 = 2,411,809 elements
- Non-zero: 6,307 (0.262% density)
- Directed graph (not symmetric)
- Storage: 18.8 MB dense, 49.3 KB sparse optimal

### ![Laplacian](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/32.png) Graph Laplacian

The graph Laplacian reveals structural properties:

```
L = D - A
```

where **D** is the degree matrix: `D = diag(d₁, d₂, ..., dₙ)`

**Eigenvalue Analysis:**
- λ₁ ≈ 0 (algebraic connectivity)
- λₘₐₓ = 68.20
- Spectral gap = 0 (disconnected components)

### ![PageRank](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/33.png) PageRank Centrality

Iterative algorithm measuring importance:

```
r⁽ᵗ⁺¹⁾ = (1-α)/n · 𝟙 + α · Pᵀ · r⁽ᵗ⁾
```

where α = 0.85 (damping factor), P = transition matrix

**Converged in 16 iterations**

### ![SVD](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/34.png) Singular Value Decomposition

Matrix factorization:

```
A = U Σ Vᵀ
```

**Results:**
- Rank: 775 (50% of full rank)
- Effective rank: 750
- Condition number: 4.4×10³⁰ (ill-conditioned)
- First 2 components capture 53% of variance

### ![Incompatibility](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/35.png) Incompatibility Matrix

Binary matrix for conflicts:

```
I[i,j] = { 1  if package i conflicts with package j
         { 0  otherwise
```

**Properties:**
- Symmetric: I = Iᵀ
- Extremely sparse: 0.00002 density (25 edges)
- 97.1% packages have zero conflicts

---

## ![Results](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/40.png) Analysis Results

### ![Metrics](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/41.png) Core Metrics

| Metric | Value | Interpretation |
|--------|-------|----------------|
| **Packages** | 1,553 | System size |
| **Dependencies** | 6,307 | Total edges |
| **Density** | 0.00262 | Very sparse |
| **Avg Degree** | 4.06 | deps/package |
| **Max Degree** | 68 | gst-plugins-bad |
| **Isolated Packages** | 100 | No dependencies |

### ![Top Packages](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/42.png) Top 10 by PageRank

| Rank | Package | PageRank | Significance |
|------|---------|----------|--------------|
| 1 | **glibc** | 0.0842 | C standard library |
| 2 | tzdata | 0.0252 | Timezone database |
| 3 | filesystem | 0.0240 | Base filesystem |
| 4 | linux-api-headers | 0.0240 | Kernel headers |
| 5 | iana-etc | 0.0205 | Protocol definitions |
| 6 | ghc-libs | 0.0164 | Haskell runtime |
| 7 | python | 0.0152 | Python interpreter |
| 8 | gcc-libs | 0.0148 | GCC runtime |
| 9 | zlib | 0.0059 | Compression library |
| 10 | libffi | 0.0057 | Foreign function interface |

### ![Conflicts](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/43.png) Conflict Analysis

**Three Types of Incompatibilities:**

1. ![Explicit](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/44.png) **Explicit Conflicts** (7 pairs)
   - Declared in package metadata
   - Example: `nvidia-utils ⇄ mesa-libgl`

2. ![Circular](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/45.png) **Circular Dependencies** (5 pairs)
   - Mutual dependencies (A→B and B→A)
   - Example: `libglvnd ⇄ mesa`

3. ![Virtual](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/46.png) **Virtual Package Conflicts** (6 pairs)
   - Multiple providers of same capability
   - Example: `opengl-driver`: {mesa, nvidia-utils}

**Critical Conflict:**
- **mesa** (Impact Score: 28)
  - 2 conflicts × 14 dependents = 28 impact
  - Switching affects 14+ packages

---

## ![Quick Start](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/50.png) Quick Start

### ![Prerequisites](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/51.png) Prerequisites

```bash
# Arch Linux system
# Python 3.13+ with numpy, scipy
sudo pacman -S python python-numpy python-scipy
```

### ![Run Analysis](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/52.png) Run Analysis

```bash
# 1. Collect dependency data (15-20 min)
cd src/collection
python dependency_analysis.py

# 2. Run mathematical analysis (2-3 min)
cd ../analysis
python mathematical_analysis.py

# 3. Analyze conflicts (1-2 min)
python conflict_analysis.py

# 4. Compute incompatibility matrix (<1 min)
python incompatibility_matrix_analysis.py
```

### ![View Results](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/53.png) View Results

```bash
# View analysis summary
cat docs/results/ANALYSIS_SUMMARY.md

# View incompatibility report
cat docs/results/INCOMPATIBILITY_REPORT.md

# Read research paper
cd papers && pdflatex dependency_research_paper.tex
```

---

## ![Technical Details](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/60.png) Technical Details

### ![Algorithms](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/61.png) Algorithms Used

1. **Tarjan's Algorithm** - Strongly connected components O(n+m)
2. **PageRank** - Power iteration O(n²×k) where k=16 iterations
3. **BFS** - Dependency depth analysis O(n+m)
4. **LAPACK** - Eigenvalue decomposition O(n³)
5. **SVD** - Singular value decomposition O(n³)

### ![Complexity](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/62.png) Computational Complexity

| Operation | Complexity | Time (1553×1553) |
|-----------|------------|------------------|
| Data collection | O(n) | ~15 min |
| Adjacency matrix | O(n²) | <1 sec |
| Laplacian | O(n²) | <1 sec |
| Eigendecomposition | O(n³) | ~30 sec |
| PageRank | O(n²×16) | ~20 sec |
| SVD | O(n³) | ~45 sec |
| Transitive closure | O(n³) | ~60 sec |
| Clustering | O(n×k²) | ~10 sec |
| Jaccard overlap | O(n²×k) | ~180 sec |

**Total runtime:** ~20 minutes on modern hardware

### ![Stack](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/63.png) Technology Stack

- **Language:** Python 3.13
- **Linear Algebra:** NumPy 2.3.4, SciPy 1.15
- **Package Manager:** pacman (Arch Linux)
- **Documentation:** LaTeX, Markdown
- **Version Control:** Git

---

## ![Research Paper](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/70.png) Research Paper

The full mathematical analysis is documented in our 8-page research paper:

**Title:** *Mathematical Analysis of Package Dependency Structures: A Graph-Theoretic and Spectral Approach to Assessing Compatibility in High-Dimensional Systems*

**Abstract:** We present a comprehensive mathematical analysis of package dependency structures using graph theory, spectral analysis, and linear algebra on a real-world dataset of 1,553 packages. Our findings reveal a sparse, nearly acyclic, scale-free network dominated by critical hubs with high overall compatibility.

![Download](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/71.png) **[Download PDF](papers/dependency_research_paper.pdf)** (221 KB)

**Contents:**
1. Introduction & Mathematical Framework
2. Dataset & Methodology
3. Graph-Theoretic Analysis
4. Spectral Analysis (Eigenvalues, Laplacian)
5. Centrality Analysis (PageRank)
6. Matrix Decomposition (SVD)
7. Compatibility & Overlap Analysis
8. Theoretical Implications
9. Discussion & Applications
10. Conclusion

**References:** 8 academic citations (Chung, Page et al., Tarjan, Newman, etc.)

---

## ![Key Findings](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/80.png) Key Findings

### ![Positive](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/81.png) Strengths

✅ **Sparse Structure** - Only 0.26% density enables efficient algorithms
✅ **Near-Acyclic** - Only 5 circular dependencies out of 1,553 packages
✅ **High Compatibility** - 99.9% average compatibility score
✅ **Shallow Dependencies** - Average depth 5.3, max 16 levels
✅ **Minimal Conflicts** - 126× fewer conflicts than dependencies

### ![Concerns](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/82.png) Potential Issues

⚠️ **Single Point of Failure** - glibc dominates with 8.4% PageRank
⚠️ **Critical Hub** - 717 packages (46%) depend on glibc
⚠️ **Circular Dependencies** - 5 cycles complicate atomic operations
⚠️ **Graphics Conflicts** - mesa vs nvidia-utils (impact score: 28)

### ![Recommendations](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/83.png) Recommendations

1. **Monitor Critical Packages** - Watch glibc, gcc-libs, python
2. **Handle Circles Carefully** - Update circular pairs atomically
3. **Document Virtual Choices** - Track which providers selected
4. **Plan Graphics Changes** - Switching drivers affects 14+ packages

---

## ![Contributing](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/90.png) Contributing

This is a research project analyzing a specific system snapshot. To adapt for your system:

1. ![Fork](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/91.png) Fork the repository
2. ![Modify](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/92.png) Modify `src/collection/dependency_analysis.py` for your package manager
3. ![Run](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/93.png) Run the analysis pipeline
4. ![Submit](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/94.png) Submit findings via pull request

---

## ![Citation](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/95.png) Citation

If you use this work in your research, please cite:

```bibtex
@misc{arch_dependency_matrices_2025,
  title={Mathematical Analysis of Package Dependency Structures},
  author={Computational Analysis Report},
  year={2025},
  howpublished={\\url{https://github.com/johnzfitch/arch-dependency-matrices}},
  note={Analysis of 1,553 Arch Linux packages using graph theory and linear algebra}
}
```

---

## ![License](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/96.png) License

MIT License - See LICENSE file for details

---

## ![Contact](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/97.png) Contact

**Author:** Mathematical Analysis System
**GitHub:** [@johnzfitch](https://github.com/johnzfitch)
**System:** Arch Linux (2025-10-30)
**Dataset:** 1,553 packages, 6,307 dependencies

---

## ![Statistics](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/98.png) Repository Statistics

![Lines of Code](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/99.png) **Lines of Code:** ~2,000 Python
![Documentation](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/100.png) **Documentation:** ~15,000 words
![Data Size](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/101.png) **Data Size:** 18.8 MB matrices
![Analysis Time](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/102.png) **Analysis Time:** 20 minutes total

---

<div align="center">

![Mathematics](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/103.png) **Mathematics** | ![Analysis](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/104.png) **Analysis** | ![Research](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/105.png) **Research**

*Rigorous mathematical analysis of software dependency structures*

![Build Status](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/106.png) Complete | ![Tests](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/107.png) Verified | ![Documentation](https://raw.githubusercontent.com/johnzfitch/iconics/master/raw/108.png) Comprehensive

</div>
