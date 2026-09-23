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
    expect(cards.length).toBe(2);
    expect(cards[0].textContent).toContain('Jugador Superior');
    expect(cards[0].textContent).toContain('ST');
    expect(cards[1].textContent).toContain('Jugador Segundo');
    expect(cards[1].textContent).toContain('CM');
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
});
