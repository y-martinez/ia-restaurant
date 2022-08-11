import React from 'react';


function SelectedProductsList(props) {
    if (props.products.length === 0) {
        return(
            <h4>Please select any product, listed above</h4>
        );
    }
    return (
        <ul>
            {props.products.map(product => {
                return (
                    <li key={product.id}>
                        <div>
                            <span>{product.name}</span>
                            <span>{product.price}</span>
                            <span>{product.quantity}</span>
                            <button onClick={e => props.handleRemoveProductClick(e, product)}>del</button>
                            <button onClick={e => props.handleReduceProductClick(e, product)}>-</button>
                        </div>
                    </li>
                );
            })}
        </ul>
    );
}


function OrderForm(props) {
    return (
        <form onSubmit={props.handleSubmitOrder}>
            <div className='form-group'>
                <label>Table</label>
                <select className='form-select' name='table' onChange={props.handleEditOrder} required>
                    <option hidden disabled selected value>Select</option>
                    {props.tables.map(table => {
                        return (
                            <option key={table.id} value={table.id}>{table.id}</option>
                        );
                    })}
                </select>

                <label>Employee</label>
                <select className='form-select' name='employee' onChange={props.handleEditOrder} required>
                    <option hidden disabled selected value>Select</option>
                    {props.employees.map(employee => {
                        return (
                            <option key={employee.id} value={employee.id}>{employee.id}</option>
                        );
                    })}
                </select>
                
                <label>Products</label>
                <SelectedProductsList products={props.selectedProducts}
                                      handleRemoveProductClick={props.handleRemoveProduct}
                                      handleReduceProductClick={props.handleReduceProduct}/>
            </div>

            <input type="submit" value="Submit" />
        </form>
    );
}


export default OrderForm;