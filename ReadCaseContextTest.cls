@IsTest private class ReadCaseContextTest {
    @IsTest static void emptyAndWrongTypeFailClosed() {
        Account a=new Account(Name='Synthetic test'); insert a;
        ReadCaseContext.Request wrong=new ReadCaseContext.Request(); wrong.caseId=a.Id;
        Test.startTest();
        List<ReadCaseContext.Result> r=ReadCaseContext.read(new List<ReadCaseContext.Request>{wrong,null});
        Test.stopTest();
        System.assertEquals(2,r.size());
        for(ReadCaseContext.Result item:r) { System.assertEquals('UNAVAILABLE',item.status); System.assertEquals(null,item.evidence); }
    }
    @IsTest static void emptyBatchReturnsEmpty() {
        System.assertEquals(0,ReadCaseContext.read(new List<ReadCaseContext.Request>()).size());
    }
}
