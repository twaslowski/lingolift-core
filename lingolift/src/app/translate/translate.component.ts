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
        translation: string,
        source_language: string,
    };
    syntaxBreakdown!: {
        literal_translation: string;
        original_sentence: string;
        morph_analysis: Array<{
            word: string;
            lemma: string;
            morph_analysis: string;
            dependencies: string;
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
        this.isLoadingSyntax = true;
        console.log("Fetching translation for sentence: %s", this.sentence)
        this.apiService.translate(this.sentence).subscribe(data => {
            this.results = data;
            this.isLoadingTranslation = false;

            console.log("Fetching morphological analysis for sentence %s in language %s.",
                this.sentence, this.results.source_language)
            this.apiService.getSyntacticalAnalysis(this.sentence, this.results.source_language)
                .subscribe(data => {
                    console.log(data)
                    this.syntaxBreakdown = data;
                    this.isLoadingSyntax = false;
                });
        });

        this.isLoadingSuggestions = true;
        this.apiService.getResponseSuggestions(this.sentence).subscribe(data => {
            this.responseSuggestions = data;
            this.isLoadingSuggestions = false;
        });
    }

}
