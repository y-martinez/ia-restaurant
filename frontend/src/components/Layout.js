import React from 'react';
import { Outlet, Link } from 'react-router-dom';

function Layout() {
    return (
        <div>
            <nav className='app-navbar'>
                <Link to='/'>Home</Link> |{' '}
                <Link to='/orders'>Orders</Link> |{' '}
                <Link to='/orders/new'>New Order</Link>
            </nav>
            <Outlet />
        </div>    
    );
}
  
export default Layout;