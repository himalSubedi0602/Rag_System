---
title: "GitLab Token Management Standard"
version_group: "hb:security/policies_and_standards/token-management-standard"
is_current: false
synthetic_old_version: true
updated_date: "2023-01-16"
department: "security"
# SYNTHETIC OLD VERSION for evaluation (Phase 5). Derived from GitLab handbook page
# hb:security/policies_and_standards/token-management-standard (CC BY-SA 4.0) with these facts deliberately changed:
#   'Personal Access Tokens - 30 days' -> 'Personal Access Tokens - 90 days'
---

### Token Creation and Distribution

1. Sharing and distribution of tokens will be limited, and must include documentation, and identity verification of who the token is being distributed to (IA-5(a) `*`).
1. GitLab team members will not distribute tokens to non-team members (AC-21, AC-22 `*`).
1. Token names will include the Group/Project name, and the creation date (YYYYMMDD) (IA-2, IA-5(b) `*`).
1. Tokens will be created with the minimum role and scope necessary to perform the desired task(s) (AC-6 `*`).
1. Tokens will never be created with the Maintainer or Owner role (AC-6 `*`).
1. Tokens will be created with the shortest reasonable expiration time to accomplish the desired task, but in all cases shall have expiration date not to exceed: (AC-2(3) `*`)
    - Personal Access Tokens - 90 days
    - Group Tokens – 1 year
    - Project Tokens – 1 year
    - Deploy tokens – 72 hours
    - Deploy keys – 72 hours
    - Impersonation Tokens – 24 hours
    - Runner Tokens – 1 year
    - Runner Registration Keys – 72 hours
1. The "random" part of a token (excluding prefixes and other additions) will be generated using a FIPS-certified and cryptographically-approved algorithm.
