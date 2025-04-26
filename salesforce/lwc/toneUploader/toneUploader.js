
import { LightningElement, track } from 'lwc';
import analyzeTone from '@salesforce/apex/ToneTranslatorController.analyzeTone';

export default class ToneUploader extends LightningElement {
    fileData;
    userMessage='';
    @track caseUrl;
    @track macroName;

    handleFile(e){
        const file = e.target.files[0];
        const reader = new FileReader();
        reader.onload = () => {
            this.fileData = reader.result.split(',')[1];
        };
        reader.readAsDataURL(file);
    }

    handleMsg(e){
        this.userMessage = e.target.value;
    }

    async submit(){
        if(!this.fileData){ alert('Upload audio'); return;}
        const result = await analyzeTone({base64Audio:this.fileData,userMessage:this.userMessage});
        this.caseUrl = '/'+result.caseId;
        this.macroName = result.macroName;
    }

    insertMacro(){
        // placeholder – could fire event to chat panel
        alert('Macro inserted: '+this.macroName);
    }
}
