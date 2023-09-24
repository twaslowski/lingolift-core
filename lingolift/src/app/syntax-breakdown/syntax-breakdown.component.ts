import {Component, Input, OnInit} from '@angular/core';
import {HighlightService} from "../highlight.service";

@Component({
    selector: 'app-syntax-breakdown',
    templateUrl: './syntax-breakdown.component.html',
    styleUrls: ['./syntax-breakdown.component.css']
})
export class SyntaxBreakdownComponent implements OnInit {
    @Input() analysisData!: {
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

    @Input() isLoading: boolean = false;
    activeWord: string | null = null;

    ngOnInit(): void {
        this.highlightService.highlightedWord$.subscribe(word => {
            this.activeWord = word;
        });
    }


    constructor(private highlightService: HighlightService) {
    }

    setActiveWord(word: string): void {
        this.highlightService.setHighlightedWord(word);
    }

    clearActiveWord(): void {
        this.highlightService.clearHighlightedWord();
    }
}
