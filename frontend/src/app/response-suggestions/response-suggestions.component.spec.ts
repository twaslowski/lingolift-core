import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ResponseSuggestionsComponent } from './response-suggestions.component';

describe('ResponsesComponent', () => {
  let component: ResponseSuggestionsComponent;
  let fixture: ComponentFixture<ResponseSuggestionsComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ResponseSuggestionsComponent]
    });
    fixture = TestBed.createComponent(ResponseSuggestionsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
