import { TestBed } from '@angular/core/testing';

import { Label2nameService } from './label2name.service';

describe('Label2nameService', () => {
  let service: Label2nameService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Label2nameService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
