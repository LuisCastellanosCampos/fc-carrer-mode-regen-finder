import { provideHttpClient } from '@angular/common/http';
import {
  HttpTestingController,
  provideHttpClientTesting
} from '@angular/common/http/testing';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RegenSearchForm } from './regen-search-form';

const responseWithMatches = {
  query: {
    birth_date: '1998-04-12',
    nationality: 'Spain',
    position: 'ST'
  },
  matches: [
    {
      player: {
        id: 'p-87',
        name: 'Jugador Superior',
        birth_date: '1998-04-12',
        nationality: 'Spain',
        position: 'ST',
        overall: 90,
        age: 24,
        season: '2026'
      },
      match: {
        birth_date: true,
        nationality: true,
        position: true,
        is_possible_regen: true,
        message: 'Posible regen: coinciden fecha de nacimiento, nacionalidad y posición.'
      }
    },
    {
      player: {
        id: 'p-85',
        name: 'Jugador Segundo',
        birth_date: '1998-04-12',
        nationality: 'Spain',
        position: 'CM',
        overall: 85,
        age: 22,
        season: '2026'
      },
      match: {
        birth_date: true,
        nationality: true,
        position: false,
        is_possible_regen: true,
        message: 'Posible regen: coinciden fecha de nacimiento y nacionalidad.'
      }
    },
    {
      player: {
        id: 'p-84',
        name: 'Jugador Sin Posición',
        birth_date: '1997-09-03',
        nationality: 'Portugal',
        position: 'CB',
        overall: 84,
        age: 21,
        season: '2026'
      },
      match: {
        birth_date: false,
        nationality: false,
        position: null,
        is_possible_regen: false,
        message: 'No coincide la fecha ni la nacionalidad y no hay posición para comparar.'
      }
    }
  ],
  message: null
};

