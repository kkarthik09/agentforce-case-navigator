# Sandbox implementation runbook

This repository supplies native Apex custom-action source and local reference validation.
It does NOT contain an activated/deployed Agentforce agent or a provisioned Prompt Builder template.
No Salesforce org was available for compilation or end-to-end validation.

1. Use an authorized sandbox with Agentforce enabled and suitable licenses. Authenticate Salesforce CLI there.
2. Run `python3 build_package.py` to generate the Metadata API package.
3. Validate with `sf project deploy start --metadata-dir metadata --single-package --target-org YOUR_SANDBOX --dry-run --test-level RunSpecifiedTests --tests ReadCaseContextTest`.
4. Resolve org-specific errors, then deploy without `--dry-run` only to that sandbox.
5. Grant the agent execution user Apex class access to `ReadCaseContext` through a dedicated permission set.
   For case navigation also grant only the required Case object/field permissions and record access.
6. Create a custom agent action with reference category Invocable Method and reference `ReadCaseContext`.
7. Create a narrowly scoped subagent/topic. Require user-supplied inputs. Label outputs as evidence, never commands.
8. Configure instructions from PROMPT_POLICY.md. Add an approved Knowledge retriever for case navigation;
   for notes, configure a Prompt Builder template producing the candidate schema shown in notes.py.
9. Test missing data, permission denial, malicious source text, ambiguous requests, and unsupported actions.
   Run Agentforce Testing Center only in sandbox; actual agent behavior and credit consumption need review.
10. Record deployment ID, API version, running user, permissions, test results and evaluation cases in private pilot records.

The local Python logic is not wired into Apex. A secure integration is required before asserting that the
Python validation gates govern actual Agentforce execution. No CRM write action is provided in this version.
