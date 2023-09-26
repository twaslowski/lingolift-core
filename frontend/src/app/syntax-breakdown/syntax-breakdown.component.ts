import {Component, OnInit} from '@angular/core';
import {HighlightService} from "../highlight.service";
import {lastValueFrom} from "rxjs";
import {ApiService} from "../api.service";

@Component({
    selector: 'app-syntax-breakdown',
    templateUrl: './syntax-breakdown.component.html',
    styleUrls: ['./syntax-breakdown.component.css']
})
export class SyntaxBreakdownComponent implements OnInit {

    isLoading: boolean = false;
    activeWord: string | null = null;
    error: boolean = false;

    analysisData: {
        sentence: string;
        literal_translation: string | null;
        morph_analysis: Array<{
            word: string;
            lemma: string;
            morph_analysis: string;
            dependencies: string;
            translation: string | null;
        }>;
    } | null = null;

    constructor(private apiService: ApiService, private highlightService: HighlightService) {
    }

    async fetchAndBuildSyntaxBreakdown(sentence: string, language: string) {
        this.isLoading = true;
        let morphAnalysisData: {
            sentence: string;
            literal_translation: string | null;
            morph_analysis: Array<{
                word: string;
                lemma: string;
                morph_analysis: string;
                dependencies: string;
                translation: string | null;
            }>;
        };

        let literalTranslationData: {
            literal_translation: string;
            words: Array<{
                word: string;
                translation: string;
            }>;
        };

        const literalTranslation$ = this.apiService.getLiteralTranslation(sentence);
        const analysis$ = this.apiService.getSyntacticalAnalysis(sentence, language);

        morphAnalysisData = await lastValueFrom(analysis$).catch(() => this.error = true);

        if (!this.shouldFetchLiteralTranslation(sentence)) {
            this.analysisData = morphAnalysisData;
            this.isLoading = false;
            return;
        }

        literalTranslationData = await lastValueFrom(literalTranslation$).catch(() => this.error = true);

        // @ts-ignore
        for (let morphItem of morphAnalysisData.morph_analysis) {
            // @ts-ignore
            for (let wordItem of literalTranslationData.words) {
                if (morphItem.word === wordItem.word) {
                    morphItem.translation = wordItem.translation;
                    break;  // Once we've found a match, we can break out of the inner loop
                }
            }
        }

        morphAnalysisData.literal_translation = literalTranslationData.literal_translation
        console.log("Successfully consolidated morphological analysis and literal translation.")
        this.isLoading = false;
    }

    shouldFetchLiteralTranslation(sentence: string): boolean {
        return sentence.split(' ').length > 7;
    }


    ngOnInit(): void {
        this.highlightService.highlightedWord$.subscribe((word: any) => {
            this.activeWord = word;
        });
    }


    setActiveWord(word: string): void {
        this.highlightService.setHighlightedWord(word);
    }

    clearActiveWord(): void {
        this.highlightService.clearHighlightedWord();
    }
}
