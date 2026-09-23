import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { RegenSearchForm } from './features/regen/regen-search-form';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, RegenSearchForm],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('regen-finder-frontend');
}
