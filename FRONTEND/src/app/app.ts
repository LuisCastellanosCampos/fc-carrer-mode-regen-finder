import { Component } from '@angular/core';
import { RegenSearchForm } from './features/regen/regen-search-form';

@Component({
  selector: 'app-root',
  imports: [RegenSearchForm],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {}