describe('RegenSearchForm T23', () => {
  let fixture: ComponentFixture<RegenSearchForm>;
  let httpTesting: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RegenSearchForm],
      providers: [provideHttpClient(), provideHttpClientTesting()]
    }).compileComponents();

    fixture = TestBed.createComponent(RegenSearchForm);
    httpTesting = TestBed.inject(HttpTestingController);
    fixture.componentInstance.searchForm.setValue({
      birthDate: '1998-04-12',
      nationality: 'Spain',
      position: 'ST'
    });
    fixture.detectChanges();
  });

  afterEach(() => httpTesting.verify());

  it('announces the initial state and the criteria needed to start', () => {
    const initialState = fixture.nativeElement.querySelector(
      '.initial-state[role="status"]'
    ) as HTMLElement;

    expect(fixture.componentInstance.status()).toBe('idle');
    expect(initialState.textContent).toContain('fecha de nacimiento');
    expect(initialState.textContent).toContain('nacionalidad');
    expect(initialState.textContent).toContain('posición');
  });

  it('associates every search input with its visible label', () => {
    const expectedLabels = new Map([
      ['birth-date', 'Fecha de nacimiento'],
      ['nationality', 'Nacionalidad'],
      ['position', 'Posición (opcional)']
    ]);

    for (const [inputId, expectedLabel] of expectedLabels) {
      const input = fixture.nativeElement.querySelector(`#${inputId}`) as HTMLInputElement;
      const labels = Array.from(input.labels ?? []);

      expect(labels.some((label) => label.contains(input))).toBe(true);
      expect(labels.map((label) => label.querySelector('.field-label')?.textContent?.replace(/\s+/g, ' ').trim()))
        .toContain(expectedLabel);
    }
  });

  it('keeps field controls anchored when validation errors are shown', () => {
    const controls = fixture.componentInstance.searchForm.controls;
    controls.birthDate.setValue('');
    controls.nationality.setValue('');
    controls.birthDate.markAsTouched();
    controls.nationality.markAsTouched();
    fixture.detectChanges();

    const labels = fixture.nativeElement.querySelectorAll('.field-grid > label');
    expect(fixture.nativeElement.querySelectorAll('.error')).toHaveLength(2);
    expect(window.getComputedStyle(fixture.nativeElement.querySelector('.field-grid')).alignItems)
      .toBe('flex-start');
    expect(labels).toHaveLength(3);
  });

  it('keeps the optional position hint beside its label', () => {
    const fieldLabel = fixture.nativeElement.querySelector(
      '.field-grid label:nth-child(3) .field-label'
    ) as HTMLElement;

    expect(fieldLabel.textContent.trim()).toBe('Posición (opcional)');
    expect(window.getComputedStyle(fieldLabel).display).toBe('flex');
  });

  it('clears the filters and returns to the initial state', () => {
    const clearButton = fixture.nativeElement.querySelector('.clear-button') as HTMLButtonElement;
    expect(clearButton).toBeTruthy();

    clearButton.click();
    fixture.detectChanges();

    expect(fixture.componentInstance.searchForm.getRawValue()).toEqual({
      birthDate: '',
      nationality: '',
      position: ''
    });
    expect(fixture.componentInstance.status()).toBe('idle');
    expect(fixture.componentInstance.matches()).toEqual([]);
    expect(fixture.componentInstance.searchForm.pristine).toBe(true);
    expect(fixture.componentInstance.searchForm.untouched).toBe(true);
  });

  it('shows validation errors beside and associated with invalid fields', () => {
    const controls = fixture.componentInstance.searchForm.controls;
    controls.birthDate.setValue('');
    controls.nationality.setValue('');

    fixture.componentInstance.onSubmit();
    fixture.detectChanges();

    expect(fixture.nativeElement.querySelector('#birth-date-error')?.textContent).toContain(
      'Introduce una fecha válida.'
    );
    expect(fixture.nativeElement.querySelector('#nationality-error')?.textContent).toContain(
      'La nacionalidad es obligatoria.'
    );
    expect(fixture.nativeElement.querySelector('#birth-date')?.getAttribute('aria-describedby'))
      .toBe('birth-date-error');
    expect(fixture.nativeElement.querySelector('#nationality')?.getAttribute('aria-invalid'))
      .toBe('true');
    expect(fixture.nativeElement.querySelector('.validation-summary[role="alert"]')?.textContent)
      .toContain('Revisa los campos');
    expect(fixture.nativeElement.querySelector('.initial-state')).toBeNull();
  });

  it('rejects an ISO-formatted date that is not a calendar date without requesting results', () => {
    fixture.componentInstance.searchForm.controls.birthDate.setValue('2000-02-30');

    fixture.componentInstance.onSubmit();
    fixture.detectChanges();

    expect(fixture.componentInstance.searchForm.controls.birthDate.invalid).toBe(true);
    expect(fixture.nativeElement.querySelector('#birth-date-error')?.textContent).toContain(
      'Introduce una fecha válida.'
    );
    httpTesting.expectNone((request) => request.url === '/api/v1/regens');
  });

  it('sends only one request while a search is loading', () => {
    const component = fixture.componentInstance;
    component.onSubmit();
    fixture.detectChanges();
    expect(fixture.nativeElement.querySelector('.search-button').disabled).toBe(true);
    expect(fixture.nativeElement.querySelector('.clear-button').disabled).toBe(true);
    component.onSubmit();

    const requests = httpTesting.match((req) => req.url === '/api/v1/regens');
    requests.forEach((request) => request.flush(responseWithMatches));

    expect(requests).toHaveLength(1);
  });

  it('preserves search criteria after a successful response', () => {
    fixture.nativeElement.querySelector('.search-button').click();
    httpTesting.expectOne((req) => req.url === '/api/v1/regens').flush(responseWithMatches);
    fixture.detectChanges();

    expect(fixture.componentInstance.searchForm.getRawValue()).toEqual({
      birthDate: '1998-04-12',
      nationality: 'Spain',
      position: 'ST'
    });
  });

  it('allows filter fields to wrap without panel overflow at 320px', () => {
    Object.defineProperty(window, 'innerWidth', { configurable: true, value: 320 });
    window.dispatchEvent(new Event('resize'));
    fixture.detectChanges();

    const panel = fixture.nativeElement.querySelector('.search-panel') as HTMLElement;
    const grid = fixture.nativeElement.querySelector('.field-grid') as HTMLElement;

    expect(window.getComputedStyle(panel).boxSizing).toBe('border-box');
    expect(window.getComputedStyle(grid).display).toBe('flex');
    expect(window.getComputedStyle(grid).flexWrap).toBe('wrap');
  });

  it('should request the required parameters and omit an empty position', () => {
    fixture.componentInstance.searchForm.controls.position.setValue('');
    fixture.nativeElement.querySelector('button[type="submit"]').click();

    const request = httpTesting.expectOne(
      (req) => req.url === '/api/v1/regens' && req.method === 'GET'
    );

    expect(request.request.params.get('birth_date')).toBe('1998-04-12');
    expect(request.request.params.get('nationality')).toBe('Spain');
    expect(request.request.params.has('position')).toBe(false);
    request.flush({ query: {}, matches: [], message: 'No se encontraron posibles regens.' });
  });

  it('sends the complete search payload with trimmed values and no extra parameters', () => {
    fixture.componentInstance.searchForm.setValue({
      birthDate: '1998-04-12',
      nationality: '  Spain  ',
      position: '  ST  '
    });

    fixture.componentInstance.onSubmit();

    const request = httpTesting.expectOne(
      (req) => req.url === '/api/v1/regens' && req.method === 'GET'
    );
    expect(request.request.params.keys()).toEqual(['birth_date', 'nationality', 'position']);
    expect(request.request.params.get('birth_date')).toBe('1998-04-12');
    expect(request.request.params.get('nationality')).toBe('Spain');
    expect(request.request.params.get('position')).toBe('ST');
    request.flush(responseWithMatches);
  });

  it('should show a loading state while the request is pending', () => {
    fixture.nativeElement.querySelector('button[type="submit"]').click();
    fixture.detectChanges();

    expect(fixture.nativeElement.querySelector('[role="status"]')?.textContent).toContain(
      'Buscando posibles regens'
    );
    httpTesting.expectOne((req) => req.url === '/api/v1/regens').flush(responseWithMatches);
  });

  it('should render matches in the order received with their positions', () => {
    fixture.nativeElement.querySelector('button[type="submit"]').click();
    httpTesting.expectOne((req) => req.url === '/api/v1/regens').flush(responseWithMatches);
    fixture.detectChanges();

    const cards = fixture.nativeElement.querySelectorAll('.match-card');
    expect(cards.length).toBe(3);
    expect(cards[0].querySelector('.player-name')?.textContent).toContain('Jugador Superior');
    expect(cards[0].querySelector('.player-overall')?.textContent).toContain('90');
    expect(cards[0].querySelector('.player-age')?.textContent).toContain('24');
    expect(cards[0].querySelector('.player-position')?.textContent).toContain('ST');
    expect(cards[0].querySelector('.player-nationality')?.textContent).toContain('Spain');
    expect(cards[0].querySelector('.player-birth-date')?.textContent).toContain('1998-04-12');
    expect(cards[0].querySelector('.player-season')?.textContent).toContain('2026');
    expect(cards[0].querySelector('.match-message')?.textContent).toContain('Posible regen');
    expect(cards[0].querySelector('.date-match')?.textContent).toContain('Coincide');
    expect(cards[0].querySelector('.nationality-match')?.textContent).toContain('Coincide');
    expect(cards[0].querySelector('.position-match')?.textContent).toContain('Coincide');

    expect(cards[1].querySelector('.player-name')?.textContent).toContain('Jugador Segundo');
    expect(cards[1].querySelector('.player-position')?.textContent).toContain('CM');
    expect(cards[1].querySelector('.position-match')?.textContent).toContain('No coincide');

    expect(cards[2].querySelector('.player-name')?.textContent).toContain('Jugador Sin Posición');
    expect(cards[2].querySelector('.date-match')?.textContent).toContain('No coincide');
    expect(cards[2].querySelector('.nationality-match')?.textContent).toContain('No coincide');
    expect(cards[2].querySelector('.position-match')?.textContent).toContain('No informada');
    expect(fixture.nativeElement.querySelector('.results-summary[role="status"]')).toBeTruthy();
  });

  it('summarizes the submitted criteria and number of matches', () => {
    fixture.nativeElement.querySelector('.search-button').click();
    httpTesting.expectOne((req) => req.url === '/api/v1/regens').flush(responseWithMatches);
    fixture.detectChanges();

    const summary = fixture.nativeElement.querySelector('.results-summary') as HTMLElement;
    expect(summary.textContent).toContain('3');
    expect(summary.textContent).toContain('1998-04-12');
    expect(summary.textContent).toContain('Spain');
    expect(summary.textContent).toContain('ST');
  });

  it('should show the API message when there are no matches', () => {
    fixture.nativeElement.querySelector('button[type="submit"]').click();
    httpTesting.expectOne((req) => req.url === '/api/v1/regens').flush({
      query: {},
      matches: [],
      message: 'No se encontraron posibles regens.'
    });
    fixture.detectChanges();

    expect(fixture.nativeElement.querySelector('.empty-state')?.textContent).toContain(
      'No se encontraron posibles regens.'
    );
  });

  it('should show a Spanish error when the API is unavailable', () => {
    fixture.nativeElement.querySelector('button[type="submit"]').click();
    httpTesting.expectOne((req) => req.url === '/api/v1/regens').flush('unavailable', {
      status: 503,
      statusText: 'Service Unavailable'
    });
    fixture.detectChanges();

    expect(fixture.nativeElement.querySelector('.error-state')?.textContent).toContain(
      'No se pudo consultar el catálogo.'
    );
  });

  it('offers a retry after a recoverable error and keeps the search criteria', () => {
    fixture.nativeElement.querySelector('.search-button').click();
    httpTesting.expectOne((req) => req.url === '/api/v1/regens').flush('unavailable', {
      status: 503,
      statusText: 'Service Unavailable'
    });
    fixture.detectChanges();

    const retryButton = fixture.nativeElement.querySelector('.retry-button') as HTMLButtonElement;
    expect(retryButton).toBeTruthy();
    retryButton.click();
    fixture.detectChanges();

    const retryRequest = httpTesting.expectOne((req) => req.url === '/api/v1/regens');
    expect(retryRequest.request.params.get('birth_date')).toBe('1998-04-12');
    expect(retryRequest.request.params.get('nationality')).toBe('Spain');
    expect(retryRequest.request.params.get('position')).toBe('ST');
    retryRequest.flush(responseWithMatches);
    fixture.detectChanges();

    expect(fixture.componentInstance.status()).toBe('success');
    expect(fixture.componentInstance.searchForm.getRawValue()).toEqual({
      birthDate: '1998-04-12',
      nationality: 'Spain',
      position: 'ST'
    });
  });

  it('should show a Spanish error and preserve values after an HTTP 400', () => {
    fixture.nativeElement.querySelector('button[type="submit"]').click();
    httpTesting.expectOne((req) => req.url === '/api/v1/regens').flush(
      { detail: 'La fecha de nacimiento es inválida.' },
      { status: 400, statusText: 'Bad Request' }
    );
    fixture.detectChanges();

    expect(fixture.nativeElement.querySelector('.error-state')?.textContent).toContain(
      'No se pudo consultar el catálogo.'
    );
    expect(fixture.componentInstance.searchForm.getRawValue()).toEqual({
      birthDate: '1998-04-12',
      nationality: 'Spain',
      position: 'ST'
    });
  });
});
