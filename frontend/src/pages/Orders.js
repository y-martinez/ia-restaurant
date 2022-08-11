import React from 'react';
import {Link} from 'react-router-dom';

import OrdersClient from '../clients/OrdersClient';
import OrdersList from '../components/OrdersList';


class Orders extends React.Component {
    constructor(props) {
        super(props);
        this.api = new OrdersClient();
        this.state = {
            loading: true, 
        };
    }    

    async fetchData() {
        this.setState({loading: true});
        let response = await this.api.getAll();
        this.setState({loading: false, ...response});
    }

    componentDidMount() {
        this.fetchData();
    }
    
    render() {
        if(this.state.loading === true) {
            return 'Loading...';
        }

        if(this.state.error) {
            return `Error: ${this.state.error}`;
        }

        return (
            <React.Fragment>
                <div className='orders-hero'>
                    <div className='orders-container'>
                        <h1>Orders</h1>
                    </div>
                </div>

                <div className='orders-container'>
                    <div className="orders-buttons">
                        <Link to="/orders/new" className="btn btn-primary">
                            New Order
                        </Link>
                    </div>
                </div>

                <OrdersList orders={this.state.data} />
            </React.Fragment>
        );
    }
}

export default Orders;