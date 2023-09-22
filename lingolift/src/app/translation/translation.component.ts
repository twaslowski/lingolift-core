import {Component, Input, OnInit} from '@angular/core';
import {HighlightService} from "../highlight.service";

@Component({
  selector: 'app-translation',
  templateUrl: './translation.component.html',
  styleUrls: ['./translation.component.css']
})
export class TranslationComponent implements OnInit {
  @Input() translationResult!: {
    natural_translation: string,
    literal_translation: string,
    original_sentence: string
  };

  @Input() analysisData!: Array<{
    grammatical_context: string;
    translation: string;
    word: string;
  }>;

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
