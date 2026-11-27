# Validation
Run python3 validation/check.py locally from the repository root. No internet or external Python packages required.
Run python3 validation/live_check.py only to check public APIs online.
For GitHub Actions, go to Settings > Secrets and variables > Actions > Variables. Set VALE_ENABLE_ACTIONS=true for offline validation. Set VALE_ENABLE_PUBLIC_REFRESH=true as well to enable live checks and monthly refresh. Workflows use standard runners and a 3-minute timeout; no AI APIs. If neither variable is configured jobs skip. The refresh stores a separate external snapshot, not the Android pack. The pack revision only changes following a reviewed catalog edit.
A catalog hash checks integrity, not publisher authenticity. Protect main, do not publish secrets, and review changes.
