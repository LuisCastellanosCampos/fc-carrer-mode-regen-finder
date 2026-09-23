import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

export interface RegenSearchQuery {
  birth_date: string;
  nationality: string;
  position: string | null;
}

export interface Player {
  id: string;
  name: string;
  birth_date: string;
  nationality: string;
  position: string;
  overall: number;
  age: number;
  season: string;
}

export interface RegenMatch {
  player: Player;
  match: {
    birth_date: boolean;
    nationality: boolean;
    position: boolean | null;
    is_possible_regen: boolean;
    message: string;
  };
}

export interface RegenSearchResponse {
  query: RegenSearchQuery;
  matches: RegenMatch[];
  message: string | null;
}

@Injectable({ providedIn: 'root' })
export class RegenApiService {
  private readonly http = inject(HttpClient);
  private readonly endpoint = '/api/v1/regens';

  search(query: RegenSearchQuery): Observable<RegenSearchResponse> {
    let params = new HttpParams()
      .set('birth_date', query.birth_date)
      .set('nationality', query.nationality);

    if (query.position) {
      params = params.set('position', query.position);
    }

    return this.http.get<RegenSearchResponse>(this.endpoint, { params });
  }
}
