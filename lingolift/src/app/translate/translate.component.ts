import { Component } from '@angular/core';
import { ApiService } from '../api.service';

@Component({
  selector: 'app-translate',
  templateUrl: './translate.component.html',
  styleUrls: ['./translate.component.css']
})
export class TranslateComponent {

  sentence: string = '';
  results: any;
  syntaxBreakdown!: {
    literal_translation: string;
    original_sentence: string;
    syntactical_analysis: Array<{
      grammatical_context: string;
      translation: string;
      word: string;
    }>;
  }

  constructor(private apiService: ApiService) {}

  processSentence() {
    this.apiService.translate(this.sentence).subscribe(data => {
      this.results = data;
    });

    this.apiService.getSyntacticalAnalysis(this.sentence).subscribe(data => {
      this.syntaxBreakdown = data;
      }
    )
  }

  highlightWord(word: any) {
    // Logic to highlight corresponding words in the original and literal translation
  }

  resetHighlight() {
    // Logic to reset highlights
  }
}
