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

    sentence: string = '';
    isLoading: boolean = false;
    activeWord: string | null = null;

    analysisData: {
        sentence: string;
        literal_translation: string;
        morph_analysis: Array<{
            word: string;
            lemma: string;
            morph_analysis: string;
            dependencies: string;
            translation: string;
        }>;
    } | null = null;

    constructor(private apiService: ApiService, private highlightService: HighlightService) {
    }

    async fetchAndBuildSyntaxBreakdown(sentence: string) {
        this.isLoading = true;
        let morphAnalysisData: {
            sentence: string;
            literal_translation: string;
            morph_analysis: Array<{
                word: string;
                lemma: string;
                morph_analysis: string;
                dependencies: string;
                translation: string;
            }>;
        };

        let literalTranslationData: {
            literal_translation: string;
            words: Array<{
                word: string;
                translation: string;
            }>;
        };

        const literalTranslation$ = this.apiService.getLiteralTranslation(this.sentence);
        const analysis$ = this.apiService.getSyntacticalAnalysis(this.sentence, "russian");

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

        this.analysisData = morphAnalysisData;
        this.isLoading = false;
    }

    ngOnInit(): void {
        this.highlightService.highlightedWord$.subscribe(word => {
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
