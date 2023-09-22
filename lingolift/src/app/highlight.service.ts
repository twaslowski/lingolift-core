import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class HighlightService {
  private _highlightedWordSubject = new BehaviorSubject<string>('');
  highlightedWord$ = this._highlightedWordSubject.asObservable();

  setHighlightedWord(word: string): void {
    console.log("Highlighting word " + word)
    this._highlightedWordSubject.next(word);
  }

  clearHighlightedWord(): void {
    console.log("clearing highlighted word")
    this._highlightedWordSubject.next('');
  }
}
