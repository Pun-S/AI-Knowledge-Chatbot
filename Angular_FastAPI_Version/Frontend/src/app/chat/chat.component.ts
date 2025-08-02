import { Component, ElementRef, ViewChild } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
    selector: 'app-chat',
    templateUrl: './chat.component.html',
    styleUrls: ['./chat.component.css']
})
export class ChatComponent {
    query = '';
    messages: { user: string, text: string }[] = [];
    backendUrl = 'http://localhost:8000';
    loading = false;
    fileUploaded = false;
    uploadedFileName = '';

    @ViewChild('chatWindow') chatWindow!: ElementRef;

    constructor(private http: HttpClient) { }

    scrollToBottom() {
        setTimeout(() => {
            if (this.chatWindow) {
                this.chatWindow.nativeElement.scrollTop = this.chatWindow.nativeElement.scrollHeight;
            }
        }, 100);
    }

    onFileSelected(event: any) {
        const file: File = event.target.files[0];
        if (file) {
            this.uploadedFileName = file.name;
            const formData = new FormData();
            formData.append('file', file);

            this.http.post(`${this.backendUrl}/upload`, formData)
                .subscribe((res: any) => {
                    alert(res.message);
                    this.fileUploaded = true;
                });
        }
    }

    sendMessage() {
        if (!this.query.trim()) return;

        this.messages.push({ user: 'user', text: this.query });
        this.scrollToBottom();

        this.loading = true;

        const formData = new FormData();
        formData.append('query', this.query);

        this.http.post(`${this.backendUrl}/ask`, formData)
            .subscribe((res: any) => {
                this.messages.push({ user: 'bot', text: res.answer });
                this.loading = false;
                this.scrollToBottom();
            }, () => {
                this.loading = false;
            });

        this.query = '';
    }

    resetChat() {
        this.messages = [];
        this.http.post(`${this.backendUrl}/reset`, {})
            .subscribe(() => {
                alert("Chat and memory reset.");
            });
    }
}