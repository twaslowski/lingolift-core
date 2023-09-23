import {Component, Input, OnInit} from '@angular/core';
import {HighlightService} from "../highlight.service";

@Component({
  selector: 'app-syntax-breakdown',
  templateUrl: './syntax-breakdown.component.html',
  styleUrls: ['./syntax-breakdown.component.css']
})
export class SyntaxBreakdownComponent implements OnInit {
  @Input() analysisData!: {
    literal_translation: string;
    original_sentence: string;
    syntactical_analysis: Array<{
      grammatical_context: string;
      translation: string;
      word: string;
    }>;
  };

  @Input() isLoading: boolean = false;
  activeWord: string | null = null;

  ngOnInit(): void {
    this.highlightService.highlightedWord$.subscribe(word => {
      this.activeWord = word;
    });
  }


  constructor(private highlightService: HighlightService) {}

  setActiveWord(word: string): void {
    this.highlightService.setHighlightedWord(word);
  }

  clearActiveWord(): void {
    this.highlightService.clearHighlightedWord();
  }

}
