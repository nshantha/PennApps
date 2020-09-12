import React from 'react';
import logo from './logo.svg';
import './App.css';

import HeatMap from './HeatMap';

function App() {
    return (
        <div style={{ height: '100vh', width: '100%' }}>
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
