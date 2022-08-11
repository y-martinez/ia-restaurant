import React from 'react';
import {Link} from 'react-router-dom';


function ProductsListItem(props) {
    return(
        <div className="product-container list-item" 
             onClick={e => props.handleClick(e, props.product)}>
            <h1 className='product-title'>{props.product.name}</h1>
            <span className='product-quantity'>{props.product.quantityOrdered}</span>
            <span className='product-price'>Unit price:{props.product.price}</span>
            <span className='product-stock'>{props.product.stock}</span>
        </div>
    );
}


function ProductsList(props) {
    if (props.products.length === 0) {
        return (
            <div className='products-container'>
                <h3>No products were found</h3>
                <Link className="btn btn-primary" to="/products/new">
                Create a new product
                </Link>
            </div>
        );
    }

    return (
        <div className="products-container">
            <ul className="products-list list-unstyled">
                {props.products.map(product => {
                return (
                    <li key={product.id}>
                    <ProductsListItem product={product} 
                                      handleClick={props.handleSelectProduct}/>
                    </li>
                );
                })}
            </ul>
        </div>
    );
}

export default ProductsList;