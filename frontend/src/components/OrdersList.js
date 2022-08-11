import React from 'react';
import {Link} from 'react-router-dom';


function ProductListItem(props) {
    return (
        <div className='order-products-item'>
            <h3 className='product-title'>{props.product.name}</h3>
            <span className='product-quantity'>{props.product.quantityOrdered}</span>
            <span className='product-price'>{props.product.price}</span>
        </div>
    );
}


function ProductList(props) {
    if (props.products.length === 0) {
        return;
    }
    return (
        <ul className='order-products list-unstyled'>
            {props.products.map(product => {
                return (
                    <li key={product.id}>
                         <ProductListItem product={product} />
                    </li>
                );
            })}
        </ul>
    );
}


function OrdersListItem(props) {
    return(
        <div className="list-item order-container">
            <h1 className='order-title'>Order #{props.order.id}</h1>
            <span className='order-created-date'>{props.order.createdAt}</span>
            <span className='order-updated-date'>{props.order.updatedAt}</span>
            <span className='order-status'>{props.order.status}</span>
            <span className='order-table'>{props.order.table}</span>

            <ProductList products={props.order.products} />
        </div>
    );
}


function OrdersList(props) {
    console.log(props);
    if (props.orders.length === 0) {
        return (
            <div className='orders-container'>
                <h3>No orders were found</h3>
                <Link className="btn btn-primary" to="/orders/new">
                Create new order
                </Link>
            </div>
        );
    }

    return (
        <div className="orders-container">
            <ul className="orders-list list-unstyled">
                {props.orders.map(order => {
                return (
                    <li key={order.id}>
                    <OrdersListItem order={order} />
                    </li>
                );
                })}
            </ul>
        </div>
    );
};

export default OrdersList;