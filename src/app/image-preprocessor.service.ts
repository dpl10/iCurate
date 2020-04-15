/* imports from node_modules */
import * as tf from '@tensorflow/tfjs';
import { Injectable } from '@angular/core';
export class ImageExtract {
	data: Uint8Array;
	width: number;
	height: number
}
@Injectable({
	providedIn: 'root'
})
export class ImagePreprocessorService {
	private async url2image(u: string): Promise<HTMLImageElement> {
		return(new Promise((resolve) => {
			let i = new Image();
			i.onload = ((): void => {
				resolve(i);
			});
			i.src = u;
		}));
	}
	constructor(){
	}
	public async image2array(u: string, d: number, m: Array<number>, v: Array<number>): Promise<tf.Tensor4D> {
		const i: HTMLImageElement = await this.url2image(u);
		let h: number = Math.trunc(d*(i.height/i.width));
		let w: number = d;
		let ph: number = (d-h)/2;
		let pw: number = 0;
		if(i.width < i.height){
			h = d;
			w = Math.trunc(d*(i.width/i.height));
			ph = 0;
			pw = (d-w)/2;
		}
		const n: tf.Tensor3D = tf.browser.fromPixels(i, 3).toFloat().div(255);
// normalizing should be done, but results are generally worse...
		const b: tf.Tensor3D = tf.batchNorm3d(n, m, v);
		const r: tf.Tensor3D = tf.image.resizeBilinear(b, [h, w], false);
//		const r: tf.Tensor3D = tf.image.resizeBilinear(n, [h, w], false);
		const z: tf.Tensor3D = tf.pad3d(r, [[Math.floor(ph), Math.ceil(ph)], [Math.floor(pw), Math.ceil(pw)], [0, 0]], 0);
		const t: tf.Tensor3D = tf.transpose(z, [2, 0, 1]);
		return(tf.tidy((): tf.Tensor4D => {
			return(tf.expandDims(t));
		}));
	}
}
