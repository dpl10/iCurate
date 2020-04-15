/* imports from node_modules */
import { AppComponent } from './app.component';
import { BrowserModule } from '@angular/platform-browser';
import { ButtonModule } from 'primeng/button';
import { CardModule } from 'primeng/card';
import { CarouselModule } from 'primeng/carousel';
import { DataViewModule } from 'primeng/dataview';
import { FileUploadModule } from 'primeng/fileupload';
import { LoadingBarHttpClientModule } from '@ngx-loading-bar/http-client';
import { NgModule } from '@angular/core';
/* imports from app */
import { Herbarium2019Component } from './herbarium2019/herbarium2019.component';
/* module */
@NgModule({
	declarations: [
		AppComponent,
		Herbarium2019Component
	],
	imports: [
		BrowserModule,
		ButtonModule,
		CardModule,
		CarouselModule,
		DataViewModule,
		FileUploadModule,
		LoadingBarHttpClientModule
	],
	providers: [],
	bootstrap: [AppComponent]
})
export class AppModule {}
