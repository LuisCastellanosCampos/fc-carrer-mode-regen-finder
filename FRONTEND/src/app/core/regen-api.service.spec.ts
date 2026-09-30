import { provideHttpClient } from '@angular/common/http';
import {
  HttpTestingController,
  provideHttpClientTesting
} from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { RegenApiService } from './regen-api.service';

describe('RegenApiService', () => {
  let service: RegenApiService;
  let httpTesting: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting()]
    });
    service = TestBed.inject(RegenApiService);
    httpTesting = TestBed.inject(HttpTestingController);
  });

  afterEach(() => httpTesting.verify());

  it('preserves the GET contract names and values for the regen search', () => {
    service.search({
      birth_date: '1998-04-12',
      nationality: 'Spain',
      position: 'ST'
    }).subscribe();

    const request = httpTesting.expectOne((candidate) => candidate.url === '/api/v1/regens');
    expect(request.request.method).toBe('GET');
    expect(request.request.params.keys().sort()).toEqual(['birth_date', 'nationality', 'position']);
    expect(request.request.params.get('birth_date')).toBe('1998-04-12');
    expect(request.request.params.get('nationality')).toBe('Spain');
    expect(request.request.params.get('position')).toBe('ST');
    request.flush({ query: {}, matches: [], message: null });
  });

  it('omits the optional position parameter when it is not provided', () => {
    service.search({
      birth_date: '1998-04-12',
      nationality: 'Spain',
      position: null
    }).subscribe();

    const request = httpTesting.expectOne((candidate) => candidate.url === '/api/v1/regens');
    expect(request.request.method).toBe('GET');
    expect(request.request.params.keys().sort()).toEqual(['birth_date', 'nationality']);
    expect(request.request.params.get('birth_date')).toBe('1998-04-12');
    expect(request.request.params.get('nationality')).toBe('Spain');
    request.flush({ query: {}, matches: [], message: null });
  });
});