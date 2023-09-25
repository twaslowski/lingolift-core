import {Component, Input} from '@angular/core';
import {ApiService} from "../api.service";
import {lastValueFrom} from "rxjs";

@Component({
    selector: 'app-translation',
    templateUrl: './translation.component.html',
    styleUrls: ['./translation.component.css']
})
export class TranslationComponent {

    @Input() sentence: string = '';

    translationResult: {
        translation: string,
        source_language: string,
    } | null = null;

    isLoading: boolean = false;

    constructor(private apiService: ApiService) {};

    async fetchTranslation(sentence: string) {
        this.isLoading = true;
        const translation$ = this.apiService.translate(sentence);
        this.translationResult = await lastValueFrom(translation$).catch(
            (err: any) => console.log("error occurred while fetching translation: " + err.toString())
        )
        this.isLoading = false;
    }
}
