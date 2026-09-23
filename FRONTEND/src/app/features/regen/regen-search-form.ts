import { ChangeDetectionStrategy, Component } from '@angular/core';
import {
  AbstractControl,
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  ValidationErrors,
  Validators
} from '@angular/forms';

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
    this.searchForm.markAllAsTouched();
  }
}
