import { TestBed } from '@angular/core/testing';
import { App } from './app';
import { RegenSearchForm } from './features/regen/regen-search-form';

describe('App', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [App],
    }).compileComponents();
  });

  it('should create the app', () => {
    const fixture = TestBed.createComponent(App);
    const app = fixture.componentInstance;
    expect(app).toBeTruthy();
  });

  it('should render the regen search fields', async () => {
    const fixture = TestBed.createComponent(App);
    await fixture.whenStable();
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('form')).toBeTruthy();
    expect(compiled.querySelector('input[name="birthDate"]')).toBeTruthy();
    expect(compiled.querySelector('input[name="nationality"]')).toBeTruthy();
    expect(compiled.querySelector('input[name="position"]')).toBeTruthy();
  });

  it('should block submission when required fields are invalid', async () => {
    const fixture = TestBed.createComponent(RegenSearchForm);
    await fixture.whenStable();
    fixture.detectChanges();

    const form = fixture.nativeElement.querySelector('form') as HTMLFormElement;
    const submitButton = fixture.nativeElement.querySelector('button[type="submit"]') as HTMLButtonElement;

    expect(form.checkValidity()).toBe(false);
    expect(submitButton.disabled).toBe(true);
  });

  it('should allow a valid search without a position', async () => {
    const fixture = TestBed.createComponent(RegenSearchForm);
    await fixture.whenStable();
    const component = fixture.componentInstance;

    component.searchForm.setValue({
      birthDate: '1998-04-12',
      nationality: 'Spain',
      position: ''
    });
    fixture.detectChanges();

    const submitButton = fixture.nativeElement.querySelector('button[type="submit"]') as HTMLButtonElement;
    expect(component.searchForm.valid).toBe(true);
    expect(submitButton.disabled).toBe(false);
  });

  it('should reject a date that is not an ISO calendar date', async () => {
    const fixture = TestBed.createComponent(RegenSearchForm);
    await fixture.whenStable();
    const component = fixture.componentInstance;

    component.searchForm.setValue({
      birthDate: '12/04/1998',
      nationality: 'Spain',
      position: ''
    });

    expect(component.searchForm.valid).toBe(false);
  });
});
