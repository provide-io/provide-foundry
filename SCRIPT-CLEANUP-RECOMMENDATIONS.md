# Script Cleanup & Standardization Recommendations

## Executive Summary

Analysis of `scripts/` directories across 18 provide.io projects reveals:
- **63 total script files** across projects
- **11 likely stale/removable** scripts (17%)
- **16 documentation-related** scripts with duplication
- **3 scripts duplicated** across multiple projects

---

## 🗑️ RECOMMENDED FOR REMOVAL

### Stale Development/Testing Scripts

**provide-foundation** (9 scripts - likely from old testing work):
```bash
rm scripts/benchmark_performance.py      # Old benchmark script
rm scripts/cut_up_chuck.py               # Unknown/stale utility
rm scripts/debug_xdist_freeze.sh         # Debug script for specific issue
rm scripts/extreme_performance_test.py   # Old performance test
rm scripts/fix_macos_fd_limit.sh         # macOS-specific workaround
rm scripts/fix_split_imports.py          # One-time migration script
rm scripts/split_large_tests.py          # Old test splitting utility
rm scripts/split_remaining_files.sh      # Old test splitting utility
rm scripts/update-all-uv.sh              # Superseded by workspace tools
```

**tofusoup** (2 non-script files in scripts/):
```bash
rm scripts/MIGRATION_SUMMARY.md          # Documentation file misplaced
rm scripts/README.md                     # Documentation file misplaced
```

**All projects** (__pycache__ directories):
```bash
# Remove Python cache directories from scripts/
rm -rf */scripts/__pycache__
```

**Total recommended removals:** 12+ files

---

## 🔄 DUPLICATED SCRIPTS TO STANDARDIZE

### 1. mkdocs_hooks.py (3 copies)

**Current state:**
- terraform-provider-pyvider/scripts/mkdocs_hooks.py
- terraform-provider-tofusoup/scripts/mkdocs_hooks.py
- tofusoup/scripts/mkdocs_hooks.py

**Recommendation:**
- Compare the 3 versions to see if they're identical
- If identical: Move to `provide-foundry/src/provide/foundry/theme/hooks/`
- Extract via `extract_base_mkdocs()` so all projects use the same version
- If different: Keep project-specific versions but document why

### 2. Documentation Validation Scripts (Fragmented)

**Current fragmentation:**
- pyvider/scripts/check_doc_links.py
- pyvider-components/scripts/validate_docs.py
- pyvider-components/scripts/build_docs_and_examples.py
- terraform-provider-pyvider/scripts/validate_examples.sh

**Already centralized in provide-foundry:**
- scripts/docs_validate.py (comprehensive validation)
- scripts/validate_partials.py (partial validation)
- scripts/validate_standardization.py (compliance checking)

**Recommendation:**
- Review if project-specific validators have unique logic
- If generic: Remove and use central `docs_validate.py`
- If project-specific: Keep but document purpose

### 3. gen_ref_pages Scripts (Partially centralized)

**Current state:**
- pyvider-rpcplugin/scripts/mkdocs_gen_ref_pages.py
- provide-foundry/scripts/gen_monorepo_ref_pages.py
- Central version: .provide/foundry/gen_ref_pages.py (extracted to projects)

**Recommendation:**
- Check if rpcplugin version is different from central
- If same: Remove and use extracted version
- If custom: Rename to `mkdocs_gen_ref_pages_custom.py` to indicate it's intentional

---

## 📋 KEEP (PROJECT-SPECIFIC UTILITIES)

### Build & Packaging Scripts (Keep)
- ci-tooling/scripts/extract_package_name.py
- ci-tooling/scripts/extract_version.py
- ci-tooling/scripts/migrate-workflow.py
- pyvider/scripts/build_provider.py
- pyvider/scripts/runtime-hook.py
- pyvider-components/scripts/build.sh

### Setup & Environment Scripts (Keep)
- provide-foundation/scripts/setup_github_auth.py
- provide-foundation/scripts/version_checker.py
- provide-workspace/scripts/bootstrap.sh
- provide-workspace/scripts/setup.sh
- wrknv/scripts/shell-integration.sh
- pyvider/scripts/install-opentofu.sh
- pyvider/scripts/install-opentofu-wrapper.sh
- pyvider/scripts/install-uv.sh

