/* imports from node_modules */
import { Component, OnInit } from '@angular/core';
/* imports from app */
import { ImagePreprocessorService } from '../image-preprocessor.service';
import { Label2nameService } from '../label2name.service';
import { Specimen } from '../Specimen';
import { TouvronEtAl2019Service } from '../TouvronEtaAl2019.service';
import specimens from '../../assets/herbarium2019/taxa.json'; /* tail -n +2 categories.txt | perl -F, -lane 'BEGIN{print("[")}{$y=join(",",@F[1..$#F]);$y=~tr/"//d;@x=split(/ /,$y);print("{\"Genus\":\"".$x[0]."\",\"specificEpithet\":\"".$x[1]."\",\"author\":\"".join(" ", @x[2..$#x])."\"},")}END{print("]")}' > taxa.json */
@Component({
	selector: 'app-herbarium2019',
	templateUrl: './herbarium2019.component.html',
	styleUrls: ['./herbarium2019.component.scss']
})
export class Herbarium2019Component implements OnInit {
	constructor(private imagePreprocessorService: ImagePreprocessorService, private label2nameService: Label2nameService, private touvronEtAl2019Service: TouvronEtAl2019Service){
		this.linkOut = document.createElement('a');
		this.linkOut.target = '_blank';
		this.linkOut.setAttribute('visibility', 'hidden');
	}
	ngOnInit(): void {
	}
	public formatAuthor(x: Specimen): string {
		return(this.label2nameService.authorFormatter(x, specimens));
	}
	public formatBinomial(x: Specimen): string {
		return(this.label2nameService.binomialFormatter(x, specimens));
	}
	public imageUploaded: boolean = false;
	public async imageUploader(x: {files: File}): Promise<void> {
		let f = new FileReader();
		f.onload = async (): Promise<void> => {
			this.uploadedImage = f.result as string;
			this.imageUploaded = true;
			this.predictions = await this.touvronEtAl2019Service.ResNet50(await this.imagePreprocessorService.image2array(f.result as string, this.touvronEtAl2019Service.inputlayerXY, [0.485, 0.456, 0.406], [0.229*0.229, 0.224*0.224, 0.225*0.225]));
			this.predicted = true;
		}
		f.readAsDataURL(x.files[0]);
	}
	private linkOut: HTMLAnchorElement;
	public predicted: boolean = false;
	public predictions: Array<Specimen>;
// should be typed
	public responsiveOptions = [
		{
			breakpoint: '1024px',
			numVisible: 4,
			numScroll: 2
		},{
			breakpoint: '768px',
			numVisible: 2,
			numScroll: 1
		},{
			breakpoint: '560px',
			numVisible: 1,
			numScroll: 1
		}
	];
	public async runNetwork(x: Specimen): Promise<void> {
		this.predictions = await this.touvronEtAl2019Service.ResNet50(await this.imagePreprocessorService.image2array('assets/herbarium2019/' + x.taxon + '-' + x.file + '.jpg', this.touvronEtAl2019Service.inputlayerXY, [0.485, 0.456, 0.406], [0.229*0.229, 0.224*0.224, 0.225*0.225]));
		this.predicted = true;
	}
	public specimen: Array<Specimen> = [
		{
			taxon: 34,
			file: '00007v',
			probability: 1
		},{
			taxon: 194,
			file: '00001v',
			probability: 1
		},{
			taxon: 250,
			file: '00000v',
			probability: 1
		},{
			taxon: 269,
			file: '00001v',
			probability: 1
		},{
			taxon: 290,
			file: '00000v',
			probability: 1
		},{
			taxon: 342,
			file: '00003v',
			probability: 1
		},{
			taxon: 513,
			file: '00000v',
			probability: 1
		},{
			taxon: 611,
			file: '00002v',
			probability: 1
		}
	];
	public uploadedImage: string; /* data uri */
	public virtualHerbarium(x: Specimen): void {
		this.linkOut.href = 'http://sweetgum.nybg.org/science/vh/specimen-list/?SummaryData=' + this.label2nameService.htmlFormatter(x, specimens)
		this.linkOut.click();
	}
}
