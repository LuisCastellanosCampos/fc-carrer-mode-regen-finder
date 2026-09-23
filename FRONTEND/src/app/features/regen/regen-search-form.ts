import { ChangeDetectionStrategy, Component, inject, signal } from '@angular/core';
import {
  AbstractControl,
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  ValidationErrors,
  Validators
} from '@angular/forms';
import { RegenApiService, RegenMatch } from '../../core/regen-api.service';

function isoDateValidator(control: AbstractControl): ValidationErrors | null {
  const value = control.value as string;
  if (!value) {
    return null;
  }

  const matchesFormat = /^\d{4}-\d{2}-\d{2}$/.test(value);
  const parsedDate = new Date(`${value}T00:00:00Z`);
  const isCalendarDate = !Number.isNaN(parsedDate.getTime()) && parsedDate.toISOString().startsWith(value);

  return matchesFormat && isCalendarDate ? null : { isoDate: true };
}

@Component({
  selector: 'app-regen-search-form',
  imports: [ReactiveFormsModule],
  templateUrl: './regen-search-form.html',
  styleUrl: './regen-search-form.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class RegenSearchForm {
  private readonly regenApi = inject(RegenApiService);

  readonly status = signal<'idle' | 'loading' | 'success' | 'error'>('idle');
  readonly matches = signal<RegenMatch[]>([]);
  readonly message = signal<string | null>(null);

  readonly searchForm = new FormGroup({
    birthDate: new FormControl('', {
      nonNullable: true,
      validators: [Validators.required, isoDateValidator]
    }),
    nationality: new FormControl('', {
      nonNullable: true,
      validators: [Validators.required]
    }),
    position: new FormControl('', { nonNullable: true })
  });

  onSubmit(): void {
    if (this.searchForm.invalid) {
      this.searchForm.markAllAsTouched();
      return;
    }

    const { birthDate, nationality, position } = this.searchForm.getRawValue();
    this.status.set('loading');
    this.message.set(null);

    this.regenApi
      .search({
        birth_date: birthDate,
        nationality: nationality.trim(),
        position: position.trim() || null
      })
      .subscribe({
        next: (response) => {
          this.matches.set(response.matches);
          this.message.set(response.message);
          this.status.set('success');
        },
        error: () => {
          this.matches.set([]);
          this.message.set('No se pudo consultar el catálogo.');
          this.status.set('error');
        }
      });
  }
}
