/* imports from node_modules */
import * as tf from '@tensorflow/tfjs';
import { Injectable } from '@angular/core';
/* imports from app */
import { Specimen } from './Specimen';
@Injectable({
	providedIn: 'root'
})
export class TouvronEtAl2019Service {
	readonly inputlayerXY: number = 224;
	private loaded: boolean = false;
	constructor(){
		this.load();
	}
	private async loadNetwork(): Promise<number> {
		this.network = await tf.loadLayersModel('assets/herbarium2019/TouvronEtAl2019ResNet50.json', {
			strict: true
		});
		const x: tf.Tensor = await this.query(tf.zeros([1, 3, this.inputlayerXY, this.inputlayerXY], 'float32')); /* if it is not primed, it will not work... wft */
		return(x.dataSync()[1]);
	}
	private network: tf.InferenceModel;
	private load(): void {
		this.loadNetwork().then((): void => {
			this.loaded = true;
		});
	}
	private async reCheck(ms: number): Promise<boolean> {
		if(await this.timeout(10) === true){
			return(true);
		} else if((ms-10) < 0){
			return(false);
		} else {
			return(this.reCheck(ms-10));
		}
	}
	private timeout(ms: number): Promise<boolean> {
		return(new Promise(resolve => setTimeout(resolve, ms, this.loaded)));
	}
	private topThree(x: tf.Tensor): Array<Specimen> {
		const y: Float32Array = x.dataSync() as Float32Array;
		let z: Array<Specimen> = [new Specimen(), new Specimen(), new Specimen()];
		for(let k = y.length-1; k >= 0; k--){
			for(let j = 0; j <= z.length; j++){}
			if(y[k] >= z[0].probability){
				z[2].probability = z[1].probability;
				z[2].taxon = z[1].taxon;
				z[1].probability = z[0].probability;
				z[1].taxon = z[0].taxon;
				z[0].probability = y[k];
				z[0].taxon = k;
			} else if(y[k] >= z[1].probability){
				z[2].probability = z[1].probability;
				z[2].taxon = z[1].taxon;
				z[1].probability = y[k];
				z[1].taxon = k;
			} else if(y[k] >= z[2].probability){
				z[2].probability = y[k];
				z[2].taxon = k;
			}
		}
		return(z);
	}
	private async query(x: tf.Tensor4D): Promise<tf.Tensor> { /* tensorflowjs_converter --quantization_bytes 1 --input_format keras herbarium_fixresnet50.hdf5 TouvronEtAl2019/ */
		return(this.network.predict(x, {
			batchSize: 1,
			verbose: false
		}) as tf.Tensor);
	}
	public async ResNet50(x: tf.Tensor4D): Promise<Array<Specimen>> {
		if(this.loaded === true){
			return(this.topThree(await this.query(x)));
		} else if(await this.reCheck(60000) === true){
			return(this.topThree(await this.query(x)));
		} else {
			console.error('Could not load TouvronEtAl2019ResNet50 after 60 seconds!');
			return([new Specimen(), new Specimen(), new Specimen()]);
		}
	}
}
