import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { Herbarium2019Component } from './herbarium2019.component';

describe('Herbarium2019Component', () => {
  let component: Herbarium2019Component;
  let fixture: ComponentFixture<Herbarium2019Component>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ Herbarium2019Component ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(Herbarium2019Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
