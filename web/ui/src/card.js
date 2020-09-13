import React from 'react';

export default class Card extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className="Card">
              <p>{this.props.name}</p> <hr/>
              <div className="card-content">
                {this.props.children}
              </div>
            </div>
        );
    }
}
