import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import Layout from './Layout';
import Home from '../pages/Home';
import Orders from '../pages/Orders';
import OrderNew from '../pages/OrderNew';
import NotFound from '../pages/NotFound'



function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Layout />}>
          <Route index element={<Home />} />
          <Route path='orders/new' element={<OrderNew />} />
          <Route path='orders' element={<Orders />} />
          <Route path='*' element={<NotFound />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
