import React from 'react';

import OrdersClient from '../clients/OrdersClient';
import ProductsClient from '../clients/ProductsClient';
import OrderForm from '../components/OrderForm';
import ProductsList from '../components/ProductsList';


let onlyIdExample = [
    {
        id: 1
    },
    {
        id: 2
    },
    {
        id: 5
    }
];

let productsExample = [
    {
      "name": "soda",
      "price": 1.5,
      "stock": 100,
      "sku": "P-XGRZ8I",
      "id": 1
    },
    {
      "name": "burger",
      "price": 4.5,
      "stock": 100,
      "sku": "P-X31G8I",
      "id": 2
    },
    {
      "name": "pasta",
      "price": 7.5,
      "stock": 50,
      "sku": "P-123G8I",
      "id": 3
    },
    {
      "name": "fries",
      "price": 2.5,
      "stock": 150,
      "sku": "P-13GI00",
      "id": 4
    }
];


class OrderNew extends React.Component {
    ordersApi = new OrdersClient();
    productsApi = new ProductsClient();
    state = {
        loading: false,
        error: null,
        data: {
            tables: onlyIdExample,
            employees: onlyIdExample,
            products: productsExample
        },
        selectedProducts: [],
        order: {
            employee: '',
            table: '',
            products: [],
        }
    }

    constructor(props) {
        super(props);
        this.selectProductEvent = this.selectProductEvent.bind(this);
        this.removeSelectedProductEvent = this.removeSelectedProductEvent.bind(this);
        this.reduceSelectedProductEvent = this.reduceSelectedProductEvent.bind(this);
        this.editOrderEvent = this.editOrderEvent.bind(this);
        this.submitOrderEvent = this.submitOrderEvent.bind(this);
    }

    selectProductEvent(event, selectedProduct) {
        event.preventDefault();

        let products = this.state.selectedProducts;
        
        if(Array.isArray(products)) {
            let currentIndex = products.findIndex(product => product.id === selectedProduct.id);
            
            if(currentIndex < 0){
                selectedProduct.quantity = 1;
                products.push(selectedProduct);
            } else {
                products[currentIndex].quantity++;
            }
            this.setState({selectedProducts: products});
        }
    }

    removeSelectedProductEvent(event, productToRemove) {
        event.preventDefault();
        
        let products = this.state.selectedProducts;
        
        if(Array.isArray(products)) {
            this.setState({selectedProducts: products.filter(product => product.id !== productToRemove.id)});
        }
    }

    reduceSelectedProductEvent(event, productToReduce) {
        event.preventDefault();

        let products = this.state.selectedProducts;
        
        if(Array.isArray(products)) {
            let currentIndex = products.findIndex(product => product.id === productToReduce.id);

            if(products[currentIndex].quantity === 1) {
                products = products.filter(product => product.id !== productToReduce.id);
            } else {
                products[currentIndex].quantity--;
            }
            this.setState({selectedProducts: products});
        }
    }

    editOrderEvent(event) {
        event.preventDefault();

        this.setState({
            order: {
              ...this.state.order,
              [event.target.name]: event.target.value,
            },
          });
    }

    submitOrderEvent(event) {
        this.setState({ loading: true, error: null,});

        if (this.state.selectedProducts.length === 0) {
            // TODO: send error message, products should not be empty
        } else {
            let productsId = this.state.selectedProducts.map(p => Array(p.quantity).fill(p.id)).flat();
            this.setState({
                order: {
                    ...this.state.order,
                    products: productsId
                }
            });
            this.createOrder();
            event.preventDefault();
            // TODO: show success message or something else
        }
    }

    async createOrder(){
        if(this.state.loading){
            const response = await this.ordersApi.create(this.state.order);
            console.log(response);
            this.setState({ loading: false, ...response });
        }        
    }

    render() {
        return (
            <React.Fragment>
                <h1>New Order</h1>
                <ProductsList products={this.state.data.products}
                              handleSelectProduct={this.selectProductEvent} />
                <br /><br />
                <OrderForm tables={this.state.data.tables} 
                           employees={this.state.data.employees}
                           selectedProducts={this.state.selectedProducts}
                           handleRemoveProduct={this.removeSelectedProductEvent}
                           handleReduceProduct={this.reduceSelectedProductEvent}
                           handleEditOrder={this.editOrderEvent}
                           handleSubmitOrder={this.submitOrderEvent}
                />
                            
            </React.Fragment>
        );
    }
}

export default OrderNew;