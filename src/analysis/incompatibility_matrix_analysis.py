#!/usr/bin/python3
"""
Mathematical Analysis of Package Incompatibilities
Creates incompatibility matrices and conflict metrics
"""

import json
import numpy as np
from collections import defaultdict

def analyze_incompatibility_matrix():
    """Create and analyze the incompatibility matrix."""

    # Load data
    with open('/home/zack/dependency_data.json', 'r') as f:
        dep_data = json.load(f)

    with open('/home/zack/conflict_analysis.json', 'r') as f:
        conflict_data = json.load(f)

    packages = dep_data['packages']
    n = len(packages)
    pkg_to_idx = dep_data['pkg_to_idx']

    print("="*70)
    print("INCOMPATIBILITY MATRIX CONSTRUCTION")
    print("="*70)

    # Initialize incompatibility matrix I
    I = np.zeros((n, n), dtype=int)
    conflict_types = np.zeros((n, n), dtype=object)

    print("\nBuilding incompatibility matrix I[i,j]...")
    print("  I[i,j] = 1 if package i is incompatible with package j")

    # 1. Explicit conflicts
    print("\n[1/4] Processing explicit conflicts...")
    explicit_count = 0
    for pkg, conflicts in conflict_data['explicit_conflicts'].items():
        if pkg in pkg_to_idx:
            i = pkg_to_idx[pkg]
            for conflict in conflicts:
                # Strip version constraints
                conflict_base = conflict.split('<')[0].split('>')[0].split('=')[0]
                if conflict_base in pkg_to_idx:
                    j = pkg_to_idx[conflict_base]
                    I[i, j] = 1
                    I[j, i] = 1  # Conflicts are symmetric
                    conflict_types[i, j] = 'explicit'
                    conflict_types[j, i] = 'explicit'
                    explicit_count += 1

    print(f"   Added {explicit_count} explicit conflict edges")

    # 2. Circular dependencies
    print("\n[2/4] Processing circular dependencies...")
    circular_count = 0
    for pkg1, pkg2 in conflict_data['circular_dependencies']:
        if pkg1 in pkg_to_idx and pkg2 in pkg_to_idx:
            i = pkg_to_idx[pkg1]
            j = pkg_to_idx[pkg2]
            I[i, j] = 1
            I[j, i] = 1
            if conflict_types[i, j] == 0:
                conflict_types[i, j] = 'circular'
                conflict_types[j, i] = 'circular'
            else:
                conflict_types[i, j] = f"{conflict_types[i, j]},circular"
                conflict_types[j, i] = f"{conflict_types[j, i]},circular"
            circular_count += 1

    print(f"   Added {circular_count} circular dependency conflicts")

    # 3. Virtual package conflicts (packages providing same thing)
    print("\n[3/4] Processing virtual package conflicts...")
    virtual_count = 0
    for virtual, providers in conflict_data['virtual_package_conflicts'].items():
        # All providers are mutually incompatible (can't install both)
        provider_indices = [pkg_to_idx[p] for p in providers if p in pkg_to_idx]
        for i in range(len(provider_indices)):
            for j in range(i+1, len(provider_indices)):
                idx_i = provider_indices[i]
                idx_j = provider_indices[j]
                I[idx_i, idx_j] = 1
                I[idx_j, idx_i] = 1
                if conflict_types[idx_i, idx_j] == 0:
                    conflict_types[idx_i, idx_j] = f'virtual:{virtual}'
                    conflict_types[idx_j, idx_i] = f'virtual:{virtual}'
                else:
                    conflict_types[idx_i, idx_j] = f"{conflict_types[idx_i, idx_j]},virtual"
                    conflict_types[idx_j, idx_i] = f"{conflict_types[idx_j, idx_i]},virtual"
                virtual_count += 1

    print(f"   Added {virtual_count} virtual package conflicts")

    print("\n[4/4] Computing incompatibility metrics...")

    # Calculate metrics
    total_incompatibilities = np.sum(I) // 2  # Divide by 2 for symmetric matrix
    incompatibility_density = total_incompatibilities / (n * (n-1) / 2)

    # Incompatibility degree (how many packages each package conflicts with)
    incomp_degrees = np.sum(I, axis=1)

    # Most incompatible packages
    top_incomp_indices = np.argsort(incomp_degrees)[-20:][::-1]

    print("\n" + "="*70)
    print("INCOMPATIBILITY ANALYSIS RESULTS")
    print("="*70)

    print(f"\n1. INCOMPATIBILITY MATRIX PROPERTIES:")
    print(f"   Dimensions: {n} × {n}")
    print(f"   Total incompatibility edges: {total_incompatibilities}")
    print(f"   Incompatibility density: {incompatibility_density:.8f}")
    print(f"   Comparison to dependency density: {incompatibility_density/0.002615:.4f}x sparser")

    print(f"\n2. INCOMPATIBILITY DEGREE DISTRIBUTION:")
    print(f"   Mean incompatibilities per package: {np.mean(incomp_degrees):.2f}")
    print(f"   Median: {np.median(incomp_degrees):.0f}")
    print(f"   Max: {np.max(incomp_degrees)}")
    print(f"   Packages with zero conflicts: {np.sum(incomp_degrees == 0)}")

    print(f"\n3. TOP 20 MOST INCOMPATIBLE PACKAGES:")
    print(f"   {'Package':<35} {'Conflicts':<10} {'Type'}")
    print(f"   {'-'*70}")
    for idx in top_incomp_indices:
        pkg_name = packages[idx]
        degree = int(incomp_degrees[idx])
        # Find conflict types
        conflict_with = np.where(I[idx, :] > 0)[0]
        types = set()
        for j in conflict_with[:3]:
            if conflict_types[idx, j] != 0:
                types.add(str(conflict_types[idx, j]).split(',')[0].split(':')[0])
        type_str = ', '.join(types) if types else 'unknown'
        print(f"   {pkg_name:<35} {degree:<10} {type_str}")

    # Critical conflict analysis
    print(f"\n4. CRITICAL CONFLICTS (high-impact packages):")
    A = np.array(dep_data['adjacency_matrix'])
    in_degrees = np.sum(A, axis=0)  # How many depend on this package

    critical_conflicts = []
    for i in range(n):
        if incomp_degrees[i] > 0 and in_degrees[i] > 10:
            critical_conflicts.append((packages[i], int(incomp_degrees[i]), int(in_degrees[i])))

    critical_conflicts.sort(key=lambda x: x[1] * x[2], reverse=True)

    if critical_conflicts:
        print(f"   Packages that conflict AND have many dependents:")
        print(f"   {'Package':<30} {'Conflicts':<12} {'Dependents':<12} {'Impact'}")
        print(f"   {'-'*70}")
        for pkg, conflicts, dependents in critical_conflicts[:15]:
            impact = conflicts * dependents
            print(f"   {pkg:<30} {conflicts:<12} {dependents:<12} {impact}")

    # Analyze conflict by type
    print(f"\n5. CONFLICT BREAKDOWN BY TYPE:")
    type_counts = defaultdict(int)
    for i in range(n):
        for j in range(i+1, n):
            if I[i, j] > 0:
                ctype = str(conflict_types[i, j])
                if 'explicit' in ctype:
                    type_counts['explicit'] += 1
                if 'circular' in ctype:
                    type_counts['circular'] += 1
                if 'virtual' in ctype:
                    type_counts['virtual'] += 1

    for ctype, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
        pct = (count / total_incompatibilities) * 100 if total_incompatibilities > 0 else 0
        print(f"   {ctype:.<30} {count:>5} ({pct:>5.1f}%)")

    # Incompatibility clusters (strongly incompatible groups)
    print(f"\n6. INCOMPATIBILITY CLUSTERS:")
    # Find packages with >5 mutual conflicts
    clusters = []
    for i in range(n):
        if incomp_degrees[i] >= 5:
            conflicting = np.where(I[i, :] > 0)[0]
            # Check how many of these also conflict with each other
            mutual_conflicts = 0
            for j in range(len(conflicting)):
                for k in range(j+1, len(conflicting)):
                    if I[conflicting[j], conflicting[k]] > 0:
                        mutual_conflicts += 1
            if mutual_conflicts > 3:
                clusters.append((packages[i], int(incomp_degrees[i]), mutual_conflicts))

    if clusters:
        print(f"   Found {len(clusters)} packages in high-conflict clusters:")
        for pkg, conflicts, mutual in sorted(clusters, key=lambda x: x[2], reverse=True)[:10]:
            print(f"     • {pkg}: {conflicts} conflicts, {mutual} mutual")

    # Save results
    results = {
        'matrix_properties': {
            'dimensions': n,
            'total_incompatibilities': int(total_incompatibilities),
            'density': float(incompatibility_density),
            'mean_incompatibilities': float(np.mean(incomp_degrees)),
            'max_incompatibilities': int(np.max(incomp_degrees))
        },
        'top_incompatible_packages': [
            {
                'package': packages[idx],
                'conflicts': int(incomp_degrees[idx])
            }
            for idx in top_incomp_indices
        ],
        'critical_conflicts': [
            {
                'package': pkg,
                'conflicts': conflicts,
                'dependents': dependents,
                'impact_score': conflicts * dependents
            }
            for pkg, conflicts, dependents in critical_conflicts[:20]
        ],
        'conflict_types': dict(type_counts),
        'packages_with_zero_conflicts': int(np.sum(incomp_degrees == 0))
    }

    with open('/home/zack/incompatibility_matrix_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("\n" + "="*70)
    print("Results saved to: incompatibility_matrix_results.json")
    print("="*70)

    return I, conflict_types, results

if __name__ == "__main__":
    I, conflict_types, results = analyze_incompatibility_matrix()
