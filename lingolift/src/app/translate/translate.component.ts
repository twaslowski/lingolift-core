import {Component} from '@angular/core';
import {ApiService} from '../api.service';

@Component({
    selector: 'app-translate',
    templateUrl: './translate.component.html',
    styleUrls: ['./translate.component.css']
})
export class TranslateComponent {

    sentence: string = '';
    results!: {
        natural_translation: string,
        literal_translation: string,
        original_sentence: string
    };
    syntaxBreakdown!: {
        literal_translation: string;
        original_sentence: string;
        syntactical_analysis: Array<{
            grammatical_context: string;
            translation: string;
            word: string;
        }>;
    }
    responseSuggestions!: {
        response_suggestions: Array<{
            suggestion: string,
            translation: string
        }>;
    }

    isLoadingTranslation!: boolean;
    isLoadingSyntax!: boolean;
    isLoadingSuggestions!: boolean;

    constructor(private apiService: ApiService) {
    }

    processSentence() {
        this.isLoadingTranslation = true;
        this.apiService.translate(this.sentence).subscribe(data => {
            this.results = data;
            this.isLoadingTranslation = false;
        });

        this.isLoadingSyntax = true;
        this.apiService.getSyntacticalAnalysis(this.sentence).subscribe(data => {
            this.syntaxBreakdown = data;
            this.isLoadingSyntax = false;
        });

        this.isLoadingSuggestions = true;
        this.apiService.getResponseSuggestions(this.sentence).subscribe(data => {
            this.responseSuggestions = data;
            this.isLoadingSuggestions = false;
        });
    }

}
