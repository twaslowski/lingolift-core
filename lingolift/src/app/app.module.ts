import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {HttpClientModule} from '@angular/common/http';
import {FormsModule} from '@angular/forms';

import {AppComponent} from './app.component';
import {ParentComponent} from './parent/parent.component';
import {ApiService} from './api.service';
import {TranslationComponent} from './translation/translation.component';
import {SyntaxBreakdownComponent} from './syntax-breakdown/syntax-breakdown.component';
import {ResponseSuggestionsComponent} from './response-suggestions/response-suggestions.component';
import {TooltipModule} from "./ui/tooltip/tooltip.module";

@NgModule({
    declarations: [
        AppComponent,
        ParentComponent,
        TranslationComponent,
        SyntaxBreakdownComponent,
        ResponseSuggestionsComponent
    ],
    imports: [
        BrowserModule,
        HttpClientModule,
        FormsModule,
        TooltipModule
    ],
    providers: [ApiService],
    bootstrap: [AppComponent]
})
export class AppModule {
}
