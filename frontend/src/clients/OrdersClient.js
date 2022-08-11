import ApiClient from "./api";

class OrdersClient extends ApiClient {
    defaultErrorMessage = "There is an error to connect to the external Orders Service"

    create(orderData) {
        return this.run(`/orders`, {
            method: 'POST',
            body: JSON.stringify(orderData),
        });
    }

    getAll() {
        return this.run('/orders');
    }

    getById(orderId) {
        return this.run(`/orders/${orderId}`);
    }

    update(orderId, orderData) {
        return this.run(`/orders/${orderId}`, {
            method: 'PUT',
            body: JSON.stringify(orderData),
          });
    }
}

export default OrdersClient;