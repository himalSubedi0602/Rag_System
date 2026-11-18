---
title: "GitLab Password Standards"
version_group: "hb:security/policies_and_standards/password-standard"
is_current: false
synthetic_old_version: true
updated_date: "2022-05-10"
department: "security"
# SYNTHETIC OLD VERSION for evaluation (Phase 5). Derived from GitLab handbook page
# hb:security/policies_and_standards/password-standard (CC BY-SA 4.0) with these facts deliberately changed:
#   'Minimum Length = 12 characters' -> 'Minimum Length = 8 characters'
#   'minimum password length needs to be set to 12 characters' -> 'minimum password length needs to be set to 8 characters'
---

### Password Requirements

- Minimum Length = 8 characters
- Special Characters = No
- Password Reuse = No
- Password expiration = No
- Multi-factor authentication (MFA) = Yes, whenever possible

To make a secure password you can remember, consider using a combination of 5 or more random words or generate in 1Password and store. This helps ensure the password isn't easily guessable and will be unique across sites.



### System Password Configuration Requirements

- For systems where a password can be configured the minimum password length needs to be set to 8 characters.
- The use of special characters is not required or even recommended.
- If a particular system requires a password history, configuration should be set for 25 remembered passwords.
- Passwords are not acceptable if they match the subsequent patterns, and must be checked against commonly used or expected patterns, including: known breached password lists, dictionary words, repetitive or sequential characters, or context specific words such as the name of the service, username, or derivatives thereof.
- System administrators of applications and/or devices must change default passwords.
- System administrators need to enable password strength on third party applications and/or tools, where applicable.
- For applications where a password is the only source of authentication, a password must be expired within a maximum of 90 calendar days.
- Systems should monitor and log failed login attempts.
- Information related to authentication failed login attempts need to be recorded within the application logs if technically feasible; such as: name, date, number of failed attempts, unique log identifier.
- Repeated failed login attempts need to trigger a temporary account lockout after 10 failed attempts. If the particular system will not support lockout after 10 attempts or less, the lockout needs to be configured to the minimum value allowed by the system. The lockout may end after a designated period of time, or require a manual unlock, depending on the profile of the application.
- Multi Factor Authentication (MFA) must be enforced.
