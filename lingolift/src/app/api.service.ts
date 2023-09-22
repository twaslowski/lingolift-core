import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private baseUrl = 'http://localhost:5001';

  constructor(private http: HttpClient) {}

  translate(sentence: string): Observable<any> {
    console.log("Translating " + sentence)
    return this.http.post(`${this.baseUrl}/translate`, { sentence: sentence });
  }

  getResponses(sentence: string): Observable<any> {
    return this.http.post(`${this.baseUrl}/responses`, { sentence: sentence });
  }

  getSyntacticalAnalysis(sentence: string): Observable<any> {
    return this.http.post(`${this.baseUrl}/syntactical-analysis`, { sentence: sentence });
  }
}
