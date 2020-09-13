import React from 'react';
import './App.scss';
import { animateScroll as scroll } from "react-scroll";

import HeatMap from './HeatMap';

function App() {
    return (
        <div className="App">
          <header className="App-header">
	    <h2> SafeMaps </h2>
            <p className="App-subtext"> SafeMaps allows you to enjoy public spaces safetly. Use the map below to view real-time data on how well social distancing measures are being followed in popular areas. The more red an area appears the more people are packed together. </p>

            <button
              onClick={() => scroll.scrollToBottom()}>
              See the map!
            </button>

	  </header>
          <div className="App-banner">
            <div className="banner-card">
              <p className="App-subtext"> Using OpenCV, we are able to recognize moving bodies in video footage from cameras placed in public spaces like parks and busy streets</p>
              <img src="./opencv.png"/>
            </div>
            <div className="banner-card">
              <p className="App-subtext"> By compiling data collected by the computer vision recognition algorithm, we are able to create a map which represents the state of social distancing in real time. </p>
              <img src="./people.gif"/>
            </div>
          </div>
	  <HeatMap

            center={{
                lat: 40.7804577,
                lng: -73.9665439
            }}
            zoom={13}
          />
        </div>
    );
}

export default App;
