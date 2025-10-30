#!/usr/bin/python3
"""
Package Conflict and Incompatibility Analysis
Identifies packages that conflict, have circular dependencies, or version mismatches
"""

import subprocess
import json
import re
from collections import defaultdict
import numpy as np

def get_package_conflicts(package):
    """Get explicit conflicts declared by a package."""
    try:
        result = subprocess.run(
            ['pacman', '-Qi', package],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if line.startswith('Conflicts With'):
                    conflicts_str = line.split(':', 1)[1].strip()
                    if conflicts_str and conflicts_str != 'None':
                        return [c.strip() for c in conflicts_str.split()]
        return []
    except:
        return []

def get_package_provides(package):
    """Get what virtual packages this package provides."""
    try:
        result = subprocess.run(
            ['pacman', '-Qi', package],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if line.startswith('Provides'):
                    provides_str = line.split(':', 1)[1].strip()
                    if provides_str and provides_str != 'None':
                        return [p.strip() for p in provides_str.split()]
        return []
    except:
        return []

def get_package_replaces(package):
    """Get what packages this package replaces."""
    try:
        result = subprocess.run(
            ['pacman', '-Qi', package],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if line.startswith('Replaces'):
                    replaces_str = line.split(':', 1)[1].strip()
                    if replaces_str and replaces_str != 'None':
                        return [r.strip() for r in replaces_str.split()]
        return []
    except:
        return []

def analyze_conflicts():
    """Analyze all types of package conflicts."""

    # Load existing data
    with open('/home/zack/dependency_data.json', 'r') as f:
        data = json.load(f)

    packages = data['packages']
    A = np.array(data['adjacency_matrix'])
    n = len(packages)

    print("="*70)
    print("PACKAGE CONFLICT AND INCOMPATIBILITY ANALYSIS")
    print("="*70)

    conflicts = defaultdict(list)
    provides_map = defaultdict(list)
    replaces_map = defaultdict(list)

    print("\n[1/4] Scanning for explicit conflicts...")
    for i, pkg in enumerate(packages):
        if i % 100 == 0:
            print(f"  Scanning package {i}/{n}: {pkg}")

        pkg_conflicts = get_package_conflicts(pkg)
        if pkg_conflicts:
            conflicts[pkg] = pkg_conflicts

        pkg_provides = get_package_provides(pkg)
        for provided in pkg_provides:
            provides_map[provided].append(pkg)

        pkg_replaces = get_package_replaces(pkg)
        if pkg_replaces:
            replaces_map[pkg] = pkg_replaces

    print("\n[2/4] Analyzing circular dependencies...")
    circular_deps = []
    for i in range(n):
        for j in range(i+1, n):
            # Check if both i depends on j AND j depends on i
            if A[i, j] > 0 and A[j, i] > 0:
                circular_deps.append((packages[i], packages[j]))

    print("\n[3/4] Finding version conflicts...")
    # Find packages that provide the same thing (potential conflicts)
    virtual_conflicts = {}
    for virtual, providers in provides_map.items():
        if len(providers) > 1:
            virtual_conflicts[virtual] = providers

    print("\n[4/4] Identifying incompatible dependency chains...")
    # Find packages with mutually exclusive dependencies
    incompatible_chains = []
    for i in range(n):
        deps_i = set(np.where(A[i, :] > 0)[0])
        for dep_idx in deps_i:
            # Check if this dependency conflicts with the parent package
            dep_name = packages[dep_idx]
            if packages[i] in conflicts.get(dep_name, []):
                incompatible_chains.append((packages[i], dep_name, "parent conflicts with dependency"))

    # Save results
    results = {
        'explicit_conflicts': {k: v for k, v in conflicts.items()},
        'circular_dependencies': circular_deps,
        'virtual_package_conflicts': {k: v for k, v in virtual_conflicts.items() if len(v) > 1},
        'replaces': {k: v for k, v in replaces_map.items()},
        'incompatible_chains': incompatible_chains,
        'statistics': {
            'packages_with_conflicts': len(conflicts),
            'circular_dependency_pairs': len(circular_deps),
            'virtual_packages_with_multiple_providers': len([v for v in virtual_conflicts.values() if len(v) > 1]),
            'packages_that_replace_others': len(replaces_map),
            'incompatible_dependency_chains': len(incompatible_chains)
        }
    }

    with open('/home/zack/conflict_analysis.json', 'w') as f:
        json.dump(results, f, indent=2)

    # Print summary
    print("\n" + "="*70)
    print("CONFLICT ANALYSIS RESULTS")
    print("="*70)

    print(f"\n1. EXPLICIT CONFLICTS (via Conflicts With field):")
    print(f"   Total packages declaring conflicts: {len(conflicts)}")
    if conflicts:
        print(f"   Examples:")
        for pkg, conflicting in list(conflicts.items())[:10]:
            print(f"     • {pkg} conflicts with: {', '.join(conflicting[:5])}")
            if len(conflicting) > 5:
                print(f"       ... and {len(conflicting) - 5} more")
    else:
        print(f"   ✓ No explicit conflicts declared!")

    print(f"\n2. CIRCULAR DEPENDENCIES (A→B and B→A):")
    print(f"   Total circular pairs: {len(circular_deps)}")
    if circular_deps:
        print(f"   These create dependency cycles:")
        for pkg1, pkg2 in circular_deps[:20]:
            print(f"     • {pkg1} ⇄ {pkg2}")
        if len(circular_deps) > 20:
            print(f"     ... and {len(circular_deps) - 20} more")
    else:
        print(f"   ✓ No circular dependencies found!")

    print(f"\n3. VIRTUAL PACKAGE CONFLICTS (multiple providers):")
    print(f"   Virtual packages with multiple providers: {len([v for v in virtual_conflicts.values() if len(v) > 1])}")
    if virtual_conflicts:
        print(f"   These can cause selection conflicts:")
        for virtual, providers in list(virtual_conflicts.items())[:15]:
            if len(providers) > 1:
                print(f"     • '{virtual}' provided by: {', '.join(providers)}")

    print(f"\n4. PACKAGE REPLACEMENTS:")
    print(f"   Packages that replace others: {len(replaces_map)}")
    if replaces_map:
        print(f"   Examples:")
        for pkg, replaced in list(replaces_map.items())[:10]:
            print(f"     • {pkg} replaces: {', '.join(replaced)}")

    print(f"\n5. INCOMPATIBLE DEPENDENCY CHAINS:")
    print(f"   Found: {len(incompatible_chains)}")
    if incompatible_chains:
        print(f"   Examples:")
        for pkg1, pkg2, reason in incompatible_chains[:10]:
            print(f"     • {pkg1} → {pkg2} ({reason})")

    print("\n" + "="*70)
    print("Results saved to: conflict_analysis.json")
    print("="*70)

    return results

if __name__ == "__main__":
    results = analyze_conflicts()
