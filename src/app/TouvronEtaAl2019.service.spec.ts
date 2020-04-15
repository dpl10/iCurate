import { TestBed } from '@angular/core/testing';

import { TouvronEtAl2019Service } from './TouvronEtaAl2019.service';

describe('TouvronEtAl2019Service', () => {
  let service: TouvronEtAl2019Service;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(TouvronEtAl2019Service);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
