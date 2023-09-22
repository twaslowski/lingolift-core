import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SyntaxBreakdownComponent } from './syntax-breakdown.component';

describe('SyntaxBreakdownComponent', () => {
  let component: SyntaxBreakdownComponent;
  let fixture: ComponentFixture<SyntaxBreakdownComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [SyntaxBreakdownComponent]
    });
    fixture = TestBed.createComponent(SyntaxBreakdownComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
