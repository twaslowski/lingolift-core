import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {env} from "../environments/environment";

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private baseUrl = env.apiEndpoint

  constructor(private http: HttpClient) {}

  translate(sentence: string): Observable<any> {
    console.log("Translating " + sentence)
    return this.http.post(`${this.baseUrl}/translate`, { sentence: sentence });
  }

  getResponseSuggestions(sentence: string): Observable<any> {
    return this.http.post(`${this.baseUrl}/responses`, { sentence: sentence });
  }

  getSyntacticalAnalysis(sentence: string, sourceLanguage: string): Observable<any> {
    return this.http.post(`${this.baseUrl}/syntactical-analysis`, { sentence: sentence, source_language: sourceLanguage });
  }

  getLiteralTranslation(sentence: string): Observable<any> {
    return this.http.post(`${this.baseUrl}/literal-translation`, { sentence: sentence });
  }
}
