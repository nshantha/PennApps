/* global google */
import React from 'react';
import GoogleMapReact from 'google-map-react';
import './App.scss';

export default class HeatMap extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            mapData: {
                positions: []
                ,
                options: {   
                    radius: 20,   
                    opacity: 0.6,
                }
            }
        };

        this.updateMap();
    }

    async updateMap() {
        var xhr = new XMLHttpRequest();
        xhr.addEventListener('load', () => {
            this.setState({
                ...this.state,
                mapData: {
                    ...this.state.mapData,
                    positions: JSON.parse(xhr.responseText),
                }
            });
            console.log(this.state);
        });
        xhr.open('GET', 'http://localhost:8080');
        xhr.send();

        setTimeout(
            () => this.updateMap(), 
            15000
        );
    }

    render() {
	return (
            <div style={{ height: '90vh', width: '100%' }}>
              <GoogleMapReact
                ref={(el) => this._googleMap = el}
                bootstrapURLKeys={{ key: 'AIzaSyCR_GkgHY3y09arfYxLv4v_2BODFGPDY0s', libraries: ['places'] }}
                defaultCenter={this.props.center}
                defaultZoom={this.props.zoom}
                heatmapLibrary={true}          
                heatmap={this.state.mapData}
              >
              </GoogleMapReact>
            </div>
	);
    }
}
