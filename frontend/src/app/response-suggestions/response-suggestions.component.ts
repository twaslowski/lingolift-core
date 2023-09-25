import {Component, Input} from '@angular/core';

@Component({
  selector: 'app-response-suggestions',
  templateUrl: './response-suggestions.component.html',
  styleUrls: ['./response-suggestions.component.css']
})
export class ResponseSuggestionsComponent {
  @Input() responseSuggestions!: {
    response_suggestions: Array<{
      suggestion: string;
      translation: string;
    }>;
  };
  @Input() isLoading: boolean = false;
  protected readonly navigator = navigator;
}
