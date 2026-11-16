# Case navigation

Authenticated Salesforce user -> ReadCaseContext invocable Apex -> user-mode Case query -> numbered evidence.
Agent combines case context with an authorized Knowledge retriever configured in the sandbox.
The independent Python navigator is a deterministic lexical retrieval/routing reference for synthetic data.
It filters by caller-supplied authorized article IDs, publication status and expiry before scoring.
No evidence produces human escalation; High/Critical priorities always route to humans. Output is verbatim excerpts,
not a generated resolution. Lexical overlap is not confidence or a measure of factual correctness.

No Case closure, refunds, entitlement changes or outbound messages. The Apex action exposes only Id,
CaseNumber, Subject, Status and Priority; permission failure returns a generic unavailable result.
WITH USER_MODE plus with sharing are explicit. Validate FLS, sharing and action execution permissions in-org.
Python caller must authenticate/derive allowed_ids server-side. It is not itself an authorization server.
No real Knowledge connector, org deployment, agent routing or prompt-injection resilience is claimed as tested.

Official references:
- https://developer.salesforce.com/docs/platform/lwc/guide/apex-security
- https://developer.salesforce.com/docs/ai/agentforce/guide/apex-examples-custom-action.html
