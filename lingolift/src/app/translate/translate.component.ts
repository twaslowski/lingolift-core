import {Component} from '@angular/core';
import {ApiService} from '../api.service';
import {lastValueFrom} from "rxjs";

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

    morphAnalysis!: {
        sentence: string;
        literal_translation: string;
        morph_analysis: Array<{
            word: string;
            lemma: string;
            morph_analysis: string;
            dependencies: string;
            translation: string;
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

    async processSentence() {
        this.isLoadingTranslation = true;
        this.isLoadingSyntax = true;
        console.log("Fetching translation for sentence: %s", this.sentence)

        this.apiService.translate(this.sentence).subscribe(data => {
            this.results = data;
            this.isLoadingTranslation = false;

            console.log("Fetching morphological analysis for sentence %s in language %s.",
                this.sentence, this.results.source_language)

            this.getMorphAnalysis();
        });

        this.isLoadingSuggestions = true;
        this.apiService.getResponseSuggestions(this.sentence).subscribe(data => {
            this.responseSuggestions = data;
            this.isLoadingSuggestions = false;
        });
    }

    async getMorphAnalysis() {
        let morphAnalysisData!: {
            sentence: string;
            literal_translation: string;
            morph_analysis: Array<{
                word: string;
                lemma: string;
                morph_analysis: string;
                dependencies: string;
                translation: string;
            }>;
        }

        let literalTranslationData!: {
            literal_translation: string;
            words: Array<{
                word: string;
                translation: string;
            }>;
        }

        const literalTranslation$ = this.apiService.getLiteralTranslation(this.sentence);
        const analysis$ = this.apiService.getSyntacticalAnalysis(this.sentence, this.results.source_language);

        morphAnalysisData = await lastValueFrom(analysis$);
        literalTranslationData = await lastValueFrom(literalTranslation$);

        for (let morphItem of morphAnalysisData.morph_analysis) {
            for (let wordItem of literalTranslationData.words) {
                if (morphItem.word === wordItem.word) {
                    morphItem.translation = wordItem.translation;
                    break;  // Once we've found a match, we can break out of the inner loop
                }
            }
        }
        morphAnalysisData.literal_translation = literalTranslationData.literal_translation
        console.log("Successfully consolidated morphological analysis and literal translation.")

        this.morphAnalysis = morphAnalysisData;
        this.isLoadingSyntax = false;
    }

}
