import React, { Component } from 'react';
import axios from 'axios';
import Player from "./Player.js";
import "./Form.css";

export default class Form extends Component {
    constructor() {
        super();
        this.state = {
            name: '',
            res: '',
            planet: '',
            dataReceived: false,
            key: 0,
        };
    }

    onChange = (event) => {
        this.setState({ 
            [event.target.name]: event.target.value,
        });
    }

    onSubmit = (event) => {
        event.preventDefault();       //prevent page refresh
        
        let { name } = this.state;     //pull from state
        
        name += this.state.planet;

        axios.post('http://brainstorm-it.herokuapp.com/api', { name })
            .then((result) => {
                this.setState( {res: result.data} );
                this.setState( {dataReceived: true} );
                this.setState({ key: Math.random() }); // re-render player
            });
        
    }

    render() {
        const { name, res, dataReceived } = this.state;

        return (
            <form onSubmit={this.onSubmit}>
                <input
                    type="text"
                    name="name"
                    value={name}
                    placeholder="Name"
                    onChange={this.onChange}
                />
                <select name="planet" onChange={this.onChange}>
                    <option value=""></option>
                    <option value="mercury">Mercury</option>
                    <option value="venus">Venus</option>
                    <option value="mars">Mars</option>
                    <option value="jupiter">Jupiter</option>
                    <option value="saturn">Saturn</option>
                    <option value="uranus">Uranus</option>
                    <option value="neptune">Neptune</option>
                    <option value="pluto">Pluto</option> {/* "but it's not a planet!" see next two */}
                    <option value="sun">Sun</option>
                    <option value="moon">Moon</option>
                </select>
                <button 
                    type="submit">
                        Submit
                </button>

                {dataReceived &&
                    <Player key={this.state.key} filename={res}/>
                }
                
            </form>
        );
    }
}