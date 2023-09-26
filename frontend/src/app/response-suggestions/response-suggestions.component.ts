import {Component, EventEmitter, Input, Output} from '@angular/core';
import {ApiService} from "../api.service";
import {lastValueFrom} from "rxjs";

@Component({
    selector: 'app-response-suggestions',
    templateUrl: './response-suggestions.component.html',
    styleUrls: ['./response-suggestions.component.css']
})
export class ResponseSuggestionsComponent {
    isLoading: boolean = false;

    // @ts-ignore
    protected readonly navigator = navigator;

    responseSuggestions: {
        response_suggestions: Array<{
            suggestion: string;
            translation: string;
        }>;
    } | null = null;

    @Output() analysisRequest = new EventEmitter<string>();

    constructor(private apiService: ApiService) {
    };

    async fetchResponseSuggestions(sentence: string) {
        this.isLoading = true;
        const suggestions$ = this.apiService.getResponseSuggestions(sentence);
        this.responseSuggestions = await lastValueFrom(suggestions$).catch(
            (err: any) => console.log("error occurred while fetching response suggestions: " + err.toString())
        )
        this.isLoading = false;
    }

    emitAnalysisRequest(sentence: string) {
        this.analysisRequest.emit(sentence);
    }
}
