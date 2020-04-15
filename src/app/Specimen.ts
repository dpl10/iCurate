export class Specimen {
	protected static SInit = (() => {
		Specimen.prototype.taxon = -1;
		Specimen.prototype.probability = -1;
		Specimen.prototype.file = '00000';
	})();
	taxon: number;
	file: string;
	probability: number;
}
