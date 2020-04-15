/* imports from node_modules */
import { Injectable } from '@angular/core';
/* imports from app */
import { Specimen } from './Specimen';
export class taxonRecord {
	Genus: string;
	specificEpithet: string;
	author: string;
}
@Injectable({
	providedIn: 'root'
})
export class Label2nameService {
	constructor(){
	}
	public authorFormatter(x: Specimen, t: Array<taxonRecord>): string {
		if(x.taxon < 0){
			return('');
		} else if(x.taxon >= t.length){
			return('');
		} else {
			return(t[x.taxon].author);
		}
	}
	public binomialFormatter(x: Specimen, t: Array<taxonRecord>): string {
		if(x.taxon < 0){
			return('');
		} else if(x.taxon >= t.length){
			return('');
		} else {
			return(t[x.taxon].Genus + ' ' + t[x.taxon].specificEpithet);
		}
	}
	public htmlFormatter(x: Specimen, t: Array<taxonRecord>): string {
		return(encodeURI(this.binomialFormatter(x, t)));
	}
}
