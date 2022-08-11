import ApiClient from "./api";

class ProductsClient extends ApiClient {
    defaultErrorMessage = "There is an error to connect to the external Products Service"

    create(productData) {
        return this.run(`/products`, {
            method: 'POST',
            body: JSON.stringify(productData),
        });
    }

    getAll() {
        return this.run('/products');
    }

    getById(productId) {
        return this.run(`/products/${productId}`);
    }

    update(productId, productData) {
        return this.run(`/products/${productId}`, {
            method: 'PUT',
            body: JSON.stringify(productData),
          });
    }
}

export default ProductsClient;