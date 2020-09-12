import React from 'react';
import './App.scss';
import { animateScroll as scroll } from "react-scroll";

import HeatMap from './HeatMap';

function App() {
    return (
        <div className="App">
          <header className="App-header">
	    <h2> SafeMaps </h2>
            <button
              onClick={() => scroll.scrollToBottom()}>
              See the map!
            </button>
	  </header>
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
