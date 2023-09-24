import {Component, Input, OnInit} from '@angular/core';
import {HighlightService} from "../highlight.service";

@Component({
  selector: 'app-translation',
  templateUrl: './translation.component.html',
  styleUrls: ['./translation.component.css']
})
export class TranslationComponent {
  @Input() translationResult!: {
    translation: string,
    source_language: string,
  };
  @Input() isLoading: boolean = false;
}