### Testing & Quality Scripts (Keep)
- provide-foundation/scripts/apply_header.py
- provide-testkit/scripts/check_compliance.py
- provide-testkit/scripts/conform.py
- provide-testkit/scripts/coverage
- supsrc/scripts/run_background.sh
- supsrc/scripts/run_real_config_tests.py
- supsrc/scripts/test_interactive.py
- tofusoup/scripts/verify_harness_cli.py
- pyvider-cty/scripts/performance_characterization.py

### Provider-Specific Scripts (Keep)
- pyvider/scripts/terraform-provider-pyvider
- pyvider-components/scripts/terraform-provider-pyvider
- terraform-provider-pyvider/scripts/check-registry.sh
- terraform-provider-pyvider/scripts/sync-registry.sh
- terraform-provider-pyvider/scripts/clean_artifacts.sh
- terraform-provider-pyvider/scripts/inject_partials.py

### Central Documentation Scripts (Keep - already optimized)
- provide-foundry/scripts/docs_preflight.py (NEW - Phase 3)
- provide-foundry/scripts/docs_serve.py (NEW - Phase 3)
- provide-foundry/scripts/docs_validate.py
- provide-foundry/scripts/validate_docs.sh
- provide-foundry/scripts/validate_partials.py
- provide-foundry/scripts/validate_standardization.py (NEW - Phase 2)
- provide-foundry/scripts/gen_monorepo_ref_pages.py

---

## 🎯 ACTION PLAN

### Phase 1: Cleanup (Low Risk)
1. Remove stale provide-foundation scripts (9 files)
2. Remove misplaced markdown files from tofusoup/scripts (2 files)
3. Remove all __pycache__ directories from scripts/
4. **Estimated time:** 15 minutes
5. **Risk:** Very low (removing obviously stale files)

### Phase 2: Standardize mkdocs_hooks.py (Medium Risk)
1. Compare the 3 versions of mkdocs_hooks.py
2. If identical, move to central theme/hooks/
3. Test in terraform providers after centralization
4. **Estimated time:** 1 hour
5. **Risk:** Medium (need to verify builds still work)

### Phase 3: Review Documentation Scripts (Medium Risk)
1. Compare pyvider/check_doc_links.py with central docs_validate.py
2. Compare pyvider-components/validate_docs.py with central
3. Determine if unique logic exists or can consolidate
4. **Estimated time:** 1-2 hours
5. **Risk:** Medium (need to preserve unique functionality)

### Phase 4: Compare Before Extracting (Current Request)
1. Do NOT re-extract Makefiles yet
2. Compare current Makefiles with updated template
3. Identify differences that need to be preserved
4. Plan selective extraction
5. **Estimated time:** 30 minutes
6. **Risk:** Low (comparison only)

---

## 📊 SUMMARY STATISTICS

**Current State:**
- Total scripts: ~63 files
- Stale/removable: 12+ files (19%)
- Duplicated: 3 scripts across multiple projects
- Documentation scripts: 16 files (fragmented)

**After Cleanup:**
- Total scripts: ~48 files (-24%)
- Duplicated: 0 (centralized)
- Stale: 0 (removed)
- Well-organized: Yes

**Benefits:**
- Reduced maintenance burden
- Clear separation: project-specific vs centralized
- No confusion about which script to use
- Easier to find and update scripts

---

## 🚀 NEXT STEPS

**Immediate (Do Now):**
1. Review this report with team
2. Get approval for Phase 1 cleanup
3. Execute Phase 1 removals

**Short-term (This Week):**
1. Compare mkdocs_hooks.py versions
2. Review documentation script overlap
3. Plan consolidation strategy

**Before Re-extracting:**
1. Compare current Makefiles with template
2. Document intentional differences
3. Selective extraction (not blanket re-extract)

---

## ⚠️ IMPORTANT NOTES

**Do NOT remove without verification:**
- Any script referenced in Makefiles
- Any script referenced in CI/CD workflows
- Any script referenced in documentation
- Any script with recent git activity

**Always check git history before removal:**
```bash
git log --oneline scripts/suspicious-script.py
```

**Test after removal:**
```bash
make test
make docs-build
# Check CI passes
```

---

This analysis provides a clear path to cleaning up stale scripts while preserving important project-specific utilities.
