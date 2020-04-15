import { TestBed } from '@angular/core/testing';

import { ImagePreprocessorService } from './image-preprocessor.service';

describe('ImagePreprocessorService', () => {
  let service: ImagePreprocessorService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ImagePreprocessorService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
