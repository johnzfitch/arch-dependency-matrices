#!/usr/bin/python3
"""
Mathematical Analysis of Package Dependencies
Uses linear algebra, graph theory, and spectral methods
"""

import json
import numpy as np
from scipy import linalg, sparse
from collections import defaultdict
import math

class DependencyAnalyzer:
    """Analyzes package dependency structure using mathematical methods."""

    def __init__(self, data_file):
        """Load dependency data."""
        with open(data_file, 'r') as f:
            data = json.load(f)

        self.packages = data['packages']
        self.n = len(self.packages)
        self.A = np.array(data['adjacency_matrix'], dtype=np.float64)
        self.pkg_to_idx = data['pkg_to_idx']

        print(f"Loaded {self.n} packages")
        print(f"Total edges: {np.sum(self.A)}")
        print(f"Graph density: {np.sum(self.A) / (self.n**2):.6f}")

    def compute_graph_laplacian(self):
        """Compute the graph Laplacian matrix L = D - A."""
        # Degree matrix (out-degrees for directed graph)
        D = np.diag(np.sum(self.A, axis=1))
        L = D - self.A
        return L

    def compute_normalized_laplacian(self):
        """Compute normalized Laplacian: L_norm = D^(-1/2) * L * D^(-1/2)."""
        D = np.sum(self.A, axis=1)
        D[D == 0] = 1  # Avoid division by zero
        D_inv_sqrt = np.diag(1.0 / np.sqrt(D))
        L = self.compute_graph_laplacian()
        L_norm = D_inv_sqrt @ L @ D_inv_sqrt
        return L_norm

    def spectral_analysis(self):
        """Perform spectral analysis on the Laplacian."""
        print("\nPerforming spectral analysis...")
        L = self.compute_graph_laplacian()

        # Compute eigenvalues and eigenvectors
        eigenvalues, eigenvectors = linalg.eigh(L)

        # Sort by magnitude
        idx = np.argsort(np.abs(eigenvalues))
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]

        # Algebraic connectivity (second smallest eigenvalue)
        algebraic_connectivity = eigenvalues[1] if len(eigenvalues) > 1 else 0

        return {
            'eigenvalues': eigenvalues,
            'eigenvectors': eigenvectors,
            'algebraic_connectivity': algebraic_connectivity,
            'spectral_gap': eigenvalues[1] - eigenvalues[0] if len(eigenvalues) > 1 else 0
        }

    def pagerank(self, alpha=0.85, max_iter=100, tol=1e-6):
        """Compute PageRank centrality."""
        print("\nComputing PageRank...")
        n = self.n

        # Normalize adjacency matrix by out-degree
        out_degree = np.sum(self.A, axis=1)
        out_degree[out_degree == 0] = 1  # Avoid division by zero

        # Transition matrix
        P = (self.A.T / out_degree).T

        # Initialize PageRank
        pr = np.ones(n) / n

        for iteration in range(max_iter):
            pr_new = (1 - alpha) / n + alpha * (P.T @ pr)

            if np.linalg.norm(pr_new - pr, 1) < tol:
                print(f"PageRank converged in {iteration+1} iterations")
                break

            pr = pr_new

        return pr

    def compute_clustering_coefficient(self):
        """Compute local clustering coefficients."""
        print("\nComputing clustering coefficients...")
        clustering = np.zeros(self.n)

        for i in range(self.n):
            # Get neighbors
            neighbors = np.where(self.A[i, :] > 0)[0]
            k = len(neighbors)

            if k < 2:
                clustering[i] = 0
                continue

            # Count edges between neighbors
            edges_between_neighbors = 0
            for j in range(len(neighbors)):
                for l in range(j + 1, len(neighbors)):
                    if self.A[neighbors[j], neighbors[l]] > 0:
                        edges_between_neighbors += 1

            # Clustering coefficient
            max_edges = k * (k - 1) / 2
            clustering[i] = edges_between_neighbors / max_edges if max_edges > 0 else 0

        return clustering

    def strongly_connected_components(self):
        """Identify strongly connected components using Tarjan's algorithm."""
        print("\nFinding strongly connected components...")

        index_counter = [0]
        stack = []
        lowlinks = {}
        index = {}
        on_stack = defaultdict(lambda: False)
        sccs = []

        def strongconnect(node):
            # Set the depth index for node
            index[node] = index_counter[0]
            lowlinks[node] = index_counter[0]
            index_counter[0] += 1
            on_stack[node] = True
            stack.append(node)

            # Consider successors
            successors = np.where(self.A[node, :] > 0)[0]
            for successor in successors:
                if successor not in index:
                    strongconnect(successor)
                    lowlinks[node] = min(lowlinks[node], lowlinks[successor])
                elif on_stack[successor]:
                    lowlinks[node] = min(lowlinks[node], index[successor])

            # If node is a root node, pop the stack and generate SCC
            if lowlinks[node] == index[node]:
                scc = []
                while True:
                    successor = stack.pop()
                    on_stack[successor] = False
                    scc.append(successor)
                    if successor == node:
                        break
                sccs.append(scc)

        for node in range(self.n):
            if node not in index:
                strongconnect(node)

        return sccs

    def dependency_depth_analysis(self):
        """Analyze dependency depths using BFS."""
        print("\nAnalyzing dependency depths...")
        depths = np.zeros(self.n)
        max_depth = 0

        for i in range(self.n):
            visited = set()
            queue = [(i, 0)]

            while queue:
                node, depth = queue.pop(0)
                if node in visited:
                    continue
                visited.add(node)
                depths[i] = max(depths[i], depth)
                max_depth = max(max_depth, depth)

                # Add dependencies
                deps = np.where(self.A[node, :] > 0)[0]
                for dep in deps:
                    if dep not in visited:
                        queue.append((dep, depth + 1))

        return depths, max_depth

    def compute_overlap_matrix(self):
        """Compute pairwise dependency overlap using Jaccard similarity."""
        print("\nComputing pairwise overlap matrix...")
        overlap = np.zeros((self.n, self.n))

        for i in range(self.n):
            deps_i = set(np.where(self.A[i, :] > 0)[0])

            for j in range(i + 1, self.n):
                deps_j = set(np.where(self.A[j, :] > 0)[0])

                if len(deps_i) == 0 and len(deps_j) == 0:
                    overlap[i, j] = overlap[j, i] = 0
                else:
                    # Jaccard similarity
                    intersection = len(deps_i.intersection(deps_j))
                    union = len(deps_i.union(deps_j))
                    overlap[i, j] = overlap[j, i] = intersection / union if union > 0 else 0

        return overlap

    def compute_compatibility_score(self):
        """
        Compute compatibility scores based on:
        1. Direct dependencies
        2. Transitive dependencies
        3. Dependency overlap
        """
        print("\nComputing compatibility scores...")

        # Transitive closure (reachability matrix)
        # Using matrix powers: R = A + A^2 + A^3 + ... until convergence
        R = self.A.copy()
        prev_R = np.zeros_like(R)
        power = 1

        while not np.array_equal(R > 0, prev_R > 0) and power < 20:
            prev_R = R.copy()
            R = R + np.linalg.matrix_power(self.A, power)
            R = (R > 0).astype(float)  # Binary reachability
            power += 1

        print(f"Transitive closure computed (depth: {power})")

        # Compatibility: packages are compatible if they don't create cycles
        compatibility = np.ones((self.n, self.n))

        for i in range(self.n):
            for j in range(self.n):
                if i == j:
                    compatibility[i, j] = 1.0
                # If both can reach each other, they're in a cycle (less compatible)
                elif R[i, j] > 0 and R[j, i] > 0:
                    compatibility[i, j] = 0.5
                # If one depends on the other, they're compatible but directional
                elif R[i, j] > 0 or R[j, i] > 0:
                    compatibility[i, j] = 0.8

        return compatibility, R

    def matrix_decomposition(self):
        """Perform SVD and other decompositions."""
        print("\nPerforming matrix decompositions...")

        # Singular Value Decomposition
        U, s, Vh = linalg.svd(self.A, full_matrices=False)

        # Effective rank (number of significant singular values)
        threshold = 0.01 * s[0]
        effective_rank = np.sum(s > threshold)

        return {
            'singular_values': s,
            'left_singular_vectors': U,
            'right_singular_vectors': Vh,
            'effective_rank': effective_rank,
            'rank': np.linalg.matrix_rank(self.A),
            'condition_number': s[0] / s[-1] if s[-1] > 0 else np.inf
        }

    def generate_report(self):
        """Generate comprehensive analysis report."""
        print("\n" + "="*60)
        print("COMPREHENSIVE DEPENDENCY ANALYSIS REPORT")
        print("="*60)

        results = {}

        # Basic statistics
        results['basic_stats'] = {
            'num_packages': self.n,
            'total_dependencies': int(np.sum(self.A)),
            'density': float(np.sum(self.A) / (self.n**2)),
            'avg_dependencies_per_package': float(np.mean(np.sum(self.A, axis=1))),
            'max_dependencies': int(np.max(np.sum(self.A, axis=1))),
            'packages_with_no_dependencies': int(np.sum(np.sum(self.A, axis=1) == 0))
        }

        # Spectral analysis
        spectral = self.spectral_analysis()
        results['spectral'] = {
            'algebraic_connectivity': float(spectral['algebraic_connectivity']),
            'spectral_gap': float(spectral['spectral_gap']),
            'top_10_eigenvalues': spectral['eigenvalues'][-10:].tolist()
        }

        # PageRank
        pagerank = self.pagerank()
        top_pr_indices = np.argsort(pagerank)[-20:][::-1]
        results['pagerank'] = {
            'top_20_packages': [(self.packages[i], float(pagerank[i])) for i in top_pr_indices]
        }

        # Clustering
        clustering = self.compute_clustering_coefficient()
        results['clustering'] = {
            'avg_clustering_coefficient': float(np.mean(clustering)),
            'max_clustering': float(np.max(clustering))
        }

        # SCCs
        sccs = self.strongly_connected_components()
        scc_sizes = sorted([len(scc) for scc in sccs], reverse=True)
        results['strongly_connected_components'] = {
            'num_sccs': len(sccs),
            'largest_scc_size': scc_sizes[0] if scc_sizes else 0,
            'top_10_scc_sizes': scc_sizes[:10]
        }

        # Dependency depths
        depths, max_depth = self.dependency_depth_analysis()
        results['dependency_depths'] = {
            'max_dependency_depth': int(max_depth),
            'avg_dependency_depth': float(np.mean(depths))
        }

        # Matrix decomposition
        decomp = self.matrix_decomposition()
        results['matrix_decomposition'] = {
            'rank': int(decomp['rank']),
            'effective_rank': int(decomp['effective_rank']),
            'condition_number': float(decomp['condition_number']) if not np.isinf(decomp['condition_number']) else 'infinity',
            'top_10_singular_values': decomp['singular_values'][:10].tolist()
        }

        # Compatibility
        compatibility, reachability = self.compute_compatibility_score()
        results['compatibility'] = {
            'avg_compatibility': float(np.mean(compatibility)),
            'min_compatibility': float(np.min(compatibility)),
            'reachable_pairs': int(np.sum(reachability > 0))
        }

        # Overlap analysis
        overlap = self.compute_overlap_matrix()
        results['overlap'] = {
            'avg_overlap': float(np.mean(overlap)),
            'max_overlap': float(np.max(overlap)),
            'highly_overlapping_pairs': int(np.sum(overlap > 0.5) / 2)  # Divide by 2 for symmetry
        }

        # Save results
        with open('/home/zack/analysis_results.json', 'w') as f:
            json.dump(results, f, indent=2)

        print("\nResults saved to /home/zack/analysis_results.json")
        return results


if __name__ == "__main__":
    analyzer = DependencyAnalyzer('/home/zack/dependency_data.json')
    results = analyzer.generate_report()

    print("\n" + "="*60)
    print("ANALYSIS COMPLETE")
    print("="*60)
