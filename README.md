# git_security

git security repository for checking git security best practrices

1. Repository Permissions:

   Misconfiguration: Incorrect access levels for collaborators (e.g., giving write access where read would suffice).
   Risk: Unauthorized users might push unwanted changes or access sensitive data.
   Fix: Regularly review and adjust access levels; use teams for managing permissions systematically.

2. Protection of Main Branches:

   Misconfiguration: Failure to protect main branches (like main or master), allowing direct pushes without reviews.
   Risk: Introducing unreviewed changes can lead to security vulnerabilities or operational issues.
   Fix: Enable branch protection rules that require pull request reviews and status checks before merging.

3. Exposed Sensitive Data:

   Misconfiguration: Committing sensitive data like secrets, passwords, or API keys to the repository.
   Risk: Exposure of sensitive information can lead to data breaches or unauthorized access to other services.
   Fix: Use tools like Git hooks to scan commits for sensitive data pre-commit or employ secrets scanning tools to detect and revoke exposed secrets.

4. Lack of 2-Factor Authentication (2FA):

   Misconfiguration: Not enforcing 2FA for organization members.
   Risk: Accounts are more susceptible to compromise without 2FA, increasing the risk of unauthorized repository changes.
   Fix: Enforce 2FA for all collaborators in organization settings.

5. Dependency Management:

   Misconfiguration: Using outdated or vulnerable dependencies.
   Risk: Dependencies with known vulnerabilities can be exploited to compromise the application.
   Fix: Use GitHub’s Dependabot to automatically open pull requests to update dependencies to the latest, patched versions.
