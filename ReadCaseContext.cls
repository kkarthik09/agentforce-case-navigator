public with sharing class ReadCaseContext {
    public class Request {
        @InvocableVariable(required=true label='Case record ID' description='Exact Case ID selected by the user; never infer an ID.')
        public Id caseId;
    }
    public class Result {
        @InvocableVariable(label='Authorized case evidence') public String evidence;
        @InvocableVariable(label='Status') public String status;
    }
    @InvocableMethod(label='Read Authorized Case Context' description='Read-only Case context respecting user permissions. No case updates, messages, refunds or closure.')
    public static List<Result> read(List<Request> requests) {
        Set<Id> ids=new Set<Id>();
        for(Request r:requests) if(r!=null && r.caseId!=null && r.caseId.getSObjectType()==Case.SObjectType) ids.add(r.caseId);
        Map<Id,Case> cases=new Map<Id,Case>();
        try {
            cases=new Map<Id,Case>([SELECT Id,CaseNumber,Subject,Status,Priority FROM Case WHERE Id IN :ids WITH USER_MODE]);
        } catch(QueryException e) {
            // Fail closed. Do not expose field names or existence of inaccessible records.
        }
        List<Result> results=new List<Result>();
        for(Request r:requests) {
            Result out=new Result(); Case c=r==null?null:cases.get(r.caseId);
            out.status=c==null?'UNAVAILABLE':'READ_ONLY_EVIDENCE';
            if(c!=null) out.evidence=JSON.serialize(new Map<String,Object>{
                'recordId'=>c.Id,'caseNumber'=>c.CaseNumber,'subject'=>c.Subject,'status'=>c.Status,'priority'=>c.Priority});
            results.add(out);
        }
        return results;
    }
}
