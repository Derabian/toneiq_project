
public with sharing class ToneTranslatorController {
    @AuraEnabled
    public static Map<String, String> analyzeTone(String base64Audio, String userMessage){
        HttpRequest req = new HttpRequest();
        req.setEndpoint('callout:ToneIQ/analyze');
        req.setMethod('POST');
        req.setHeader('Content-Type','application/json');
        Map<String,String> body = new Map<String,String>{
            'audio' => base64Audio,
            'message' => userMessage
        };
        req.setBody(JSON.serialize(body));
        HttpResponse res = new Http().send(req);
        if(res.getStatusCode()!=200){
            throw new AuraHandledException('Tone service error '+res.getBody());
        }
        Map<String,Object> response = (Map<String,Object>) JSON.deserializeUntyped(res.getBody());

        // Create Case
        Case c = new Case();
        c.Subject       = (String)response.get('intent') + ' – Auto';
        c.Tone__c       = (String)response.get('tone');
        c.Intent__c     = (String)response.get('intent');
        c.Stress_Score__c = (Decimal)response.get('stress_score');
        c.Description   = (String)response.get('revised_message');
        insert c;

        // trigger flow by Platform Event or invocable logic here (omitted)

        // Suggest macro (simplified)
        String macroName = 'Calm-Billing-Walkthrough';
        return new Map<String,String>{
            'caseId'=>c.Id,
            'macroName'=>macroName
        };
    }
}
