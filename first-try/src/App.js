 /* global google */
 import React from 'react';
 import logo from './logo.svg';
 import './App.css';
 
 // import HeatMap from './mapview/HeatMap'
 import './HeatMap.css'
 
 import {
   InfoWindow, 
   withScriptjs,
   withGoogleMap,
   GoogleMap,
   Marker,
 } from "react-google-maps";
 
 import Geocode from "react-geocode";
 
 //autocomplete
 import AutoComplete from 'react-google-autocomplete';
 
 
 
 //set the api key
 Geocode.setApiKey("AIzaSyCR_GkgHY3y09arfYxLv4v_2BODFGPDY0s")
 
 
 class HeatMap extends React.Component {
   static defaultProps = {
     center: {
       lat: 59.95,
       lng: 30.33
     },
     zoom: 11
   }
 
   constructor(props) {
     super(props)
     this.state = {
       heatmapVisible: true,
       heatmapPoints: [
           {lat: 59.95, lng: 30.33},
           {lat: 59.96, lng: 30.32}
         ]
     }
   }
 
   onMapClick({x, y, lat, lng, event}) {
     if (!this.state.heatmapVisible) {
       return
     }
     
     this.setState({
       heatmapPoints: [ ...this.state.heatmapPoints, {lat, lng}]
     })
     if (this._googleMap !== undefined) {      
       const point = new google.maps.LatLng(lat, lng)
       this._googleMap.heatmap.data.push(point)
     }
   }
 
   toggleHeatMap() {    
     this.setState({
       heatmapVisible: !this.state.heatmapVisible
     }, () => {
       if (this._googleMap !== undefined) {
         this._googleMap.heatmap.setMap(this.state.heatmapVisible ? this._googleMap.map_ : null)
       }      
     })
 
   }
 }
 
 
 class App extends React.Component{
 
   state = {
     address: "",
     city: "",
     area: "",
     state: "",
     zoom: 15,
     height : 500,
     mapPosition: {
       lat:0,
       lng:0,
     },
     markerPosition: {
       lat:0,
       lng:0,
     }
   }
 
 
   componentDidMount() {
     if (navigator.geolocation) {
       navigator.geolocation.getCurrentPosition(position => {
         this.setState({
           mapPosition: {
             lat : position.coords.latitude,
             lng : position.coords.longitude,
           },
           markerPosition: {
             lat: position.coords.latitude,
             lng: position.coords.longitude,
           }
         },
           () => {
             Geocode.fromLatLng(position.coords.latitude, position.coords.longitude).then(
                 response => {
                     console.log(response)
                     const address = response.results[0].formatted_address,
                         addressArray = response.results[0].address_components,
                         city = this.getCity(addressArray),
                         area = this.getArea(addressArray),
                         state = this.getState(addressArray);
                     // console.log('city', city, area, state);
                     this.setState({
                         address: (address) ? address : '',
                         area: (area) ? area : '',
                         city: (city) ? city : '',
                         state: (state) ? state : '',
                     })
                 },
                 error => {
                     console.error(error);
                 }
             );
         })
       });
     }
 
 
     
   }
 
 
 
   getCity = (addressArray) => {
     let city = '';
     for (let index = 0; index < addressArray.length; index++) {
       if (addressArray[index].types[0] && 'adminstartive_area_level_2' === addressArray[index].types[0]) {
         city = addressArray[index].long_name;
         return city;
       }
     }
   }
 
   getArea = (addressArray) => {
     let area = '';
     for (let i = 0; i < addressArray.length; i++) {
         if (addressArray[i].types[0]) {
             for (let j = 0; j < addressArray[i].types.length; j++) {
                 if ('sublocality_level_1' === addressArray[i].types[j] || 'locality' === addressArray[i].types[j]) {
                     area = addressArray[i].long_name;
                     return area;
                 }
             }
         }
     }
 };
 
 getState = (addressArray) => {
     let state = '';
     for (let i = 0; i < addressArray.length; i++) {
         for (let i = 0; i < addressArray.length; i++) {
             if (addressArray[i].types[0] && 'administrative_area_level_1' === addressArray[i].types[0]) {
                 state = addressArray[i].long_name;
                 return state;
             }
         }
     }
 };
 
   onMarkerDragEnd = (event) => {
     let newLat = event.latLng.lat();
     let newLng = event.latLng.lng();
     // console.log(newLat,newLng);
 
     //then we need to know the city and address
     Geocode.fromLatLng(newLat,newLng).then(response =>{
       // console.log(response);
 
       const address = response.results[0].formatted_address,
             addressArray = response.results[0].address_components,
             city  = this.getCity(addressArray),
             area = this.getArea(addressArray),
             state = this.getState(addressArray);
 
 
       this.setState ({
         address: (address) ?address :"",
         area: (area) ? area : "",
         city: (city) ? city : "",
         state: (state) ? city : "",
         markerPosition : {
           lat: newLat,
           lng: newLng
         },
         mapPosition:{
           lat: newLat,
           lng: newLng
         },
 
       })
 
     })
 
   }
 
 
   onPlaceSelected = (place) => {
     console.log('plc', place);
     const address = place.formatted_address,
         addressArray = place.address_components,
         city = this.getCity(addressArray),
         area = this.getArea(addressArray),
         state = this.getState(addressArray),
         latValue = place.geometry.location.lat(),
         lngValue = place.geometry.location.lng();
 
     console.log('latvalue', latValue)
     console.log('lngValue', lngValue)
 
     // Set these values in the state.
     this.setState({
         address: (address) ? address : '',
         area: (area) ? area : '',
         city: (city) ? city : '',
         state: (state) ? state : '',
         markerPosition: {
             lat: latValue,
             lng: lngValue
         },
         mapPosition: {
             lat: latValue,
             lng: lngValue
         },
     })
 };
 
 
 
 
 
   render() {
     
     const heatMapData = {
       positions: this.state.heatmapPoints,
       options: {
       radius: 20,
       opacity: 0.6
       }
     }
     const MapWithAMarker = withScriptjs ( withGoogleMap ( props => //higher order Component
       <GoogleMap
         defaultZoom={8}
         defaultCenter={{ lat: this.state.mapPosition.lat, lng: this.state.mapPosition.lng }}
       >
         <Marker
           draggable = {true}
           onDragEnd = {this.onMarkerDragEnd}
           position={{ lat: this.state.markerPosition.lat, lng: this.state.markerPosition.lng }}
         >
 
         <InfoWindow>
             <div>
             <span style={{ padding: 0, margin: 0 }}>{this.state.address}</span>
             </div>
         </InfoWindow>
 
       </Marker>
 
       <AutoComplete style = {{ width :"100%",height:'40px',paddingLeft: 16, marginTop:2, marginBottom:"2rem"}}
          onPlaceSelected = {this.onPlaceSelected}
 
       />
 
 
 
       </GoogleMap>
     ));
 
     return (
       <div style = {{padding:'1rem',margin:'0 aut0',minWidth:1000}}>
 
         <h1> Google Map Basic</h1>
 
         <MapWithAMarker
         googleMapURL="https://maps.googleapis.com/maps/api/js?key=AIzaSyCR_GkgHY3y09arfYxLv4v_2BODFGPDY0s&v=3.exp&libraries=geometry,drawing,places"
         loadingElement={<div style={{ height: `100%` }} />}
         containerElement={<div style={{ height: `400px` }} />}
         mapElement={<div style={{ height: `100%` }} />}
         heatmapLibrary={true}
         heatmap={heatMapData}
         >
         </MapWithAMarker>
         
 
       </div>
     );
   }
 
 }
 
 export default App;
 